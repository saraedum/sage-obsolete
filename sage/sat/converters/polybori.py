"""
ANF to CNF Converter.

AUTHORS:

- Martin Albrecht - (2008-09) initial version of 'anf2cnf.py'
- Michael Brickenstein - (2009) 'cnf.py' for PolyBoRi
- Mate Soos - (2010) improved version of 'anf2cnf.py'
- Martin Albrecht - (2012) unified and added to Sage
"""

##############################################################################
#  Copyright (C) 2008-2009 Martin Albrecht <martinralbrecht@googlemail.com>
#  Copyright (C) 2009 Michael Brickenstein <brickenstein@mfo.de>
#  Copyright (C) 2010 Mate Soos
#  Copyright (C) 2012 Martin Albrecht <martinralbrecht@googlemail.com>
#  Distributed under the terms of the GNU General Public License (GPL)
#  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
##############################################################################

from random import Random
from sage.rings.polynomial.pbori import if_then_else as ite
from sage.rings.integer_ring import ZZ
from sage.functions.other import ceil
from sage.misc.cachefunc import cached_method, cached_function
from sage.combinat.permutation import Permutations
from sage.sat.converters import ANF2CNFConverter

class CNFEncoder(ANF2CNFConverter):
    """
    ANF to CNF Converter.
    """
    def __init__(self, solver, ring, max_vars_sparse=6, use_xor_clauses=None, cutting_number=6, random_seed=16):
        """
        Construct ANF to CNF converter over ``ring`` passing clauses to ``solver``.

        This converter distinguishes two classes of
        polynomials. 

        1. Sparse polynomials are those with at most ``max_vars_sparse``
        variables. Those are converted using reduced truth-tables
        based on PolyBoRi's internal representation.

        2. Polynomials with more variables are converted by
        introducing new variables for monomials and by converting
        these linearised polynomials.

        Linearised polynomials are converted either by splitting XOR
        chains -- into chunks of length ``cutting_number`` -- or by
        constructing XOR clauses if the underlying solver supports
        it. This behaviour is disabled by passing
        ``use_xor_clauses=False``.

        INPUT:

        - ``solver`` - a SAT-solver instance

        - ``ring`` - a :cls:`BooleanPolynomialRing`

        - ``max_vars_sparse`` - maximum number of variables for direct conversion

        - ``use_xor_clauses`` - use XOR clauses; if ``None`` use if
          ``solver`` supports it. (default: ``None``)

        - ``cutting_number`` - maximum length of XOR chains after
          splitting if XOR clauses are not supported (default: 6)

        - ``random_seed`` - the direct conversion method uses
          randomness, this sets the seed (default: 16)

        EXAMPLE:

        We compare the sparse and the dense strategies, sparse first::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B)
            sage: e.clauses_sparse(a*b + a + 1)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 3 2
            1 0
            -2 0
            sage: e.phi
            [None, a, b, c]

        Now, we convert using the dense strategy::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B)
            sage: e.clauses_dense(a*b + a + 1)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 4 5
            1 -4 0
            2 -4 0
            4 -1 -2 0
            -4 -1 0
            4 1 0
            sage: e.phi
            [None, a, b, c, a*b]

        .. note::

            This constructer generates SAT variables for each Boolean
            polynomial variable.

        """
        self.random_generator = Random(random_seed)
        self.one_set = ring.one().set()
        self.empty_set = ring.zero().set()

        self.solver = solver
        self.max_vars_sparse = max_vars_sparse
        self.cutting_number = cutting_number

        if use_xor_clauses is None:
            use_xor_clauses = hasattr(solver,"add_xor_clause")
        self.use_xor_clauses = use_xor_clauses

        self.ring = ring

        # If you change this, make sure we are calling m.index()
        # below, as this relies on phi being sorted like this.
        self._phi = [None]
        for x in sorted([x.lm() for x in self.ring.gens()], key=lambda x: x.index()):
            self.var(x)

    def var(self, m=None, decision=None):
        """
        Return a *new* variable.

        This is a thin wrapper around the SAT-solvers function where
        we keep track of which SAT variable corresponds to which
        monomial.

        INPUT:

        - ``m`` - something the new variables maps to, usually a monomial
        - ``decision`` - is this variable a deicison variable?

        EXAMPLE::

            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: ce = CNFEncoder(DIMACS(), B)
            sage: ce.var()
            4
        """
        self._phi.append(m)
        return self.solver.var(decision=decision)

    @property
    def phi(self):
        """
        Map SAT variables to polynomial variables.

        EXAMPLE::

            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: ce = CNFEncoder(DIMACS(), B)
            sage: ce.var()
            4
            sage: ce.phi
            [None, a, b, c, None]
        """
        return list(self._phi)

    ##################################################
    # Encoding based on polynomial roots
    ##################################################

    def zero_blocks(self, f):
        """
        Divides the zero set of ``f`` into blocks.

        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: e = CNFEncoder(DIMACS(), B)
            sage: sorted(e.zero_blocks(a*b*c))
            [{c: 0}, {b: 0}, {a: 0}]

        .. note::

            This function is randomised.
        """
        variables = f.vars_as_monomial()

        space = variables.divisors()
        variables = list(variables.variables())
        zeros = f.zeros_in(space)
        rest = zeros
        res = list()

        def choose(s):
            indices = []
            assert not s.empty()
            nav = s.navigation()
            while not nav.constant():
                e = nav.else_branch()
                t = nav.then_branch()
                if e.constant() and not e.terminal_one():
                    indices.append(nav.value())
                    nav = t
                else:
                    if self.random_generator.randint(0,1):
                        indices.append(nav.value())
                        nav = t

                    else:
                        nav = e
            assert nav.terminal_one()
            res = self.one_set
            for i in reversed(indices):
                res = ite(i, res, self.empty_set)
            return iter(res).next()

        while not rest.empty():
            l = choose(rest)
            l_variables = set(l.variables())
            block_dict = dict([(v, 1 if v in l_variables else 0) for v in variables])
            l = l.set()
            self.random_generator.shuffle(variables)
            for v in variables:
                candidate = l.change(v.index())
                if candidate.diff(zeros).empty():
                    l = l.union(candidate)
                    del block_dict[v]
            rest = rest.diff(l)
            res.append(block_dict)
        return res

    def clauses_sparse(self, f):
        """
        Convert ``f`` using the sparse strategy.

        INPUT:

        - ``f`` - a :cls:`BooleanPolynomial`


        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B)
            sage: e.clauses_sparse(a*b + a + 1)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 3 2
            1 0
            -2 0
            sage: e.phi
            [None, a, b, c]
        """
        # we form an expression for a var configuration *not* lying in
        # the block it is evaluated to 0 by f, iff it is not lying in
        # any zero block of f+1

        blocks = self.zero_blocks(f+1)
        C = [dict([(variable, 1-value) for (variable, value) in b.iteritems()]) for b in blocks ]

        def to_dimacs_index(v):
            return v.index()+1

        def clause(c):
            return [to_dimacs_index(variable) if value == 1 else -to_dimacs_index(variable) for (variable, value) in c.iteritems()]

        for c in C:
            self.solver.add_clause(clause(c))

    ###################################################
    # Indirect conversion, may add new variables
    ###################################################

    def clauses_dense(self, f):
        """
        Convert ``f`` using the dense strategy.

        INPUT:

        - ``f`` - a :cls:`BooleanPolynomial`

        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B)
            sage: e.clauses_dense(a*b + a + 1)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 4 5
            1 -4 0
            2 -4 0
            4 -1 -2 0
            -4 -1 0
            4 1 0
            sage: e.phi
            [None, a, b, c, a*b]
        """
        equal_zero = not bool(f.constant_coefficient())

        f = (f - f.constant_coefficient())
        f = [self.monomial(m) for m in f]

        if self.use_xor_clauses:
            self.solver.add_xor_clause(f, equal_zero)
        elif f > self.cutting_number:
            for fpart, this_equal_zero in self.split_xor(f, equal_zero):
                ll = len(fpart)
                for p in self.permutations(ll, this_equal_zero):
                    self.solver.add_clause([ p[i]*fpart[i] for i in range(ll) ])
        else:
            ll = len(f)
            for p in self.permutations(ll, equal_zero):
                self.solver.add_clause([ p[i]*f[i] for i in range(ll) ])

    @cached_method
    def monomial(self, m):
        """
        Return SAT variable for ``m``

        INPUT:

        - ``m`` - a monomial.

        OUTPUT: An index for a SAT variable corresponding to ``m``.

        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B)
            sage: e.clauses_dense(a*b + a + 1)
            sage: e.phi
            [None, a, b, c, a*b]

       If monomial is called on a new monomial, a new variable is created::

            sage: e.monomial(a*b*c)
            5
            sage: e.phi
            [None, a, b, c, a*b, a*b*c]

       If monomial is called on a monomial that was queried before,
       the index of the old variable is returned and no new variable
       is created::

            sage: e.monomial(a*b)
            4
            sage: e.phi
            [None, a, b, c, a*b, a*b*c]

        .. note::

            For correctness, this function is cached.
        """
        if m.deg() == 1:
            return m.index()+1
        else:
            # we need to encode the relationship between the monomial
            # and its variables
            variables = [self.monomial(v) for v in m.variables()]
            monomial = self.var(m)

            # (a | -w) & (b | -w) & (w | -a | -b) <=> w == a*b
            for v in variables:
                self.solver.add_clause( (v, -monomial) )
            self.solver.add_clause( tuple([monomial] + [-v for v in variables]) )

            return monomial

    @cached_function
    def permutations(length, equal_zero):
        """
        Return permutations of length ``length`` which are equal to
        zero if ``equal_zero`` and equal to one otherwise.

        A variable is false if the integer in its position is smaller
        than zero and true otherwise.

        INPUT:

        - ``length`` - the number of variables
        - ``equal_zero`` - should the sum be equal to zero?

        EXAMPLE::


            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: ce = CNFEncoder(DIMACS(), B)
            sage: ce.permutations(3, True)
            [[-1, -1, -1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]]

            sage: ce.permutations(3, False)
            [[1, -1, -1], [-1, 1, -1], [-1, -1, 1], [1, 1, 1]]
        """
        E = []
        for num_negated in range(0, length+1) :
            if (((num_negated % 2) ^ ((length+1) % 2)) == equal_zero) : 
                continue
            start = []
            for i in range(num_negated) :
                start.append(1)
            for i in range(length - num_negated) :
                start.append(-1)
            E.extend(Permutations(start))
        return E

    def split_xor(self, monomial_list, equal_zero):
        """
        INPUT:

        - ``monomial_list`` - a list of monomials
        - ``equal_zero`` - is the constant coefficient zero?

        EXAMPLE::

            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: B.<a,b,c,d,e,f> = BooleanPolynomialRing()
            sage: ce = CNFEncoder(DIMACS(), B, cutting_number=3)
            sage: ce.split_xor([1,2,3,4,5,6], False)
            [[[1, 7], False], [[7, 2, 8], True], [[8, 3, 9], True], [[9, 4, 10], True], [[10, 5, 11], True], [[11, 6], True]]

            sage: ce = CNFEncoder(DIMACS(), B, cutting_number=4)
            sage: ce.split_xor([1,2,3,4,5,6], False)
            [[[1, 2, 7], False], [[7, 3, 4, 8], True], [[8, 5, 6], True]]

            sage: ce = CNFEncoder(DIMACS(), B, cutting_number=5)
            sage: ce.split_xor([1,2,3,4,5,6], False)
            [[[1, 2, 3, 7], False], [[7, 4, 5, 6], True]]
        """
        c = self.cutting_number

        nm = len(monomial_list)
        step = ceil((c-2)/ZZ(nm) * nm)
        M = []

        new_variables = []
        for j in range(0, nm, step):
            m =  new_variables + monomial_list[j:j+step]
            if (j + step) < nm:
                new_variables = [self.var(None)]
                m += new_variables
            M.append([m, equal_zero])
            equal_zero = True
        return M

    ###################################################
    # Highlevel Functions
    ###################################################

    def clauses(self, f):
        """
        Convert ``f`` using the sparse strategy if f.nvariables() is
        at most ``max_vars_sparse`` and the dense strategy otherwise.

        INPUT:

        - ``f`` - a :cls:`BooleanPolynomial`

        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B, max_vars_sparse=2)
            sage: e.clauses(a*b + a + 1)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 3 2
            1 0
            -2 0
            sage: e.phi
            [None, a, b, c]

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B, max_vars_sparse=2)
            sage: e.clauses(a*b + a + c)
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 4 7
            1 -4 0
            2 -4 0
            4 -1 -2 0
            -4 -1 -3 0
            4 1 -3 0
            4 -1 3 0
            -4 1 3 0

            sage: e.phi
            [None, a, b, c, a*b]
        """
        if f.nvariables() <= self.max_vars_sparse:
            self.clauses_sparse(f)
        else:
            self.clauses_dense(f)

    def __call__(self, F):
        """
        Encode the boolean polynomials in ``F`` .

        INPUT:

        - ``F`` - an iterable of Boolean polynomials

        OUTPUT: An inverse map int -> variable


        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B, max_vars_sparse=2)
            sage: e([a*b + a + 1, a*b+ a + c])
            [None, a, b, c, a*b]
            sage: _ = solver.write()
            sage: print open(fn).read()
            p cnf 4 9
            1 0
            -2 0
            1 -4 0
            2 -4 0
            4 -1 -2 0
            -4 -1 -3 0
            4 1 -3 0
            4 -1 3 0
            -4 1 3 0

            sage: e.phi
            [None, a, b, c, a*b]
        """
        res = []
        for f in F:
            self.clauses(f)
        return self.phi

    ####################################################
    # Highlevel Functions
    ###################################################

    def to_polynomial(self, c):
        """
        Convert clause to :cls:`BooleanPolynomial`

        INPUT:

        - ``c`` - a clause

        EXAMPLE::

            sage: B.<a,b,c> = BooleanPolynomialRing()
            sage: from sage.sat.converters.polybori import CNFEncoder
            sage: from sage.sat.solvers.dimacs import DIMACS
            sage: fn = tmp_filename()
            sage: solver = DIMACS(filename=fn)
            sage: e = CNFEncoder(solver, B, max_vars_sparse=2)
            sage: _ = e([a*b + a + 1, a*b+ a + c])
            sage: e.to_polynomial( (1,-2,3) )
            a*b*c + a*b + b*c + b
        """
        def product(l):
            # order of these multiplications for performance
            res = l[0]
            for p in l[1:]:
                res = res*p
            return res

        phi = self.phi
        product = self.ring(1)
        for v in c:
            if phi[abs(v)] is None:
                raise ValueError("Clause containst an XOR glueing variable.")
            product *= phi[abs(v)] + int(v>0)
        return product