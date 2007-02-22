r"""
AUTHOR:
    -- David Joyner (2005-11-22, 2006-12-03): initial version
    -- Nick Alexander (2006-12-10): factor GUAVA code to guava.py
"""

import copy
import sage.modules.free_module as fm
import sage.modules.module as module
import sage.modules.free_module_element as fme
from sage.databases.lincodes import linear_code_bound
from sage.interfaces.all import gap
from sage.misc.preparser import *
from sage.matrix.matrix_space import MatrixSpace
from sage.rings.finite_field import *
from sage.groups.perm_gps.permgroup import *
from sage.misc.sage_eval import sage_eval
from sage.misc.misc import prod, add
from sage.misc.functional import log
from sage.rings.rational_field import QQ
from sage.structure.parent_gens import ParentWithGens
from linear_code import *

def HammingCode(r,F):
    """
    The $r^{th}$ Hamming code over $F=GF(q)$ is an $[n,k,d]$ code
    with length $n=(q^r-1)/(q-1)$, dimension $k=(q^r-1)/(q-1) - r$ and
    minimum distance $d=3$.
    The parity check matrix of a Hamming code has rows consisting of 
    all nonzero vectors of length r in its columns, modulo a scalar factor
    so no parallel columns arise. A Hamming code is a single error-correcting
    code.
     
    INPUT:
        r -- an integer > 2
        F -- a finite field.
    
    OUTPUT:
        Returns the r-th q-ary Hamming code.
    
    EXAMPLES:
        sage: C = HammingCode(3,GF(3))
        sage: C
        Linear code of length 13, dimension 10 over Finite Field of size 3
        sage: C.minimum_distance()
        3
        sage: C.gen_mat()
        [2 2 1 0 0 0 0 0 0 0 0 0 0]
        [1 2 0 1 0 0 0 0 0 0 0 0 0]
        [2 0 0 0 2 1 0 0 0 0 0 0 0]
        [1 0 0 0 2 0 1 0 0 0 0 0 0]
        [0 2 0 0 2 0 0 1 0 0 0 0 0]
        [2 2 0 0 2 0 0 0 1 0 0 0 0]
        [1 2 0 0 2 0 0 0 0 1 0 0 0]
        [0 1 0 0 2 0 0 0 0 0 1 0 0]
        [2 1 0 0 2 0 0 0 0 0 0 1 0]
        [1 1 0 0 2 0 0 0 0 0 0 0 1]
        sage: C = HammingCode(3,GF(4,'a'))
        sage: C
        Linear code of length 21, dimension 18 over Finite Field in a of size 2^2

    AUTHOR: David Joyner (11-2005)
    """
    q = F.order()
    gap.eval("C:=HammingCode("+str(r)+", GF("+str(q)+"))")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))
    
def QuadraticResidueCode(n,F):
    r"""
    A quadratic residue code (or QR code) is a cyclic code whose
    generator polynomial is the product of the polynomials $x-\alpha^i$ 
    ($\alpha$ is a primitive $n^{th}$ root of unity; $i$ ranges over
    the set of quadratic residues modulo $n$).
        
    INPUT:
        n -- an odd prime
        F -- a finite prime field F whose order must be a quadratic
             residue modulo n. 
    
    OUTPUT:
        Returns a quadratic residue code. 
    
    EXAMPLES:
        sage: C = QuadraticResidueCode(7,GF(2))
        sage: C
        Linear code of length 7, dimension 4 over Finite Field of size 2
        sage: C = QuadraticResidueCode(17,GF(2))
        sage: C
        Linear code of length 17, dimension 9 over Finite Field of size 2
    
    AUTHOR: David Joyner (11-2005)
    """
    q = F.order()
    gap.eval("C:=QRCode("+str(n)+", GF("+str(q)+"))")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def ExtendedQuadraticResidueCode(n,F):
    """
    The extended quadratic residue code (or XQR code) is obtained from
    a QR code by adding a check bit to the last coordinate. (These codes
    have very remarkable properties such as large automorphism groups and
    duality properties - see [HP], \S 6.6.3-6.6.4.)
        
    INPUT:
        n -- an odd prime
        F -- a finite prime field F whose order must be a quadratic
             residue modulo n. 
    
    OUTPUT:
        Returns an extended quadratic residue code. 
    
    EXAMPLES:
        sage: C = ExtendedQuadraticResidueCode(7,GF(2))
        sage: C
        Linear code of length 8, dimension 4 over Finite Field of size 2
        sage: C = ExtendedQuadraticResidueCode(17,GF(2))
        sage: C
        Linear code of length 18, dimension 9 over Finite Field of size 2
    
    AUTHOR: David Joyner (07-2006)
    """
    q = F.order()
    gap.eval("C:=QRCode("+str(n)+", GF("+str(q)+"))")
    gap.eval("XC:=ExtendedCode(C)")
    gap.eval("G:=GeneratorMat(XC)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def QuasiQuadraticResidueCode(p):
    r"""
    A (binary) quasi-quadratic residue code (or QQR code), as defined by 
    Proposition 2.2 in [BM], has a generator matrix in the block form $G=(Q,N)$. 
    Here $Q$ is a $p \\times p$ circulant matrix whose top row 
    is $(0,x_1,...,x_{p-1})$, where $x_i=1$ if and only if $i$ 
    is a quadratic residue $\mod p$, and $N$ is a $p \\times p$ circulant matrix whose top row
    is $(0,y_1,...,y_{p-1})$, where $x_i+y_i=1$ for all i. 
        
    INPUT:
        p -- a prime >2.
    
    OUTPUT: 
        Returns a QQR code of length 2p.
    
    EXAMPLES:
        sage: C = QuasiQuadraticResidueCode(11)
        sage: C
        Linear code of length 22, dimension 11 over Finite Field of size 2

    REFERENCES:
        [BM] Bazzi and Mitter, {\it Some constructions of codes from group actions}, (preprint
             March 2003, available on Mitter's MIT website). 
        [J]  D. Joyner, {\it On quadratic residue codes and hyperelliptic curves}, (preprint 2006)
        
    These are self-orthogonal in general and self-dual when $p \\equiv 3 \\pmod 4$.

    AUTHOR: David Joyner (11-2005)
    """
    F = GF(2)
    gap.eval("C:=QQRCode("+str(p)+")")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def BinaryReedMullerCode(r,k):
    """
    The binary 'Reed-Muller code' with dimension k and 
    order r is a code with length $2^k$ and minimum distance $2^k-r$
    (see for example, section 1.10 in [HP]). By definition, the
    $r^{th}$ order binary Reed-Muller code of length $n=2^m$, for
    $0 \leq r \leq m$, is the set of all vectors $(f(p)\ |\ p \\in GF(2)^m)$,
    where $f$ is a multivariate polynomial of degree at most $r$ in $m$ variables.
        
    INPUT:
        r, k -- positive integers with $2^k>r$.
    
    OUTPUT:
        Returns the binary 'Reed-Muller code' with dimension k and order r. 
    
    EXAMPLE:
        sage: C = BinaryReedMullerCode(2,4)
        sage: C
        Linear code of length 16, dimension 11 over Finite Field of size 2
        sage: C.minimum_distance()
        4
        sage: C.gen_mat()
	[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
	[0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1]
	[0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1]
	[0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1]
	[0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1]
	[0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1]
	[0 0 0 0 0 0 0 0 0 0 1 1 0 0 1 1]
	[0 0 0 0 0 0 0 0 0 1 0 1 0 1 0 1]
	[0 0 0 0 0 0 1 1 0 0 0 0 0 0 1 1]
	[0 0 0 0 0 1 0 1 0 0 0 0 0 1 0 1]
	[0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1]

    AUTHOR: David Joyner (11-2005)
    """
    F = GF(2)
    gap.eval("C:=ReedMullerCode("+str(r)+", "+str(k)+")")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def BinaryGolayCode():
    """
    BinaryGolayCode() returns a binary Golay code. This is a perfect [23,12,7] code.
    It is also cyclic, and has generator polynomial $g(x)=1+x^2+x^4+x^5+x^6+x^{10}+x^{11}$. 
    Extending it yields the extended Golay code (see ExtendedBinaryGolayCode). 

    EXAMPLE:
        sage: C = BinaryGolayCode()
        sage: C
        Linear code of length 23, dimension 12 over Finite Field of size 2
        sage: C.minimum_distance()               # long time
        7

    AUTHOR: David Joyner (11-2005)
    """
    F = GF(2)
    gap.eval("C:=BinaryGolayCode()")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def ExtendedBinaryGolayCode():
    """
    ExtendedBinaryGolayCode() returns the extended binary Golay code. This is a
    perfect [24,12,8] code. This code is self-dual.
    
    EXAMPLES:
        sage: C = ExtendedBinaryGolayCode()
        sage: C
        Linear code of length 24, dimension 12 over Finite Field of size 2
        sage: C.minimum_distance()               # long time
        8

    AUTHOR: David Joyner (11-2005)
    """
    F = GF(2)
    gap.eval("C:=ExtendedBinaryGolayCode()")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def TernaryGolayCode():
    """
    TernaryGolayCode returns a ternary Golay code. This is a perfect [11,6,5] code.
    It is also cyclic, and has generator polynomial $g(x)=2+x^2+2x^3+x^4+x^5$. 
    
    EXAMPLES:
        sage: C = TernaryGolayCode()
        sage: C
        Linear code of length 11, dimension 6 over Finite Field of size 3
        sage: C.minimum_distance()
        5

    AUTHOR: David Joyner (11-2005)
    """
    F = GF(3)
    gap.eval("C:=TernaryGolayCode()")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def ExtendedTernaryGolayCode():
    """
    ExtendedTernaryGolayCode returns a ternary Golay code. This is a self-dual perfect [12,6,6] code. 

    EXAMPLES:
        sage: C = ExtendedTernaryGolayCode()
        sage: C
        Linear code of length 12, dimension 6 over Finite Field of size 3
        sage: C.minimum_distance()
        6
        sage: C.gen_mat()
	[1 0 2 1 2 2 0 0 0 0 0 1]
	[0 1 0 2 1 2 2 0 0 0 0 1]
	[0 0 1 0 2 1 2 2 0 0 0 1]
	[0 0 0 1 0 2 1 2 2 0 0 1]
	[0 0 0 0 1 0 2 1 2 2 0 1]
	[0 0 0 0 0 1 0 2 1 2 2 1]

    AUTHOR: David Joyner (11-2005)
    """
    F = FiniteField(3)
    gap.eval("C:=ExtendedTernaryGolayCode()")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))

def RandomLinearCode(n,k,F):
    """
    The method used is to first construct a $k \\times n$ matrix of the block form $(I,A)$, 
    where $I$ is a $k \\times k$ identity matrix and $A$ is a $k \\times (n-k)$ matrix
    constructed using random elements of $F$. Then the columns are permuted 
    using a randomly selected element of the symmetric group $S_n$.

    INPUT:
        Integers n,k, with n>k>1.
    
    OUTPUT:
        Returns a "random" linear code with length n, dimension k over field F. 

    EXAMPLES:
        sage: C = RandomLinearCode(30,15,GF(2))
        sage: C                                        # random output
        Linear code of length 30, dimension 15 over Finite Field of size 2
        sage: C = RandomLinearCode(10,5,GF(4,'a'))
        sage: C                                       # random output
        Linear code of length 10, dimension 5 over Finite Field in x of size 2^2

    AUTHOR: David Joyner (11-2005)
    """
    q = F.order()
    gap.eval("C:=RandomLinearCode("+str(n)+","+str(k)+", GF("+str(q)+"))")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(G))


def ToricCode(P,F):
    """
    Let $P$ denote a list of lattice points in $\Z^d$ and let $T$ denote the
    set of all points in $(F^x )^d$ (ordered in some fixed way). Put $n=|T|$
    and let $k$ denote the dimension of the vector space of functions
    $V = Span \{x^e \ |\ e \\in P\}$. The associated {\it toric code} $C$ is the
    evaluation code which is the image of the evaluation map
    $$
                        eval_T : V \\rightarrow F^n,
    $$
    where $x^e$ is the multi-index notation ($x=(x_1,...,x_d)$, $e=(e_1,...,e_d)$, and
    $x^e = x_1^{e_1}...x_d^{e_d}$), where $eval_T (f(x)) = (f(t_1),...,f(t_n))$, and
    where $T=\{t_1,...,t_n\}$. This function returns the toric codes discussed in [J].
    
    INPUT:
        P -- all the integer lattice points in a polytope defining the toric variety.
        F -- a finite field.
        
    OUTPUT:
        Returns toric code with length n = , dimension k over field F. 

    EXAMPLES:
        sage: C = ToricCode([[0,0],[1,0],[2,0],[0,1],[1,1]],GF(7))
        sage: C     
        Linear code of length 36, dimension 5 over Finite Field of size 7
        sage: C.minimum_distance()
        24
        sage: C.minimum_distance_upper_bound()  # optional (requires internet)
        28
        sage: C = ToricCode([[-2,-2],[-1,-2],[-1,-1],[-1,0],[0,-1],[0,0],[0,1],[1,-1],[1,0]],GF(5))
        sage: C
        Linear code of length 16, dimension 9 over Finite Field of size 5
        sage: C.minimum_distance()
        6
        sage: C.minimum_distance_upper_bound()   # optional -- uses internet
        6
        sage: C = ToricCode([ [0,0],[1,1],[1,2],[1,3],[1,4],[2,1],[2,2],[2,3],[3,1],[3,2],[4,1]],GF(8,'a'))
        sage: C
        Linear code of length 49, dimension 11 over Finite Field in a of size 2^3
        sage: C.minimum_distance()  ## long time -- very time consuming
        28
        sage: print linear_code_bound(8,49,11)[0]    # optional -- uses internet
        28

        
    AUTHOR: David Joyner (07-2006)

    REFERENCES:
        [J] D. Joyner, {\it Toric codes over finite fields}, Applicable Algebra in Engineering,
            Communication and Computing, 15, (2004), p. 63--79
    """
    from sage.combinat.combinat import tuples
    mset = [x for x in F if x!=0]
    d = len(P[0])
    pts = tuples(mset,d) 
    n = len(pts) ## (q-1)^d
    k = len(P)
    e = P[0]
    B = []
    for e in P:
       tmpvar = [prod([t[i]**e[i] for i in range(d)]) for t in pts]
       B.append(tmpvar)
    ## now B0 *should* be a full rank matrix
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(B))

def TrivialCode(F,n):
    MS = MatrixSpace(F,1,n)
    return LinearCode(MS(0))

def CyclicCode(g,n,F):
    """
    Here $g$ is a polynomial in $F[x]$ which divides $x^n-1$. The
    cyclic code C associated to (g,n,F) is isomorphic as a vector space)
    to the principal ideal $(g)$ in the ring $R = F[x]/(x^n-1)$ generated by g.

    If $g$ does not divide $x^n-1$, instead of returning an error, a
    code generated by $gcd(x^n-1,g)$ is created.
    
    EXAMPLES:
        sage: x = PolynomialRing(GF(2),"x").gen()
        sage: g = x^3+x+1
        sage: C = CyclicCode(g,7,GF(2))
        sage: C
        Linear code of length 7, dimension 4 over Finite Field of size 2
    """
    q = F.order()    
    R = gap.PolynomialRing(F)
    I = R.IndeterminatesOfPolynomialRing()
    _ = gap.eval("x := %s[1];"%I.name())
    gap_g = str(gap(str(g)))
    gap.eval("x_1:=X(GF("+str(q)+"))")
    gap.eval("C:=GeneratorPolCode("+gap_g+","+str(n)+", GF("+str(q)+"))")
    gap.eval("G:=GeneratorMat(C)")
    k = eval(gap.eval("Length(G)"))
    n1 = eval(gap.eval("Length(G[1])"))
    G = [[gap_to_sage(gap.eval("G["+str(i)+"]["+str(j)+"]"),F) for j in range(1,n1+1)] for i in range(1,k+1)]
    MS = MatrixSpace(F,k,n1)
    return LinearCode(MS(G))
