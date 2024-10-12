# a secret message to be printed into stdout
104 101 108 108 111 32 119 111 114 108 100 33 12 WRITEB CR

10 20 30.123456
# 1 trace
+ + . CR

0 . CR

3 2 / . CR

: ADD1 1 + ;
: ADD39 38 ADD1 + ;

5 2 - ADD39 . CR

# 2/3 1/4 + . CR

: i 1j ;

: pi 3.141592653589793 ;

: e 2.718281828459045 ;

: euler pi i * e flip pow ;

999 . CR
euler . CR

2 10 pow 1.61 7 pow 1j * . CR

2/3 dup . CR
3 dup . CR
pow dup . CR
1 flip / . CR
