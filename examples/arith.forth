10 20 30.123456

+ + . CR

0 . CR

3 2 / . CR

: add1 1 + ;
: add39 38 add1 + ;

5 2 - add39 . CR

# 2/3 1/4 + . CR

: i 1j ;

: pi 3.141592653589793 ;

: e 2.718281828459045 ;

: euler pi i * e FLIP POW ;

999 . CR
euler . CR

2 10 POW 1.61 7 POW 1j * . CR

2/3 DUP . CR
3 DUP . CR
POW DUP . CR
1 FLIP / . CR
