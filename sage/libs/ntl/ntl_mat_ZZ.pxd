include "decl.pxi"
include "../../ext/cdefs.pxi"

cdef class ntl_mat_ZZ:
    cdef mat_ZZ_c x
    cdef long __nrows, __ncols
