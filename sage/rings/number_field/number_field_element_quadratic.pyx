"""
Optimized Quadratic Number Field Elements

AUTHORS: 
    -- Robert Bradshaw (2007-09): Initial version
    -- David Harvey (2007-10): fix up a few bugs, polish around the edges

TODO:
    the _new() method should be overridden in this class to copy the D attribute

"""
#*****************************************************************************
#     Copyright (C) 2007 Robert Bradshaw <robertwb@math.washington.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

include '../../ext/interrupt.pxi'
include "../../ext/stdsage.pxi"
    
cdef object QQ, ZZ
from sage.rings.rational_field import QQ
from sage.rings.integer_ring import ZZ
from sage.categories.morphism cimport Morphism
from sage.rings.number_field.number_field_element import _inverse_mod_generic

import number_field

# TODO: this doesn't belong here, but robert thinks it would be nice
# to have globally available....
#
# cdef mpz_to_str(mpz_t z):
#     cdef Integer zz = PY_NEW(Integer)
#     mpz_set(zz.value, z)
#     return str(zz)


def __make_NumberFieldElement_quadratic0(parent, a, b, denom):
    """
    Used in unpickling elements of number fields.
    
    TEST: 
        sage: K.<a> = NumberField(x^2-x+13)
        sage: loads(dumps(a)) == a
        True
    """
    return NumberFieldElement_quadratic(parent, (a, b, denom))


cdef class NumberFieldElement_quadratic(NumberFieldElement_absolute):

    def __init__(self, parent, f):
        """
        Construct a NumberFieldElement_quadratic object as an
        efficiently represented member of an absolute quadratic field.

        Elements are represented internally as triples (a, b, denom)
        of integers, where gcd(a, b, denom) == 1 and denom > 0,
        representing the element (a + b*sqrt(disc)) / denom.
        
        TESTS:
            sage: from sage.rings.number_field.number_field_element_quadratic import NumberFieldElement_quadratic
            
          Setup some fields: 
            sage: K.<a> = NumberField(x^2+23)
            sage: a.parts()
            (0, 1)
            sage: F.<b> = NumberField(x^2-x+7)
            sage: b.parts()
            (1/2, 3/2)

          By polynomials:
            sage: NumberFieldElement_quadratic(K, x-1)
            a - 1
            sage: NumberFieldElement_quadratic(F, x-1)
            b - 1
            
          By triples of Integers:
            sage: NumberFieldElement_quadratic(K, (1,2,3))
            2/3*a + 1/3
            sage: NumberFieldElement_quadratic(F, (1,2,3))
            4/9*b + 1/9
            sage: NumberFieldElement_quadratic(F, (1,2,3)).parts()
            (1/3, 2/3)
            
          By pairs of Rationals:
            sage: NumberFieldElement_quadratic(K, (1/2,1/3))
            1/3*a + 1/2
            sage: NumberFieldElement_quadratic(F, (1/2,1/3))
            2/9*b + 7/18
            sage: NumberFieldElement_quadratic(F, (1/2,1/3)).parts()
            (1/2, 1/3)
            
          Direct from Rational:
            sage: NumberFieldElement_quadratic(K, 2/3)
            2/3
            sage: NumberFieldElement_quadratic(F, 2/3)
            2/3

        This checks a bug when converting from lists:
            sage: w = CyclotomicField(3)([1/2,1])
            sage: w == w.__invert__().__invert__()
            True
            """
        self.D = parent._D
        cdef Integer a, b, denom
        cdef Rational ad, bd
        
        cdef NumberFieldElement_quadratic gen

        if PY_TYPE_CHECK(f, NumberFieldElement_quadratic):
            self._parent = parent   # NOTE: We do *not* call NumberFieldElement_absolute.__init__, for speed reasons.
            mpz_set(self.a, (<NumberFieldElement_quadratic>f).a)
            mpz_set(self.b, (<NumberFieldElement_quadratic>f).b)
            mpz_set(self.denom, (<NumberFieldElement_quadratic>f).denom)
            
        elif PY_TYPE_CHECK_EXACT(f, Rational):
            NumberFieldElement_absolute.__init__(self, parent, None)
            mpz_set(self.a, mpq_numref((<Rational>f).value))
            mpz_set_ui(self.b, 0)
            mpz_set(self.denom, mpq_denref((<Rational>f).value))
            
        elif PY_TYPE_CHECK_EXACT(f, tuple) and len(f) == 2:
            NumberFieldElement_absolute.__init__(self, parent, None)
            ad, bd = f
            mpz_lcm(self.denom, mpq_denref(ad.value), mpq_denref(bd.value))
            mpz_divexact(self.a, self.denom, mpq_denref(ad.value))
            mpz_mul(self.a, self.a, mpq_numref(ad.value))
            mpz_divexact(self.b, self.denom, mpq_denref(bd.value))
            mpz_mul(self.b, self.b, mpq_numref(bd.value))
            
        elif PY_TYPE_CHECK_EXACT(f, tuple) and len(f) == 3:
            NumberFieldElement_absolute.__init__(self, parent, None)
            a, b, denom = f
            mpz_set(self.a, a.value)
            mpz_set(self.b, b.value)
            mpz_set(self.denom, denom.value)
            self._reduce_c_()
            
        else:
            NumberFieldElement_absolute.__init__(self, parent, f)
            # poly is in gen (which may not be sqrt(d))
            self._ntl_coeff_as_mpz(&self.a, 0)
            self._ntl_coeff_as_mpz(&self.b, 1)
            if mpz_cmp_ui(self.a, 0) or mpz_cmp_ui(self.b, 0):
                gen = parent.gen() # should this be cached? 
                self._ntl_denom_as_mpz(&self.denom)
                if mpz_cmp_ui(self.b, 0):
                    mpz_mul(self.a, self.a, gen.denom)
                    mpz_addmul(self.a, self.b, gen.a)
                    mpz_mul(self.b, self.b, gen.b)
                    mpz_mul(self.denom, self.denom, gen.denom)
            else:
                mpz_set_ui(self.denom, 1)
            self._reduce_c_()

    cdef _new(self):
        """
        Quickly creates a new initialized NumberFieldElement with the
        same parent as self.
        """
        cdef NumberFieldElement_quadratic x
        x = <NumberFieldElement_quadratic>PY_NEW_SAME_TYPE(self)
        x._parent = self._parent
        x.D = self.D
        return x

    cdef number_field(self):
        return self._parent

    def __copy__(self):
        r"""
        Returns a new copy of self.

        TESTS:
            sage: K.<a> = QuadraticField(-3)
            sage: b = a + 3
            sage: c = b.__copy__()
            sage: b
            a + 3
            sage: c
            a + 3
            sage: b is c
            False
            sage: b == c
            True
        """
        cdef NumberFieldElement_quadratic x = <NumberFieldElement_quadratic>self._new()
        mpz_set(x.a, self.a)
        mpz_set(x.b, self.b)
        mpz_set(x.denom, self.denom)
        return x
        

    def __new__(self, parent=None, f=None):
        mpz_init(self.a)
        mpz_init(self.b)
        mpz_init(self.denom)

        
    def __dealloc__(self):
        mpz_clear(self.a)
        mpz_clear(self.b)
        mpz_clear(self.denom)

        
    def __reduce__(self):
        """
        TEST: 
            sage: K.<a> = NumberField(x^2-13)
            sage: loads(dumps(a)) == a
            True
            sage: loads(dumps(a/3+5)) == a/3+5
            True
        """
        cdef Integer a = <Integer>PY_NEW(Integer)
        cdef Integer b = <Integer>PY_NEW(Integer)
        cdef Integer denom = <Integer>PY_NEW(Integer)
        mpz_set(a.value, self.a)
        mpz_set(b.value, self.b)
        mpz_set(denom.value, self.denom)
        return __make_NumberFieldElement_quadratic0, (self._parent, a, b, denom)

    def _lift_cyclotomic_element(self, new_parent):
        """
        Creates an element of the passed field from this field.  This
        is specific to creating elements in a cyclotomic field from
        elements in another cyclotomic field, in the case that
        self.number_field()._n() divides new_parent()._n().  This
        function aims to make this common coercion extremely fast!
        
        More general coercion (i.e. of zeta6 into CyclotomicField(3))
        is implemented in the _coerce_from_other_cyclotomic_field
        method of a CyclotomicField.

        EXAMPLES:
            sage: C.<zeta4>=CyclotomicField(4)
            sage: CyclotomicField(20)(zeta4+1)  # The function _lift_cyclotomic_element does the heavy lifting in the background
            zeta20^5 + 1
            sage: (zeta4+1)._lift_cyclotomic_element(CyclotomicField(40))  # There is rarely a purpose to call this function directly
            zeta40^10 + 1
            
            sage: cf3 = CyclotomicField(3) ; z3 = cf3.0
            sage: cf6 = CyclotomicField(6) ; z6 = cf6.0
            sage: z6._lift_cyclotomic_element(cf3)
            Traceback (most recent call last):
            ...
            TypeError: The zeta_order of the new field must be a multiple of the zeta_order of the original.
            sage: cf3(z6)
            zeta3 + 1
            sage: z3._lift_cyclotomic_element(cf6)
            zeta6 - 1

        AUTHOR:
            -- Joel B. Mohler (original version)
            -- Craig Citro (reworked for quadratic elements)
        """
        if not isinstance(self.number_field(), number_field.NumberField_cyclotomic) \
               or not isinstance(new_parent, number_field.NumberField_cyclotomic):
            raise TypeError, "The field and the new parent field must both be cyclotomic fields."

        small_order = self.number_field()._n()
        large_order = new_parent._n()

        try:
            _rel = ZZ(large_order / small_order)
        except TypeError:
            raise TypeError, "The zeta_order of the new field must be a multiple of the zeta_order of the original."

        cdef NumberFieldElement_quadratic x2
        cdef int n = int(self.parent()._n())

        if new_parent.degree() == 2:
            ## since self is a *quadratic* element, we can only get
            ## here if self.parent() and new_parent are:
            ## - CyclotomicField(3) and CyclotomicField(6)
            ## - CyclotomicField(3) and CyclotomicField(3)
            ## - CyclotomicField(6) and CyclotomicField(6)
            ## - CyclotomicField(4) and CyclotomicField(4)
            ## In all cases, conversion of elements is trivial!
            x2 = <NumberFieldElement_quadratic>(self._new())
            x2._parent = new_parent
            mpz_set(x2.a, self.a)
            mpz_set(x2.b, self.b)
            mpz_set(x2.denom, self.denom)
            x2.D = self.D
            return x2

        cdef NumberFieldElement x
        cdef ZZX_c elt_num
        cdef ZZ_c elt_den, tmp_coeff
        cdef mpz_t tmp_mpz
        cdef long tmp_const

        x = <NumberFieldElement_absolute>PY_NEW(NumberFieldElement_absolute)

        mpz_to_ZZ(&elt_den, &(self.denom))

        mpz_init(tmp_mpz)
        
        ## set the two terms in the polynomial
        if n == 4:
            mpz_to_ZZ(&tmp_coeff, &(self.a))
            ZZX_SetCoeff(elt_num, 0, tmp_coeff)
            mpz_to_ZZ(&tmp_coeff, &(self.b))
            ZZX_SetCoeff(elt_num, 1, tmp_coeff)
                
        elif n == 3:
            ## num[0] = a + b
            mpz_add(tmp_mpz, tmp_mpz, self.a)
            mpz_add(tmp_mpz, tmp_mpz, self.b)
            mpz_to_ZZ(&tmp_coeff, &tmp_mpz)
            ZZX_SetCoeff(elt_num, 0, tmp_coeff)

            ## num[1] = 2*b
            mpz_sub(tmp_mpz, tmp_mpz, self.a)
            tmp_const = 2
            mpz_mul_si(tmp_mpz, tmp_mpz, tmp_const)
            mpz_to_ZZ(&tmp_coeff, &tmp_mpz)
            ZZX_SetCoeff(elt_num, 1, tmp_coeff)

        elif n == 6:
            ## num[0] = a - b
            mpz_add(tmp_mpz, tmp_mpz, self.a)
            mpz_sub(tmp_mpz, tmp_mpz, self.b)
            mpz_to_ZZ(&tmp_coeff, &tmp_mpz)
            ZZX_SetCoeff(elt_num, 0, tmp_coeff)

            ## num[1] = 2*b
            mpz_sub(tmp_mpz, tmp_mpz, self.a)
            tmp_const = -2
            mpz_mul_si(tmp_mpz, tmp_mpz, tmp_const)
            mpz_to_ZZ(&tmp_coeff, &tmp_mpz)
            ZZX_SetCoeff(elt_num, 1, tmp_coeff)

        mpz_clear(tmp_mpz)

        x._parent = <ParentWithBase>new_parent
        x.__fld_numerator, x.__fld_denominator = new_parent.polynomial_ntl()
        x.__denominator = elt_den
        cdef ZZX_c result
        cdef ZZ_c tmp
        cdef int i
        cdef int rel = _rel
        cdef ntl_ZZX _num
        cdef ntl_ZZ _den
        _num, _den = new_parent.polynomial_ntl()
        for i from 0 <= i <= ZZX_deg(elt_num):
            tmp = ZZX_coeff(elt_num, i)
            ZZX_SetCoeff(result, i*rel, tmp)
        ZZX_rem(x.__numerator, result, _num.x)
        (<NumberFieldElement_absolute>x)._reduce_c_()
        return x

    def parts(self):
        """
        This function returns a pair of rationals $a$ and $b$ such that
        self = $a+b\sqrt{D}$. 
        
        This is much closer to the internal storage format of the 
        elements, unless the generator is equal to $\sqrt{D}$ will 
        be different than the polynomial representation coefficients. 
        
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2-13)
            sage: K.discriminant()
            13
            sage: a.parts()
            (0, 1)
            sage: (a/2-4).parts()
            (-4, 1/2)
            sage: K.<a> = NumberField(x^2-7)
            sage: K.discriminant()
            28
            sage: a.parts()
            (0, 1)
            sage: K.<a> = NumberField(x^2-x+7)
            sage: a.parts()
            (1/2, 3/2)
            sage: a._coefficients()
            [0, 1]                    
        """
        cdef Rational ad = <Rational>PY_NEW(Rational), bd = <Rational>PY_NEW(Rational)
        if mpz_cmp_ui(self.a, 0) == 0:
            mpq_set_ui(ad.value, 0, 1)
        else:
            mpz_set(mpq_numref(ad.value), self.a)
            mpz_set(mpq_denref(ad.value), self.denom)
            mpq_canonicalize(ad.value)
        if mpz_cmp_ui(self.b, 0) == 0:
            mpq_set_ui(bd.value, 0, 1)
        else:
            mpz_set(mpq_numref(bd.value), self.b)
            mpz_set(mpq_denref(bd.value), self.denom)
            mpq_canonicalize(bd.value)

        return ad, bd

    cdef bint is_sqrt_disc(self):
        r"""
        Returns true if self is sqrt(D).
        """
        return mpz_cmp_ui(self.denom, 1)==0 and mpz_cmp_ui(self.a, 0)==0 and mpz_cmp_ui(self.b, 1)==0
                
                
#########################################################
# Arithmetic
#########################################################

    cdef void _reduce_c_(self):
        r"""
        Reduces into canonical form.

        WARNING: this mutates self.
        """
        cdef mpz_t gcd
        # cancel out common factors
        mpz_init(gcd)
        mpz_gcd(gcd, self.a, self.denom)
        mpz_gcd(gcd, gcd, self.b)
        if mpz_cmp_si(gcd, 1): # != 0 (i.e. it is not 1)
            mpz_divexact(self.a, self.a, gcd)
            mpz_divexact(self.b, self.b, gcd)
            mpz_divexact(self.denom, self.denom, gcd)
        # make denominator positive
        if mpz_sgn(self.denom) < 0:
            mpz_neg(self.denom, self.denom)
            mpz_neg(self.a, self.a)
            mpz_neg(self.b, self.b)
        mpz_clear(gcd)

        
    cpdef ModuleElement _add_(self, ModuleElement other_m):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2-5)
            sage: K.discriminant()
            5
            sage: a+a
            2*a
            sage: s = (a+2)/6; s
            1/6*a + 1/3
            sage: s+a
            7/6*a + 1/3
            sage: s+10
            1/6*a + 31/3
            sage: s+(2*a+5)/7
            19/42*a + 22/21
            sage: s+(1+a)/2
            2/3*a + 5/6
            sage: s+(1+a)/8
            7/24*a + 11/24
            sage: s+(a+5)/6
            1/3*a + 7/6
            sage: (a/3+2/3) + (2*a/3+1/3)
            a + 1            
        """
        cdef NumberFieldElement_quadratic other = <NumberFieldElement_quadratic>other_m
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        cdef mpz_t gcd, tmp
        if mpz_cmp(self.denom, other.denom) == 0:
            mpz_add(res.a, self.a, other.a)
            mpz_add(res.b, self.b, other.b)
            mpz_set(res.denom, self.denom)
        else:
            mpz_init(gcd)
            mpz_gcd(gcd, self.denom, other.denom)
            if mpz_cmp_ui(gcd, 1) == 0:
                mpz_mul(res.a, self.a, other.denom)
                mpz_addmul(res.a, self.denom, other.a)
                mpz_mul(res.b, self.b, other.denom)
                mpz_addmul(res.b, self.denom, other.b)
                mpz_mul(res.denom, self.denom, other.denom)
            else:
                mpz_init(tmp)
                mpz_divexact(tmp, other.denom, gcd)
                mpz_mul(res.a, self.a, tmp)
                mpz_mul(res.b, self.b, tmp)
                mpz_divexact(tmp, self.denom, gcd)
                mpz_addmul(res.a, other.a, tmp)
                mpz_addmul(res.b, other.b, tmp)
                mpz_mul(res.denom, other.denom, tmp)
                mpz_clear(tmp)
            mpz_clear(gcd)
        res._reduce_c_()
        return res

    
    cpdef ModuleElement _sub_(self, ModuleElement other_m):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2-13)
            sage: b = (a-3)/10; b
            1/10*a - 3/10
            sage: b-1
            1/10*a - 13/10
            sage: b-a
            -9/10*a - 3/10
            sage: b-1/2
            1/10*a - 4/5
            sage: b-a/15
            1/30*a - 3/10
        """
        cdef NumberFieldElement_quadratic other = <NumberFieldElement_quadratic>other_m
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        cdef mpz_t gcd, tmp
        if mpz_cmp(self.denom, other.denom) == 0:
            mpz_sub(res.a, self.a, other.a)
            mpz_sub(res.b, self.b, other.b)
            mpz_set(res.denom, self.denom)
        else:
            mpz_init(gcd)
            mpz_gcd(gcd, self.denom, other.denom)
            if mpz_cmp_ui(gcd, 1) == 0:
                mpz_mul(res.a, self.a, other.denom)
                mpz_submul(res.a, self.denom, other.a)
                mpz_mul(res.b, self.b, other.denom)
                mpz_submul(res.b, self.denom, other.b)
                mpz_mul(res.denom, self.denom, other.denom)
            else:
                mpz_init(tmp)
                mpz_divexact(tmp, other.denom, gcd)
                mpz_mul(res.a, self.a, tmp)
                mpz_mul(res.b, self.b, tmp)
                mpz_divexact(tmp, self.denom, gcd)
                mpz_submul(res.a, other.a, tmp)
                mpz_submul(res.b, other.b, tmp)
                mpz_mul(res.denom, other.denom, tmp)
                mpz_clear(tmp)
            mpz_clear(gcd)
        res._reduce_c_()
        return res

        
    def __neg__(self):
        """
        EXAMPLES:
            sage: K.<a> = NumberField(x^2+163)
            sage: -a
            -a
            sage: -(a+4)
            -a - 4
            sage: b = (a-3)/2
            sage: -b
            -1/2*a + 3/2
        """
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_neg(res.a, self.a)
        mpz_neg(res.b, self.b)
        mpz_set(res.denom, self.denom)
        return res

    
    cpdef RingElement _mul_(self, RingElement other_m):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+23)
            sage: a*a
            -23
            sage: (a+1)*(a-1)
            -24
            sage: (a+1)*(a+2)
            3*a - 21
            sage: (a+1)/2 * (a+2)
            3/2*a - 21/2
            sage: (a+1)/2 * (a+2)/3
            1/2*a - 7/2
            sage: (2*a+4) * (3*a)/2
            6*a - 69
            
        Verify Karatsuba
            sage: K.<a> = NumberField(x^2-41)
            sage: (10^1000 * (a+1)) * K(2+3*a) == 10^1000 * ((a+1) * K(2+3*a))
            True
        """
        cdef NumberFieldElement_quadratic other = <NumberFieldElement_quadratic>other_m
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        cdef mpz_t tmp
        
        if mpz_size(self.a) + mpz_size(self.b) < 8: # could I use a macro instead?
            # Do it the traditional way
            mpz_mul(res.a, self.b, other.b)
            mpz_mul(res.a, res.a, self.D.value)
            mpz_addmul(res.a, self.a, other.a)
            
            mpz_mul(res.b, self.a, other.b)
            mpz_addmul(res.b, self.b, other.a)
            
        else:
            # Karatsuba
            _sig_on
            mpz_init(tmp)
            mpz_add(res.a, self.a, self.b) # using res.a as tmp
            mpz_add(tmp, other.a, other.b)
            mpz_mul(res.b, res.a, tmp) # res.b = (self.a + self.b)(other.a + other.b)
            
            mpz_mul(res.a, self.a, other.a)
            mpz_sub(res.b, res.b, res.a)
            mpz_mul(tmp, self.b, other.b)
            mpz_sub(res.b, res.b, tmp)
            mpz_mul(tmp, tmp, self.D.value)
            mpz_add(res.a, res.a, tmp)
            mpz_clear(tmp)
            _sig_off
        
        mpz_mul(res.denom, self.denom, other.denom)
        res._reduce_c_()
        return res

        
    cpdef ModuleElement _rmul_(self, RingElement _c):
        """
        EXAMPLE: 
            sage: K.<a> = NumberField(x^2+43)
            sage: (1+a)*3
            3*a + 3
        """
        cdef Rational c =  <Rational>_c
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_mul(res.a, self.a, mpq_numref(c.value))
        mpz_mul(res.b, self.b, mpq_numref(c.value))
        mpz_mul(res.denom, self.denom, mpq_denref(c.value))
        res._reduce_c_()
        return res

        
    cpdef ModuleElement _lmul_(self, RingElement _c):
        """
        EXAMPLE: 
            sage: K.<a> = NumberField(x^2+43)
            sage: 5*(a-1/5)
            5*a - 1            
        """
        cdef Rational c =  <Rational>_c
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_mul(res.a, self.a, mpq_numref(c.value))
        mpz_mul(res.b, self.b, mpq_numref(c.value))
        mpz_mul(res.denom, self.denom, mpq_denref(c.value))
        res._reduce_c_()
        return res

        
    cpdef RingElement _div_(self, RingElement other):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2-5)
            sage: 2/a
            2/5*a
            sage: (a+2)/(a+1)
            1/4*a + 3/4
            sage: (a+1)*(a+2)/(a+1)
            a + 2
            sage: (a+1/3)*(5*a+2/7)/(a+1/3)
            5*a + 2/7        
        """
        return self * ~other

        
    def __invert__(self):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2-5)
            sage: ~a
            1/5*a
            sage: ~(a+1)
            1/4*a - 1/4
            sage: (a-1)*(a+1)
            4
            sage: b = ~(5*a-3); b
            5/116*a + 3/116
            sage: b*(5*a-3)
            1
            sage: b = ~((3*a-2)/7); b
            21/41*a + 14/41
            sage: (3*a-2)/7 * b
            1
        """
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        cdef mpz_t tmp, gcd
        mpz_init(tmp)
        mpz_init(gcd)
        
        mpz_gcd(gcd, self.a, self.b)
        if mpz_cmp_si(gcd, 1): # != 0 (i.e. it is not 1)
            # cancel out g (g(a'-b'd)) / (g^2 (a'^2-b'^2d^2))
            mpz_divexact(res.a, self.a, gcd)
            mpz_divexact(res.b, self.b, gcd)
            mpz_neg(res.b, res.b)
        else:
            mpz_set(res.a, self.a)
            mpz_neg(res.b, self.b)

        mpz_pow_ui(res.denom, res.a, 2)
        mpz_pow_ui(tmp, res.b, 2)
        mpz_mul(tmp, tmp, self.D.value)
        mpz_sub(res.denom, res.denom, tmp)
        # need to multiply the leftover g back in
        mpz_mul(res.denom, res.denom, gcd)
        
        mpz_mul(res.a, res.a, self.denom)
        mpz_mul(res.b, res.b, self.denom)

        mpz_clear(tmp)
        mpz_clear(gcd)

        res._reduce_c_()
        return res

        
    cdef NumberFieldElement conjugate_c(self):
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_set(res.a, self.a)
        mpz_neg(res.b, self.b)
        mpz_set(res.denom, self.denom)
        return res

        
#################################################################################
# We must override everything that makes uses of self.__numerator/__denominator
#################################################################################
            
    cdef int _cmp_c_impl(self, Element _right) except -2:
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+163)
            sage: K(1/2)==1/2
            True
            sage: a == 1/2
            False
            sage: 2+a == a+2
            True
        """
        cdef NumberFieldElement_quadratic right = _right
        return not mpz_cmp(self.a, right.a)==0  \
            or not mpz_cmp(self.b, right.b)==0  \
            or not mpz_cmp(self.denom, right.denom) == 0


    def __nonzero__(self):
        """
        EXAMPLES:
            sage: K.<a> = NumberField(x^2+163)
            sage: not a
            False
            sage: not (a-a)
            True        
        """
        return mpz_cmp_ui(self.a, 0) != 0 or mpz_cmp_ui(self.b, 0) != 0

    
    def _integer_(self, Z=None):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+163)
            sage: (a+1-a)._integer_()
            1
            sage: (a+1/2-a)._integer_()
            Traceback (most recent call last):
            ...
            TypeError: Unable to coerce 1/2 to an integer
        """
        cdef Integer res
        if mpz_cmp_ui(self.b, 0) != 0 or mpz_cmp_ui(self.denom, 1) != 0:
            raise TypeError, "Unable to coerce %s to an integer"%self
        else:
            res = PY_NEW(Integer)
            mpz_set(res.value, self.a)
            return res


    def _rational_(self):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+163)
            sage: (a+1/2-a)._rational_()
            1/2
            sage: (a+1/2)._rational_()
            Traceback (most recent call last):
            ...
            TypeError: Unable to coerce a + 1/2 to a rational
        """
        cdef Rational res
        if mpz_cmp_ui(self.b, 0)!=0:
            raise TypeError, "Unable to coerce %s to a rational"%self
        else:
            res = <Rational>PY_NEW(Rational)
            mpz_set(mpq_numref(res.value), self.a)
            mpz_set(mpq_denref(res.value), self.denom)
            mpq_canonicalize(res.value)
            return res


    def _coefficients(self):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+41)
            sage: a._coefficients()
            [0, 1]
            sage: K.<a> = NumberField(x^2+x+41)
            sage: a._coefficients()
            [0, 1]
            sage: b = 3*a+1/5
            sage: b._coefficients()
            [1/5, 3]
        """
        # In terms of the generator...
        cdef NumberFieldElement_quadratic gen = self.number_field().gen() # should this be cached? 
        cdef Rational const = <Rational>PY_NEW(Rational), lin = <Rational>PY_NEW(Rational)
        ad, bd = self.parts()
        if not self:
            return []
        if not bd:
            return [ad]
        if gen.is_sqrt_disc():
            return [ad,bd]
        else:
            alpha, beta = gen.parts()
            scale = bd/beta
            return [ad - scale*alpha, scale]

        
    def denominator(self):
        """
        EXAMPLES:
            sage: K.<a> = NumberField(x^2+x+41)
            sage: a.denominator()
            1
            sage: b = (2*a+1)/6
            sage: b.denominator()
            6
            sage: K(1).denominator()
            1
            sage: K(1/2).denominator()
            2
            sage: K(0).denominator()
            1
        """
        # In terms of the generator...
        cdef NumberFieldElement_quadratic gen = self.number_field().gen() # should this be cached? 
        cdef Integer denom
        if gen.is_sqrt_disc():
            denom = PY_NEW(Integer)
            mpz_set(denom.value, self.denom)
            return denom
        else:
            c = self._coefficients()
            if len(c) == 2:
                const, lin = c
            elif len(c) == 1:
                const = c[0]
                lin = Rational(0)
            else:
                const = lin = Rational(0)
            return const.denominator().lcm(lin.denominator())

        
    cdef bint is_rational_c(self):
        return mpz_cmp_ui(self.b, 0) == 0


#########################################################
# Some things are so much easier to compute
#########################################################

    def trace(self):
        """
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2+x+41)
            sage: a.trace()
            -1
            sage: a.matrix()
            [  0   1]
            [-41  -1]
            
        The trace is additive:
            sage: K.<a> = NumberField(x^2+7)
            sage: (a+1).trace()
            2
            sage: K(3).trace()
            6
            sage: (a+4).trace()
            8
            sage: (a/3+1).trace()
            2
        """
        # trace = 2*self.a / self.denom
        cdef Rational res = <Rational>PY_NEW(Rational)
        if mpz_odd_p(self.denom):
            mpz_mul_2exp(mpq_numref(res.value), self.a, 1)
            mpz_set(mpq_denref(res.value), self.denom)
        else:
            mpz_set(mpq_numref(res.value), self.a)
            mpz_divexact_ui(mpq_denref(res.value), self.denom, 2)
        mpq_canonicalize(res.value)
        return res


    def norm(self):
        """
        EXAMPLES:
            sage: K.<a> = NumberField(x^2-x+3)
            sage: a.norm()
            3
            sage: a.matrix()
            [ 0  1]
            [-3  1]
            sage: K.<a> = NumberField(x^2+5)
            sage: (1+a).norm()
            6
            
        The norm is multiplicative:
            sage: K.<a> = NumberField(x^2-3)
            sage: a.norm()
            -3
            sage: K(3).norm()
            9
            sage: (3*a).norm()
            -27
        """
        # norm = (a^2 - d b^2) / self.denom^2
        cdef Rational res = <Rational>PY_NEW(Rational)
        mpz_pow_ui(mpq_numref(res.value), self.a, 2)
        mpz_pow_ui(mpq_denref(res.value), self.b, 2) # use as temp
        mpz_mul(mpq_denref(res.value), mpq_denref(res.value), self.D.value)
        mpz_sub(mpq_numref(res.value), mpq_numref(res.value), mpq_denref(res.value))
        mpz_pow_ui(mpq_denref(res.value), self.denom, 2)
        mpq_canonicalize(res.value)
        return res


    def is_integral(self):
        r"""
        Returns whether this element is an algebraic integer.

        TESTS:
            sage: K.<a> = QuadraticField(-1)
            sage: a.is_integral()
            True
            sage: K(1).is_integral()
            True
            sage: K(1/2).is_integral()
            False
            sage: K(a/2).is_integral()
            False
            sage: K((a+1)/2).is_integral()
            False
            sage: K(a/3).is_integral()
            False

            sage: K.<a> = QuadraticField(-3)
            sage: a.is_integral()
            True
            sage: K(1).is_integral()
            True
            sage: K(1/2).is_integral()
            False
            sage: K(a/2).is_integral()
            False
            sage: ((a+1)/2).is_integral()
            True
        """
        if mpz_cmp_ui(self.denom, 1) == 0:
            return True
        else:
            return self.norm().denom() == 1 and self.trace().denom() == 1
        
    def charpoly(self, var='x'):
        r"""
        The characteristic polynomial of this element over $\Q$.

        EXAMPLES:
            sage: K.<a> = NumberField(x^2-x+13)
            sage: a.charpoly()
            x^2 - x + 13
            sage: b = 3-a/2
            sage: f = b.charpoly(); f
            x^2 - 11/2*x + 43/4
            sage: f(b)
            0
        """
        R = QQ[var]
        return R([self.norm(), -self.trace(), 1])
        
    def minpoly(self, var='x'):
        r"""
        The minimal polynomial of this element over $\Q$.

        EXAMPLES:
            sage: K.<a> = NumberField(x^2+13)
            sage: a.minpoly()
            x^2 + 13
            sage: (a+1/2-a).minpoly()
            x - 1/2        
        """
        if self.is_rational_c():
            R = QQ[var]
            return R([-self._rational_(), 1])
        else: 
            return self.charpoly()


cdef class OrderElement_quadratic(NumberFieldElement_quadratic):
    """
    Element of an order in a quadratic field. 

    EXAMPLES:
        sage: K.<a> = NumberField(x^2 + 1)
        sage: O2 = K.order(2*a)
        sage: w = O2.1; w
        2*a
        sage: parent(w)
        Order in Number Field in a with defining polynomial x^2 + 1
    """
    def __init__(self, order, f):
        K = order.number_field()
        NumberFieldElement_quadratic.__init__(self, K, f)
        (<Element>self)._parent = order
        
    def norm(self):
        """
        The norm of an element of the ring of integers is an Integer. 
        
        EXAMPLES: 
            sage: K.<a> = NumberField(x^2 + 3)
            sage: O2 = K.order(2*a)
            sage: w = O2.gen(1); w
            2*a
            sage: w.norm()
            12
            sage: parent(w.norm())
            Integer Ring
        """
        return ZZ(NumberFieldElement_quadratic.norm(self))

    def trace(self):
        """
        The trace of an element of the ring of integers is an Integer. 

        EXAMPLES: 
            sage: K.<a> = NumberField(x^2 - 5)
            sage: R = K.ring_of_integers()
            sage: b = R((1+a)/2)
            sage: b.trace()
            1
            sage: parent(b.trace())
            Integer Ring
        """
        return ZZ(NumberFieldElement_quadratic.trace(self))

    def charpoly(self, var='x'):
        r"""
        The characteristic polynomial of this element, which is over $\Z$ 
        because this element is an algebraic integer.

        EXAMPLES:
            sage: K.<a> = NumberField(x^2 - 5)
            sage: R = K.ring_of_integers()
            sage: b = R((5+a)/2)
            sage: f = b.charpoly('x'); f
            x^2 - 5*x + 5
            sage: f.parent()
            Univariate Polynomial Ring in x over Integer Ring
            sage: f(b)
            0
        """
        R = ZZ[var]
        return R([self.norm(), -self.trace(), 1])

    def minpoly(self, var='x'):
        r"""
        The minimal polynomial of this element over $\Z$.

        EXAMPLES:
            sage: K.<a> = NumberField(x^2 + 163)
            sage: R = K.ring_of_integers()
            sage: f = R(a).minpoly('x'); f
            x^2 + 163
            sage: f.parent()
            Univariate Polynomial Ring in x over Integer Ring
            sage: R(5).minpoly()
            x - 5
        """
        if self.is_rational_c():
            R = ZZ[var]
            return R([-self._rational_(), 1])
        else: 
            return self.charpoly()

    cdef number_field(self):
        # So few functions actually use self.number_field() for quadratic elements, so
        # it is better *not* to return a cached value (since the call to _parent.number_field())
        # is expensive.
        return self._parent.number_field()
        
    # We must override these since the basering is now ZZ not QQ. 
    cpdef ModuleElement _rmul_(self, RingElement _c):
        """
        EXAMPLE: 
            sage: K.<a> = NumberField(x^2-27)
            sage: R = K.ring_of_integers()
            sage: aa = R.gen(1); aa
            1/3*a
            sage: 5 * aa
            5/3*a
        """
        cdef Integer c = <Integer>_c
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_mul(res.a, self.a, c.value)
        mpz_mul(res.b, self.b, c.value)
        mpz_set(res.denom, self.denom)
        res._reduce_c_()
        return res

        
    cpdef ModuleElement _lmul_(self, RingElement _c):
        """
        EXAMPLE: 
            sage: K.<a> = NumberField(x^2+43)
            sage: R = K.ring_of_integers()
            sage: aa = R.gen(0); aa
            1/2*a + 1/2
            sage: aa*3
            3/2*a + 3/2
        """
        cdef Integer c = <Integer>_c
        cdef NumberFieldElement_quadratic res = <NumberFieldElement_quadratic>self._new()
        mpz_mul(res.a, self.a, c.value)
        mpz_mul(res.b, self.b, c.value)
        mpz_set(res.denom, self.denom)
        res._reduce_c_()
        return res

    cpdef RingElement _div_(self, RingElement other):
        r"""
        Implement division, checking that the result has the
        right parent. It's not so crucial what the parent actually
        is, but it is crucial that the returned value really is an
        element of its supposed parent! This fixes trac \#4190.

        EXAMPLES:
            sage: K = NumberField(x^2 - 17, 'a')
            sage: OK = K.ring_of_integers()
            sage: a = OK(K.gen())
            sage: (17/a).parent() is K
            True
            sage: 17/a in OK
            True
            sage: (17/(2*a)).parent() is OK
            False
            sage: (17/(2*a)) in OK
            False
            sage: (17/(2*a)).parent() is K
            True
        """     
        cdef NumberFieldElement_quadratic x 
        x = NumberFieldElement_quadratic._div_(self, other)
        return self._parent.number_field()(x)

    def __invert__(self):
        r"""
        Implement inversion, checking that the return value has the right parent.
        See trac \#4190.
        
        EXAMPLES:
            sage: K = NumberField(x^2 -x + 2, 'a')
            sage: OK = K.ring_of_integers()
            sage: a = OK(K.gen())
            sage: (~a).parent() is K
            True
            sage: (~a) in OK
            False
            sage: a**(-1) in OK
            False
        """
        return self._parent.number_field()(NumberFieldElement_quadratic.__invert__(self))

    def inverse_mod(self, I):
        r""" 
        Return an inverse of self modulo the given ideal.
        
        EXAMPLES:
            sage: OE = QuadraticField(-7, 's').ring_of_integers()
            sage: w = OE.ring_generators()[0]
            sage: w.inverse_mod(13) + (7*w + 6) in 13*OE
            True
            sage: w.inverse_mod(2*OE)
            Traceback (most recent call last):
            ...
            ZeroDivisionError: 1/2*s + 1/2 is not invertible modulo Fractional ideal (2)
        """
        return _inverse_mod_generic(self, I)

cdef class Q_to_quadratic_field_element(Morphism):
    """
    Morphism that coerces from rationals to elements of a
    quadratic number field K.
    """
    cdef NumberFieldElement_quadratic zero_element    # the zero element of K
    
    def __init__(self, K):
        """ K is the target quadratic field """
        import sage.categories.homset
        Morphism.__init__(self, sage.categories.homset.Hom(QQ, K))
        self.zero_element = PY_NEW(NumberFieldElement_quadratic)
        self.zero_element._parent = K
        self.zero_element.D = K._D
        

    cpdef Element _call_(self, x):
        cdef NumberFieldElement_quadratic y = self.zero_element._new()
        y.D = self.zero_element.D
        mpz_set(y.a, mpq_numref((<Rational>x).value))
        mpz_set(y.denom, mpq_denref((<Rational>x).value))
        return y

    def _repr_type(self):
        return "Natural"
