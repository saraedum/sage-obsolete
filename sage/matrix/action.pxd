from sage.structure.element cimport Element, Matrix, Vector
from sage.structure.parent_base cimport ParentWithBase
from sage.categories.action cimport Action

cdef class MatrixMulAction(Action):
    cdef ParentWithBase _codomain
    cdef bint fix_sparseness

cdef class MatrixMatrixAction(MatrixMulAction):
    pass

cdef class MatrixVectorAction(MatrixMulAction):
    pass

cdef class VectorMatrixAction(MatrixMulAction):
    pass

