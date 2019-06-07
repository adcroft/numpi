from __future__ import print_function

import hashlib
import numpi as numpy  # Module to test

def logistic_map(x, r=4.-1./32):
    """Logistic map r*x*(1-x)"""
    return r * x * ( 1. - x )
def generate_numbers(n, r=4.-1./32, x0=0.5, n0=0):
    """Generates reproducible vector of values between 0 and 1"""
    for k in range(n0):
        x0 = logistic_map( x0, r=r)
    x = numpy.zeros(n)
    x[0] = x0
    for k in range(1,n):
        x[k] = logistic_map( x[k-1], r=r)
    return x
def compare_numbers(x, y, good_hash=None):
    # Compare hashes
    status = True
    # Numerical test
    error = ( x - y )
    n = numpy.count_nonzero( error )
    if n>0:
        print(' X There were %i differences detected (out of %i) or %3.4f%% hits.'%(n,error.size,(100.*n)/error.size))
        k = numpy.nonzero( error )[0]
        print('   First few values ...')
        frac = error / x
        for j in range( min(n, 5) ):
            i = k[j]
            a,b,e,f = x[i],y[i],error[i],frac[i]
            print('      x(%i)=%23.15e y(%i)=%23.15e error=%.5e frac. err.=%.2e'%(i,a,i,b,e,f))
        print('   Largest fractional error = %.2e'%numpy.abs( frac ).max() )
        status = False
    # Bitwise (hash) test
    hx = hashlib.sha256( numpy.array( x ) ).hexdigest()
    hy = hashlib.sha256( numpy.array( y ) ).hexdigest()
    print('   hash(x) =', hx, 'min=%.15e max=%.15e'%(x.min(), x.max()))
    if hx != hy and status:
        print('   hash(y) =', hy, 'min=%.15e max=%.15e'%(y.min(), y.max()))
        print(' X Hashes do not match (i.e. bits differ).')
        status = False
    # Recorded hash
    if good_hash is not None:
        if hx == good_hash:
            print('   Hash matches recorded hash.')
        else:
            print('   hash(R) =', good_hash)
            print(' X Hash does NOT match recorded hash!')
            status = False
    return status
def writefile(filename, vals):
    f = netCDF4.Dataset(filename, 'w', clobber=True, format='NETCDF3_CLASSIC')
    v = f.createDimension('n', len(vals) )
    v = f.createVariable('results', 'f8', ('n',))
    v[:] = numpy.array(vals)[:]
    f.close()

N = 1024*1024
x01 = generate_numbers(N, r=4.-1./(1024*1024*1024*1024)) # Reproducible numbers between 0..1

print('Generated test numbers: ', end='')
for k in range(4): print( '%.15e'%x01[k], end=', ' )
print('...')
x01_hash = 'e6eb0684e329098c7c3fd2514e14436d27dfc13395237b179168ec34030e0c11'
assert compare_numbers(x01, x01, good_hash=x01_hash), 'Generated test numbers did not reproduce!'

# Generate better numbers
x01 = generate_numbers(N, r=4.-1./(1024*1024*1024*1024), n0=987654) # Reproducible numbers between 0..1
print('Generated test numbers: ', end='')
for k in range(4): print( '%.15e'%x01[k], end=', ' )
print('...')
x01_hash = 'b0e634899b6519687c044e0310b2ac9bf0e56704dcd70696749a9b84da2e3661'
assert compare_numbers(x01, x01, good_hash=x01_hash), 'Generated test numbers did not reproduce!'

print('Check that PI (numpy.pi) is bitwise as expected')
x = numpy.array([numpy.pi])
pi_hash = '8b5319c77d1df2dcfcc3c1d94ab549a29d2b8b9f61372dc803146cbb1d2800b9'
compare_numbers(x, x, good_hash=pi_hash), 'numpy.pi did not reproduce'

print('Check that maximum floating point number (numpy.finfo.max) is bitwise as expected')
x = numpy.array([numpy.finfo(float).max])
max_hash = 'dd46fdd197731f40f29d789fd02be525b10ff16ea3b7830c9f2c5b28131420ff'
assert compare_numbers(x, x, good_hash=max_hash), 'numpy.pi did not reproduce'

print('Check that pass through to numpy works')
x = numpy.finfo(float).max * ( 2.*x01 - 1. )
y = numpy.round_lastbits(x)
assert compare_numbers(x, y), 'numpi without rounding did not reproduce!'

print('Check numpi with rounding bits = 0')
numpy.set_rounding_bits(0)
y = numpy.round_lastbits(x)
assert compare_numbers(x, y), 'numpi with rounding bits=0 did not reproduce!'

print('Check numpi with rounding bits = 1')
numpy.set_rounding_bits(1)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=1!'

print('Check numpi with rounding bits = 2')
numpy.set_rounding_bits(2)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=2!'

print('Check numpi with rounding bits = 4')
numpy.set_rounding_bits(4)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=4!'

print('Check numpi with rounding bits = 8')
numpy.set_rounding_bits(8)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=8!'

print('Check numpi with rounding bits = 10')
numpy.set_rounding_bits(10)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=10!'

print('Check numpi with rounding bits = 12')
numpy.set_rounding_bits(12)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=12!'

print('Check numpi with rounding bits = 16')
numpy.set_rounding_bits(16)
y = numpy.round_lastbits(x)
assert not compare_numbers(x, y), 'No differences detected using rounding bits=16!'

print('Check numpy intrinsics for special values')
numpy.unset_rounding_bits()
x = numpy.array([ numpy.sin(numpy.pi/4), numpy.cos(numpy.pi/4), numpy.tan(numpy.pi/4) ])
y = numpy.array([ numpy.sqrt(2)/2, numpy.sqrt(2)/2,  1.0 ])
assert not compare_numbers(x, y), 'numpy intrinsics unexpectedly matched!'

print('Check numpi intrinsics with rounding bits=2 for special values')
numpy.set_rounding_bits(2)
x = numpy.array([ numpy.sin(numpy.pi/4), numpy.cos(numpy.pi/4), numpy.tan(numpy.pi/4) ])
y = numpy.array([ numpy.sqrt(2)/2, numpy.sqrt(2)/2,  1.0 ])
assert compare_numbers(x, y), 'numpi intrinsics failed to reproduce!'

print('Check numpi intrinsic sin() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.sin( (x01 - 0.5)*numpy.pi )
sin_hash = 'd1a2078401dc8020f19bdad13873765a319fa037c7da80a5289bf292918bb368'
assert compare_numbers(x, x, good_hash=sin_hash), 'numpi intrinsic sin() failed to reproduce recorded hash!'

print('Check numpi intrinsic cos() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.cos( (x01 - 0.5)*numpy.pi )
cos_hash = '6fd30baf6dc80ed098cbfaebabd85478a13c4fefd9679601bd9ebed4f946b6c5'
assert compare_numbers(x, x, good_hash=cos_hash), 'numpi intrinsic cos() failed to reproduce recorded hash!'

print('Check numpi intrinsic tan() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.tan( (x01 - 0.5)*numpy.pi )
tan_hash = '33de75e67b47e3f8bc867dd62eca8fae1c966eee38927898a354d14608c038af'
assert compare_numbers(x, x, good_hash=tan_hash), 'numpi intrinsic tan() failed to reproduce recorded hash!'

print('Check numpi intrinsic arcsin() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.arcsin( 2.*x01 - 1. )
arcsin_hash = 'ea1080e16ae6aed8da973f9edbc77252810f26063560a93270d2ef2bba89a176'
assert compare_numbers(x, x, good_hash=arcsin_hash), 'numpi intrinsic arcsin() failed to reproduce recorded hash!'

print('Check numpi intrinsic arccos() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.arccos( 2.*x01 - 1. )
arccos_hash = '2ee1dc8ecc794df21fe93d008d76a3d2499040260ed2a65e264ab92d4aedd6d8'
assert compare_numbers(x, x, good_hash=arccos_hash), 'numpi intrinsic arccos() failed to reproduce recorded hash!'

print('Check numpi intrinsic arctan() with rounding bits=12 for range of values')
numpy.set_rounding_bits(12)
x = numpy.arctan( 2.*x01 - 1. )
arctan_hash = '23caeb9e0ef686133c8d519a5de5b50e309567c9a9dc6ce5ce1a9e6347b7b4a3'
assert compare_numbers(x, x, good_hash=arctan_hash), 'numpi intrinsic arctan() failed to reproduce recorded hash!'

#print('numpy-numpi intrinsics frequency of hits with rounding bits = 1 (informational only, not a test)')
numpy.unset_rounding_bits()
x = numpy.sin( (x01 - 0.5)*numpy.pi )
numpy.set_rounding_bits(1)
y = numpy.sin( (x01 - 0.5)*numpy.pi )
#assert not compare_numbers(x, y), 'numpy numpi intrinsics unexpectedly matched!'
