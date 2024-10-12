RMDIR "docs" /S /Q
mkdir docs
pdoc similaritymeasures -o docs -d numpy
robocopy .docs_test\similaritymeasures\ docs\ /E
