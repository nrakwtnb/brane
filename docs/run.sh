# generate rst files from the docstrings
sphinx-apidoc -f -o ./source/api/ ../brane/

# generate html from source (rst, md files)
sphinx-build -b html ./source/ ./_build
#sphinx-build -b singlehtml ./source/ ./build
### not checked yet
#sphinx-autobuild -b html source _build/html
