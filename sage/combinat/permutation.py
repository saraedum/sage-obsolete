r"""
Permutations

The Permutations module. Use Permutation? to get information about
the Permutation class, and Permutations? to get information about
the combinatorial class of permutations.

.. WARNING::

   This file defined :class:`Permutation_class` which depends upon
   :class:`CombinatorialObject` despite it being deprecated (see
   :trac:`13742`). This is dangerous. In particular, the
   :meth:`Permutation_class._left_to_right_multiply_on_right` method (which can
   be called trough multiplication) disables the input checks (see
   :meth:`Permutation`). This should not happen. Do not trust the results.

What does this file define ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main part of this file consists in te definition of permutation objects,
i.e. the :meth:`Permutation` method and the
:class:`~sage.combinat.permutation.Permutation_class` class. Global options for
elements of the permutation class can be set through the
:meth:`PermutationOptions` method.

Below are listed all methods and classes defined in this file.

**Methods of Permutations objects**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~sage.combinat.permutation.Permutation_class.size` | Returns the size of the permutation 'self'.
    :meth:`~sage.combinat.permutation.Permutation_class.cycle_string` | Returns a string of the permutation in cycle notation.
    :meth:`~sage.combinat.permutation.Permutation_class.next` | Returns the permutation that follows p in lexicographic order.
    :meth:`~sage.combinat.permutation.Permutation_class.prev` | Returns the permutation that comes directly before p in lexicographic order.
    :meth:`~sage.combinat.permutation.Permutation_class.to_tableau_by_shape` | Returns a tableau of shape shape with the entries in self.
    :meth:`~sage.combinat.permutation.Permutation_class.to_cycles` | Returns the permutation p as a list of disjoint cycles.
    :meth:`~sage.combinat.permutation.Permutation_class.to_permutation_group_element` | Returns a PermutationGroupElement equal to self.
    :meth:`~sage.combinat.permutation.Permutation_class.signature` | Returns the signature of a permutation.
    :meth:`~sage.combinat.permutation.Permutation_class.is_even` | Returns True if the permutation p is even and false otherwise.
    :meth:`~sage.combinat.permutation.Permutation_class.to_matrix` | Returns a matrix representing the permutation.
    :meth:`~sage.combinat.permutation.Permutation_class.rank` | Returns the rank of a permutation in lexicographic ordering.
    :meth:`~sage.combinat.permutation.Permutation_class.to_inversion_vector` | Returns the inversion vector of a permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.inversions` | Returns a list of the inversions of permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.show` | Displays the permutation as a drawing.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_inversions` | Returns the number of inversions in the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.length` | Returns the Coxeter length of a permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.inverse` | Returns the inverse of a permutation
    :meth:`~sage.combinat.permutation.Permutation_class.ishift` | Returns an the i-shift of self.
    :meth:`~sage.combinat.permutation.Permutation_class.iswitch` | Returns an the i-switch of self.
    :meth:`~sage.combinat.permutation.Permutation_class.runs` | Returns a list of the runs in the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.longest_increasing_subsequence_length` | Returns the length of the longest increasing subsequences
    :meth:`~sage.combinat.permutation.Permutation_class.longest_increasing_subsequences` | Returns the list of the longest increasing subsequences
    :meth:`~sage.combinat.permutation.Permutation_class.cycle_type` | Returns a partition of len(p) corresponding to the cycle type of p.
    :meth:`~sage.combinat.permutation.Permutation_class.to_lehmer_code` | Returns the Lehmer code of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.to_lehmer_cocode` | Returns the Lehmer cocode of p.
    :meth:`~sage.combinat.permutation.Permutation_class.reduced_word` | Returns the reduced word of a permutation.
    :meth:`~sage.combinat.permutation.Permutation_class.reduced_words` | Returns a list of the reduced words of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.reduced_word_lexmin` | Returns a lexicographically minimal reduced word of a permutation.
    :meth:`~sage.combinat.permutation.Permutation_class.fixed_points` | Returns a list of the fixed points of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_fixed_points` | Returns the number of fixed points of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.recoils` | Returns the list of the positions of the recoils of the permutation
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_recoils` | Returns the number of recoils of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.recoils_composition` | Returns the composition corresponding to recoils
    :meth:`~sage.combinat.permutation.Permutation_class.descents` | Returns the list of the descents of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.idescents` | Returns a list of the idescents of self
    :meth:`~sage.combinat.permutation.Permutation_class.idescents_signature` | Each position in self is mapped to -1 if it is an idescent and 1 if it is not an idescent.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_descents` | Returns the number of descents of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_idescents` | Returns the number of descents of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.descents_composition` | Returns the composition corresponding to the descents.
    :meth:`~sage.combinat.permutation.Permutation_class.descent_polynomial` | Returns the descent polynomial of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.major_index` | Returns the major index of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.imajor_index` | Returns the inverse major index of the permutation self.
    :meth:`~sage.combinat.permutation.Permutation_class.to_major_code` | Returns the major code of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.peaks` | Returns a list of the peaks of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_peaks` | Returns the number of peaks of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.saliances` | Returns a list of the saliances of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.number_of_saliances` | Returns the number of saliances of the permutation p.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_lequal` | Returns True if self is less than p2 in the Bruhat order.
    :meth:`~sage.combinat.permutation.Permutation_class.weak_excedences` | Returns all the numbers self[i] such that self[i] >= i+1.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_inversions` | Returns the list of inversions of p such that the application of this inversion to p decrements its number of inversions.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_inversions_iterator` | Returns an iterator over Bruhat inversions
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_succ` | Returns a list of the permutations strictly greater than p in the Bruhat order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_succ_iterator` | An iterator for the permutations that are strictly greater than p in the Bruhat order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_pred` | Returns a list of the permutations strictly smaller than p in the Bruhat order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_pred_iterator` | An iterator for the permutations strictly smaller than p in the Bruhat order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_smaller` | Returns a the combinatorial class of permutations smaller than or equal to p in the Bruhat order.
    :meth:`~sage.combinat.permutation.Permutation_class.bruhat_greater` | Returns the combinatorial class of permutations greater than or equal to p in the Bruhat order.
    :meth:`~sage.combinat.permutation.Permutation_class.permutohedron_lequal` | Returns True if self is less than p2 in the permutohedron order.
    :meth:`~sage.combinat.permutation.Permutation_class.permutohedron_succ` | Returns a list of the permutations strictly greater than p in the permutohedron order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.permutohedron_pred` | Returns a list of the permutations strictly smaller than p in the permutohedron order such that there is no permutation between one of those and p.
    :meth:`~sage.combinat.permutation.Permutation_class.permutohedron_smaller` | Returns a list of permutations smaller than or equal to p in the permutohedron order.
    :meth:`~sage.combinat.permutation.Permutation_class.permutohedron_greater` | Returns a list of permutations greater than or equal to p in the permutohedron order.
    :meth:`~sage.combinat.permutation.Permutation_class.has_pattern` | Tests whether the permutation matches the pattern.
    :meth:`~sage.combinat.permutation.Permutation_class.avoids` | Tests whether the permutation avoids the pattern.
    :meth:`~sage.combinat.permutation.Permutation_class.pattern_positions` | Returns the list of positions where the pattern patt appears in p.
    :meth:`~sage.combinat.permutation.Permutation_class.reverse` | Returns the permutation obtained by reversing the list.
    :meth:`~sage.combinat.permutation.Permutation_class.complement` | Returns the complement of the permutation which is obtained by replacing each value `x` in the list with `n - x + 1`
    :meth:`~sage.combinat.permutation.Permutation_class.dict` | Returns a dictionary corresponding to the permutation.
    :meth:`~sage.combinat.permutation.Permutation_class.action` | Returns the action of the permutation on a list.
    :meth:`~sage.combinat.permutation.Permutation_class.robinson_schensted` | Returns the pair of standard tableaux obtained by running the Robinson-Schensted Algorithm on self.
    :meth:`~sage.combinat.permutation.Permutation_class.left_tableau` | Returns the right standard tableau after performing the RSK
    :meth:`~sage.combinat.permutation.Permutation_class.right_tableau` | Returns the right standard tableau after performing the RSK
    :meth:`~sage.combinat.permutation.Permutation_class.remove_extra_fixed_points` | Returns the permutation obtained by removing any fixed points at the end of self.
    :meth:`~sage.combinat.permutation.Permutation_class.hyperoctahedral_double_coset_type` | Returns the coset-type of ``self`` as a partition.

**Other classes defined in this file**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :class:`Permutations_nk` |
    :class:`Permutations_mset` |
    :class:`Permutations_set` |
    :class:`Permutations_msetk` |
    :class:`Permutations_setk` |
    :meth:`Arrangements` |
    :class:`Arrangements_msetk` |
    :class:`Arrangements_setk` |
    :class:`StandardPermutations_all` |
    :class:`StandardPermutations_n` |
    :class:`StandardPermutations_descents` |
    :class:`StandardPermutations_recoilsfiner` |
    :class:`StandardPermutations_recoilsfatter` |
    :class:`StandardPermutations_recoils` |
    :class:`StandardPermutations_bruhat_smaller` |
    :class:`StandardPermutations_bruhat_greater` |
    :class:`CyclicPermutations_mset` |
    :meth:`CyclicPermutations` |
    :meth:`CyclicPermutationsOfPartition` |
    :class:`CyclicPermutationsOfPartition_partition` |
    :class:`StandardPermutations_avoiding_12` |
    :class:`StandardPermutations_avoiding_21` |
    :class:`StandardPermutations_avoiding_132` |
    :class:`StandardPermutations_avoiding_123` |
    :class:`StandardPermutations_avoiding_321` |
    :class:`StandardPermutations_avoiding_231` |
    :class:`StandardPermutations_avoiding_312` |
    :class:`StandardPermutations_avoiding_213` |
    :class:`StandardPermutations_avoiding_generic` |
    :class:`PatternAvoider` |
    :meth:`Permutations` |

**Functions defined in this file**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`from_major_code` | Returns the permutation corresponding to major code mc.
    :meth:`from_permutation_group_element` | Returns a Permutation give a PermutationGroupElement pge.
    :meth:`from_rank` | Returns the permutation with the specified lexicographic rank. The
    :meth:`from_inversion_vector` | Returns the permutation corresponding to inversion vector iv.
    :meth:`from_cycles` | Returns the permutation corresponding to cycles.
    :meth:`from_lehmer_code` | Returns the permutation with Lehmer code lehmer.
    :meth:`from_reduced_word` | Returns the permutation corresponding to the reduced word rw.
    :meth:`robinson_schensted_inverse` | Returns the permutation corresponding to the pair of tableaux `(p,q)`
    :meth:`bistochastic_as_sum_of_permutations` | Returns the matrix as a linear combination of permutations.
    :meth:`descents_composition_list` | Returns a list of all the permutations that have a descent
    :meth:`descents_composition_first` | Computes the smallest element of a descent class having a descent
    :meth:`descents_composition_last` | Returns the largest element of a descent class having a descent
    :meth:`bruhat_lequal` | Returns True if p1 is less than p2 in the Bruhat order.
    :meth:`permutohedron_lequal` | Returns True if p1 is less than p2 in the permutohedron order.
    :meth:`to_standard` | Returns a standard permutation corresponding to the permutation p.

AUTHORS:

- Mike Hansen

- Dan Drake (2008-04-07): allow Permutation() to take lists of tuples

- Sebastien Labbe (2009-03-17): added robinson_schensted_inverse

- Travis Scrimshaw (2012-08-16): to_standard() no longer modifies input

Classes and methods
===================
"""
#*****************************************************************************
#       Copyright (C) 2007 Mike Hansen <mhansen@gmail.com>,
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
from sage.interfaces.all import gap
from sage.rings.all import ZZ, Integer, PolynomialRing, factorial
from sage.matrix.all import matrix
from sage.combinat.tools import transitive_ideal
import sage.combinat.subword as subword
from sage.combinat.composition import Composition, Composition
import tableau
import sage.combinat.partition
from permutation_nk import PermutationsNK
from sage.groups.perm_gps.permgroup_named import SymmetricGroup
from sage.groups.perm_gps.permgroup_element import PermutationGroupElement
from sage.misc.prandom import sample
from sage.graphs.digraph import DiGraph
import itertools
import __builtin__
from combinat import CombinatorialClass, CombinatorialObject, catalan_number, InfiniteAbstractCombinatorialClass
import copy
from necklace import Necklaces
from sage.misc.misc import uniq
from backtrack import GenericBacktracker
from sage.combinat.combinatorial_map import combinatorial_map

permutation_options = {'display':'list', 'mult':'l2r'}

def PermutationOptions(**kwargs):
    """
    Sets the global options for elements of the permutation class. The
    defaults are for permutations to be displayed in list notation and
    the multiplication done from left to right (like in GAP).
    
    display: 'list' - the permutations are displayed in list notation
    'cycle' - the permutations are displayed in cycle notation
    'singleton' - the permutations are displayed in cycle notation with
    singleton cycles shown as well.
    
    mult: 'l2r' - the multiplication of permutations is done like
    composition of functions from left to right. That is, if we think
    of the permutations p1 and p2 as functions, then (p1\*p2)(x) =
    p2(p1(x)). This is the default in multiplication in GAP. 'r2l' -
    the multiplication of permutations is done right to left so that
    (p1\*p2)(x) = p1(p2(x))
    
    If no parameters are set, then the function returns a copy of the
    options dictionary.
    
    Note that these options have no effect on
    PermutationGroupElements.
    
    EXAMPLES::
    
        sage: p213 = Permutation([2,1,3])
        sage: p312 = Permutation([3,1,2])
        sage: PermutationOptions(mult='l2r', display='list')
        sage: po = PermutationOptions()
        sage: po['display']
        'list'
        sage: p213
        [2, 1, 3]
        sage: PermutationOptions(display='cycle')
        sage: p213
        (1,2)
        sage: PermutationOptions(display='singleton')
        sage: p213
        (1,2)(3)
        sage: PermutationOptions(display='list')
    
    ::
    
        sage: po['mult']
        'l2r'
        sage: p213*p312
        [1, 3, 2]
        sage: PermutationOptions(mult='r2l')
        sage: p213*p312
        [3, 2, 1]
        sage: PermutationOptions(mult='l2r')
    """
    global permutation_options
    if kwargs == {}:
        return copy.copy(permutation_options)
    
    if 'mult' in kwargs:
        if kwargs['mult'] not in ['l2r', 'r2l']:
            raise ValueError, "mult must be either 'l2r' or 'r2l'"
        else:
            permutation_options['mult'] = kwargs['mult']

    if 'display' in kwargs:
        if kwargs['display'] not in ['list', 'cycle', 'singleton']:
            raise ValueError, "display must be either 'cycle' or 'list'"
        else:
            permutation_options['display'] = kwargs['display']

def Permutation(l, check_input = True):
    """
    Converts ``l`` to a permutation on `1...n`

    INPUT:

    -  an instance of :class:`Permutation_class`,

    - list of integers, viewed as one-line permutation notation,

    - string, expressing the permutation in cycle notation,

    - list of tuples of integers, the permutation in cycle notation.

    - a :class:`PermutationGroupElement`

    - a pair of two tableaux of the same shape, where the second one is
      standard. This uses the inverse of Robinson Schensted algorithm.

    - ``check_input`` (boolean) -- whether to check that input is correct. Slows
       the function down, but ensures that nothing bad happens. This is set to
       ``True`` by default.

    .. WARNING::

       Since :trac:`13742` the input is checked for correctness : it is not
       accepted unless actually is a permutation on `1...n`. It means that some
       :meth:`Permutation` objects cannot be created anymore without setting
       ``check_input = False``, as there is no certainty that its functions can
       handle them, and this should be fixed in a much better way ASAP (the
       functions should be rewritten to handle those cases, and new tests be
       added).

    OUTPUT:

    - :class:`Permutation_class` object.

    EXAMPLES::

        sage: Permutation([2,1])
        [2, 1]
        sage: Permutation([2, 1, 4, 5, 3])
        [2, 1, 4, 5, 3]
        sage: Permutation('(1,2)')
        [2, 1]
        sage: Permutation('(1,2)(3,4,5)')
        [2, 1, 4, 5, 3]
        sage: Permutation( ((1,2),(3,4,5)) )
        [2, 1, 4, 5, 3]
        sage: Permutation( [(1,2),(3,4,5)] )
        [2, 1, 4, 5, 3]
        sage: Permutation( ((1,2)) )
        [2, 1]
        sage: Permutation( (1,2) )
        [2, 1]
        sage: Permutation( ((1,2),) )
        [2, 1]
        sage: p = Permutation((1, 2, 5)); p
        [2, 5, 3, 4, 1]
        sage: type(p)
        <class 'sage.combinat.permutation.Permutation_class'>
    
    Construction from a string in cycle notation
    
    ::
    
        sage: p = Permutation( '(4,5)' ); p
        [1, 2, 3, 5, 4]
    
    The size of the permutation is the maximum integer appearing; add
    a 1-cycle to increase this::
    
        sage: p2 = Permutation( '(4,5)(10)' ); p2
        [1, 2, 3, 5, 4, 6, 7, 8, 9, 10]
        sage: len(p); len(p2)
        5
        10
    
    We construct a Permutation from a PermutationGroupElement::
    
        sage: g = PermutationGroupElement([2,1,3])
        sage: Permutation(g)
        [2, 1, 3]
    
    From a pair of tableaux of the same shape. This uses the inverse
    of Robinson Schensted algorithm::

        sage: p = [[1, 4, 7], [2, 5], [3], [6]]
        sage: q = [[1, 2, 5], [3, 6], [4], [7]]
        sage: P = Tableau(p)
        sage: Q = Tableau(q)
        sage: Permutation( (p, q) )
        [3, 6, 5, 2, 7, 4, 1]
        sage: Permutation( [p, q] )
        [3, 6, 5, 2, 7, 4, 1]
        sage: Permutation( (P, Q) )
        [3, 6, 5, 2, 7, 4, 1]
        sage: Permutation( [P, Q] )
        [3, 6, 5, 2, 7, 4, 1]


    TESTS::

        sage: Permutation([()])
        [1]
        sage: Permutation('()')
        [1]
        sage: Permutation(())
        [1]

    From a pair of empty tableaux ::

        sage: Permutation( ([], []) )
        []
        sage: Permutation( [[], []] )
        []
    """
    if isinstance(l, Permutation_class):
        return l
    elif isinstance(l, PermutationGroupElement):
        l = l.list()

    #if l is a string, then assume it is in cycle notation
    elif isinstance(l, str):
        if l == "()":
            return from_cycles(1,[])
        cycles = l.split(")(")
        cycles[0] = cycles[0][1:]
        cycles[-1] = cycles[-1][:-1]
        cycle_list = []
        for c in cycles:
            cycle_list.append(map(int, c.split(",")))

        return from_cycles(max([max(c) for c in cycle_list]), cycle_list)

    #if l is a pair of tableaux or a pair of lists
    elif isinstance(l, (tuple, list)) and len(l) == 2 and \
        all(map(lambda x: isinstance(x, tableau.Tableau), l)):
        return robinson_schensted_inverse(*l)
    elif isinstance(l, (tuple, list)) and len(l) == 2 and \
        all(map(lambda x: isinstance(x, list), l)):
        P,Q = map(tableau.Tableau, l)
        return robinson_schensted_inverse(P, Q)

    # if it's a tuple or nonempty list of tuples, also assume cycle
    # notation
    elif isinstance(l, tuple) or \
         (isinstance(l, list) and len(l) > 0 and
         all(map(lambda x: isinstance(x, tuple), l))):
        if len(l) >= 1 and (isinstance(l[0],(int,Integer)) or len(l[0]) > 0):
            if isinstance(l[0], tuple):
                n = max( map(max, l) )
                return from_cycles(n, map(list, l))
            else:
                n = max(l)
                l = [list(l)]
                return from_cycles(n, l)
        elif len(l) <= 1:
            return Permutation([1])
        else:
            raise ValueError, "cannot convert l (= %s) to a Permutation"%l

    # otherwise, it gets processed by CombinatorialObject's __init__.
    return Permutation_class(l, check_input = check_input)

class Permutation_class(CombinatorialObject):
    def __init__(self, l, check_input = True):
        """
        Constructor. Checks that INPUT is not a mess, and calls
        :class:`CombinatorialObject`. It should not, because
        :class:`CombinatorialObject` is deprecated.

        INPUT:

        - ``l`` -- a list of ``int`` variables.

        - ``check_input`` (boolean) -- whether to check that input is
          correct. Slows the function down, but ensures that nothing bad
          happens.

          This is set to ``True`` by default.

        TESTS::

            sage: from sage.combinat.permutation import Permutation_class
            sage: Permutation_class([1,2,3])
            [1, 2, 3]
            sage: Permutation_class([1,2,2,4])
            Traceback (most recent call last):
            ...
            ValueError: An element appears twice in the input. It should not.
            sage: Permutation_class([1,2,4,-1])
            Traceback (most recent call last):
            ...
            ValueError: The elements must be strictly positive integers.
            sage: Permutation_class([1,2,4,5])
            Traceback (most recent call last):
            ...
            ValueError: The permutation has length 4 but its maximal element is
            5. Some element may be repeated, or an element is missing, but there
            is something wrong with its length.
        """
        if check_input:
            l = list(l)
            # Is input a list of positive integers ?
            for i in l:
                try:
                    i=int(i)
                except TypeError:
                    raise ValueError("The elements must be integer variables")
                if i < 1:
                    print i
                    raise ValueError("The elements must be strictly positive integers.")


            sorted_copy = list(l)

            # Empty list ?
            if len(sorted_copy) == 0:
                CombinatorialObject.__init__(self, l)


            else:
                sorted_copy.sort()
                # Is the maximum element of the permutation the length of input,
                # or is some integer missing ?
                if int(sorted_copy[-1]) != len(l):
                    raise ValueError("The permutation has length "+str(len(l))+
                                     " but its maximal element is "+
                                     str(int(sorted_copy[-1]))+". Some element "+
                                     "may be repeated, or an element is missing"+
                                     ", but there is something wrong with its length.")

                # Do the elements appear only once ?
                previous = sorted_copy[0]-1

                for i in sorted_copy:
                    if i == previous:
                        raise ValueError("An element appears twice in the input. It should not.")
                    else:
                        previous = i

                CombinatorialObject.__init__(self, l)
        else:
            CombinatorialObject.__init__(self, l)

    def __hash__(self):
        """
        TESTS::

            sage: d = {}
            sage: p = Permutation([1,2,3])
            sage: d[p] = 1
            sage: d[p]
            1
        """
        if self._hash is None:
            self._hash = str(self).__hash__()
        return self._hash

    def __str__(self):
        """
        TESTS::

            sage: PermutationOptions(display='list')
            sage: p = Permutation([2,1,3])
            sage: str(p)
            '[2, 1, 3]'
            sage: PermutationOptions(display='cycle')
            sage: str(p)
            '(1,2)'
            sage: PermutationOptions(display='singleton')
            sage: str(p)
            '(1,2)(3)'
            sage: PermutationOptions(display='list')
        """
        return repr(self)

    def __repr__(self):
        """
        TESTS::

            sage: PermutationOptions(display='list')
            sage: p = Permutation([2,1,3])
            sage: repr(p)
            '[2, 1, 3]'
            sage: PermutationOptions(display='cycle')
            sage: repr(p)
            '(1,2)'
            sage: PermutationOptions(display='singleton')
            sage: repr(p)
            '(1,2)(3)'
            sage: PermutationOptions(display='list')
        """
        global permutation_options
        display = permutation_options['display']
        if display == 'list':
            return repr(self._list)
        elif display == 'cycle':
            return self.cycle_string()
        elif display == 'singleton':
            return self.cycle_string(singletons=True)
        else:
            raise ValueError, "permutation_options['display'] should be one of 'list', 'cycle', or 'singleton'"

    def _gap_(self, gap):
        """
        Returns a GAP version of this permutation.
        
        EXAMPLES::
        
            sage: gap(Permutation([1,2,3]))
            ()
            sage: gap(Permutation((1,2,3)))
            (1,2,3)
            sage: type(_)
            <class 'sage.interfaces.gap.GapElement'>
        """
        return self.to_permutation_group_element()._gap_(gap)

    def size(self):
        """
        Returns the size of the permutation 'self'.

        EXAMPLES::
        
            sage: Permutation([3,4,1,2,5]).size()
            5
        """
        return len(self)

    def cycle_string(self, singletons=False):
        """
        Returns a string of the permutation in cycle notation.
        
        If singletons=True, it includes 1-cycles in the string.
        
        EXAMPLES::
        
            sage: Permutation([1,2,3]).cycle_string()
            '()'
            sage: Permutation([2,1,3]).cycle_string()
            '(1,2)'
            sage: Permutation([2,3,1]).cycle_string()
            '(1,2,3)'
            sage: Permutation([2,1,3]).cycle_string(singletons=True)
            '(1,2)(3)'
        """
        cycles = self.to_cycles(singletons=singletons)
        if cycles == []:
            return "()"
        else:
            return "".join(["("+",".join([str(l) for l in x])+")" for x in cycles])

    def next(self):
        r"""
        Returns the permutation that follows p in lexicographic order. If p
        is the last permutation, then next returns false.
        
        EXAMPLES::
        
            sage: p = Permutation([1, 3, 2])
            sage: p.next()
            [2, 1, 3]
            sage: p = Permutation([4,3,2,1])
            sage: p.next()
            False
        """
        p = self[:]
        n = len(self)
        first = -1

        #Starting from the end, find the first o such that
        #p[o] < p[o+1]
        for i in reversed(range(0,n-1)):
            if p[i] < p[i+1]:
                first = i
                break

        #If first is still -1, then we are already at the last permutation
        if first == -1:
            return False

        #Starting from the end, find the first j such that p[j] > p[first]
        j = n - 1
        while p[j] < p[first]:
            j -= 1

        #Swap positions first and j
        (p[j], p[first]) = (p[first], p[j])

        #Reverse the list between first and the end
        first_half = p[:first+1]
        last_half  = p[first+1:]
        last_half.reverse()
        p = first_half + last_half

        return Permutation(p)

    def prev(self):
        r"""
        Returns the permutation that comes directly before p in
        lexicographic order. If p is the first permutation, then it returns
        False.
        
        EXAMPLES::
        
            sage: p = Permutation([1,2,3])
            sage: p.prev()
            False
            sage: p = Permutation([1,3,2])
            sage: p.prev()
            [1, 2, 3]
        """

        p = self[:]
        n = len(self)
        first = -1

        #Starting from the beginning, find the first o such that
        #p[o] > p[o+1]
        for i in range(0, n-1):
            if p[i] > p[i+1]:
                first = i
                break

        #If first is still -1, that is we didn't find any descents,
        #then we are already at the last permutation
        if first == -1:
            return False

        #Starting from the end, find the first j such that p[j] > p[first]
        j = n - 1
        while p[j] > p[first]:
            j -= 1

        #Swap positions first and j
        (p[j], p[first]) = (p[first], p[j])

        #Reverse the list between first+1 and end
        first_half = p[:first+1]
        last_half  = p[first+1:]
        last_half.reverse()
        p = first_half + last_half

        return Permutation(p)

    
    def to_tableau_by_shape(self, shape):
        """
        Returns a tableau of shape shape with the entries in self.
        
        EXAMPLES::
        
            sage: Permutation([3,4,1,2,5]).to_tableau_by_shape([3,2])
            [[1, 2, 5], [3, 4]]
            sage: Permutation([3,4,1,2,5]).to_tableau_by_shape([3,2]).to_permutation()
            [3, 4, 1, 2, 5]
        """
        if sum(shape) != len(self):
            raise ValueError, "the size of the partition must be the size of self"

        t = []
        w = list(self)
        for i in reversed(shape):
            t = [ w[:i] ] + t
            w = w[i:]
        return tableau.Tableau(t)

    def to_cycles(self, singletons=True):
        """
        Returns the permutation p as a list of disjoint cycles.

        If ``singletons=False`` is given, don't returns the singletons in the
        list of cycles.

        EXAMPLES::

            sage: Permutation([2,1,3,4]).to_cycles()
            [(1, 2), (3,), (4,)]
            sage: Permutation([2,1,3,4]).to_cycles(singletons=False)
            [(1, 2)]

        The algorithm is of complexity `O(n)` where `n` is the size of the
        given permutation.

        TESTS::

            sage: from sage.combinat.permutation import from_cycles
            sage: for n in range(1,6):
            ...      for p in Permutations(n):
            ...         if from_cycles(n, p.to_cycles()) != p:
            ...            print "There is a problem with ",p
            ...            break
            sage: size = 10000
            sage: sample = (Permutations(size).random_element() for i in range(5))
            sage: all(from_cycles(size, p.to_cycles()) == p for p in sample)
            True


        Note: there is an alternative implementation called ``_to_cycle_set``
        which could be slightly (10%) faster for some input (typically for
        permutations of size in the range [100, 10000]. You can run the
        following benchmarks. For small permutations::

            sage: for size in range(9): # not tested
            ...    print size
            ...    lp = Permutations(size).list()
            ...    timeit('[p.to_cycles(False) for p in lp]')
            ...    timeit('[p._to_cycles_set(False) for p in lp]')
            ...    timeit('[p._to_cycles_list(False) for p in lp]')
            ...    timeit('[p._to_cycles_orig(False) for p in lp]') 

       and larger one::

            sage: for size in [10, 20, 50, 75, 100, 200, 500, 1000, # not tested
            ...         2000, 5000, 10000, 15000, 20000, 30000,
            ...         50000, 80000, 100000]: 
            ...      print(size)
            ...      lp = [Permutations(size).random_element() for i in range(20)]
            ...      timeit("[p.to_cycles() for p in lp]")
            ...      timeit("[p._to_cycles_set() for p in lp]")
            ...      timeit("[p._to_cycles_list() for p in lp]") # not tested
        """
        cycles = []

        l = self[:]

        #Go through until we've considered every number between 1 and len(p)
        for i in range(len(l)):
            if l[i] == False:
                continue
            cycleFirst = i+1
            cycle = [ cycleFirst ]
            l[i], next = False, l[i]
            while next != cycleFirst:
                cycle.append( next )
                l[next - 1], next  = False, l[next - 1]
            #Add the cycle to the list of cycles
            if singletons or len(cycle) > 1:
                cycles.append(tuple(cycle))
        return cycles

    cycle_tuples = to_cycles

    def _to_cycles_orig(self, singletons=True):
        r"""
        Returns the permutation p as a list of disjoint cycles.

        EXAMPLES::

            sage: Permutation([2,1,3,4])._to_cycles_orig()
            [(1, 2), (3,), (4,)]
            sage: Permutation([2,1,3,4])._to_cycles_orig(singletons=False)
            [(1, 2)]
        """
        p = self[:]
        cycles = []
        toConsider = -1

        #Create the list [1,2,...,len(p)]
        l = [ i+1 for i in range(len(p))]
        cycle = []

        #Go through until we've considered every number between
        #1 and len(p)
        while len(l) > 0:
            #If we are at the end of a cycle
            #then we want to add it to the cycles list
            if toConsider == -1:
                #Add the cycle to the list of cycles
                if singletons:
                    if cycle != []:
                        cycles.append(tuple(cycle))
                else:
                    if len(cycle) > 1:
                        cycles.append(tuple(cycle))
                #Start with the first element in the list
                toConsider = l[0]
                l.remove(toConsider)
                cycle = [ toConsider ]
                cycleFirst = toConsider

            #Figure out where the element under consideration
            #gets mapped to.
            next = p[toConsider - 1]

            #If the next element is the first one in the list
            #then we've reached the end of the cycle
            if next == cycleFirst:
                toConsider = -1
            else:
                cycle.append( next )
                l.remove( next )
                toConsider = next

        #When we're finished, add the last cycle
        if singletons:
            if cycle != []:
                cycles.append(tuple(cycle))
        else:
            if len(cycle) > 1:
                cycles.append(tuple(cycle))
        return cycles

    def _to_cycles_set(self, singletons=True):
        r"""
        Returns the permutation p as a list of disjoint cycles.

        EXAMPLES::

            sage: Permutation([2,1,3,4])._to_cycles_set()
            [(1, 2), (3,), (4,)]
            sage: Permutation([2,1,3,4])._to_cycles_set(singletons=False)
            [(1, 2)]

        TESTS::

            sage: all((p._to_cycles_set(False) == p._to_cycles_orig(False)
            ...            for i in range(7) for p in Permutations(i)))
            True
        """
        p = self[:]
        cycles = []

        if not singletons:
            #remove the fixed points
            L = set( i+1 for i,pi in enumerate(p) if pi != i+1 )
        else:
            L = set(range(1,len(p)+1))

        from bisect import bisect_left

        #Go through until we've considered every remaining number
        while len(L) > 0:
            # take the first remaining element
            cycleFirst = L.pop()
            next = p[cycleFirst-1]
            cycle = [cycleFirst]
            while next != cycleFirst:
                cycle.append(next)
                L.remove(next)
                next = p[next-1]
            # add the cycle
            cycles.append(tuple(cycle))

        return cycles

    def _to_cycles_list(self, singletons=True):
        r"""
        Returns the permutation p as a list of disjoint cycles.

        EXAMPLES::

            sage: Permutation([2,1,3,4])._to_cycles_list()
            [(1, 2), (3,), (4,)]
            sage: Permutation([2,1,3,4])._to_cycles_list(singletons=False)
            [(1, 2)]

        TESTS::

            sage: all((p._to_cycles_list(False) == p._to_cycles_orig(False)
            ...            for i in range(7) for p in Permutations(i)))
            True
        """
        p = self[:]
        cycles = []

        if not singletons:
            #remove the fixed points
            L = [i+1 for i,pi in enumerate(p) if pi != i+1]
        else:
            L = range(1,len(p)+1)

        from bisect import bisect_left

        #Go through until we've considered every remaining number
        while len(L) > 0:
            # take the first remaining element
            cycleFirst = L.pop(0)
            next = p[cycleFirst-1]
            cycle = [cycleFirst]
            while next != cycleFirst:
                cycle.append(next)
                # remove next from L
                # we use a binary search to find it
                L.pop(bisect_left(L,next))
                next = p[next-1]
            # add the cycle
            cycles.append(tuple(cycle))

        return cycles


    def to_permutation_group_element(self):
        """
        Returns a PermutationGroupElement equal to self.

        EXAMPLES::
        
            sage: Permutation([2,1,4,3]).to_permutation_group_element()
            (1,2)(3,4)
            sage: Permutation([1,2,3]).to_permutation_group_element()
            ()
        """
        cycles = self.to_cycles(singletons=False)
        grp = SymmetricGroup(len(self))
        if cycles == []:
            return PermutationGroupElement( '()', parent=grp )
        else:
            return PermutationGroupElement( cycles , parent=grp)

    def signature(p):
        r"""
        Returns the signature of a permutation. 

        .. NOTE::

            sign may be used as an alias to signature.
        
        EXAMPLES::
        
            sage: Permutation([4, 2, 3, 1, 5]).signature()
            -1
            sage: Permutation([1,3,2,5,4]).sign()
            1
        """
        return (-1)**(len(p)-len(p.to_cycles()))

    #one can also use sign as an alias for signature
    sign = signature

    def is_even(self):
        r"""
        Returns True if the permutation p is even and false otherwise.
        
        EXAMPLES::
        
            sage: Permutation([1,2,3]).is_even()
            True
            sage: Permutation([2,1,3]).is_even()
            False
        """

        if self.signature() == 1:
            return True
        else:
            return False


    def to_matrix(self):
        r"""
        Returns a matrix representing the permutation.
        
        EXAMPLES::
        
            sage: Permutation([1,2,3]).to_matrix()
            [1 0 0]
            [0 1 0]
            [0 0 1]
        
        ::
        
            sage: Permutation([1,3,2]).to_matrix()
            [1 0 0]
            [0 0 1]
            [0 1 0]
        
        Notice that matrix multiplication corresponds to permutation
        multiplication only when the permutation option mult='r2l'
        
        ::
        
            sage: PermutationOptions(mult='r2l')
            sage: p = Permutation([2,1,3])
            sage: q = Permutation([3,1,2])
            sage: (p*q).to_matrix()
            [0 0 1]
            [0 1 0]
            [1 0 0]
            sage: p.to_matrix()*q.to_matrix()
            [0 0 1]
            [0 1 0]
            [1 0 0]
            sage: PermutationOptions(mult='l2r')
            sage: (p*q).to_matrix()
            [1 0 0]
            [0 0 1]
            [0 1 0]
        """
        p = self[:]
        n = len(p)

        #Build the dictionary of entries since the matrix
        #is extremely sparse
        entries = {}
        for i in range(n):
            entries[(p[i]-1,i)] = 1
        return matrix(n, entries, sparse = True)

    def __mul__(self, rp):
        """
        TESTS::
        
            sage: p213 = Permutation([2,1,3])
            sage: p312 = Permutation([3,1,2])
            sage: PermutationOptions(mult='l2r')
            sage: p213*p312
            [1, 3, 2]
            sage: PermutationOptions(mult='r2l')
            sage: p213*p312
            [3, 2, 1]
            sage: PermutationOptions(mult='l2r')
        """
        global permutation_options
        if permutation_options['mult'] == 'l2r':
            return self._left_to_right_multiply_on_right(rp)
        else:
            return self._left_to_right_multiply_on_left(rp)

    def __rmul__(self, lp):
        """
        TESTS::

            sage: p213 = Permutation([2,1,3])
            sage: p312 = Permutation([3,1,2])
            sage: PermutationOptions(mult='l2r')
            sage: p213*p312
            [1, 3, 2]
            sage: PermutationOptions(mult='r2l')
            sage: p213*p312
            [3, 2, 1]
            sage: PermutationOptions(mult='l2r')
        """
        global permutation_options
        if permutation_options['mult'] == 'l2r':
            return self._left_to_right_multiply_on_left(lp)
        else:
            return self._left_to_right_multiply_on_right(lp)

    def _left_to_right_multiply_on_left(self,lp):
        """
        EXAMPLES::

            sage: p = Permutation([2,1,3])
            sage: q = Permutation([3,1,2])
            sage: p._left_to_right_multiply_on_left(q)
            [3, 2, 1]
            sage: q._left_to_right_multiply_on_left(p)
            [1, 3, 2]
        """
        #Pad the permutations if they are of
        #different sizes
        new_lp = lp[:] + [i+1 for i in range(len(lp), len(self))]
        new_p1 = self[:] + [i+1 for i in range(len(self), len(lp))]
        return Permutation([ new_p1[i-1] for i in new_lp ])

    def _left_to_right_multiply_on_right(self, rp):
        """
        EXAMPLES::

            sage: p = Permutation([2,1,3])
            sage: q = Permutation([3,1,2])
            sage: p._left_to_right_multiply_on_right(q)
            [1, 3, 2]
            sage: q._left_to_right_multiply_on_right(p)
            [3, 2, 1]
        """
        #Pad the permutations if they are of
        #different sizes
        new_rp = rp[:] + [i+1 for i in range(len(rp), len(self))]
        new_p1 = self[:] + [i+1 for i in range(len(self), len(rp))]
        return Permutation([ new_rp[i-1] for i in new_p1 ])

    def __call__(self, i):
        r"""
        Returns the image of the integer i under this permutation.
        
        EXAMPLES::
        
            sage: p = Permutation([2, 1, 4, 5, 3])
            sage: p(1)
            2
            sage: p = Permutation(((1,2),(4,3,5)))
            sage: p(4)
            3
            sage: p(2)
            1
            sage: p = Permutation([5,2,1,6,3,7,4])
            sage: map(p, range(1,8))
            [5, 2, 1, 6, 3, 7, 4]
        
        TESTS::
        
            sage: p = Permutation([5,2,1,6,3,7,4])
            sage: p(-1)
            Traceback (most recent call last):
            ...
            TypeError: i (= -1) must be between 1 and 7
            sage: p(10)
            Traceback (most recent call last):
            ...
            TypeError: i (= 10) must be between 1 and 7
        """
        if isinstance(i,(int,Integer)) and 1 <= i <= len(self):
            return self[i-1]
        else:
            raise TypeError, "i (= %s) must be between %s and %s" % (i,1,len(self))

    ########
    # Rank #
    ########

    def rank(self):
        r"""
        Returns the rank of a permutation in lexicographic ordering.
        
        EXAMPLES::
        
            sage: Permutation([1,2,3]).rank()
            0
            sage: Permutation([1, 2, 4, 6, 3, 5]).rank()
            10
            sage: perms = Permutations(6).list()
            sage: [p.rank() for p in perms ] == range(factorial(6))
            True
        """
        n = len(self)

        factoradic = self.to_lehmer_code()

        #Compute the index
        rank = 0
        for i in reversed(range(0, n)):
            rank += factoradic[n-1-i]*factorial(i)

        return rank

    ##############
    # Inversions #
    ##############

    def to_inversion_vector(self):
        r"""
        Returns the inversion vector of a permutation p.
        
        If `iv` is the inversion vector, then `iv[i]` is the number of elements
        larger than `i` that appear to the left of `i` in the permutation.
        
        The algorithm is of complexity `O(n\log(n))` where `n` is the size of
        the given permutation.

        EXAMPLES::
        
            sage: Permutation([5,9,1,8,2,6,4,7,3]).to_inversion_vector()
            [2, 3, 6, 4, 0, 2, 2, 1, 0]
            sage: Permutation([8,7,2,1,9,4,6,5,10,3]).to_inversion_vector()
            [3, 2, 7, 3, 4, 3, 1, 0, 0, 0]
            sage: Permutation([3,2,4,1,5]).to_inversion_vector()
            [3, 1, 0, 0, 0]

        TESTS::

            sage: from sage.combinat.permutation import from_inversion_vector
            sage: all(from_inversion_vector(p.to_inversion_vector()) == p
            ...     for n in range(6) for p in Permutations(n))
            True

            sage: P = Permutations(1000)
            sage: sample = (P.random_element() for i in range(5))
            sage: all(from_inversion_vector(p.to_inversion_vector()) == p
            ...     for p in sample) 
            True 
        """
        p = self._list
        l = len(p)
        # lightning fast if the length is less than 3
        # (is it really usefull?)
        if l<4:
            if l==0:
                return []
            if l==1:
                return [0]
            if l==2:
                return [p[0]-1,0]
            if l==3:
                if p[0]==1:
                    return [0,p[1]-2,0]
                if p[0]==2:
                    if p[1]==1:
                        return [1,0,0]
                    return [2,0,0]
                return [p[1],1,0]
        # choose the best one
        if l<411:
            return self._to_inversion_vector_small()
        else:
            return self._to_inversion_vector_divide_and_conquer()

    def _to_inversion_vector_orig(self):
        r"""
        Returns the inversion vector of a permutation p.

        (it's probably not the most efficient implementation)
        
        If iv is the inversion vector, then iv[i] is the number of elements
        larger than i that appear to the left of i in the permutation.

        EXAMPLE::
            sage: p = Permutation([5,9,1,8,2,6,4,7,3])
            sage: p._to_inversion_vector_orig()
            [2, 3, 6, 4, 0, 2, 2, 1, 0]
        
        """
        p = self._list
        iv = [0]*len(p)
        for i in xrange(len(p)):
            for pj in p:
                if pj>i+1:
                    iv[i]+=1
                elif pj == i+1:
                    break
        return iv

    def _to_inversion_vector_small(self):
        r"""
        Returns the inversion vector of a permutation p.

        (best choice for `5 < size < 420` approximately)
        
        If iv is the inversion vector, then iv[i] is the number of elements
        larger than i that appear to the left of i in the permutation.

        EXAMPLE::
            sage: p = Permutation([5,9,1,8,2,6,4,7,3])
            sage: p._to_inversion_vector_small()
            [2, 3, 6, 4, 0, 2, 2, 1, 0]
        
        """
        p = self._list
        l = len(p)+1
        iv = [0]*l
        checked = [1]*l
        for pi in reversed(p):
            checked[pi] = 0
            iv[pi] = sum(checked[pi:])
        return iv[1:]
    
    def _to_inversion_vector_divide_and_conquer(self):
        r"""
        Returns the inversion vector of a permutation p.

        (best choice for `size > 410` approximately)
        
        If iv is the inversion vector, then iv[i] is the number of elements
        larger than i that appear to the left of i in the permutation.

        EXAMPLE::
            sage: p = Permutation([5,9,1,8,2,6,4,7,3])
            sage: p._to_inversion_vector_divide_and_conquer()
            [2, 3, 6, 4, 0, 2, 2, 1, 0]
        
        """
        # for big permutations, 
        # we use a divide-and-conquer strategy
        # it's a merge sort, plus counting inversions
        def merge_and_countv((ivA,A),(ivB,B)):
            # iv* is the inversion vector of *
            C = []
            i,j = 0,0
            ivC = []
            lA, lB = len(A), len(B)
            while( i<lA and j<lB ):
                if B[j] < A[i]:
                    C.append(B[j])
                    ivC.append(ivB[j] + lA - i)
                    j += 1
                else:
                    C.append(A[i])
                    ivC.append(ivA[i])
                    i += 1
            if i < lA:
                C.extend(A[i:])
                ivC.extend(ivA[i:])
            else:
                C.extend(B[j:])
                ivC.extend(ivB[j:])
            return ivC,C

        def base_case(L):
            s = sorted(L)
            d = dict((j,i) for (i,j) in enumerate(s))
            iv = [0]*len(L)
            checked = [1]*len(L)
            for pi in reversed(L):
                dpi = d[pi]
                checked[dpi] = 0
                iv[dpi] = sum(checked[dpi:])
            return iv,s

        def sort_and_countv(L):
            if len(L)<250:
                return base_case(L)
            l = len(L)//2
            return merge_and_countv( sort_and_countv(L[:l]),
                                     sort_and_countv(L[l:]) )

        return sort_and_countv(self._list)[0]

    def inversions(self):
        r"""
        Returns a list of the inversions of permutation p.

        EXAMPLES::

            sage: Permutation([3,2,4,1,5]).inversions()
            [[0, 1], [0, 3], [1, 3], [2, 3]]
        """
        p = self[:]
        inversion_list = []

        for i in range(len(p)):
            for j in range(i+1,len(p)):
                if  p[i] > p[j]:
                    #inversion_list.append((p[i],p[j]))
                    inversion_list.append([i,j])

        return inversion_list

    def show(self, representation = "cycles", orientation = "landscape", **args):
        r"""
        Displays the permutation as a drawing.

        INPUT:

        - ``representation`` -- different kinds of drawings are available

            - ``"cycles"`` (default) -- the permutation is displayed as a
              collection of directed cycles

            - ``"braid"`` -- the permutation is displayed as segments linking
              each element `1, ..., n` to its image on a parallel line.

              When using this drawing, it is also possible to display the
              permutation horizontally (``orientation = "landscape"``, default
              option) or vertically (``orientation = "portrait"``).

            - ``"chord-diagram"`` -- the permutation is displayed as a directed
              graph, all of its vertices being located on a circle.

        All additional arguments are forwarded to the ``show`` subcalls.

        EXAMPLES::

            sage: Permutations(20).random_element().show(representation = "cycles")
            sage: Permutations(20).random_element().show(representation = "chord-diagram")
            sage: Permutations(20).random_element().show(representation = "braid")
            sage: Permutations(20).random_element().show(representation = "braid", orientation='portrait')

        TESTS::

            sage: Permutations(20).random_element().show(representation = "modern_art")
            Traceback (most recent call last):
            ...
            ValueError: The value of 'representation' must be equal to 'cycles', 'chord-digraph' or 'braid'
        """

        if representation == "cycles" or representation == "chord-diagram":
            from sage.graphs.digraph import DiGraph
            d = DiGraph(loops = True)
            for i in range(len(self)):
                d.add_edge(i+1, self[i])

            if representation == "cycles":
                d.show(**args)
            else:
                d.show(layout = "circular", **args)

        elif representation == "braid":
            from sage.plot.line import line
            from sage.plot.text import text

            if orientation == "landscape":
                r = lambda x,y : (x,y)
            elif orientation == "portrait":
                r = lambda x,y : (-y,x)
            else:
                raise ValueError("The value of 'orientation' must be either "+
                                 "'landscape' or 'portrait'.")

            p = self[:]

            L = line([r(1,1)])
            for i in range(len(p)):
                L += line([r(i,1.0), r(p[i]-1,0)])
                L += text(str(i), r(i,1.05)) + text(str(i), r(p[i]-1,-.05))

            return L.show(axes = False, **args)

        else:
            raise ValueError("The value of 'representation' must be equal to "+
                             "'cycles', 'chord-digraph' or 'braid'")


    def number_of_inversions(self):
        r"""
        Returns the number of inversions in the permutation p.

        An inversion of a permutation is a pair of elements (p[i],p[j])
        with i < j and p[i] > p[j].

        REFERENCES:

        - http://mathworld.wolfram.com/PermutationInversion.html
        
        EXAMPLES::
        
            sage: Permutation([3,2,4,1,5]).number_of_inversions()
            4
            sage: Permutation([1, 2, 6, 4, 7, 3, 5]).number_of_inversions()
            6
        """

        return sum(self.to_inversion_vector())


    def length(self):
        r"""
        Returns the Coxeter length of a permutation p. The length is given by
        the number of inversions of p.

        EXAMPLES::

            sage: Permutation([5, 1, 3, 4, 2]).length()
            6
        """
        return self.number_of_inversions()

    @combinatorial_map(order=2,name='inverse')
    def inverse(self):
        r"""
        Returns the inverse of a permutation

        EXAMPLES::

            sage: Permutation([3,8,5,10,9,4,6,1,7,2]).inverse()
            [8, 10, 1, 6, 3, 7, 9, 2, 5, 4]
            sage: Permutation([2, 4, 1, 5, 3]).inverse()
            [3, 1, 5, 2, 4]
        """
        w = range(len(self))
        for i,j in enumerate(self):
            w[j-1] = i+1
        return Permutation(w)

    def _icondition(self, i):
        """
        Returns a string which shows the relative positions of i-1,i,i+1 in
        self. Note that i corresponds to a 2 in the string.
        
        .. note::

           An imove can only be applied when the relative positions
           are one of '213', '132', '231', or '312'. None is returned
           in the other cases to signal that an imove cannot be
           applied.
        
        EXAMPLES::
        
            sage: Permutation([2,1,3])._icondition(2)
            ('213', 1, 0, 2)
            sage: Permutation([1,3,2])._icondition(2)
            ('132', 0, 2, 1)
            sage: Permutation([2,3,1])._icondition(2)
            ('231', 2, 0, 1)
            sage: Permutation([3,1,2])._icondition(2)
            ('312', 1, 2, 0)
            sage: Permutation([1,2,3])._icondition(2)
            (None, 0, 1, 2)
            sage: Permutation([1,3,2,4])._icondition(3)
            ('213', 2, 1, 3)
            sage: Permutation([2,1,3])._icondition(3)
            Traceback (most recent call last):
            ...
            ValueError: i (= 3) must be between 2 and n-1
        """
        if i not in range(2, len(self)):
            raise ValueError, "i (= %s) must be between 2 and n-1"%i
        pos_i   = self.index(i)
        pos_ip1 = self.index(i+1)
        pos_im1 = self.index(i-1)

        if pos_i < pos_im1 and pos_im1 < pos_ip1:
            state = '213'
        elif pos_im1 < pos_ip1 and pos_ip1 < pos_i:
            state =  '132'
        elif pos_i < pos_ip1 and pos_ip1 < pos_im1:
            state =  '231'
        elif pos_ip1 < pos_im1 and pos_im1 < pos_i:
            state = '312'
        else:
            state = None

        return (state, pos_im1, pos_i, pos_ip1)

    def ishift(self, i):
        """
        Returns an the i-shift of self. If an i-shift of self can't be
        performed, then None is returned.
        
        An i-shift can be applied when i is not in between i-1 and i+1. The
        i-shift moves i to the other side, and leaves the relative
        positions of i-1 and i+1 in place.
        
        EXAMPLES: Here, 2 is to the left of both 1 and 3. A 2-shift can be
        applied which moves the 2 to the right and leaves 1 and 3 in their
        same relative order.
        
        ::
        
            sage: Permutation([2,1,3]).ishift(2)
            [1, 3, 2]
        
        Note that the movement is done in place::
        
            sage: Permutation([2,4,1,3]).ishift(2)
            [1, 4, 3, 2]
        
        Since 2 is between 1 and 3 in [1,2,3], an 2-shift cannot be
        applied.
        
        ::
        
            sage: Permutation([1,2,3]).ishift(2) 
            [1, 2, 3]
        """
        state = self._icondition(i)
        if state[0] is None:
            return self

        state, pos_im1, pos_i, pos_ip1 = state
        l = list(self)
        
        if state == '213':   #goes to 132
            l[pos_i]   = i-1
            l[pos_im1] = i+1
            l[pos_ip1] = i
        elif state == '132': #goes to 213
            l[pos_im1] = i
            l[pos_ip1] = i-1
            l[pos_i]   = i+1
        elif state == '231': #goes to 312
            l[pos_i]   = i+1
            l[pos_ip1] = i-1
            l[pos_im1] = i
        elif state == '312': #goes to 231
            l[pos_ip1] = i
            l[pos_im1] = i+1
            l[pos_i]   = i-1
        else:
            raise ValueError, "invalid state"


        return Permutation_class(l)

        

    def iswitch(self, i):
        """
        Returns an the i-switch of self. If an i-switch of self can't be
        performed, then self is returned.
        
        An i-shift can be applied when i is not in between i-1 and i+1. The
        i-shift moves i to the other side, and switches the relative
        positions of i-1 and i+1 in place.
        
        EXAMPLES: Here, 2 is to the left of both 1 and 3. A 2-switch can be
        applied which moves the 2 to the right and switches the relative
        order between 1 and 3.
        
        ::
        
            sage: Permutation([2,1,3]).iswitch(2)
            [3, 1, 2]
        
        Note that the movement is done in place::
        
            sage: Permutation([2,4,1,3]).iswitch(2)
            [3, 4, 1, 2]
        
        Since 2 is between 1 and 3 in [1,2,3], an 2-switch cannot be
        applied.
        
        ::
        
            sage: Permutation([1,2,3]).iswitch(2) 
            [1, 2, 3]
        """
        if i not in range(2, len(self)):
            raise ValueError, "i (= %s) must between 2 and n-1"%i
        
        state = self._icondition(i)
        if state[0] is None:
            return self

        state, pos_im1, pos_i, pos_ip1 = state
        l = list(self)
        
        if state == '213':    #goes to 312
            l[pos_i]   = i+1
            l[pos_im1] = i-1
            l[pos_ip1] = i
        elif state == '132':  #goes to 231
            l[pos_im1] = i
            l[pos_ip1] = i+1
            l[pos_i]   = i-1
        elif state == '231':  #goes to 132
            l[pos_i]   = i-1
            l[pos_ip1] = i+1
            l[pos_im1] = i
        elif state == '312':  #goes to 213
            l[pos_ip1] = i    
            l[pos_im1] = i-1
            l[pos_i]   = i+1
        else:
            raise ValueError, "invalid state"


        return Permutation_class(l)

    def runs(self):
        r"""
        Returns a list of the runs in the permutation p.
        
        REFERENCES:

        - http://mathworld.wolfram.com/PermutationRun.html
        
        EXAMPLES::
        
            sage: Permutation([1,2,3,4]).runs()
            [[1, 2, 3, 4]]
            sage: Permutation([4,3,2,1]).runs()
            [[4], [3], [2], [1]]
            sage: Permutation([2,4,1,3]).runs()
            [[2, 4], [1, 3]]
        """
        p = self[:]
        runs = []
        current_value = p[0]
        current_run = [p[0]]
        for i in range(1, len(p)):
            if p[i] < current_value:
                runs.append(current_run)
                current_run = [p[i]]
            else:
                current_run.append(p[i])

            current_value = p[i]
        runs.append(current_run)

        return runs

    def longest_increasing_subsequence_length(self):
        r"""
        Returns the length of the longest increasing subsequences of the
        permutation p.

        EXAMPLES::
        
            sage: Permutation([2,3,1,4]).longest_increasing_subsequence_length()
            3
            sage: all([i.longest_increasing_subsequence_length() == len(i.robinson_schensted()[0][0]) for i in Permutations(5)])
            True
        """
        r=[]
        for x in self:
            if max(r+[0]) > x:
                y = min(filter(lambda z: z > x, r))
                r[r.index(y)] = x
            else:
                r.append(x)
        return len(r)

    def longest_increasing_subsequences(self):
        r"""
        Returns the list of the longest increasing subsequences of the
        permutation p.

        .. note::

           The algorithm is not optimal.
        
        EXAMPLES::
        
            sage: Permutation([2,3,4,1]).longest_increasing_subsequences()
            [[2, 3, 4]]
            sage: Permutation([5, 7, 1, 2, 6, 4, 3]).longest_increasing_subsequences()
            [[1, 2, 6], [1, 2, 4], [1, 2, 3]]
        """
        patt=range(1,self.longest_increasing_subsequence_length()+1)
        return map(lambda m : map(lambda i : self[i],m) , self.pattern_positions(patt))

    def cycle_type(self):
        r"""
        Returns a partition of len(p) corresponding to the cycle type of p.
        This is a non-increasing sequence of the cycle lengths of p.
        
        EXAMPLES::
        
            sage: Permutation([3,1,2,4]).cycle_type()
            [3, 1]
        """
        cycle_type = [len(c) for c in self.to_cycles()]
        cycle_type.sort(reverse=True)
        return sage.combinat.partition.Partition(cycle_type)

    def to_lehmer_code(self):
        r"""
        Returns the Lehmer code of the permutation p.
        `c[i]` is the number of `j>i` such that `p(j)<p(i)`.

        EXAMPLES::
        
            sage: p = Permutation([2,1,3])
            sage: p.to_lehmer_code()
            [1, 0, 0]
            sage: q = Permutation([3,1,2])
            sage: q.to_lehmer_code()
            [2, 0, 0]


        TESTS::

            sage: from sage.combinat.permutation import from_lehmer_code
            sage: all(from_lehmer_code(p.to_lehmer_code()) == p
            ...     for n in range(6) for p in Permutations(n))
            True
            
            sage: P = Permutations(1000)
            sage: sample = (P.random_element() for i in range(5))
            sage: all(from_lehmer_code(p.to_lehmer_code()) == p
            ...     for p in sample) 
            True 

        """
        l = len(self._list)
        # choose the best implementations
        if l<577:
            return self._to_lehmer_code_small()
        else:
            return self.inverse().to_inversion_vector()

    def _to_lehmer_code_small(self):
        r"""
        Returns the Lehmer code of the permutation p.
        `c[i]` is the number of `j>i` such that `p(j)<p(i)`.

        (best choice for `size<577` approximately)
        
        EXAMPLES::
        
            sage: p = Permutation([7, 6, 10, 2, 3, 4, 8, 1, 9, 5])
            sage: p._to_lehmer_code_small()
            [6, 5, 7, 1, 1, 1, 2, 0, 1, 0]
        """
        p = self._list
        l = len(p)
        lehmer = []
        checked = [1]*l
        for pi in p:
            checked[pi-1] = 0
            lehmer.append(sum(checked[:pi]))
        return lehmer

    def to_lehmer_cocode(self):
        r"""
        Returns the Lehmer cocode of p.
        
        EXAMPLES::
        
            sage: p = Permutation([2,1,3])
            sage: p.to_lehmer_cocode()
            [0, 1, 0]
            sage: q = Permutation([3,1,2])
            sage: q.to_lehmer_cocode()
            [0, 1, 1]
        """
        p = self[:]
        n = len(p)
        cocode = [0] * n
        for i in range(1, n):
            for j in range(0, i):
                if p[j] > p[i]:
                    cocode[i] += 1
        return cocode



    #################
    # Reduced Words #
    #################

    def reduced_word(self):
        r"""
        Returns the reduced word of a permutation.
        
        EXAMPLES::
        
            sage: Permutation([3,5,4,6,2,1]).reduced_word()
            [2, 1, 4, 3, 2, 4, 3, 5, 4, 5]
        """
        code = self.to_lehmer_code()
        reduced_word = []
        for piece in  [ [ i + code[i] - j for j in range(code[i])] for i in range(len(code))]:
            reduced_word += piece

        return reduced_word

    def reduced_words(self):
        r"""
        Returns a list of the reduced words of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([2,1,3]).reduced_words()
            [[1]]
            sage: Permutation([3,1,2]).reduced_words()
            [[2, 1]]
            sage: Permutation([3,2,1]).reduced_words()
            [[1, 2, 1], [2, 1, 2]]
            sage: Permutation([3,2,4,1]).reduced_words()
            [[1, 2, 3, 1], [1, 2, 1, 3], [2, 1, 2, 3]]
        """
        p = self[:]
        n = len(p)
        rws = []
        descents = self.descents()

        if len(descents) == 0:
            return [[]]

        for d in descents:
            pp = p[:d] + [p[d+1]] + [p[d]] + p[d+2:]
            z = lambda x: x + [d+1]
            rws += (map(z, Permutation(pp).reduced_words()))

        return rws



    def reduced_word_lexmin(self):
        r"""
        Returns a lexicographically minimal reduced word of a permutation.
        
        EXAMPLES::
        
            sage: Permutation([3,4,2,1]).reduced_word_lexmin()
            [1, 2, 1, 3, 2]
        """
        cocode = self.inverse().to_lehmer_cocode()

        rw = []
        for i in range(len(cocode)):
            piece = [j+1 for j in range(i-cocode[i],i)]
            piece.reverse()
            rw += piece

        return rw


    ################
    # Fixed Points #
    ################

    def fixed_points(self):
        r"""
        Returns a list of the fixed points of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([1,3,2,4]).fixed_points()
            [1, 4]
            sage: Permutation([1,2,3,4]).fixed_points()
            [1, 2, 3, 4]
        """
        fixed_points = []
        for i in range(len(self)):
            if i+1 == self[i]:
                fixed_points.append(i+1)

        return fixed_points

    def number_of_fixed_points(self):
        r"""
        Returns the number of fixed points of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([1,3,2,4]).number_of_fixed_points()
            2
            sage: Permutation([1,2,3,4]).number_of_fixed_points()
            4
        """

        return len(self.fixed_points())


    ############
    # Recoils  #
    ############
    def recoils(self):
        r"""
        Returns the list of the positions of the recoils of the permutation
        p.
        
        A recoil of a permutation is an integer i such that i+1 is to the
        left of it.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).recoils()
            [2, 3]
        """
        p = self
        recoils  = []
        for i in range(len(p)):
            if p[i] != len(self) and self.index(p[i]+1) < i:
                recoils.append(i)

        return recoils

    def number_of_recoils(self):
        r"""
        Returns the number of recoils of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).number_of_recoils()
            2
        """
        return len(self.recoils())

    def recoils_composition(self):
        """
        Returns the composition corresponding to recoils of the
        permutation.
        
        EXAMPLES::
        
            sage: Permutation([1,3,2,4]).recoils_composition()
            [3]
        """
        d = self.recoils()
        d = [ -1 ] + d
        return [ d[i+1]-d[i] for i in range(len(d)-1)]


    ############
    # Descents #
    ############

    def descents(self, final_descent=False):
        r"""
        Returns the list of the descents of the permutation p.
        
        A descent of a permutation is an integer i such that p[i] > p[i+1].
        With the final_descent option, the last position of a non empty
        permutation is also considered as a descent.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).descents()
            [1, 2]
            sage: Permutation([1,4,3,2]).descents(final_descent=True)
            [1, 2, 3]
        """
        p = self
        descents = []
        for i in range(len(p)-1):
            if p[i] > p[i+1]:
                descents.append(i)

        if final_descent:
            descents.append(len(p)-1)

        return descents

    def idescents(self, final_descent=False):
        """
        Returns a list of the idescents of self, that is the list of the
        descents of self's inverse.
        
        With the final_descent option, the last position of a non empty
        permutation is also considered as a descent.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).idescents()
            [1, 2]
            sage: Permutation([1,4,3,2]).idescents(final_descent=True)
            [1, 2, 3]
        """
        return self.inverse().descents(final_descent=final_descent)

    def idescents_signature(self, final_descent=False):
        """
        Each position in self is mapped to -1 if it is an idescent and 1 if
        it is not an idescent.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).idescents()
            [1, 2]
            sage: Permutation([1,4,3,2]).idescents_signature()
            [1, -1, -1, 1]
        """
        idescents = self.idescents(final_descent=final_descent)
        d = {True:-1, False:1}
        return [d[i in idescents] for i in range(len(self))]

    def number_of_descents(self, final_descent=False):
        r"""
        Returns the number of descents of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).number_of_descents()
            2
            sage: Permutation([1,4,3,2]).number_of_descents(final_descent=True)
            3
        """
        return len(self.descents(final_descent))
    
    def number_of_idescents(self, final_descent=False):
        r"""
        Returns the number of descents of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2]).number_of_idescents()
            2
            sage: Permutation([1,4,3,2]).number_of_idescents(final_descent=True)
            3
        """
        return len(self.idescents(final_descent))

    @combinatorial_map(name='descent composition')
    def descents_composition(self):
        """
        Returns the composition corresponding to the descents of the
        permutation.

        EXAMPLES::

            sage: Permutation([1,3,2,4]).descents_composition()
            [2, 2]
        """
        d = self.descents()
        d = [ -1 ] + d + [len(self)-1]
        return Composition([ d[i+1]-d[i] for i in range(len(d)-1)])

    def descent_polynomial(self):
        r"""
        Returns the descent polynomial of the permutation p.
        
        The descent polynomial of p is the product of all the z[p[i]] where
        i ranges over the descents of p.
        
        REFERENCES:

        - Garsia and Stanton 1984
        
        EXAMPLES::
        
            sage: Permutation([2,1,3]).descent_polynomial()
            z1
            sage: Permutation([4,3,2,1]).descent_polynomial()
            z1*z2^2*z3^3
        """
        p = self
        z = []
        P = PolynomialRing(ZZ, len(p), 'z')
        z = P.gens()
        result = 1
        pol = 1
        for i in range(len(p)-1):
            pol *= z[p[i]-1]
            if p[i] > p[i+1]:
                result *= pol

        return result


    ##############
    # Major Code #
    ##############

    def major_index(self, final_descent=False):
        r"""
        Returns the major index of the permutation p.
        
        The major index is the sum of the descents of p. Since our
        permutation indices are 0-based, we need to add one the number of
        descents.
        
        EXAMPLES::
        
            sage: Permutation([2,1,3]).major_index()
            1
            sage: Permutation([3,4,1,2]).major_index()
            2
            sage: Permutation([4,3,2,1]).major_index()
            6
        """
        descents = self.descents(final_descent)

        return sum(descents)+len(descents)

    def imajor_index(self, final_descent=False):
        """
        Returns the inverse major index of the permutation self, which is
        the major index of the inverse of self.
        
        The major index is the sum of the descents of p. Since our
        permutation indices are 0-based, we need to add one the number of
        descents.
        
        EXAMPLES::
        
            sage: Permutation([2,1,3]).imajor_index()
            1
            sage: Permutation([3,4,1,2]).imajor_index()
            2
            sage: Permutation([4,3,2,1]).imajor_index()
            6
        """
        idescents = self.idescents(final_descent)

        return sum(idescents)+len(idescents)

    def to_major_code(self, final_descent=False):
        r"""
        Returns the major code of the permutation p, which is defined as
        the list [m1-m2, m2-m3,..,mn] where mi := maj(pi) is the major
        indices of the permutation math obtained by erasing the letters
        smaller than math in p.
        
        REFERENCES:

        - Carlitz, L. 'q-Bernoulli and Eulerian Numbers' Trans.
          Amer. Math. Soc. 76 (1954) 332-350 Skandera, M. 'An Eulerian
          Partner for Inversions', Sem. Lothar. Combin. 46 (2001)
          B46d.
        
        EXAMPLES::
        
            sage: Permutation([9,3,5,7,2,1,4,6,8]).to_major_code()
            [5, 0, 1, 0, 1, 2, 0, 1, 0]
            sage: Permutation([2,8,4,3,6,7,9,5,1]).to_major_code()
            [8, 3, 3, 1, 4, 0, 1, 0, 0]
        """
        p = self
        major_indices = [0]*(len(p)+1)
        smaller = p[:]
        for i in range(len(p)):
            major_indices[i] = Permutation(smaller).major_index(final_descent)
            #Create the permutation that "erases" all the numbers
            #smaller than i+1
            smaller.remove(1)
            smaller = [i-1 for i in smaller]

        major_code = [ major_indices[i] - major_indices[i+1] for i in range(len(p)) ]
        return major_code

    #########
    # Peaks #
    #########

    def peaks(self):
        r"""
        Returns a list of the peaks of the permutation p.
        
        A peak of a permutation is an integer i such that p[i-1] < p[i] and
        p[i] > p[i+1].
        
        EXAMPLES::
        
            sage: Permutation([1,3,2,4,5]).peaks()
            [1]
            sage: Permutation([4,1,3,2,6,5]).peaks()
            [2, 4]
        """
        p = self
        peaks = []
        for i in range(1,len(p)-1):
            if p[i-1] <= p[i] and p[i] > p[i+1]:
                peaks.append(i)

        return peaks


    def number_of_peaks(self):
        r"""
        Returns the number of peaks of the permutation p.
        
        A peak of a permutation is an integer i such that p[i-1] < p[i] and
        p[i] > p[i+1].
        
        EXAMPLES::
        
            sage: Permutation([1,3,2,4,5]).number_of_peaks()
            1
            sage: Permutation([4,1,3,2,6,5]).number_of_peaks()
            2
        """
        return len(self.peaks())

    #############
    # Saliances #
    #############

    def saliances(self):
        r"""
        Returns a list of the saliances of the permutation p.
        
        A saliance of a permutation p is an integer i such that p[i] > p[j]
        for all j > i.
        
        EXAMPLES::
        
            sage: Permutation([2,3,1,5,4]).saliances()
            [3, 4]
            sage: Permutation([5,4,3,2,1]).saliances()
            [0, 1, 2, 3, 4]
        """
        p = self
        saliances = []
        for i in range(len(p)):
            is_saliance = True
            for j in range(i+1, len(p)):
                if p[i] <= p[j]:
                    is_saliance = False
            if is_saliance:
                saliances.append(i)

        return saliances


    def number_of_saliances(self):
        r"""
        Returns the number of saliances of the permutation p.
        
        EXAMPLES::
        
            sage: Permutation([2,3,1,5,4]).number_of_saliances()
            2
            sage: Permutation([5,4,3,2,1]).number_of_saliances()
            5
        """
        return len(self.saliances())

    ################
    # Bruhat Order #
    ################
    def bruhat_lequal(self, p2):
        r"""
        Returns True if self is less than p2 in the Bruhat order.
        
        EXAMPLES::
        
            sage: Permutation([2,4,3,1]).bruhat_lequal(Permutation([3,4,2,1])) 
            True
        """
        p1 = self
        n1 = len(p1)

        if n1 == 0:
            return True

        if p1[0] > p2[0] or p1[n1-1] < p2[n1-1]:
            return False

        for i in range(n1):
            c = 0
            for j in range(n1):
                if p2[j] > i+1:
                    c += 1
                if p1[j] > i+1:
                    c -= 1
                if c < 0:
                    return False

        return True

    def weak_excedences(self):
        """
        Returns all the numbers self[i] such that self[i] >= i+1.
        
        EXAMPLES::
        
            sage: Permutation([1,4,3,2,5]).weak_excedences()
            [1, 4, 3, 5]
        """
        res = []
        for i in range(len(self)):
            if self[i] >= i + 1:
                res.append(self[i])
        return res
    

    def bruhat_inversions(self):
        r"""
        Returns the list of inversions of p such that the application of
        this inversion to p decrements its number of inversions.
        
        Equivalently, it returns the list of pairs (i,j), i < j such that p[i]
        < p[j] and such that there exists no k between i and j satisfying
        p[i] < p[k].
        
        EXAMPLES::
        
            sage: Permutation([5,2,3,4,1]).bruhat_inversions()
            [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4]]
            sage: Permutation([6,1,4,5,2,3]).bruhat_inversions()
            [[0, 1], [0, 2], [0, 3], [2, 4], [2, 5], [3, 4], [3, 5]]
        """
        return __builtin__.list(self.bruhat_inversions_iterator())

    def bruhat_inversions_iterator(self):
        """
        Returns the iterator for the inversions of p such that the
        application of this inversion to p decrements its number of
        inversions.
        
        EXAMPLES::
        
            sage: list(Permutation([5,2,3,4,1]).bruhat_inversions_iterator())
            [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4]]
            sage: list(Permutation([6,1,4,5,2,3]).bruhat_inversions_iterator())
            [[0, 1], [0, 2], [0, 3], [2, 4], [2, 5], [3, 4], [3, 5]]
        """
        p = self
        n = len(p)

        for i in range(n-1):
            for j in range(i+1,n):
                if p[i] > p[j]:
                    ok = True
                    for k in range(i+1, j):
                        if p[i] > p[k] and p[k] > p[j]:
                            ok = False
                            break
                    if ok:
                        yield [i,j]


    def bruhat_succ(self):
        r"""
        Returns a list of the permutations strictly greater than p in the
        Bruhat order such that there is no permutation between one of those
        and p.
        
        EXAMPLES::
        
            sage: Permutation([6,1,4,5,2,3]).bruhat_succ()
            [[6, 4, 1, 5, 2, 3],
             [6, 2, 4, 5, 1, 3],
             [6, 1, 5, 4, 2, 3],
             [6, 1, 4, 5, 3, 2]]
        """
        return __builtin__.list(self.bruhat_succ_iterator())

    def bruhat_succ_iterator(self):
        """
        An iterator for the permutations that are strictly greater than p
        in the Bruhat order such that there is no permutation between one
        of those and p.
        
        EXAMPLES::
        
            sage: [x for x in Permutation([6,1,4,5,2,3]).bruhat_succ_iterator()]
            [[6, 4, 1, 5, 2, 3],
             [6, 2, 4, 5, 1, 3],
             [6, 1, 5, 4, 2, 3],
             [6, 1, 4, 5, 3, 2]]
        """
        p = self
        n = len(p)

        for z in Permutation(map(lambda x: n+1-x, p)).bruhat_inversions_iterator():
            pp = p[:]
            pp[z[0]] = p[z[1]]
            pp[z[1]] = p[z[0]]
            yield Permutation(pp)



    def bruhat_pred(self):
        r"""
        Returns a list of the permutations strictly smaller than p in the
        Bruhat order such that there is no permutation between one of those
        and p.
        
        EXAMPLES::
        
            sage: Permutation([6,1,4,5,2,3]).bruhat_pred()
            [[1, 6, 4, 5, 2, 3],
             [4, 1, 6, 5, 2, 3],
             [5, 1, 4, 6, 2, 3],
             [6, 1, 2, 5, 4, 3],
             [6, 1, 3, 5, 2, 4],
             [6, 1, 4, 2, 5, 3],
             [6, 1, 4, 3, 2, 5]]
        """
        return __builtin__.list(self.bruhat_pred_iterator())

    def bruhat_pred_iterator(self):
        """
        An iterator for the permutations strictly smaller than p in the
        Bruhat order such that there is no permutation between one of those
        and p.
        
        EXAMPLES::
        
            sage: [x for x in Permutation([6,1,4,5,2,3]).bruhat_pred_iterator()]
            [[1, 6, 4, 5, 2, 3],
             [4, 1, 6, 5, 2, 3],
             [5, 1, 4, 6, 2, 3],
             [6, 1, 2, 5, 4, 3],
             [6, 1, 3, 5, 2, 4],
             [6, 1, 4, 2, 5, 3],
             [6, 1, 4, 3, 2, 5]]
        """
        p = self
        for z in p.bruhat_inversions_iterator():
            pp = p[:]
            pp[z[0]] = p[z[1]]
            pp[z[1]] = p[z[0]]
            yield Permutation(pp)


    def bruhat_smaller(self):
        r"""
        Returns a the combinatorial class of permutations smaller than or
        equal to p in the Bruhat order.
        
        EXAMPLES::
        
            sage: Permutation([4,1,2,3]).bruhat_smaller().list()
            [[1, 2, 3, 4],
             [1, 2, 4, 3],
             [1, 3, 2, 4],
             [1, 4, 2, 3],
             [2, 1, 3, 4],
             [2, 1, 4, 3],
             [3, 1, 2, 4],
             [4, 1, 2, 3]]
        """
        return StandardPermutations_bruhat_smaller(self)


    def bruhat_greater(self):
        r"""
        Returns the combinatorial class of permutations greater than or
        equal to p in the Bruhat order.
        
        EXAMPLES::
        
            sage: Permutation([4,1,2,3]).bruhat_greater().list()
            [[4, 1, 2, 3],
             [4, 1, 3, 2],
             [4, 2, 1, 3],
             [4, 2, 3, 1],
             [4, 3, 1, 2],
             [4, 3, 2, 1]]
        """

        return StandardPermutations_bruhat_greater(self)

    ########################
    # Permutohedron  Order #
    ########################

    def permutohedron_lequal(self, p2, side="right"):
        r"""
        Returns True if self is less than p2 in the permutohedron order.
        
        By default, the computations are done in the right permutohedron.
        If you pass the option side='left', then they will be done in the
        left permutohedron.
        
        EXAMPLES::
        
            sage: p = Permutation([3,2,1,4])
            sage: p.permutohedron_lequal(Permutation([4,2,1,3]))
            False
            sage: p.permutohedron_lequal(Permutation([4,2,1,3]), side='left') 
            True
        """
        p1 = self
        l1 = p1.number_of_inversions()
        l2 = p2.number_of_inversions()

        if l1 > l2:
            return False

        if side == "right":
            prod = p1._left_to_right_multiply_on_right(p2.inverse())
        else:
            prod = p1._left_to_right_multiply_on_left(p2.inverse())

        return prod.number_of_inversions() == l2 - l1

    def permutohedron_succ(self, side="right"):
        r"""
        Returns a list of the permutations strictly greater than p in the
        permutohedron order such that there is no permutation between one
        of those and p.
        
        By default, the computations are done in the right permutohedron.
        If you pass the option side='left', then they will be done in the
        left permutohedron.
        
        EXAMPLES::
        
            sage: p = Permutation([4,2,1,3])
            sage: p.permutohedron_succ()
            [[4, 2, 3, 1]]
            sage: p.permutohedron_succ(side='left')
            [[4, 3, 1, 2]]
        """
        p = self
        n = len(p)
        succ = []
        if side == "right":
            rise = lambda perm: [i for i in range(0,n-1) if perm[i] < perm[i+1]]
            for i in rise(p):
                pp = p[:]
                pp[i] = p[i+1]
                pp[i+1] = p[i]
                succ.append(Permutation(pp))
        else:
            advance = lambda perm: [i for i in range(1,n) if  perm.index(i) < perm.index(i+1)]
            for i in advance(p):
                pp = p[:]
                pp[p.index(i)] = i+1
                pp[p.index(i+1)] = i            
                succ.append(Permutation(pp))

        return succ


    def permutohedron_pred(self, side="right"):
        r"""
        Returns a list of the permutations strictly smaller than p in the
        permutohedron order such that there is no permutation between one
        of those and p.
        
        By default, the computations are done in the right permutohedron.
        If you pass the option side='left', then they will be done in the
        left permutohedron.
        
        EXAMPLES::
        
            sage: p = Permutation([4,2,1,3])
            sage: p.permutohedron_pred()            
            [[2, 4, 1, 3], [4, 1, 2, 3]]
            sage: p.permutohedron_pred(side='left')
            [[4, 1, 2, 3], [3, 2, 1, 4]]
        """
        p = self
        n = len(p)
        pred = []
        if side == "right":
            for d in p.descents():
                pp = p[:]
                pp[d] = p[d+1]
                pp[d+1] = p[d]
                pred.append(Permutation(pp))
        else:
            recoil = lambda perm: [i for i in range(1,n) if perm.index(i) > perm.index(i+1)]
            for i in recoil(p):
                pp = p[:]
                pp[p.index(i)] = i+1
                pp[p.index(i+1)] = i
                pred.append(Permutation(pp))
        return pred


    def permutohedron_smaller(self, side="right"):
        r"""
        Returns a list of permutations smaller than or equal to p in the
        permutohedron order.
        
        By default, the computations are done in the right permutohedron.
        If you pass the option side='left', then they will be done in the
        left permutohedron.
        
        EXAMPLES::
        
            sage: Permutation([4,2,1,3]).permutohedron_smaller()
            [[1, 2, 3, 4],
             [1, 2, 4, 3],
             [1, 4, 2, 3],
             [2, 1, 3, 4],
             [2, 1, 4, 3],
             [2, 4, 1, 3],
             [4, 1, 2, 3],
             [4, 2, 1, 3]]
        
        ::
        
            sage: Permutation([4,2,1,3]).permutohedron_smaller(side='left')
            [[1, 2, 3, 4],
             [1, 3, 2, 4],
             [2, 1, 3, 4],
             [2, 3, 1, 4],
             [3, 1, 2, 4],
             [3, 2, 1, 4],
             [4, 1, 2, 3],
             [4, 2, 1, 3]]
        """

        return transitive_ideal(lambda x: x.permutohedron_pred(side), self)


    def permutohedron_greater(self, side="right"):
        r"""
        Returns a list of permutations greater than or equal to p in the
        permutohedron order.
        
        By default, the computations are done in the right permutohedron.
        If you pass the option side='left', then they will be done in the
        left permutohedron.
        
        EXAMPLES::
        
            sage: Permutation([4,2,1,3]).permutohedron_greater()
            [[4, 2, 1, 3], [4, 2, 3, 1], [4, 3, 2, 1]]
            sage: Permutation([4,2,1,3]).permutohedron_greater(side='left')
            [[4, 2, 1, 3], [4, 3, 1, 2], [4, 3, 2, 1]]
        """

        return transitive_ideal(lambda x: x.permutohedron_succ(side), self)


    ############
    # Patterns #
    ############

    def has_pattern(self, patt):
        r"""
        Tests whether the permutation matches the pattern.
        
        EXAMPLES::
        
            sage: Permutation([3,5,1,4,6,2]).has_pattern([1,3,2])
            True
        """
        p = self
        n = len(p)
        l = len(patt)
        if l > n:
            return False
        for pos in subword.Subwords(range(n),l):
            if to_standard(map(lambda z: p[z] , pos)) == patt:
                return True
        return False

    def avoids(self, patt):
        """
        Tests whether the permutation avoids the pattern.

        EXAMPLES::
        
            sage: Permutation([6,2,5,4,3,1]).avoids([4,2,3,1])
            False
            sage: Permutation([6,1,2,5,4,3]).avoids([4,2,3,1])
            True
            sage: Permutation([6,1,2,5,4,3]).avoids([3,4,1,2])
            True
        """
        return not self.has_pattern(patt)

    def pattern_positions(self, patt):
        r"""
        Returns the list of positions where the pattern patt appears in p.
        
        EXAMPLES::
        
            sage: Permutation([3,5,1,4,6,2]).pattern_positions([1,3,2])
            [[0, 1, 3], [2, 3, 5], [2, 4, 5]]
        """
        p = self

        return __builtin__.list(itertools.ifilter(lambda pos: to_standard(map(lambda z: p[z], pos)) == patt, iter(subword.Subwords(range(len(p)), len(patt))) ))

    @combinatorial_map(order=2,name='reverse')
    def reverse(self):
        """
        Returns the permutation obtained by reversing the list.

        EXAMPLES::

            sage: Permutation([3,4,1,2]).reverse()
            [2, 1, 4, 3]
            sage: Permutation([1,2,3,4,5]).reverse()
            [5, 4, 3, 2, 1]
        """
        return Permutation_class( [i for i in reversed(self)] )

    @combinatorial_map(order=2,name='complement')
    def complement(self):
        """
        Returns the complement of the permutation which is obtained by
        replacing each value x in the list with n - x + 1.

        EXAMPLES::

            sage: Permutation([1,2,3]).complement()
            [3, 2, 1]
            sage: Permutation([1, 3, 2]).complement()
            [3, 1, 2]
        """
        n = len(self)
        return Permutation_class( map(lambda x: n - x + 1, self) )

    def dict(self):
        """
        Returns a dictionary corresponding to the permutation.
        
        EXAMPLES::
        
            sage: p = Permutation([2,1,3])
            sage: d = p.dict()
            sage: d[1]
            2
            sage: d[2]
            1
            sage: d[3]
            3
        """
        d = {}
        for i in range(len(self)):
            d[i+1] = self[i]
        return d

    def action(self, a):
        """
        Returns the action of the permutation on a list.
        
        EXAMPLES::
        
            sage: p = Permutation([2,1,3])
            sage: a = range(3)
            sage: p.action(a)
            [1, 0, 2]
            sage: b = [1,2,3,4]
            sage: p.action(b)
            Traceback (most recent call last):
            ...
            ValueError: len(a) must equal len(self)
        """
        if len(a) != len(self):
            raise ValueError, "len(a) must equal len(self)"
        return map(lambda i: a[self[i]-1], range(len(a)))
        
    ######################
    # Robinson-Schensted #
    ######################

    def robinson_schensted(self):
        """
        Returns the pair of standard tableaux obtained by running the
        Robinson-Schensted Algorithm on self.

        EXAMPLES::

            sage: Permutation([6,2,3,1,7,5,4]).robinson_schensted()
            [[[1, 3, 4], [2, 5], [6, 7]], [[1, 3, 5], [2, 6], [4, 7]]]

        .. WARNING::

            The following example does not check their input. This is wrong. See
            :trac:`13742`.

        It also works in the case of repeated letters. In this case only the
        second tableau is standard::

            sage: Permutation([2,3,3,2,1,3,2,3], check_input = False).robinson_schensted()
            [[[1, 2, 2, 3, 3], [2, 3], [3]], [[1, 2, 3, 6, 8], [4, 7], [5]]]

        TESTS:

        The empty permutation::

            sage: p = Permutation([])
            sage: p.robinson_schensted()
            [[], []]

        """
        from bisect import bisect
        from itertools import izip
        p = []       #the "left" tableau
        q = []       #the "recording" tableau

        #For each x in self, insert x into the tableau p.
        for i, x in enumerate(self):
            for r,qr in izip(p,q):
                if r[-1] > x:
                    #Figure out where to insert x into the row r.  The
                    #bisect command returns the position of the least
                    #element of r greater than x.  We will call it y.
                    y_pos = bisect(r, x)

                    #Switch x and y
                    x, r[y_pos] = r[y_pos], x
                else:
                    break
            else:
                #We made through all of the rows of p without breaking
                #so we need to add a new row to p and q.
                r = []; p.append(r)
                qr = []; q.append(qr)

            r.append(x)
            qr.append(i+1)

        return [tableau.Tableau(p),tableau.Tableau(q)]

    @combinatorial_map(name='Robinson-Schensted insertion tableau')
    def left_tableau(self):
        """
        Returns the right standard tableau after performing the RSK
        algorithm on self.

        EXAMPLES::

            sage: Permutation([1,4,3,2]).left_tableau()
            [[1, 2], [3], [4]]
        """
        return self.robinson_schensted()[0]

    @combinatorial_map(name='Robinson-Schensted recording tableau')
    def right_tableau(self):
        """
        Returns the right standard tableau after performing the RSK
        algorithm on self.

        EXAMPLES::

            sage: Permutation([1,4,3,2]).right_tableau()
            [[1, 2], [3], [4]]
        """
        return self.robinson_schensted()[1]

    @combinatorial_map(name='Robinson-Schensted tableau shape')
    def RS_partition(self):
        """
        Returns the partition corresponding to the tableaux of the RSK algorithm.

        EXAMPLES::

            sage: Permutation([1,4,3,2]).RS_partition()
            [2, 1, 1]
        """
        return self.robinson_schensted()[1].shape()

    def remove_extra_fixed_points(self):
        """
        Returns the permutation obtained by removing any fixed points at
        the end of self.
        
        EXAMPLES::
        
            sage: Permutation([2,1,3]).remove_extra_fixed_points()
            [2, 1]
            sage: Permutation([1,2,3,4]).remove_extra_fixed_points()
            [1]
        """
        #Strip off all extra fixed points at the end of
        #the permutation.
        i = len(self)-1
        while i >= 1:
            if i != self[i] - 1:
                break
            i -= 1
        return Permutation_class(self[:i+1])                   

    def hyperoctahedral_double_coset_type(self):
        r"""
        Returns the coset-type of ``self`` as a partition.        

        ``self`` must be a permutation of even size `2n`.  The coset-type
        determines the double class of the permutation, that is its image in
        `H_n \backslash S_2n / H_n`, where `H_n` is the hyperoctahedral group
        of order `n`.

        The coset-type is determined as follows. Consider the perfect matching
        `\{\{1,2\},\{3,4\},\dots,\{2n-1,2n\}\}` and its image by ``self`` and
        draw them simultaneously as edges of a graph whose vertices are labeled
        by `1,2,\dots,2n`. The coset-type is the ordered sequence of the
        semi-lengths of the loops of this graph (see [Mcd]_ for more details).

        EXAMPLE::

            sage: Permutation([3, 4, 6, 1, 5, 7, 2, 8]).hyperoctahedral_double_coset_type()
            [3, 1]
            sage: all([p.hyperoctahedral_double_coset_type() ==
            ...        p.inverse().hyperoctahedral_double_coset_type()
            ...         for p in Permutations(4)])
            True
            sage: Permutation([]).hyperoctahedral_double_coset_type()
            []
            sage: Permutation([3,1,2]).hyperoctahedral_double_coset_type()
            Traceback (most recent call last):
            ...
            ValueError: [3, 1, 2] is a permutation of odd size and has no coset-type

        REFERENCES:

            .. [Mcd] I. G. Macdonald, Symmetric functions and Hall
               polynomials, Oxford University Press, second edition, 1995
               (chapter VII).
        """
        from sage.combinat.perfect_matching import PerfectMatchings
        n = len(self)
        if n%2==1:
            raise ValueError, "%s is a permutation of odd size and has no coset-type"%self
        S=PerfectMatchings(n)([(2*i+1,2*i+2) for i in range(n//2)])
        return S.loop_type(S.conjugate_by_permutation(self))

################################################################

def Arrangements(mset, k):
    r"""
    An arrangement of mset is an ordered selection without repetitions
    and is represented by a list that contains only elements from mset,
    but maybe in a different order.
    
    ``Arrangements`` returns the combinatorial class of
    arrangements of the multiset mset that contain k elements.
    
    EXAMPLES::
    
        sage: mset = [1,1,2,3,4,4,5]
        sage: Arrangements(mset,2).list()
        [[1, 1],
         [1, 2],
         [1, 3],
         [1, 4],
         [1, 5],
         [2, 1],
         [2, 3],
         [2, 4],
         [2, 5],
         [3, 1],
         [3, 2],
         [3, 4],
         [3, 5],
         [4, 1],
         [4, 2],
         [4, 3],
         [4, 4],
         [4, 5],
         [5, 1],
         [5, 2], 
         [5, 3],
         [5, 4]]
         sage: Arrangements(mset,2).cardinality()
         22
         sage: Arrangements( ["c","a","t"], 2 ).list()
         [['c', 'a'], ['c', 't'], ['a', 'c'], ['a', 't'], ['t', 'c'], ['t', 'a']]
         sage: Arrangements( ["c","a","t"], 3 ).list()
         [['c', 'a', 't'],
          ['c', 't', 'a'],
          ['a', 'c', 't'],
          ['a', 't', 'c'],
          ['t', 'c', 'a'],
          ['t', 'a', 'c']]
    """
    mset = list(mset)
    if map(mset.index, mset) == range(len(mset)):
        return Arrangements_setk(mset, k)
    else:
        return Arrangements_msetk(mset, k)



class Permutations_nk(CombinatorialClass):
    def __init__(self, n, k):
        """
        TESTS::
        
            sage: P = Permutations(3,2)
            sage: P == loads(dumps(P))
            True
        """
        self.n = n
        self.k = k

    def __contains__(self, x):
        """
        EXAMPLES::
        
            sage: [1,2] in Permutations(3,2)
            True
            sage: [1,1] in Permutations(3,2)
            False
            sage: [3,2,1] in Permutations(3,2)
            False
            sage: [3,1] in Permutations(3,2)
            True
        """
        if len(x) != self.k: return False

        r = range(1, self.n+1)
        for i in x:
            if i in r:
                r.remove(i)
            else:
                return False
                
        return True

        
    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3,2))
            'Permutations of {1,...,3} of length 2'
        """
        return "Permutations of {1,...,%s} of length %s"%(self.n, self.k)
        
    def __iter__(self):
        """
        EXAMPLES::
        
            sage: [p for p in Permutations(3,2)]
            [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
            sage: [p for p in Permutations(3,0)]
            [[]]
            sage: [p for p in Permutations(3,4)]
            []
        """
        for x in PermutationsNK(self.n, self.k):
            yield [i+1 for i in x]

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(3,0).cardinality()
            1
            sage: Permutations(3,1).cardinality()
            3
            sage: Permutations(3,2).cardinality()
            6
            sage: Permutations(3,3).cardinality()
            6
            sage: Permutations(3,4).cardinality()
            0
        """
        if self.k <= self.n and self.k >= 0:
            return factorial(self.n)/factorial(self.n-self.k)
        else:
            return 0

    def random_element(self):
        """
        EXAMPLES::
        
            sage: Permutations(3,2).random_element()
            [0, 1]
        """
        return sample(range(self.n), self.k)


class Permutations_mset(CombinatorialClass):
    def __init__(self, mset):
        """
        TESTS::
        
            sage: S = Permutations(['c','a','c'])
            sage: S == loads(dumps(S))
            True
        """
        self.mset = mset

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(['c','a','c']))
            "Permutations of the multi-set ['c', 'a', 'c']"
        """
        return "Permutations of the multi-set %s"%self.mset
    
    def __iter__(self):
        r"""
        Algorithm based on:
        http://marknelson.us/2002/03/01/next-permutation/
        
        EXAMPLES::
        
            sage: [ p for p in Permutations(['c','t','t'])] # indirect doctest
            [['c', 't', 't'], ['t', 'c', 't'], ['t', 't', 'c']]
        """
        mset = self.mset
        n = len(self.mset)
        lmset = __builtin__.list(mset)
        mset_list = map(lambda x: lmset.index(x), lmset)
        mset_list.sort()
        
        yield [lmset[x] for x in mset_list]

        if n == 1:
            return

        while True:
            one = n - 2
            two = n - 1
            j   = n - 1

            #starting from the end, find the first o such that
            #mset_list[o] < mset_list[o+1]
            while two > 0 and mset_list[one] >= mset_list[two]:
                one -= 1
                two -= 1    

            if two == 0:
                return

            #starting from the end, find the first j such that
            #mset_list[j] > mset_list[one]
            while mset_list[j] <= mset_list[one]:
                j -= 1

            #Swap positions one and j
            t = mset_list[one]
            mset_list[one] = mset_list[j]
            mset_list[j] = t

            #Reverse the list between two and last
            i = int((n - two)/2)-1
            #mset_list = mset_list[:two] + [x for x in reversed(mset_list[two:])]
            while i >= 0:
                t = mset_list[ i + two ]
                mset_list[ i + two ] = mset_list[n-1 - i]
                mset_list[n-1 - i] = t
                i -= 1

            #Yield the permutation
            yield [lmset[x] for x in  mset_list]

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations([1,2,2]).cardinality()
            3
        """
        lmset = list(self.mset)
        mset_list = [lmset.index(x) for x in lmset]
        d = {}
        for i in mset_list:
            d[i] = d.get(i, 0) + 1

        c = factorial(len(lmset))
        for i in d:
            if d[i] != 1:
                c /= factorial(d[i])
        return c

class Permutations_set(CombinatorialClass):
    def __init__(self, s):
        """
        TESTS::
        
            sage: S = Permutations(['c','a','t'])
            sage: S == loads(dumps(S))
            True
        """
        self._set = s

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(['c','a','t']))
            "Permutations of the set ['c', 'a', 't']"
        """
        return "Permutations of the set %s"%self._set
    
    def __iter__(self):
        r"""
        Algorithm based on:
        http://marknelson.us/2002/03/01/next-permutation/
        
        EXAMPLES::
        
            sage: [ p for p in Permutations(['c','a','t'])] # indirect doctest
            [['c', 'a', 't'],
             ['c', 't', 'a'],
             ['a', 'c', 't'],
             ['a', 't', 'c'],
             ['t', 'c', 'a'],
             ['t', 'a', 'c']]
        """
        s = self._set
        n = len(s)
        lset = __builtin__.list(s)
        set_list = map(lambda x: lset.index(x), lset)
        set_list.sort()
        
        yield [lset[x] for x in set_list]

        if n <= 1:
            return

        while True:
            one = n - 2
            two = n - 1
            j   = n - 1

            #starting from the end, find the first o such that
            #set_list[o] < set_list[o+1]
            while two > 0 and set_list[one] >= set_list[two]:
                one -= 1
                two -= 1    

            if two == 0:
                return

            #starting from the end, find the first j such that
            #set_list[j] > set_list[one]
            while set_list[j] <= set_list[one]:
                j -= 1

            #Swap positions one and j
            t = set_list[one]
            set_list[one] = set_list[j]
            set_list[j] = t


            #Reverse the list between two and last
            i = int((n - two)/2)-1
            #set_list = set_list[:two] + [x for x in reversed(set_list[two:])]
            while i >= 0:
                t = set_list[ i + two ]
                set_list[ i + two ] = set_list[n-1 - i]
                set_list[n-1 - i] = t
                i -= 1

            #Yield the permutation
            yield [lset[x] for x in set_list]

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations([1,2,3]).cardinality()
            6
        """
        return factorial(len(self._set))
    
    def random_element(self):
        """
        EXAMPLES::
        
            sage: Permutations([1,2,3]).random_element()
            [1, 2, 3]
        """
        return sample(self._set, len(self._set))


class Permutations_msetk(CombinatorialClass):
    def __init__(self, mset, k):
        """
        TESTS::
        
            sage: P = Permutations([1,2,2],2)
            sage: P == loads(dumps(P))
            True
        """
        self.mset = mset
        self.k = k

    def __contains__(self, x):
        """
        EXAMPLES::
        
            sage: p = Permutations([1,2,2],2)
            sage: [1,2,2] in p
            False
            sage: [2,2] in p
            True
            sage: [1,1] in p
            False
            sage: [2,1] in p
            True
        """
        if len(x) != self.k: return False
        s = list(self.mset)
        for i in x:
            if i in s:
                s.remove(i)
            else:
                return False
        return True
    
    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations([1,2,2],2))
            'Permutations of the multi-set [1, 2, 2] of length 2'
        """
        return "Permutations of the multi-set %s of length %s"%(self.mset,self.k)

    def list(self):
        """
        EXAMPLES::
        
            sage: Permutations([1,2,2],2).list()
            [[1, 2], [2, 1], [2, 2]]
        """
        
        mset = self.mset
        lmset = list(mset)
        mset_list = map(lambda x: lmset.index(x), lmset)
        indices = eval(gap.eval('Arrangements(%s,%s)'%(mset_list, self.k)))
        return [[lmset[x] for x in ktuple] for ktuple in indices]


class Permutations_setk(CombinatorialClass):
    def __init__(self, s, k):
        """
        TESTS::
        
            sage: P = Permutations([1,2,3],2)
            sage: P == loads(dumps(P))
            True
        """
        self._set = s
        self.k = k

    def __contains__(self, x):
        """
        EXAMPLES::
        
            sage: p = Permutations([1,2,3],2)
            sage: [1,2,3] in p
            False
            sage: [2,2] in p
            False
            sage: [1,3] in p
            True
            sage: [2,1] in p
            True
        """
        if len(x) != self.k: return False
        s = list(self._set)
        return all(i in s for i in x) and len(uniq(x)) == len(x)


    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations([1,2,3],2))
            'Permutations of the set [1, 2, 3] of length 2'
        """
        return "Permutations of the set %s of length %s"%(self._set,self.k)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: [i for i in Permutations([1,2,3],2)] # indirect doctest
            [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
        """
        for perm in PermutationsNK(len(self._set), self.k):
            yield [self._set[x] for x in perm]
            
    def random_element(self):
        """
        EXAMPLES::
        
            sage: Permutations([1,2,3],2).random_element()
            [1, 2]
        """
        return sample(self._set, self.k)

class Arrangements_msetk(Permutations_msetk):
    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Arrangements([1,2,2],2))
            'Arrangements of the multi-set [1, 2, 2] of length 2'
        """
        return "Arrangements of the multi-set %s of length %s"%(self.mset,self.k)

class Arrangements_setk(Permutations_setk):
    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Arrangements([1,2,3],2))
            'Arrangements of the set [1, 2, 3] of length 2'
        """
        return "Arrangements of the set %s of length %s"%(self._set,self.k)


class StandardPermutations_all(InfiniteAbstractCombinatorialClass):
    def __init__(self):
        """
        TESTS::
        
            sage: SP = Permutations()
            sage: SP == loads(dumps(SP))
            True
        """

    Element = Permutation_class

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations())
            'Standard permutations'
        """
        return "Standard permutations"

    def __contains__(self,x):
        """
        TESTS::
        
            sage: [] in Permutations()
            True
            sage: [1] in Permutations()
            True
            sage: [2] in Permutations()
            False
            sage: [1,2] in Permutations()
            True
            sage: [2,1] in Permutations()
            True
            sage: [1,2,2] in Permutations()
            False
            sage: [3,1,5,2] in Permutations()
            False
            sage: [3,4,1,5,2] in Permutations()
            True
        """
        if isinstance(x, Permutation_class):
            return True
        elif isinstance(x, __builtin__.list):
            s = x[:]
            s.sort()
            if s != range(1, len(x)+1):
                return False
            return True
        else:
            return False

    def _infinite_cclass_slice(self, n):
        """
        Needed by InfiniteAbstractCombinatorialClass to build __iter__.
        
        TESTS::
        
            sage: Permutations()._infinite_cclass_slice(4) == Permutations(4)
            True
            sage: it = iter(Permutations())    # indirect doctest
            sage: [it.next() for i in range(10)]
            [[], [1], [1, 2], [2, 1], [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        """
        return StandardPermutations_n(n)
    

class StandardPermutations_n(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: SP = Permutations(3)
            sage: SP == loads(dumps(SP))
            True
        """
        self.n = n

    Element = Permutation_class

    def __call__(self, x):
        """
        A close variant of CombinatorialClass.__call__ which just
        attempts to extend the permutation

            sage: P = Permutations(5)
            sage: P([2,3,1])
            [2, 3, 1, 4, 5]
        """
        
        if len(x) < self.n:
            x = list(x) + range(len(x)+1, self.n+1)
        return super(StandardPermutations_n, self).__call__(x)

    def __contains__(self,x):
        """
        TESTS::
        
            sage: [] in Permutations(0)
            True
            sage: [1,2] in Permutations(2)
            True
            sage: [1,2] in Permutations(3)
            False
            sage: [3,2,1] in Permutations(3)
            True
        """
        
        return x in Permutations() and len(x) == self.n
    
    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3))
            'Standard permutations of 3'
        """
        return "Standard permutations of %s"%self.n
    
    def __iter__(self):
        """
        EXAMPLES::
        
            sage: [p for p in Permutations(0)] # indirect doctest
            [[]]
            sage: [p for p in Permutations(3)] # indirect doctest
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        """
        for p in Permutations_set(range(1,self.n+1)):
            yield Permutation_class(p)

    def element_in_conjugacy_classes(self,nu):
        r"""
        Returns a permutation with cycle type ``nu``

        If the size of ``nu`` is smaller than the size of permutations in ``self``, then some fixed points are added.

        EXAMPLES ::

            sage: PP=Permutations(5)
            sage: PP.element_in_conjugacy_classes([2,2])
            [2, 1, 4, 3, 5]
        """
        nu=sage.combinat.partition.Partition(nu)
        if nu.size() > self.n:
            raise ValueError, "The size of the partition (=%s) should be lower than the size of the permutations(=%s)"%(nu.size,self.n)
        l=[]
        i=0
        for nui in nu:
            for j in range(nui-1):
                l.append(i+j+2)
            l.append(i+1)
            i+=nui
        for i in range(nu.size(),self.n):
            l.append(i+1)
        return Permutation(l)
 
    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(0).cardinality()
            1
            sage: Permutations(3).cardinality()
            6
            sage: Permutations(4).cardinality()
            24
        """
        return factorial(self.n)

    
    def identity(self):
        r"""
        Returns the identity permutation of length n.
        
        EXAMPLES::
        
            sage: Permutations(4).identity()
            [1, 2, 3, 4]
            sage: Permutations(0).identity()
            []
        """

        return Permutation_class(range(1,self.n+1))

    def unrank(self, r):
        """
        EXAMPLES::
        
            sage: SP3 = Permutations(3)
            sage: l = map(SP3.unrank, range(6))
            sage: l == SP3.list()
            True
            sage: SP0 = Permutations(0)
            sage: l = map(SP0.unrank, range(1))
            sage: l == SP0.list()
            True
        """
        if r >= factorial(self.n) or r < 0:
            raise ValueError
        else:
            return from_rank(self.n, r)

    def rank(self, p):
        """
        EXAMPLES::

            sage: SP3 = Permutations(3)
            sage: map(SP3.rank, SP3)
            [0, 1, 2, 3, 4, 5]
            sage: SP0 = Permutations(0)
            sage: map(SP0.rank, SP0)
            [0]
        """
        if p in self:
            return Permutation(p).rank()
        else:
            raise ValueError, "x not in self"

    def random_element(self):
        """
        EXAMPLES::

            sage: Permutations(4).random_element()
            [1, 2, 4, 3]
        """
        return Permutation(sample(xrange(1,self.n+1), self.n))

#############################
# Constructing Permutations #
#############################
def from_permutation_group_element(pge):
    """
    Returns a Permutation give a PermutationGroupElement pge.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: pge = PermutationGroupElement([(1,2),(3,4)])
        sage: permutation.from_permutation_group_element(pge)
        [2, 1, 4, 3]
    """

    if not isinstance(pge, PermutationGroupElement):
        raise TypeError, "pge (= %s) must be a PermutationGroupElement"%pge

    return Permutation(pge.list())

def from_rank(n, rank):
    r"""
    Returns the permutation with the specified lexicographic rank. The
    permutation is of the set [1,...,n].
    
    The permutation is computed without iterating through all of the
    permutations with lower rank. This makes it efficient for large
    permutations.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: Permutation([3, 6, 5, 4, 2, 1]).rank()
        359
        sage: [permutation.from_rank(3, i) for i in range(6)]
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        sage: Permutations(6)[10]
        [1, 2, 4, 6, 3, 5]
        sage: permutation.from_rank(6,10)
        [1, 2, 4, 6, 3, 5]
    """

    #Find the factoradic of rank
    factoradic = [None] * n
    for j in range(1,n+1):
        factoradic[n-j] = Integer(rank % j)
        rank = int(rank) / int(j)

    return from_lehmer_code(factoradic)

def from_inversion_vector(iv):
    r"""
    Returns the permutation corresponding to inversion vector iv.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.from_inversion_vector([3,1,0,0,0])
        [3, 2, 4, 1, 5]
        sage: permutation.from_inversion_vector([2,3,6,4,0,2,2,1,0])
        [5, 9, 1, 8, 2, 6, 4, 7, 3]
    """

    p = iv[:]
    open_spots = range(len(iv))
    for i,ivi in enumerate(iv):
        p[open_spots.pop(ivi)] = i+1

    return Permutation(p)

def from_cycles(n, cycles):
    r"""
    Returns the permutation corresponding to cycles.

    This function checks that its input is correct (i.e. that the cycles are
    disjoint and its elements integers among `1...n`). It raises an exception
    otherwise.

    .. WARNING::

        It assumes that the elements are of ``int`` type.

    EXAMPLES::

        sage: import sage.combinat.permutation as permutation
        sage: permutation.from_cycles(4, [[1,2]])
        [2, 1, 3, 4]

    Bad input (see :trac:`13742`)::

        sage: Permutation("(-12,2)(3,4)")
        Traceback (most recent call last):
        ...
        ValueError: All elements should be strictly positive integers, and I just found a negative one.
        sage: Permutation("(1,2)(2,4)")
        Traceback (most recent call last):
        ...
        ValueError: An element appears twice. It should not.
        sage: permutation.from_cycles(4, [[1,18]])
        Traceback (most recent call last):
        ...
        ValueError: You claimed that this was a permutation on 1...4 but it contains 18
    """

    p = range(1,n+1)

    # Is it really a permutation on 1...n ?
    flattened_and_sorted = []
    for c in cycles:
        flattened_and_sorted.extend(c)
    flattened_and_sorted.sort()

    # Empty input
    if len(flattened_and_sorted) == 0:
        # This is not consistent with Permutaion([]). See #13742
        return Permutation([1])

    # Only positive elements
    if int(flattened_and_sorted[0]) < 1:
        raise ValueError("All elements should be strictly positive "
                         "integers, and I just found a negative one.")

    # Really smaller than n ?
    if flattened_and_sorted[-1] > n:
        raise ValueError("You claimed that this was a permutation on 1..."+
                         str(n)+" but it contains "+str(flattened_and_sorted[-1]))

    # Disjoint cycles ?
    previous = flattened_and_sorted[0]-1
    for i in flattened_and_sorted:
        if i == previous:
            raise ValueError("An element appears twice. It should not.")
        else:
            previous = i

    for cycle in cycles:
        if not cycle:
            continue
        first = cycle[0]
        for i in range(len(cycle)-1):
            p[cycle[i]-1] = cycle[i+1]
        p[cycle[-1]-1] = first

    return Permutation(p)

def from_lehmer_code(lehmer):
    r"""
    Returns the permutation with Lehmer code lehmer.

    EXAMPLES::

        sage: import sage.combinat.permutation as permutation
        sage: Permutation([2,1,5,4,3]).to_lehmer_code()
        [1, 0, 2, 1, 0]
        sage: permutation.from_lehmer_code(_)
        [2, 1, 5, 4, 3]
    """

    p = []
    open_spots = range(1,len(lehmer)+1)
    for ivi in lehmer:
        p.append(open_spots.pop(ivi))

    return Permutation(p)

def from_reduced_word(rw):
    r"""
    Returns the permutation corresponding to the reduced word rw.

    EXAMPLES::

        sage: import sage.combinat.permutation as permutation
        sage: permutation.from_reduced_word([3,2,3,1,2,3,1])
        [3, 4, 2, 1]
        sage: permutation.from_reduced_word([])
        []
    """
    if not rw:
        return Permutation([])

    p = [i+1 for i in range(max(rw)+1)]

    for i in rw:
        (p[i-1], p[i]) = (p[i], p[i-1])

    return Permutation(p)


def robinson_schensted_inverse(p, q):
    r"""
    Returns the permutation corresponding to the pair of tableaux `(p,q)`
    using the inverse of Robinson-Schensted algorithm.

    .. WARNING::

       This function uses the :class:`Permutation_class` class in a way it is
       *NOT MEANT* to be used (i.e. the permutations are not permutations of
       integers). Do not trust it. See :trac:`13742`.

    INPUT:

     - ``p``, ``q``: two tableaux of the same shape and where ``q`` is
       standard.

    EXAMPLES::

        sage: from sage.combinat.permutation import robinson_schensted_inverse
        sage: t1 = Tableau([[1, 2, 5], [3], [4]])
        sage: t2 = Tableau([[1, 2, 3], [4], [5]])
        sage: robinson_schensted_inverse(t1, t2)
        [1, 4, 5, 3, 2]
        sage: robinson_schensted_inverse(t1, t1)
        [1, 4, 3, 2, 5]
        sage: robinson_schensted_inverse(t2, t2)
        [1, 2, 5, 4, 3]
        sage: robinson_schensted_inverse(t2, t1)
        [1, 5, 4, 2, 3]

    If the first tableau is semistandard::

        sage: p = Tableau([[1,2,2]]); q = Tableau([[1,2,3]])
        sage: robinson_schensted_inverse(p, q)
        [1, 2, 2]
        sage: _.robinson_schensted()
        [[[1, 2, 2]], [[1, 2, 3]]]

    Note that currently the constructor of ``Tableau`` accept as input lists
    that are not even tableaux but only filling of a partition diagram. This
    feature should not be used with ``robinson_schensted_inverse``.
        
    TESTS:

    From empty tableaux::

        sage: robinson_schensted_inverse(Tableau([]), Tableau([]))
        []

    This function is the inverse of robinson_shensted::

        sage: f = lambda p: robinson_schensted_inverse(*p.robinson_schensted())
        sage: all(p == f(p) for n in range(7) for p in Permutations(n))
        True

        sage: n = ZZ.random_element(200)
        sage: p = Permutations(n).random_element()
        sage: is_fine = True if p == f(p) else p ; is_fine
        True

    Both tableaux must be of the same shape::

        sage: robinson_schensted_inverse(Tableau([[1,2,3]]), Tableau([[1,2]]))
        Traceback (most recent call last):
        ...
        ValueError: p(=[[1, 2, 3]]) and q(=[[1, 2]]) must have the same shape

    The second tableau must be standard::

        sage: robinson_schensted_inverse(Tableau([[1,2,3]]), Tableau([[1,3,2]]))
        Traceback (most recent call last):
        ...
        ValueError: q(=[[1, 3, 2]]) must be standard
    """
    if p.shape() != q.shape(): 
        raise ValueError, "p(=%s) and q(=%s) must have the same shape"%(p, q)
    if not q.is_standard():
        raise ValueError, "q(=%s) must be standard"%q

    from bisect import bisect

    permutation = []
    d = dict((qij,i) for i,Li in enumerate(q) for qij in Li)
    p = map(list, p)
    for i in reversed(d.values()):
        x = p[i].pop()
        for row in reversed(p[:i]):
            y = bisect(row,x) - 1
            x, row[y] = row[y], x
        permutation.append(x)
    return Permutation(reversed(permutation), check_input = False)

def bistochastic_as_sum_of_permutations(M, check = True):
    r"""
    Returns the positive sum of permutations corresponding to
    the bistochastic matrix.

    A stochastic matrix is a matrix with nonnegative real entries such that the
    sum of the elements of any row is equal to 1. A bistochastic matrix is a
    stochastic matrix whose transpose matrix is also stochastic ( there are
    conditions both on the rows and on the columns ).

    According to the Birkhoff-von Neumann Theorem, any bistochastic matrix
    can be written as a positive sum of permutation matrices, which also
    means that the polytope of bistochastic matrices is integer.

    As a non-bistochastic matrix can obviously not be written as a sum of
    permutations, this theorem is an equivalence.

    This function, given a bistochastic matrix, returns the corresponding
    decomposition.

    INPUT:

    - ``M`` -- A bistochastic matrix

    - ``check`` (boolean) -- set to ``True`` (default) to check
      that the matrix is indeed bistochastic

    OUTPUT:

    - An element of ``CombinatorialFreeModule``, which is a free `F`-module
      ( where `F` is the ground ring of the given matrix ) whose basis is 
      indexed by the permutations.

    .. NOTE::

        - In this function, we just assume 1 to be any constant : for us a matrix M
          is bistochastic if there exists `c>0` such that `M/c` is bistochastic.

        - You can obtain a sequence of pairs ``(permutation,coeff)``, where
          ``permutation` is a Sage ``Permutation`` instance, and ``coeff``
          its corresponding coefficient from the result of this function
          by applying the ``list`` function.

        - If you are interested in the matrix corresponding to a ``Permutation``
          you will be glad to learn about the ``Permutation.to_matrix()`` method.

        - The base ring of the matrix can be anything that can be coerced to ``RR``.

    .. SEEALSO:

    - :meth:`as_sum_of_permutations <sage.matrix.matrix2.as_sum_of_permutations>`
      -- to use this method through the ``Matrix`` class.

    EXAMPLE:

    We create a bistochastic matrix from a convex sum of permutations, then
    try to deduce the decomposition from the matrix ::


        sage: from sage.combinat.permutation import bistochastic_as_sum_of_permutations
        sage: L = []
        sage: L.append((9,Permutation([4, 1, 3, 5, 2])))
        sage: L.append((6,Permutation([5, 3, 4, 1, 2])))
        sage: L.append((3,Permutation([3, 1, 4, 2, 5])))
        sage: L.append((2,Permutation([1, 4, 2, 3, 5])))
        sage: M = sum([c * p.to_matrix() for (c,p) in L])
        sage: decomp = bistochastic_as_sum_of_permutations(M)
        sage: print decomp
        2*B[[1, 4, 2, 3, 5]] + 3*B[[3, 1, 4, 2, 5]] + 9*B[[4, 1, 3, 5, 2]] + 6*B[[5, 3, 4, 1, 2]]

    An exception is raised when the matrix is not positive and bistochastic::

        sage: M = Matrix([[2,3],[2,2]])
        sage: decomp = bistochastic_as_sum_of_permutations(M)
        Traceback (most recent call last):
        ...
        ValueError: The matrix is not bistochastic

        sage: bistochastic_as_sum_of_permutations(Matrix(GF(7), 2, [2,1,1,2]))
        Traceback (most recent call last):
        ...
        ValueError: The base ring of the matrix must have a coercion map to RR

        sage: bistochastic_as_sum_of_permutations(Matrix(ZZ, 2, [2,-1,-1,2]))
        Traceback (most recent call last):
        ...
        ValueError: The matrix should have nonnegative entries
    """

    from sage.graphs.bipartite_graph import BipartiteGraph
    from sage.combinat.free_module import CombinatorialFreeModule
    from sage.rings.all import RR

    n=M.nrows()

    if n != M.ncols():
        raise ValueError("The matrix is expected to be square")

    if check and not M.is_bistochastic(normalized = False):
        raise ValueError("The matrix is not bistochastic")

    if not RR.has_coerce_map_from(M.base_ring()):
        raise ValueError("The base ring of the matrix must have a coercion map to RR")

    if not all([x >= 0 for x in M.list()]):
        raise ValueError, "The matrix should have nonnegative entries"

    CFM=CombinatorialFreeModule(M.base_ring(),Permutations(n))
    value=0

    G = BipartiteGraph(M,weighted=True)

    while G.size() > 0:
        matching = G.matching(use_edge_labels=True)

        # This minimum is strictly larger than 0
        minimum = min([x[2] for x in matching])

        for (u,v,l) in matching:
            if minimum == l:
                G.delete_edge((u,v,l))
            else:
                G.set_edge_label(u,v,l-minimum)
            
        matching.sort(key=lambda x: x[0])
        value+=minimum*CFM(Permutation([x[1]-n+1 for x in matching]))

    return value
        
class StandardPermutations_descents(CombinatorialClass):
    def __init__(self, d, n):
        """
        TESTS::
        
            sage: P = Permutations(descents=([1,0,4,8],12))
            sage: P == loads(dumps(P))
            True
        """
        self.d = d
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(descents=([1,0,4,8],12)))
            'Standard permutations of 12 with descents [1, 0, 4, 8]'
        """
        return "Standard permutations of %s with descents %s"%(self.n, self.d)

    Element = Permutation_class

    def first(self):
        """
        Returns the first permutation with descents d.
        
        EXAMPLES::
        
            sage: Permutations(descents=([1,0,4,8],12)).first()
            [3, 2, 1, 4, 6, 5, 7, 8, 10, 9, 11, 12]
        """
        return descents_composition_first(Composition(descents=(self.d,self.n)))       


    def last(self):
        """
        Returns the last permutation with descents d.
        
        EXAMPLES::
        
            sage: Permutations(descents=([1,0,4,8],12)).last()
            [12, 11, 8, 9, 10, 4, 5, 6, 7, 1, 2, 3]
        """
        return descents_composition_last(Composition(descents=(self.d,self.n)))

    def list(self):
        """
         Returns a list of all the permutations that have the descents d.
         
         EXAMPLES::
         
             sage: Permutations(descents=([2,0],5)).list()
             [[2, 1, 4, 3, 5],
              [2, 1, 5, 3, 4],
              [3, 1, 4, 2, 5],
              [3, 1, 5, 2, 4],
              [4, 1, 3, 2, 5],
              [5, 1, 3, 2, 4],
              [4, 1, 5, 2, 3],
              [5, 1, 4, 2, 3],
              [3, 2, 4, 1, 5],
              [3, 2, 5, 1, 4],
              [4, 2, 3, 1, 5],
              [5, 2, 3, 1, 4],
              [4, 2, 5, 1, 3],
              [5, 2, 4, 1, 3],
              [4, 3, 5, 1, 2],
              [5, 3, 4, 1, 2]]
         """

        return descents_composition_list(Composition(descents=(self.d,self.n)))



def descents_composition_list(dc):
    """
    Returns a list of all the permutations that have a descent
    compositions dc.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.descents_composition_list([1,2,2])
        [[2, 1, 4, 3, 5],
         [2, 1, 5, 3, 4],
         [3, 1, 4, 2, 5],
         [3, 1, 5, 2, 4],
         [4, 1, 3, 2, 5],
         [5, 1, 3, 2, 4],
         [4, 1, 5, 2, 3],
         [5, 1, 4, 2, 3],
         [3, 2, 4, 1, 5],
         [3, 2, 5, 1, 4],
         [4, 2, 3, 1, 5],
         [5, 2, 3, 1, 4],
         [4, 2, 5, 1, 3],
         [5, 2, 4, 1, 3],
         [4, 3, 5, 1, 2],
         [5, 3, 4, 1, 2]]
    """
    return map(lambda p: p.inverse(), StandardPermutations_recoils(dc).list())

def descents_composition_first(dc):
    r"""
    Computes the smallest element of a descent class having a descent
    decomposition dc.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.descents_composition_first([1,1,3,4,3])
        [3, 2, 1, 4, 6, 5, 7, 8, 10, 9, 11, 12]
    """

    if not isinstance(dc, Composition):
        try:
            dc = Composition(dc)
        except TypeError:
            raise TypeError, "The argument must be of type Composition"

    cpl = [x for x in reversed(dc.conjugate())]
    res = []
    s = 0
    for i in range(len(cpl)):
        res += [s + cpl[i]-j for j in range(cpl[i])]
        s   += cpl[i]

    return Permutation(res)

def descents_composition_last(dc):
    r"""
    Returns the largest element of a descent class having a descent
    decomposition dc.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.descents_composition_last([1,1,3,4,3])
        [12, 11, 8, 9, 10, 4, 5, 6, 7, 1, 2, 3]
    """
    if not isinstance(dc, Composition):
        try:
            dc = Composition(dc)
        except TypeError:
            raise TypeError, "The argument must be of type Composition"
    s = 0
    res = []
    for i in reversed(range(len(dc))):
        res = [j for j in range(s+1,s+dc[i]+1)] + res
        s += dc[i]

    return Permutation(res)


class StandardPermutations_recoilsfiner(CombinatorialClass):
    def __init__(self, recoils):
        """
        TESTS::
        
            sage: P = Permutations(recoils_finer=[2,2])
            sage: P == loads(dumps(P))
            True
        """
        self.recoils = recoils

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(recoils_finer=[2,2]))
            'Standard permutations whose recoils composition is finer than [2, 2]'
        """
        return "Standard permutations whose recoils composition is finer than %s"%self.recoils

    Element = Permutation_class
    
    def list(self):
        """
        Returns a list of all of the permutations whose recoils composition
        is finer than recoils.
        
        EXAMPLES::
        
            sage: Permutations(recoils_finer=[2,2]).list()
            [[1, 2, 3, 4],
             [1, 3, 2, 4],
             [1, 3, 4, 2],
             [3, 1, 2, 4],
             [3, 1, 4, 2],
             [3, 4, 1, 2]]
        """
        recoils = self.recoils
        dag = DiGraph()

        #Add the nodes
        for i in range(1, sum(recoils)+1):
            dag.add_vertex(i)

        #Add the edges to guarantee a finer recoil composition
        pos = 1
        for part in recoils:
            for i in range(part-1):
                dag.add_edge(pos, pos+1)
                pos += 1
            pos += 1

        rcf = []
        for le in dag.topological_sort_generator():
            rcf.append(Permutation(le))
        return rcf

    
class StandardPermutations_recoilsfatter(CombinatorialClass):
    def __init__(self, recoils):
        """
        TESTS::
        
            sage: P = Permutations(recoils_fatter=[2,2])
            sage: P == loads(dumps(P))
            True
        """
        self.recoils = recoils

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(recoils_fatter=[2,2]))
            'Standard permutations whose recoils composition is fatter than [2, 2]'
        """
        return "Standard permutations whose recoils composition is fatter than %s"%self.recoils

    Element = Permutation_class

    def list(self):
        """
        Returns a list of all of the permutations whose recoils composition
        is fatter than recoils.
        
        EXAMPLES::
        
            sage: Permutations(recoils_fatter=[2,2]).list()
            [[1, 3, 2, 4],
             [1, 3, 4, 2],
             [1, 4, 3, 2],
             [3, 1, 2, 4],
             [3, 1, 4, 2],
             [3, 2, 1, 4],
             [3, 2, 4, 1],
             [3, 4, 1, 2],
             [3, 4, 2, 1],
             [4, 1, 3, 2],
             [4, 3, 1, 2],
             [4, 3, 2, 1]]
        """
        recoils = self.recoils
        dag = DiGraph()

        #Add the nodes
        for i in range(1, sum(recoils)+1):
            dag.add_vertex(i)

        #Add the edges to guarantee a fatter recoil composition
        pos = 0
        for i in range(len(recoils)-1):
            pos += recoils[i]
            dag.add_edge(pos+1, pos)


        rcf = []
        for le in dag.topological_sort_generator():
            rcf.append(Permutation(le))
        return rcf

class StandardPermutations_recoils(CombinatorialClass):
    def __init__(self, recoils):
        """
        TESTS::
        
            sage: P = Permutations(recoils=[2,2])
            sage: P == loads(dumps(P))
            True
        """
        self.recoils = recoils
        

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(recoils=[2,2]))
            'Standard permutations whose recoils composition is [2, 2]'
        """
        return "Standard permutations whose recoils composition is %s"%self.recoils

    Element = Permutation_class


    def list(self):
        """
        Returns a list of all of the permutations whose recoils composition
        is equal to recoils.
        
        EXAMPLES::
        
            sage: Permutations(recoils=[2,2]).list()
            [[1, 3, 2, 4], [1, 3, 4, 2], [3, 1, 2, 4], [3, 1, 4, 2], [3, 4, 1, 2]]
        """
        
        recoils = self.recoils
        dag = DiGraph()

        #Add all the nodes
        for i in range(1, sum(recoils)+1):
            dag.add_vertex(i)

        #Add the edges which guarantee a finer recoil comp.
        pos = 1
        for part in recoils:
            for i in range(part-1):
                dag.add_edge(pos, pos+1)
                pos += 1
            pos += 1

        #Add the edges which guarantee a fatter recoil comp.
        pos = 0
        for i in range(len(recoils)-1):
            pos += recoils[i]
            dag.add_edge(pos+1, pos)

        rcf = []
        for le in dag.topological_sort_generator():
            rcf.append(Permutation(le))
        return rcf



def from_major_code(mc, final_descent=False):
    r"""
    Returns the permutation corresponding to major code mc.

    .. WARNING::

       This function creates illegal permutations (i.e. ``Permutation([9])``,
       and this is dangerous as the :meth:`Permutation` class is only designed
       to handle permutations on `1...n`. This will have to be changed when Sage
       permutations will be able to handle anything, but right now this should
       be fixed. Be careful with the results.
    
    REFERENCES:

    - Skandera, M. 'An Eulerian Partner for Inversions', Sem.
      Lothar. Combin. 46 (2001) B46d.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.from_major_code([5, 0, 1, 0, 1, 2, 0, 1, 0])
        [9, 3, 5, 7, 2, 1, 4, 6, 8]
        sage: permutation.from_major_code([8, 3, 3, 1, 4, 0, 1, 0, 0])
        [2, 8, 4, 3, 6, 7, 9, 5, 1]
        sage: Permutation([2,1,6,4,7,3,5]).to_major_code()
        [3, 2, 0, 2, 2, 0, 0]
        sage: permutation.from_major_code([3, 2, 0, 2, 2, 0, 0])
        [2, 1, 6, 4, 7, 3, 5]
    """
    #define w^(n) to be the one-letter word n
    w = [len(mc)]

    #for i=n-1,..,1 let w^i be the unique word obtained by inserting
    #the letter i into the word w^(i+1) in such a way that 
    #maj(w^i)-maj(w^(i+1)) = mc[i]

    for i in reversed(range(1,len(mc))):
        #Lemma 2.2 in Skandera

        #Get the descents of w and place them in reverse order
        d = Permutation(w, check_input = False).descents(final_descent=final_descent)
        d.reverse()

        #a is the list of all positions which are not descents
        a = filter(lambda x: x not in d, range(len(w)))

        #d_k = -1    -- 0 in the lemma, but -1 due to 0-based indexing
        d.append(-1)
        l = mc[i-1]
        indices = d + a
        w.insert(indices[l]+1, i)

    return Permutation(w)


class StandardPermutations_bruhat_smaller(CombinatorialClass):
    def __init__(self, p):
        """
        TESTS::
        
            sage: P = Permutations(bruhat_smaller=[3,2,1])
            sage: P == loads(dumps(P))
            True
        """
        self.p = p

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(bruhat_smaller=[3,2,1]))
            'Standard permutations that are less than or equal to [3, 2, 1] in the Bruhat order'
        """
        return "Standard permutations that are less than or equal to %s in the Bruhat order"%self.p

    def list(self):
        r"""
        Returns a list of permutations smaller than or equal to p in the
        Bruhat order.
        
        EXAMPLES::
        
            sage: Permutations(bruhat_smaller=[4,1,2,3]).list()
            [[1, 2, 3, 4],
             [1, 2, 4, 3],
             [1, 3, 2, 4],
             [1, 4, 2, 3],
             [2, 1, 3, 4],
             [2, 1, 4, 3],
             [3, 1, 2, 4],
             [4, 1, 2, 3]]
        """
        return transitive_ideal(lambda x: x.bruhat_pred(), self.p)



class StandardPermutations_bruhat_greater(CombinatorialClass):
    def __init__(self, p):
        """
        TESTS::
        
            sage: P = Permutations(bruhat_greater=[3,2,1])
            sage: P == loads(dumps(P))
            True
        """
        self.p = p

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(bruhat_greater=[3,2,1]))
            'Standard permutations that are greater than or equal to [3, 2, 1] in the Bruhat order'
        """
        return "Standard permutations that are greater than or equal to %s in the Bruhat order"%self.p

    def list(self):
        r"""
        Returns a list of permutations greater than or equal to p in the
        Bruhat order.
        
        EXAMPLES::
        
            sage: Permutations(bruhat_greater=[4,1,2,3]).list()
            [[4, 1, 2, 3],
             [4, 1, 3, 2],
             [4, 2, 1, 3],
             [4, 2, 3, 1],
             [4, 3, 1, 2],
             [4, 3, 2, 1]]
        """
        return transitive_ideal(lambda x: x.bruhat_succ(), self.p)


################
# Bruhat Order #
################

def bruhat_lequal(p1, p2):
    r"""
    Returns True if p1 is less than p2 in the Bruhat order.
    
    Algorithm from mupad-combinat.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.bruhat_lequal([2,4,3,1],[3,4,2,1]) 
        True
    """

    n1 = len(p1)

    if n1 == 0:
        return True
    
    if p1[0] > p2[0] or p1[n1-1] < p2[n1-1]:
        return False

    for i in range(n1):
        c = 0
        for j in range(n1):
            if p2[j] > i+1:
                c += 1
            if p1[j] > i+1:
                c -= 1
            if c < 0:
                return False

    return True



#################
# Permutohedron #
#################

def permutohedron_lequal(p1, p2, side="right"):
    r"""
    Returns True if p1 is less than p2in the permutohedron order.
    
    By default, the computations are done in the right permutohedron.
    If you pass the option side='left', then they will be done in the
    left permutohedron.
    
    EXAMPLES::
    
        sage: import sage.combinat.permutation as permutation
        sage: permutation.permutohedron_lequal(Permutation([3,2,1,4]),Permutation([4,2,1,3]))
        False
        sage: permutation.permutohedron_lequal(Permutation([3,2,1,4]),Permutation([4,2,1,3]), side='left')
        True
    """
    l1 = p1.number_of_inversions()
    l2 = p2.number_of_inversions()

    if l1 > l2:
        return False

    if side == "right":
        prod = p1._left_to_right_multiply_on_right(p2.inverse())
    else:
        prod = p1._left_to_right_multiply_on_left(p2.inverse())


    return prod.number_of_inversions() == l2 - l1


############
# Patterns #
############

def to_standard(p):
    r"""
    Returns a standard permutation corresponding to the permutation p.

    EXAMPLES::

        sage: import sage.combinat.permutation as permutation
        sage: permutation.to_standard([4,2,7])
        [2, 1, 3]
        sage: permutation.to_standard([1,2,3])
        [1, 2, 3]
        sage: permutation.to_standard([])
        []
        
    TESTS:
    
    Does not mutate the list::
    
        sage: a = [1,2,4]
        sage: permutation.to_standard(a)
        [1, 2, 3]
        sage: a
        [1, 2, 4]
    """
    if not p:
        return Permutation([])
    s = [0]*len(p)
    c = p[:]
    biggest = max(p) + 1
    i = 1
    for _ in range(len(c)):
        smallest = min(c)
        smallest_index = c.index(smallest)
        s[smallest_index] = i
        i += 1
        c[smallest_index] = biggest

    return Permutation(s)



##########################################################


def CyclicPermutations(mset):
    """
    Returns the combinatorial class of all cyclic permutations of mset
    in cycle notation. These are the same as necklaces.
    
    EXAMPLES::
    
        sage: CyclicPermutations(range(4)).list()
        [[0, 1, 2, 3],
         [0, 1, 3, 2],
         [0, 2, 1, 3],
         [0, 2, 3, 1],
         [0, 3, 1, 2],
         [0, 3, 2, 1]]
        sage: CyclicPermutations([1,1,1]).list()
        [[1, 1, 1]]
    """
    return CyclicPermutations_mset(mset)

class CyclicPermutations_mset(CombinatorialClass):
    def __init__(self, mset):
        """
        TESTS::
        
            sage: CP = CyclicPermutations(range(4))
            sage: CP == loads(dumps(CP))
            True
        """
        self.mset = mset

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(CyclicPermutations(range(4)))
            'Cyclic permutations of [0, 1, 2, 3]'
        """
        return "Cyclic permutations of %s"%self.mset

    def list(self, distinct=False):
        """
        EXAMPLES::
        
            sage: CyclicPermutations(range(4)).list()
            [[0, 1, 2, 3],
             [0, 1, 3, 2],
             [0, 2, 1, 3],
             [0, 2, 3, 1],
             [0, 3, 1, 2],
             [0, 3, 2, 1]]
        """
        return list(self.iterator(distinct=distinct))

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: [ p for p in CyclicPermutations(range(4)) ]
            [[0, 1, 2, 3],
             [0, 1, 3, 2],
             [0, 2, 1, 3],
             [0, 2, 3, 1],
             [0, 3, 1, 2],
             [0, 3, 2, 1]]
             sage: [ p for p in CyclicPermutations([1,1,1]) ]
             [[1, 1, 1]]
        """
        for p in self.iterator(distinct=False):
            yield p 
    
    def iterator(self, distinct=False):
        """
        EXAMPLES::
        
            sage: CyclicPermutations(range(4)).list() # indirect doctest
            [[0, 1, 2, 3],
             [0, 1, 3, 2],
             [0, 2, 1, 3],
             [0, 2, 3, 1],
             [0, 3, 1, 2],
             [0, 3, 2, 1]]
             sage: CyclicPermutations([1,1,1]).list()
             [[1, 1, 1]]
             sage: CyclicPermutations([1,1,1]).list(distinct=True)
             [[1, 1, 1], [1, 1, 1]]
        """
        if distinct:
            content = [1]*len(self.mset)
        else:
            content = [0]*len(self.mset)
            index_list = map(self.mset.index, self.mset)
            for i in index_list:
                content[i] += 1
            
        for necklace in Necklaces(content):
            yield [self.mset[x-1] for x in necklace]

##########################################3

def CyclicPermutationsOfPartition(partition):
    """
    Returns the combinatorial class of all combinations of cyclic
    permutations of each cell of the partition. This is the same as a
    Cartesian product of necklaces.
    
    EXAMPLES::
    
        sage: CyclicPermutationsOfPartition([[1,2,3,4],[5,6,7]]).list()
        [[[1, 2, 3, 4], [5, 6, 7]],
         [[1, 2, 4, 3], [5, 6, 7]],
         [[1, 3, 2, 4], [5, 6, 7]],
         [[1, 3, 4, 2], [5, 6, 7]],
         [[1, 4, 2, 3], [5, 6, 7]],
         [[1, 4, 3, 2], [5, 6, 7]],
         [[1, 2, 3, 4], [5, 7, 6]],
         [[1, 2, 4, 3], [5, 7, 6]],
         [[1, 3, 2, 4], [5, 7, 6]],
         [[1, 3, 4, 2], [5, 7, 6]],
         [[1, 4, 2, 3], [5, 7, 6]],
         [[1, 4, 3, 2], [5, 7, 6]]]
    
    ::
    
        sage: CyclicPermutationsOfPartition([[1,2,3,4],[4,4,4]]).list()
        [[[1, 2, 3, 4], [4, 4, 4]],
         [[1, 2, 4, 3], [4, 4, 4]],
         [[1, 3, 2, 4], [4, 4, 4]],
         [[1, 3, 4, 2], [4, 4, 4]],
         [[1, 4, 2, 3], [4, 4, 4]],
         [[1, 4, 3, 2], [4, 4, 4]]]
    
    ::
    
        sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list()
        [[[1, 2, 3], [4, 4, 4]], [[1, 3, 2], [4, 4, 4]]]
    
    ::
    
        sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list(distinct=True)
        [[[1, 2, 3], [4, 4, 4]],
         [[1, 3, 2], [4, 4, 4]],
         [[1, 2, 3], [4, 4, 4]],
         [[1, 3, 2], [4, 4, 4]]]
    """
    return CyclicPermutationsOfPartition_partition(partition)

class CyclicPermutationsOfPartition_partition(CombinatorialClass):
    def __init__(self, partition):
        """
        TESTS::
        
            sage: CP = CyclicPermutationsOfPartition([[1,2,3,4],[5,6,7]])
            sage: CP == loads(dumps(CP))
            True
        """
        self.partition = partition

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(CyclicPermutationsOfPartition([[1,2,3,4],[5,6,7]]))
            'Cyclic permutations of partition [[1, 2, 3, 4], [5, 6, 7]]'
        """
        return "Cyclic permutations of partition %s"%self.partition

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: [ p for p in CyclicPermutationsOfPartition([[1,2,3,4],[5,6,7]]) ] 
            [[[1, 2, 3, 4], [5, 6, 7]],
             [[1, 2, 4, 3], [5, 6, 7]],
             [[1, 3, 2, 4], [5, 6, 7]],
             [[1, 3, 4, 2], [5, 6, 7]],
             [[1, 4, 2, 3], [5, 6, 7]],
             [[1, 4, 3, 2], [5, 6, 7]],
             [[1, 2, 3, 4], [5, 7, 6]],
             [[1, 2, 4, 3], [5, 7, 6]],
             [[1, 3, 2, 4], [5, 7, 6]],
             [[1, 3, 4, 2], [5, 7, 6]],
             [[1, 4, 2, 3], [5, 7, 6]],
             [[1, 4, 3, 2], [5, 7, 6]]]
        """
        for p in self.iterator(distinct=False):
            yield p 
    
    def iterator(self, distinct=False):
        """
        AUTHORS:

        - Robert Miller
        
        EXAMPLES::
        
            sage: CyclicPermutationsOfPartition([[1,2,3,4],[5,6,7]]).list() # indirect doctest
            [[[1, 2, 3, 4], [5, 6, 7]],
             [[1, 2, 4, 3], [5, 6, 7]],
             [[1, 3, 2, 4], [5, 6, 7]],
             [[1, 3, 4, 2], [5, 6, 7]],
             [[1, 4, 2, 3], [5, 6, 7]],
             [[1, 4, 3, 2], [5, 6, 7]],
             [[1, 2, 3, 4], [5, 7, 6]],
             [[1, 2, 4, 3], [5, 7, 6]],
             [[1, 3, 2, 4], [5, 7, 6]],
             [[1, 3, 4, 2], [5, 7, 6]],
             [[1, 4, 2, 3], [5, 7, 6]],
             [[1, 4, 3, 2], [5, 7, 6]]]
        
        ::
        
            sage: CyclicPermutationsOfPartition([[1,2,3,4],[4,4,4]]).list()
            [[[1, 2, 3, 4], [4, 4, 4]],
             [[1, 2, 4, 3], [4, 4, 4]],
             [[1, 3, 2, 4], [4, 4, 4]],
             [[1, 3, 4, 2], [4, 4, 4]],
             [[1, 4, 2, 3], [4, 4, 4]],
             [[1, 4, 3, 2], [4, 4, 4]]]
        
        ::
        
            sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list()
            [[[1, 2, 3], [4, 4, 4]], [[1, 3, 2], [4, 4, 4]]]
        
        ::
        
            sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list(distinct=True)
            [[[1, 2, 3], [4, 4, 4]],
             [[1, 3, 2], [4, 4, 4]],
             [[1, 2, 3], [4, 4, 4]],
             [[1, 3, 2], [4, 4, 4]]]
        """
        
        if len(self.partition) == 1:
            for i in CyclicPermutations_mset(self.partition[0]).iterator(distinct=distinct):
                yield [i]
        else:
            for right in CyclicPermutationsOfPartition_partition(self.partition[1:]).iterator(distinct=distinct):
                for perm in CyclicPermutations_mset(self.partition[0]).iterator(distinct=distinct):
                    yield [perm] + right


    def list(self, distinct=False):
        """
        EXAMPLES::
        
            sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list()
            [[[1, 2, 3], [4, 4, 4]], [[1, 3, 2], [4, 4, 4]]]
            sage: CyclicPermutationsOfPartition([[1,2,3],[4,4,4]]).list(distinct=True)
            [[[1, 2, 3], [4, 4, 4]],
             [[1, 3, 2], [4, 4, 4]],
             [[1, 2, 3], [4, 4, 4]],
             [[1, 3, 2], [4, 4, 4]]]
        """

        return list(self.iterator(distinct=distinct))



######
#Avoiding


class StandardPermutations_avoiding_12(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[1,2])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[1,2]))
            'Standard permutations of 3 avoiding [1, 2]'
        """
        return "Standard permutations of %s avoiding [1, 2]"%self.n

    def list(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[1,2]).list()
            [[3, 2, 1]]
        """
        return [Permutation_class(range(self.n, 0, -1))]

class StandardPermutations_avoiding_21(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[2,1])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[2,1]))
            'Standard permutations of 3 avoiding [2, 1]'
        """
        return "Standard permutations of %s avoiding [2, 1]"%self.n

    def list(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[2,1]).list()
            [[1, 2, 3]]
        """
        return [Permutation_class(range(1, self.n+1))]


class StandardPermutations_avoiding_132(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[1,3,2])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[1,3,2]))
            'Standard permutations of 3 avoiding [1, 3, 2]'
        """
        return "Standard permutations of %s avoiding [1, 3, 2]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[1, 3, 2]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[1, 3, 2]).list() )
            42
        """
        return catalan_number(self.n)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[1,3,2]).list() # indirect doctest
            [[1, 2, 3], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
            sage: Permutations(4, avoiding=[1,3,2]).list()
            [[4, 1, 2, 3],
             [4, 2, 1, 3],
             [4, 2, 3, 1],
             [4, 3, 1, 2],
             [4, 3, 2, 1],
             [3, 4, 1, 2],
             [3, 4, 2, 1],
             [2, 3, 4, 1],
             [3, 2, 4, 1],
             [1, 2, 3, 4],
             [2, 1, 3, 4],
             [2, 3, 1, 4],
             [3, 1, 2, 4],
             [3, 2, 1, 4]]
        """
        if self.n == 0:
            return
        
        elif self.n < 3:
            for p in StandardPermutations_n(self.n):
                yield p
            return

        elif self.n == 3:
            for p in StandardPermutations_n(self.n):
                if p != [1, 3, 2]:
                    yield p
            return 


        
        #Yield all the 132 avoiding permutations to the right.
        for right in StandardPermutations_avoiding_132(self.n - 1):
            yield Permutation_class([self.n] + list(right))

        #yi
        for i in range(1, self.n-1):
            for left in StandardPermutations_avoiding_132(i):
                for right in StandardPermutations_avoiding_132(self.n-i-1):
                    yield Permutation_class( map(lambda x: x+(self.n-i-1), left) + [self.n] + list(right) )


        #Yield all the 132 avoiding permutations to the left
        for left in StandardPermutations_avoiding_132(self.n - 1):
            yield Permutation_class(list(left) + [self.n])


class StandardPermutations_avoiding_123(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[1, 2, 3])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[1, 2, 3]))
            'Standard permutations of 3 avoiding [1, 2, 3]'
        """
        return "Standard permutations of %s avoiding [1, 2, 3]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[1, 2, 3]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[1, 2, 3]).list() )
            42
        """
        return catalan_number(self.n)
    
    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[1, 2, 3]).list() # indirect doctest
             [[1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
            sage: Permutations(2, avoiding=[1, 2, 3]).list()
            [[1, 2], [2, 1]]
            sage: Permutations(3, avoiding=[1, 2, 3]).list()
            [[1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        """
        if self.n == 0:
            return
        
        elif self.n < 3:
            for p in StandardPermutations_n(self.n):
                yield p
            return

        elif self.n == 3:
            for p in StandardPermutations_n(self.n):
                if p != [1, 2, 3]:
                    yield p
            return 

        
        for p in StandardPermutations_avoiding_132(self.n):
            #Convert p to a 123 avoiding permutation by
            m = self.n+1
            minima_pos = []
            minima = []
            for i in range(self.n):
                if p[i] < m:
                    minima_pos.append(i)
                    minima.append(p[i])
                    m = p[i]

            
            new_p = []
            non_minima = filter(lambda x: x not in minima, range(self.n, 0, -1))
            a = 0
            b = 0
            for i in range(self.n):
                if i in minima_pos:
                    new_p.append( minima[a] )
                    a += 1
                else:
                    new_p.append( non_minima[b] )
                    b += 1

            yield Permutation_class( new_p )
                

class StandardPermutations_avoiding_321(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[3, 2, 1])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[3, 2, 1]))
            'Standard permutations of 3 avoiding [3, 2, 1]'
        """
        return "Standard permutations of %s avoiding [3, 2, 1]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[3, 2, 1]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[3, 2, 1]).list() )
            42
        """
        return catalan_number(self.n)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[3, 2, 1]).list() #indirect doctest
            [[2, 3, 1], [3, 1, 2], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
        """
        for p in StandardPermutations_avoiding_123(self.n):
            yield p.reverse()


class StandardPermutations_avoiding_231(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[2, 3, 1])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[2, 3, 1]))
            'Standard permutations of 3 avoiding [2, 3, 1]'
        """
        return "Standard permutations of %s avoiding [2, 3, 1]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[2, 3, 1]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[2, 3, 1]).list() )
            42
        """
        return catalan_number(self.n)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[2, 3, 1]).list()
            [[3, 2, 1], [3, 1, 2], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
        """
        for p in StandardPermutations_avoiding_132(self.n):
            yield p.reverse()


class StandardPermutations_avoiding_312(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[3, 1, 2])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[3, 1, 2]))
            'Standard permutations of 3 avoiding [3, 1, 2]'
        """
        return "Standard permutations of %s avoiding [3, 1, 2]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[3, 1, 2]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[3, 1, 2]).list() )
            42
        """
        return catalan_number(self.n)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[3, 1, 2]).list()
            [[3, 2, 1], [2, 3, 1], [2, 1, 3], [1, 3, 2], [1, 2, 3]]
        """
        for p in StandardPermutations_avoiding_132(self.n):
            yield p.complement()


class StandardPermutations_avoiding_213(CombinatorialClass):
    def __init__(self, n):
        """
        TESTS::
        
            sage: p = Permutations(3, avoiding=[2, 1, 3])
            sage: p == loads(dumps(p))
            True
        """
        self.n = n

    def __repr__(self):
        """
        TESTS::
        
            sage: repr(Permutations(3, avoiding=[2, 1, 3]))
            'Standard permutations of 3 avoiding [2, 1, 3]'
        """
        return "Standard permutations of %s avoiding [2, 1, 3]"%self.n

    def cardinality(self):
        """
        EXAMPLES::
        
            sage: Permutations(5, avoiding=[2, 1, 3]).cardinality()
            42
            sage: len( Permutations(5, avoiding=[2, 1, 3]).list() )
            42
        """
        return catalan_number(self.n)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[2, 1, 3]).list()
            [[1, 2, 3], [1, 3, 2], [3, 1, 2], [2, 3, 1], [3, 2, 1]]
        """
        for p in StandardPermutations_avoiding_132(self.n):
            yield p.complement().reverse()


class StandardPermutations_avoiding_generic(CombinatorialClass):
    def __init__(self, n, a):
        """
        EXAMPLES::
        
            sage: P = Permutations(3, avoiding=[[2, 1, 3],[1,2,3]])
            sage: P == loads(dumps(P))
            True
            sage: type(P)
            <class 'sage.combinat.permutation.StandardPermutations_avoiding_generic'>
        """
        self.n = n
        self.a = a

    def __repr__(self):
        """
        EXAMPLES::
        
            sage: P = Permutations(3, avoiding=[[2, 1, 3],[1,2,3]])
            sage: P.__repr__()
            'Standard permutations of 3 avoiding [[2, 1, 3], [1, 2, 3]]'
        """
        return "Standard permutations of %s avoiding %s"%(self.n, self.a)

    def __iter__(self):
        """
        EXAMPLES::
        
            sage: Permutations(3, avoiding=[[2, 1, 3],[1,2,3]]).list()
            [[1, 3, 2], [3, 1, 2], [2, 3, 1], [3, 2, 1]]
        """
        return iter(PatternAvoider(self.n, self.a))
        

class PatternAvoider(GenericBacktracker):
    def __init__(self, n, patterns):
        """
        EXAMPLES::
        
            sage: from sage.combinat.permutation import PatternAvoider
            sage: p = PatternAvoider(4, [[1,2,3]])
            sage: loads(dumps(p))
            <sage.combinat.permutation.PatternAvoider object at 0x...>
        """
        GenericBacktracker.__init__(self, [], 1)
        self._n = n
        self._patterns = patterns
        
    def _rec(self, obj, state):
        """
        EXAMPLES::
        
            sage: from sage.combinat.permutation import PatternAvoider
            sage: p = PatternAvoider(4, [[1,2]])
            sage: list(p._rec([1], 2))
            [([2, 1], 3, False)]
        """
        i = state
        
        if state != self._n:
            new_state = state + 1
            yld = False
        else:
            new_state = None
            yld = True

        for pos in reversed(range(len(obj)+1)):
            new_obj = Permutation(obj[:pos] + [i] + obj[pos:])
            if all( not new_obj.has_pattern(p) for p in self._patterns):
                yield new_obj, new_state, yld
            
        

def Permutations(n=None,k=None, **kwargs):
    """
    Returns a combinatorial class of permutations.
    
    Permutations(n) returns the class of permutations of n, if n is an
    integer, list, set, or string.
    
    Permutations(n, k) returns the class of permutations of n (where n
    is any of the above things) of length k; k must be an integer.
    
    Valid keyword arguments are: 'descents', 'bruhat_smaller',
    'bruhat_greater', 'recoils_finer', 'recoils_fatter', 'recoils',
    and 'avoiding'. With the exception of 'avoiding', you cannot
    specify n or k along with a keyword.
    
    Permutations(descents=list) returns the class of permutations with
    descents in the positions specified by 'list'.
    
    Permutations(bruhat_smaller,greater=p) returns the class of
    permutations smaller or greater, respectively, than the given
    permutation in Bruhat order.
    
    Permutations(recoils=p) returns the class of permutations whose
    recoils composition is p.
    
    Permutations(recoils_fatter,finer=p) returns the class of
    permutations whose recoils composition is fatter or finer,
    respectively, than the given permutation.
    
    Permutations(n, avoiding=P) returns the class of permutations of n
    avoiding P. Here P may be a single permutation or a list of
    permutations; the returned class will avoid all patterns in P.
    
    EXAMPLES::
    
        sage: p = Permutations(3); p
        Standard permutations of 3
        sage: p.list()
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    
    ::
    
        sage: p = Permutations(3, 2); p
        Permutations of {1,...,3} of length 2
        sage: p.list()
        [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
    
    ::
    
        sage: p = Permutations(['c', 'a', 't']); p
        Permutations of the set ['c', 'a', 't']
        sage: p.list()
        [['c', 'a', 't'],
         ['c', 't', 'a'],
         ['a', 'c', 't'],
         ['a', 't', 'c'],
         ['t', 'c', 'a'],
         ['t', 'a', 'c']]
    
    ::
    
        sage: p = Permutations(['c', 'a', 't'], 2); p
        Permutations of the set ['c', 'a', 't'] of length 2
        sage: p.list()
        [['c', 'a'], ['c', 't'], ['a', 'c'], ['a', 't'], ['t', 'c'], ['t', 'a']]
    
    ::
    
        sage: p = Permutations([1,1,2]); p
        Permutations of the multi-set [1, 1, 2]
        sage: p.list()
        [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    
    ::
    
        sage: p = Permutations([1,1,2], 2); p
        Permutations of the multi-set [1, 1, 2] of length 2
        sage: p.list()
        [[1, 1], [1, 2], [2, 1]]
    
    ::
    
        sage: p = Permutations(descents=([1], 4)); p
        Standard permutations of 4 with descents [1]
        sage: p.list()
        [[1, 3, 2, 4], [1, 4, 2, 3], [2, 3, 1, 4], [2, 4, 1, 3], [3, 4, 1, 2]]
    
    ::
    
        sage: p = Permutations(bruhat_smaller=[1,3,2,4]); p
        Standard permutations that are less than or equal to [1, 3, 2, 4] in the Bruhat order
        sage: p.list()
        [[1, 2, 3, 4], [1, 3, 2, 4]]
    
    ::
    
        sage: p = Permutations(bruhat_greater=[4,2,3,1]); p
        Standard permutations that are greater than or equal to [4, 2, 3, 1] in the Bruhat order
        sage: p.list()
        [[4, 2, 3, 1], [4, 3, 2, 1]]
    
    ::
    
        sage: p = Permutations(recoils_finer=[2,1]); p
        Standard permutations whose recoils composition is finer than [2, 1]
        sage: p.list()
        [[1, 2, 3], [1, 3, 2], [3, 1, 2]]
    
    ::
    
        sage: p = Permutations(recoils_fatter=[2,1]); p
        Standard permutations whose recoils composition is fatter than [2, 1]
        sage: p.list()
        [[1, 3, 2], [3, 1, 2], [3, 2, 1]]
    
    ::
    
        sage: p = Permutations(recoils=[2,1]); p
        Standard permutations whose recoils composition is [2, 1]
        sage: p.list()
        [[1, 3, 2], [3, 1, 2]]
    
    ::
    
        sage: p = Permutations(4, avoiding=[1,3,2]); p
        Standard permutations of 4 avoiding [1, 3, 2]
        sage: p.list()
        [[4, 1, 2, 3],
         [4, 2, 1, 3],
         [4, 2, 3, 1],
         [4, 3, 1, 2],
         [4, 3, 2, 1],
         [3, 4, 1, 2],
         [3, 4, 2, 1],
         [2, 3, 4, 1],
         [3, 2, 4, 1],
         [1, 2, 3, 4],
         [2, 1, 3, 4],
         [2, 3, 1, 4],
         [3, 1, 2, 4],
         [3, 2, 1, 4]]
    
    ::
    
        sage: p = Permutations(5, avoiding=[[3,4,1,2], [4,2,3,1]]); p
        Standard permutations of 5 avoiding [[3, 4, 1, 2], [4, 2, 3, 1]]
        sage: p.cardinality()
        88
        sage: p.random_element()
        [5, 1, 2, 4, 3]
    """

    valid_args = ['descents', 'bruhat_smaller', 'bruhat_greater',
                  'recoils_finer', 'recoils_fatter', 'recoils', 'avoiding']

    number_of_arguments = 0
    if n is not None:
            number_of_arguments += 1
    else:
        if k is not None:
            number_of_arguments += 1
            

    #Make sure that exactly one keyword was passed
    for key in kwargs:
        if key not in valid_args:
            raise ValueError, "unknown keyword argument: %s"%key
        if key not in [ 'avoiding' ]:
            number_of_arguments += 1

    if number_of_arguments == 0:
        return StandardPermutations_all()
    
    if number_of_arguments != 1:
        raise ValueError, "you must specify exactly one argument"     

    if n is not None:
        if isinstance(n, (int, Integer)):
            if k is None:
                if 'avoiding' in kwargs:
                    a = kwargs['avoiding']
                    if a in StandardPermutations_all():
                        if a == [1,2]:
                            return StandardPermutations_avoiding_12(n)
                        elif a == [2,1]:
                            return StandardPermutations_avoiding_21(n)
                        elif a == [1,2,3]:
                            return StandardPermutations_avoiding_123(n)
                        elif a == [1,3,2]:
                            return StandardPermutations_avoiding_132(n)
                        elif a == [2,1,3]:
                            return StandardPermutations_avoiding_213(n)
                        elif a == [2,3,1]:
                            return StandardPermutations_avoiding_231(n)
                        elif a == [3,1,2]:
                            return StandardPermutations_avoiding_312(n)
                        elif a == [3,2,1]:
                            return StandardPermutations_avoiding_321(n)
                        else:
                            return StandardPermutations_avoiding_generic(n, [a])
                    elif isinstance(a, __builtin__.list):
                        return StandardPermutations_avoiding_generic(n, a)
                    else:
                        raise ValueError, "do not know how to avoid %s"%a
                else:
                    return StandardPermutations_n(n)
            else:
                return Permutations_nk(n,k)
        else:
            #In this case, we have that n is a list
            if map(n.index, n) == range(len(n)):
                if k is None:
                    return Permutations_set(n)
                else:
                    return Permutations_setk(n,k)
            else:
                if k is None:
                    return Permutations_mset(n)
                else:
                    return Permutations_msetk(n,k)
    elif 'descents' in kwargs:
        if isinstance(kwargs['descents'], tuple):
            return StandardPermutations_descents(*kwargs['descents'])
        else:
            return StandardPermutations_descents(kwargs['descents'], max(kwargs['descents'])+1)
    elif 'bruhat_smaller' in kwargs:
        return StandardPermutations_bruhat_smaller(Permutation(kwargs['bruhat_smaller']))
    elif 'bruhat_greater' in kwargs:
        return StandardPermutations_bruhat_greater(Permutation(kwargs['bruhat_greater']))
    elif 'recoils_finer' in kwargs:
        return StandardPermutations_recoilsfiner(kwargs['recoils_finer'])
    elif 'recoils_fatter' in kwargs:
        return StandardPermutations_recoilsfatter(kwargs['recoils_fatter'])
    elif 'recoils' in kwargs:
        return StandardPermutations_recoils(kwargs['recoils'])
