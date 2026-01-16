# k.py

K interpreter in 90 lines of Python.

## Run

```
python k.py
```

## Quick Start

```
  */1+!5
120

  +/!100
4950

  {x*x}[1,2,3,4]
[1, 4, 9, 16]
```

## Primitives

| Symbol | Monad | Dyad |
|--------|-------|------|
| `+` | | add |
| `-` | neg | sub |
| `*` | first | mul |
| `%` | sqrt | div |
| `&` | where | min |
| `\|` | rev | max |
| `<` | | less |
| `>` | | more |
| `=` | | eql |
| `~` | not | match |
| `!` | til | |
| `?` | rand | Rand |
| `,` | lst | cat |
| `#` | count | take |
| `_` | floor | drop |

## Adverbs

| Symbol | Usage |
|--------|-------|
| `/` | fold, each-right, converge |
| `\` | scan, each-left, converge-scan |

## Examples

Factorial:
```
 */1+!5
120
```

Average:
```
 (+/x)%#x:!100
49.5
```

Primes under 50:
```
 &2=+/0=(a)mod/a:1+!50
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

Golden ratio:
```
 0{1+1%x}/1
1.618033988749895
```

Fibonacci:
```
 5{|+\x}\1,2
[[1, 2], [3, 1], [4, 3], [7, 4], [11, 7], [18, 11]]
```

Pi (Madhava series):
```
 4*+/(-*\-_a%a:1+!n)*1%1+2*!n:1000000
3.1415916535897743
```

Euler's number:
```
 */x*1+1%#x:_x%x:1+!1000000
2.7182804690959363
```

Square root of 2 (Newton):
```
 1+100{1%2+x}/1
1.4142135623730951
```

Softmax:
```
 softmax:{exp[a]%+/exp a:x-max/x}; softmax[1,2]
[0.2689414213699951, 0.7310585786300049]
```

GCD:
```
 **(-2)_0{(0=+/0=x)*{mod[y;x]}\|x}\42,56
14
```
