make clean
. ../venv/bin/activate
PYTHONPATH=../src make clean html doctest
touch docsbuilds/html/.nojekyll
