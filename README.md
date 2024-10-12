# Forth interpreter in Python

[![Python CI](https://github.com/MawKKe/forth-py/actions/workflows/python-app.yml/badge.svg)](https://github.com/MawKKe/forth-py/actions/workflows/python-app.yml)

Stack based computing for all!

I don't think this is going to be a 100% standard compliant Forth
implementation (if there even is a standard...?). I just implement
necessary features as I go.

Working on this code is/was more of an educational experience for me.
I've had loads of fun working on it 🙂

## Running

Write your program in a file (e.g. 'testi.forth'), then run it:

    $ python3 forth.py examples/meaning-of-life.forth
    42

## Testing the implementation

    $ pytest

## Development

    $ make

Then run Ctrl+Shift+P in VScode > 'Python: Select Interpreter'.
Now you should be able to run pytests easily using VSCode Testing view.

## License

Copyright 2024 Markus Holmström (MawKKe)

The works under this repository are licenced under Apache License 2.0.
See file `LICENSE` for more information.

## Contributing

This project is hosted at https://github.com/MawKKe/forth-py

You are welcome to leave bug reports, fixes and feature requests. Thanks!
