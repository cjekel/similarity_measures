# cy_similaritymeasures

this folder shall contain stuff to cythonize the similaritymeasures functions

```
benchmark.py    #shall be the script containg a quick performance check, to be executed at last after the cythonized version was correctly built
build_cython_extension.sh   #to invoke the build from the setup.py file a command is required, and for linux such command is written in this file
cy_similaritymeasures.pyx   #the cython code with the cythonized version of the frechet function
setup.py    #a setup.py file used to build the cython code and obtain an extension from it
```

## extension building

cython code from the `*.pyx` file is not directly invokable from python, instead it should be built and transformed into an extension. To do that there is the script `build_cython_extension.sh`, which invokes `setup.py` to obtain a `.cpp` and `.so` extension file to be invoked from python.

You should have cython on your machine in order to build everything.

## results

to run the benchmark just run the `benchmark.py`. On my machine the results were:

```
average execution time for non cythonized version: 0.744819
average execution time for cythonized version: 0.433768
improvement: 41 %
```