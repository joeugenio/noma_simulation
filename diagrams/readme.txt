# For generatews UML diagrams use pyreverse

# To Install:
sudo apt-get install graphviz
pip install pylint

# To use:
pyreverse [options] <packages>
# Ex.:
pyreverse -AS *.py

# Use .dot file or covert it to other format available:
dot -Tpdf <dotfilename> -o output.pdf
# shows all the available output formats
dot -Txxx 

