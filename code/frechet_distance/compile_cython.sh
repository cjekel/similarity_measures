cython cfrechet.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o cfrechet.so cfrechet.c
cython c_frechet.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -I/usr/lib64/python2.7/site-packages/numpy/core/include -o c_frechet.so c_frechet.c
