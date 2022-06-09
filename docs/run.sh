# generate rst files from the docstrings
sphinx-apidoc -f -o ./source/api/ ../brane/
#sphinx-apidoc -f -o ./source/examples/ ../examples/

cp ../examples/00_overview/package_overview_tour.ipynb ./source/examples/

# generate html from source (rst, md files)
sphinx-build -b html ./source/ ./_build
#sphinx-build -b singlehtml ./source/ ./build
### not checked yet
#sphinx-autobuild -b html source _build/html
