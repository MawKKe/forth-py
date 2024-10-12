# Forth interpreter in Python

Stack based computing for all!

Probably not a 100% valid Forth implementation; mostly served as an educational
exercise for me. However, I had a lot of fun writing this!

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
