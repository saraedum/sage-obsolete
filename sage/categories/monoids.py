r"""
Monoids
"""
#*****************************************************************************
#  Copyright (C) 2005      David Kohel <kohel@maths.usyd.edu>
#                          William Stein <wstein@math.ucsd.edu>
#                2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2009 Florent Hivert <florent.hivert at univ-rouen.fr>
#                          Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.misc_c import prod
from sage.categories.category import Category
from sage.categories.semigroups import Semigroups
from sage.categories.subquotients import SubquotientsCategory
from sage.categories.cartesian_product import CartesianProductsCategory, cartesian_product
from sage.categories.algebra_functor import AlgebrasCategory
from sage.structure.element import generic_power

class Monoids(Category):
    r"""
    The category of (multiplicative) monoids, i.e. semigroups with a unit.

    EXAMPLES::

        sage: Monoids()
        Category of monoids
        sage: Monoids().super_categories()
        [Category of semigroups]
        sage: Monoids().all_super_categories()
        [Category of monoids,
         Category of semigroups,
         Category of magmas,
         Category of sets,
         Category of sets with partial maps,
         Category of objects]

    TESTS::

        sage: C = Monoids()
        sage: TestSuite(C).run()

    """
    @cached_method
    def super_categories(self):
        """
        Returns a list of the immediate super categories of ``self``.

        EXAMPLES::

            sage: Monoids().super_categories()
            [Category of semigroups]

        """
        return [Semigroups()]

    class ParentMethods:
        @cached_method
        def one(self):
            r"""
            Returns the one of the monoid, that is the unique neutral element for `*`.

            .. note:

               The default implementation is to coerce `1` into self.
               It is recommended to override this method because the
               coercion from the integers::

                - is not always meaningful (except for `1`);
                - often uses ``self.one()``.

            EXAMPLES::

                sage: M = Monoids().example(); M
                An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
                sage: M.one()
                ''
            """
            return self(1)

        def one_element(self):
            r"""
            Backward compatibility alias for :meth:`one`.

            TESTS::

                sage: S = Monoids().example()
                sage: S.one_element()
                ''

            """
            return self.one()

        def _test_one(self, **options):
            r"""
            Test that ``self.one()`` is an element of self and is neutral for the addition

            INPUT::

             - ``options`` -- any keyword arguments accepted by :meth:`_tester`.

            EXAMPLES:

            By default, this method tests only the elements returned by
            ``self.some_elements()``::

                sage: S = Monoids().example()
                sage: S._test_one()

            However, the elements tested can be customized with the
            ``elements`` keyword argument::

                sage: S._test_one(elements = (S('a'), S('b')))

            See the documentation for :class:`TestSuite` for more information.
            """
            tester = self._tester(**options)
            one = self.one()
            tester.assert_(one.parent() == self)
            for x in tester.some_elements():
                tester.assert_(x * one == x)
                tester.assert_(one * x == x)
            # Check that one is immutable by asking its hash;
            tester.assertEqual(type(one.__hash__()), int)
            tester.assertEqual(one.__hash__(), one.__hash__())

        def prod(self, args):
            r"""
            n-ary product

            INPUT:
             - ``args`` -- a list (or iterable) of elements of ``self``

            Returns the product of the elements in ``args``, as an element of
            ``self``.

            EXAMPLES::

                sage: S = Monoids().example()
                sage: S.prod([S('a'), S('b')])
                'ab'
            """
            return prod(args, self.one())

        def _test_prod(self, **options):
            r"""
            Run basic tests for the product method :meth:`prod` of ``self``.

            See the documentation for :class:`TestSuite` for information on
            further options.

            INPUT::

             - ``options`` -- any keyword arguments accepted by :meth:`_tester`.

            EXAMPLES::

            By default, this method tests only the elements returned by
            ``self.some_elements()``::

                sage: S = Monoids().example()
                sage: S._test_prod()

            However, the elements tested can be customized with the
            ``elements`` keyword argument::

                sage: S._test_prod(elements = (S('a'), S('b')))

            """
            tester = self._tester(**options)
            tester.assert_(self.prod([]) == self.one())
            for x in tester.some_elements():
                tester.assert_(self.prod([x]) == x)
                tester.assert_(self.prod([x, x]) == x**2)
                tester.assert_(self.prod([x, x, x]) == x**3)

    class ElementMethods:

        def is_one(self):
            r"""
            Returns whether ``self`` is the one of the monoid

            The default implementation, is to compare with ``self.one()``.

            TESTS::

                sage: S = Monoids().example()
                sage: S.one().is_one()
                True
                sage: S("aa").is_one()
                False
            """
            return self == self.parent().one()

        def __pow__(self, n):
            r"""
            INPUTS:
             - ``n``: a non negative integer

            Returns ``self`` to the `n^{th}` power.

            EXAMPLES::

                sage: S = Monoids().example()
                sage: x = S("aa")
                sage: x^0, x^1, x^2, x^3, x^4, x^5
                ('', 'aa', 'aaaa', 'aaaaaa', 'aaaaaaaa', 'aaaaaaaaaa')

            """
            if not n: # FIXME: why do we need to do that?
                return self.parent().one()
            return generic_power(self, n, self.parent().one())

        def _pow_naive(self, n):
            r"""
            A naive implementation of ``__pow__``

            INPUTS:
             - ``n``: a non negative integer

            Returns self to the `n^{th}` power, without using binary
            exponentiation (there are cases where this can actually be
            faster due to size explosion).

            EXAMPLES::

                sage: S = Monoids().example()
                sage: x = S("aa")
                sage: [x._pow_naive(i) for i in range(6)]
                ['', 'aa', 'aaaa', 'aaaaaa', 'aaaaaaaa', 'aaaaaaaaaa']
            """
            if not n:
                return self.parent().one()
            result = self
            for i in range(n-1):
                result *= self
            return result

    class Subquotients(SubquotientsCategory):

        class ParentMethods:

            def one(self):
                """
                Returns the multiplicative unit of this monoid,
                obtained by retracting that of the ambient monoid.

                EXAMPLES::

                    sage: S = Monoids().Subquotients().example() # todo: not implemented
                    sage: S.one()                                # todo: not implemented
                """
                return self.retract(self.ambient().one())

    class CartesianProducts(CartesianProductsCategory):
        """
        The category of monoids constructed as cartesian products of monoids
        """
        def extra_super_categories(self):
            """
            A cartesian product of monoids is endowed with a natural
            monoid structure.

            EXAMPLES::

                sage: Monoids().CartesianProducts().extra_super_categories()
                [Category of monoids]
                sage: Monoids().CartesianProducts().super_categories()
                [Category of monoids, Category of Cartesian products of semigroups]
            """
            return [self.base_category()]

        class ParentMethods:

            @cached_method
            def one(self):
                """
                EXAMPLES::

                    sage: cartesian_product([QQ, ZZ, RR]).one()
                    (1, 1, 1.00000000000000)
                """
                return cartesian_product([set.one() for set in self._sets])

    class Algebras(AlgebrasCategory):

        def extra_super_categories(self):
            """
            EXAMPLES::

                sage: Monoids().Algebras(QQ).extra_super_categories()
                [Category of algebras with basis over Rational Field]
                sage: Monoids().Algebras(QQ).super_categories()
                [Category of semigroup algebras over Rational Field]

                sage: Monoids().example().algebra(ZZ).categories()
                [Category of monoid algebras over Integer Ring,
                 Category of semigroup algebras over Integer Ring,
                 Category of algebras with basis over Integer Ring,
                 ...
                 Category of objects]

            """
            from sage.categories.algebras_with_basis import AlgebrasWithBasis
            return [AlgebrasWithBasis(self.base_ring())]

        class ParentMethods:

            @cached_method
            def one_basis(self):
                """
                Returns the one of the group, which index the one of this algebra,
                as per
                :meth:`AlgebrasWithBasis.ParentMethods.one_basis()
                <sage.categories.algebras_with_basis.AlgebrasWithBasis.ParentMethods.one_basis>`.

                EXAMPLES::

                    sage: A = Monoids().example().algebra(ZZ)
                    sage: A.one_basis()
                    ''
                    sage: A.one()
                    B['']
                    sage: A(3)
                    3*B['']
                """
                return self.basis().keys().one()
