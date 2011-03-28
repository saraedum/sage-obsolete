"""
Finite dimensional free algebra quotients

REMARK:

This implementation only works for finite dimensional quotients, since
a list of basis monomials and the multiplication matrices need to be
explicitly provided.

The homogeneous part of a quotient of a free algebra over a field by a
finitely generated homogeneous twosided ideal is available in a
different implementation. See
:mod:`~sage.algebras.letterplace.free_algebra_letterplace` and
:mod:`~sage.rings.quotient_ring`.

TESTS::

    sage: n = 2
    sage: A = FreeAlgebra(QQ,n,'x')
    sage: F = A.monoid()
    sage: i, j = F.gens()
    sage: mons = [ F(1), i, j, i*j ]
    sage: r = len(mons)
    sage: M = MatrixSpace(QQ,r)
    sage: mats = [M([0,1,0,0, -1,0,0,0, 0,0,0,-1, 0,0,1,0]), M([0,0,1,0, 0,0,0,1, -1,0,0,0, 0,-1,0,0]) ]
    sage: H2.<i,j> = A.quotient(mons,mats)
    sage: H2 == loads(dumps(H2))
    True
    sage: i == loads(dumps(i))
    True
"""

#*****************************************************************************
#  Copyright (C) 2005 David Kohel <kohel@maths.usyd.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty
#    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License for more details; the full text
#  is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.modules.free_module import FreeModule
from sage.algebras.algebra import Algebra
from sage.algebras.free_algebra import is_FreeAlgebra
from sage.algebras.free_algebra_quotient_element import FreeAlgebraQuotientElement
from sage.structure.parent_gens import ParentWithGens
from sage.structure.unique_representation import UniqueRepresentation

class FreeAlgebraQuotient(UniqueRepresentation, Algebra, object):
    @staticmethod
    def __classcall__(cls, A, mons, mats, names):
        """
        Used to support unique representation.

        EXAMPLES::

            sage: H = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0]  # indirect doctest
            sage: H1 = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0]
            sage: H is H1
            True
        """
        new_mats = []
        for M in mats:
            M = M.parent()(M)
            M.set_immutable()
            new_mats.append(M)
        return super(FreeAlgebraQuotient, cls).__classcall__(cls, A, tuple(mons),
                                                  tuple(new_mats), tuple(names))

    Element = FreeAlgebraQuotientElement
    def __init__(self, A, mons, mats, names):
        """
        Returns a quotient algebra defined via the action of a free algebra
        A on a (finitely generated) free module. The input for the quotient
        algebra is a list of monomials (in the underlying monoid for A)
        which form a free basis for the module of A, and a list of
        matrices, which give the action of the free generators of A on this
        monomial basis.
        
        EXAMPLES:
        
        Quaternion algebra defined in terms of three generators::
        
            sage: n = 3
            sage: A = FreeAlgebra(QQ,n,'i')
            sage: F = A.monoid()
            sage: i, j, k = F.gens()
            sage: mons = [ F(1), i, j, k ]
            sage: M = MatrixSpace(QQ,4)
            sage: mats = [M([0,1,0,0, -1,0,0,0, 0,0,0,-1, 0,0,1,0]),  M([0,0,1,0, 0,0,0,1, -1,0,0,0, 0,-1,0,0]),  M([0,0,0,1, 0,0,-1,0, 0,1,0,0, -1,0,0,0]) ]
            sage: H3.<i,j,k> = FreeAlgebraQuotient(A,mons,mats)
            sage: x = 1 + i + j + k
            sage: x
            1 + i + j + k
            sage: x**128
            -170141183460469231731687303715884105728 + 170141183460469231731687303715884105728*i + 170141183460469231731687303715884105728*j + 170141183460469231731687303715884105728*k
        
        Same algebra defined in terms of two generators, with some penalty
        on already slow arithmetic.
        
        ::
        
            sage: n = 2
            sage: A = FreeAlgebra(QQ,n,'x')
            sage: F = A.monoid()
            sage: i, j = F.gens()
            sage: mons = [ F(1), i, j, i*j ]
            sage: r = len(mons)
            sage: M = MatrixSpace(QQ,r)
            sage: mats = [M([0,1,0,0, -1,0,0,0, 0,0,0,-1, 0,0,1,0]), M([0,0,1,0, 0,0,0,1, -1,0,0,0, 0,-1,0,0]) ]
            sage: H2.<i,j> = A.quotient(mons,mats)
            sage: k = i*j
            sage: x = 1 + i + j + k
            sage: x
            1 + i + j + i*j
            sage: x**128
            -170141183460469231731687303715884105728 + 170141183460469231731687303715884105728*i + 170141183460469231731687303715884105728*j + 170141183460469231731687303715884105728*i*j

        TEST::

            sage: TestSuite(H2).run()

        """
        if not is_FreeAlgebra(A):
            raise TypeError("Argument A must be an algebra.")
        R = A.base_ring()
#        if not R.is_field():  # TODO: why?
#            raise TypeError, "Base ring of argument A must be a field."
        n = A.ngens()
        assert n == len(mats)
        self.__free_algebra = A
        self.__ngens = n
        self.__dim = len(mons)
        self.__module = FreeModule(R,self.__dim)
        self.__matrix_action = mats
        self.__monomial_basis = mons # elements of free monoid
        Algebra.__init__(self, R, names, normalize=True)

    def __eq__(self, right):
        """
        Return True if all defining properties of self and right match up.

        EXAMPLES::

            sage: HQ = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0]
            sage: HZ = sage.algebras.free_algebra_quotient.hamilton_quatalg(ZZ)[0]
            sage: HQ == HQ
            True
            sage: HQ == HZ
            False
            sage: HZ == QQ
            False
        """
        return isinstance(right, FreeAlgebraQuotient) and \
               self.ngens() == right.ngens() and \
               self.rank() == right.rank() and \
               self.module() == right.module() and \
               self.matrix_action() == right.matrix_action() and \
               self.monomial_basis() == right.monomial_basis()
    

    def _element_constructor_(self, x):
        """
        EXAMPLES::

            sage: H, (i,j,k) = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)
            sage: H._element_constructor_(i) is i
            True
            sage: a = H._element_constructor_(1); a
            1
            sage: a in H
            True
            sage: a = H._element_constructor_([1,2,3,4]); a
            1 + 2*i + 3*j + 4*k
        """
        if isinstance(x, FreeAlgebraQuotientElement) and x.parent() is self:
            return x
        return self.element_class(self,x)

    def _coerce_map_from_(self,S):
        """
        EXAMPLES::

            sage: H, (i,j,k) = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)
            sage: H._coerce_map_from_(H)
            True
            sage: H._coerce_map_from_(QQ)
            True
            sage: H._coerce_map_from_(GF(7))
            False
        """
        return S==self or self.__free_algebra.has_coerce_map_from(S)

    def _repr_(self):
        """
        EXAMPLES::

            sage: H, (i,j,k) = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)
            sage: H._repr_()
            "Free algebra quotient on 3 generators ('i', 'j', 'k') and dimension 4 over Rational Field"
        """
        R = self.base_ring()
        n = self.__ngens
        r = self.__module.dimension()
        x = self.variable_names()
        return "Free algebra quotient on %s generators %s and dimension %s over %s"%(n,x,r,R)

    def gen(self, i):
        """
        The i-th generator of the algebra.

        EXAMPLES::

            sage: H, (i,j,k) = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)
            sage: H.gen(0)
            i
            sage: H.gen(2)
            k

        An IndexError is raised if an invalid generator is requested::
        
            sage: H.gen(3)
            Traceback (most recent call last):
            ...
            IndexError: Argument i (= 3) must be between 0 and 2.

        Negative indexing into the generators is not supported::
        
            sage: H.gen(-1)
            Traceback (most recent call last):
            ...
            IndexError: Argument i (= -1) must be between 0 and 2.
        """
        n = self.__ngens
        if i < 0 or not i < n: 
            raise IndexError("Argument i (= %s) must be between 0 and %s."%(i, n-1))
        R = self.base_ring()
        F = self.__free_algebra.monoid()
        n = self.__ngens
        return self.element_class(self,{F.gen(i):R(1)})

    def ngens(self):
        """
        The number of generators of the algebra.

        EXAMPLES::
        
            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].ngens()
            3
        """
        return self.__ngens

    def dimension(self):
        """
        The rank of the algebra (as a free module).

        EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].dimension()
            4
        """
        return self.__dim

    def matrix_action(self):
        """
        EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].matrix_action()
            (
            [ 0  1  0  0]  [ 0  0  1  0]  [ 0  0  0  1]
            [-1  0  0  0]  [ 0  0  0  1]  [ 0  0 -1  0]
            [ 0  0  0 -1]  [-1  0  0  0]  [ 0  1  0  0]
            [ 0  0  1  0], [ 0 -1  0  0], [-1  0  0  0]
            )
        """
        return self.__matrix_action

    def monomial_basis(self):
        """
        EXAMPLES::
        
            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].monomial_basis()
            (1, i0, i1, i2)
        """
        return self.__monomial_basis

    def rank(self):
        """
        The rank of the algebra (as a free module).

        EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].rank()
            4
        """
        return self.__dim

    def module(self):
        """
        The free module of the algebra.

            sage: H = sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0]; H
            Free algebra quotient on 3 generators ('i', 'j', 'k') and dimension 4 over Rational Field
            sage: H.module()
            Vector space of dimension 4 over Rational Field
        """
        return self.__module

    def monoid(self):
        """
        The free monoid of generators of the algebra.

       EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].monoid()
            Free monoid on 3 generators (i0, i1, i2)
        """
        return self.__free_algebra.monoid()

    def monomial_basis(self):
        """
        The free monoid of generators of the algebra as elements of a free
        monoid.

       EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].monomial_basis()
            (1, i0, i1, i2)
        """
        return self.__monomial_basis

    def free_algebra(self):
        """
        The free algebra generating the algebra.

        EXAMPLES::

            sage: sage.algebras.free_algebra_quotient.hamilton_quatalg(QQ)[0].free_algebra()
            Free Algebra on 3 generators (i0, i1, i2) over Rational Field
        """
        return self.__free_algebra


def hamilton_quatalg(R):
    """
    Hamilton quaternion algebra over the commutative ring R,
    constructed as a free algebra quotient.

    INPUT:
        - R -- a commutative ring

    OUTPUT:
        - Q -- quaternion algebra
        - gens -- generators for Q

    EXAMPLES::

        sage: H, (i,j,k) = sage.algebras.free_algebra_quotient.hamilton_quatalg(ZZ)
        sage: H
        Free algebra quotient on 3 generators ('i', 'j', 'k') and dimension 4 over Integer Ring
        sage: i^2
        -1
        sage: i in H
        True

    Note that there is another vastly more efficient models for
    quaternion algebras in Sage; the one here is mainly for testing
    purposes::

        sage: R.<i,j,k> = QuaternionAlgebra(QQ,-1,-1)  # much fast than the above
    """
    n = 3
    from sage.algebras.free_algebra import FreeAlgebra
    from sage.matrix.all import MatrixSpace
    A = FreeAlgebra(R, n, 'i')
    F = A.monoid()
    i, j, k = F.gens()
    mons = [ F(1), i, j, k ]
    M = MatrixSpace(R,4)
    mats = [M([0,1,0,0, -1,0,0,0, 0,0,0,-1, 0,0,1,0]),  M([0,0,1,0, 0,0,0,1, -1,0,0,0, 0,-1,0,0]),  M([0,0,0,1, 0,0,-1,0, 0,1,0,0, -1,0,0,0]) ]
    H3 = FreeAlgebraQuotient(A,mons,mats, names=('i','j','k'))
    return H3, H3.gens()

