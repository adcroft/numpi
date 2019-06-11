from __future__ import print_function

# The following import allows all the numpy modules/functions to be accessed
# as if they were in this module. i.e.
#   import numpi as np
# will work as if it read "import numpy as np"
from numpy import *

# The following import gives this script hidden access to numpy
import ignore_this as _numpy
#from ignore_this import *

def abs(x):
    return _numpy._numpy.abs(x)

def reciprocal(x, n=9):
    """Returns 1/x"""
    # https://en.wikipedia.org/wiki/Division_algorithm
    m,e = frexp(x) # Mantissa and exponent in base-2
    r = ldexp(1.,-e) # First quess
    s,x = copysign(1., x), abs(x)
    for iter in range(n):
        r = r * ( 2. - x * r )
    return r * s

def sqrt(x, n=9):
    """Returns sqrt(x)"""
    # https://en.wikipedia.org/wiki/Methods_of_computing_square_roots
    m,e = frexp(x) # Mantissa and exponent in base-2
    r = ldexp(1.,(e/2).astype(int)) # First quess
    for iter in range(n):
        r = 0.5 * ( r + x / r )
    return r

def calc_pi(n=5):
    """Returns pi"""
    # https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm
    root2 = sqrt(2.)
    a,b,t,p,rn = 1, reciprocal(root2, n=20), 0.25, 1, 0
    an = 0.5 * ( a + b )
    for iter in range(n):
        bn = sqrt( a*b )
        tn = t - p * ( a - an )**2
        pn = 2 * p
        a,b,t,p = an,bn,tn,pn
        an = 0.5 * ( a + b )
        if an==a: break
    r = an**2 * reciprocal(t)
    return r

def sin(a):
    """Returns sin(x)"""
    # https://en.wikipedia.org/wiki/Sine#Series_definition
    one_eighty = calc_pi()
    three_sixty = 2.*one_eighty
    ninety = 0.5*one_eighty
    x = 1. * array( a )
    fs = 1. + 0. * x
    # Anything < -90 reflect to >-90...
    j = ( x < -ninety )
    x[j] = -one_eighty - x[j]
    # Anything > 360 shift to range 0...360
    j = ( x > three_sixty )
    n = floor( x / three_sixty )
    x[j] = x[j] - n[j] * three_sixty
    # Anything in range 180...360 shift to 0...180
    j = ( x >= one_eighty )
    x[j] = x[j] - one_eighty
    fs[j] = -1.
    # Anything in range 90...180 reflect to 90...0
    j = ( x > ninety )
    x[j] = one_eighty - x[j]
    # Use cos(90-x) for 45...90
    j = ( x >= 0.5*ninety )
    c = cos_series(ninety-x)
    r = sin_series(x)
    r[j] = c[j]
    return r * fs

def sin_series(x):
    """Returns sin(x) for x in range -pi/2 .. pi/2"""
    # https://en.wikipedia.org/wiki/Sine#Series_definition
    C=[1.,0.16666666666666666,0.05,0.023809523809523808,0.013888888888888888,0.00909090909090909,0.00641025641025641,0.004761904761904762,0.003676470588235294,0.0029239766081871343,0.002380952380952381,0.001976284584980237,0.0016666666666666668,0.0014245014245014246,0.0012315270935960591,0.001075268817204301,0.000946969696969697,0.0008403361344537816,0.0007507507507507507,0.0006747638326585695]
    N, x2, r = 20, x**2, 0.
    term = [1.] * (N)
    for n in range(1,N):
        k = 2*n+1
        #term[n] = - term[n-1] * ( x2 / ( (k-1) * k ) )
        term[n] = - term[n-1] * ( x2 * C[n] )
    for j in range(n,-1,-1):
        r = r + term[j]
    return ( r * x )

def cos(a):
    """Returns cos(x)"""
    # https://en.wikipedia.org/wiki/Trigonometric_functions#Power_series_expansion
    one_eighty = calc_pi()
    three_sixty = 2.*one_eighty
    ninety = 0.5*one_eighty
    x = 1. * array( a )
    fs = 1. + 0. * x
    # Anything < 0 reflect to >0...
    j = ( x < 0 )
    x[j] = -x[j]
    # Anything > 360 shift to range 0...360
    j = ( x > three_sixty )
    n = floor( x / three_sixty )
    x[j] = x[j] - n[j] * three_sixty
    # Anything in range 180...360 shift to 0...180
    j = ( x >= one_eighty )
    x[j] = x[j] - one_eighty
    fs[j] = -1.
    # Anything in range 90...180 reflect to 90...0
    j = ( x > ninety )
    x[j] = one_eighty - x[j]
    fs[j] = -fs[j]
    # Use sin(90-x) for 45...90
    j = ( x >= 0.5*ninety )
    c = sin_series(ninety-x)
    r = cos_series(x)
    r[j] = c[j]
    return r * fs

def cos_series(x):
    """Returns cos(x) for x in reange -pi/2 .. pi/2"""
    # https://en.wikipedia.org/wiki/Trigonometric_functions#Power_series_expansion
    C=[0.5,0.08333333333333333,0.03333333333333333,0.017857142857142856,0.011111111111111111,0.007575757575757576,0.005494505494505495,0.004166666666666667,0.0032679738562091504,0.002631578947368421,0.0021645021645021645,0.0018115942028985507,0.0015384615384615385,0.0013227513227513227,0.0011494252873563218,0.0010080645161290322,0.00089126559714795,0.0007936507936507937,0.0007112375533428165,0.000641025641025641]
    r,f,s,n = 1, 1. ,-1., len(C)
    for i in range(1,n):
        k = 2*i
        f = f * C[i-1]
        r,s = r + x**k * f * s, -s
    return r

def tan(x):
    """Returns tan(x)"""
    a = abs(x)
    s = 1. + 0.*a
    s[x<0] = -1.
    # Reduce range 45 ... 90 to 22.5 ... 45
    j4 = ( a>=0.25*pi )
    a[j4] = 0.5 * a[j4]
    # Reduce range 22.5 ... 45 to 12.25 ... 22.5
    j2 = ( a>=0.125*pi )
    a[j2] = 0.5 * a[j2]
    t = tan_series( a )
    d = 1. / ( 1. - t**2 )
    t[j2] = 2.*t[j2] *d[j2]
    t = _numpy._numpy.minimum(1., t)
    d = ( 1. - t**2 )
    jinf = ( d == 0. ) # Catch division by zero
    d = 1. / maximum( 1.e-30, d )
    t[j4] = 2.*t[j4] * d[j4]
    t[jinf] = _numpy._numpy.inf
    return t * s

def tan_series(x):
    """Returns tan(x) for x in range -pi/6 .. pi/6"""
    # http://oeis.org/A002430
    N = _numpy._numpy.array([1, 1, 2, 17, 62, 1382, 21844, 929569, 6404582, 443861162, 18888466084, 113927491862, 58870668456604, 8374643517010684, 689005380505609448, 129848163681107301953, 1736640792209901647222])
    # http://oeis.org/A036279
    D = _numpy._numpy.array([1, 3, 15, 315, 2835, 155925, 6081075, 638512875, 10854718875, 1856156927625, 194896477400625, 2900518163668125, 3698160658676859375, 1298054391195577640625, 263505041412702261046875, 122529844256906551386796875, 4043484860477916195764296875])
    C = N.astype(float) / D.astype(float)
    n, x2, xx, r = len(C), x*x, 1., 0.
    term = [1.] * (n)
    for k in range(1,n):
        xx = xx * x2
        term[k] = xx * C[k]
    for j in range(k,-1,-1):
        r = r + term[j]
    return r * x
