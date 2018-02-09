. ../venv/bin/activate
PYTHONPATH=../src make html doctest
touch _build/html/.nojekyll
