RMDIR "docs" /S /Q
mkdir docs
pdoc --html -f --output-dir .docs_test similaritymeasures
robocopy .docs_test\similaritymeasures\ docs\ /E
