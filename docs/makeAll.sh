make clean
. ../venv/bin/activate
PYTHONPATH=../src make clean html doctest
touch _build/html/.nojekyll
