. venv/bin/activate
cd src
find -name *.py | xargs python -m doctest -v
