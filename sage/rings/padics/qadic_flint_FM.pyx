from types import MethodType

include "../../libs/linkages/padics/fmpz_poly_unram.pxi"
include "../../libs/linkages/padics/unram_shared.pxi"
include "FM_template.pxi"

cdef class PowComputer_(PowComputer_flint_unram):
    def __init__(self, Integer prime, long cache_limit, long prec_cap, long ram_prec_cap, bint in_field, poly=None):
        self._prec_type = 'fixed-mod'
        PowComputer_flint_unram.__init__(self, prime, cache_limit, prec_cap, ram_prec_cap, in_field, poly)

cdef class qAdicFixedModElement(FMElement):
    frobenius = MethodType(frobenius_unram, None, qAdicFixedModElement)
    trace = MethodType(trace_unram, None, qAdicFixedModElement)
    norm = MethodType(norm_unram, None, qAdicFixedModElement)
    def _flint_rep(self, var='x'):
        """
        Replacement for _ntl_rep for use in printing and debugging.

        EXAMPLES::

            sage: R.<a> = ZqFM(27, 4)
            sage: (1+a).inverse_of_unit()._flint_rep()
            41*x^2 + 40*x + 42
            sage: (1+a)*(41*a^2+40*a+42)
            1 + O(3^4)
        """
        return self.prime_pow._new_fmpz_poly(self.value, var)

    def _flint_rep_abs(self, var='x'):
        """
        Replacement for _ntl_rep_abs for use in printing and debugging.

        EXAMPLES::

            sage: R.<a> = ZqFM(27, 4)
            sage: (3+3*a)._flint_rep_abs()
            (3*x + 3, 0)
        """
        return self._flint_rep(var), Integer(0)
