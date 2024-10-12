# TODO

Goal is not to produce a Forth that is 100% compatible with other "proper"
implementations, but to implement most of what a useful VM would need.

- [x] implement basic stack machine that processes tokens from a stream
- [x] implement support for built-int functions
- [x] implement dup, flip
- [x] implement basic arithmetic ops
- [x] implement support for additional numerical types (hex, bin, complex, fractions, etc)
- [x] implement support for user-defined functions
- [x] implement basic IO/print ops
- [x] implement halt
- [x] implement CLI interface
- [x] implement multi-file support (CLI)
- [x] implement basic stats counter (processed token count)
- [x] implement basic logical ops (<,<=,>,>=,==,and,or,not)
- [ ] implement string handling
- [ ] implement branching, loops
- [ ] implement variables (we kinda already do through user-defined funcs)


It seems achieving 100% test coverage is _trivial_, let's try keep it that way :)
