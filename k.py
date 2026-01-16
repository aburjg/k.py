from functools import reduce; from itertools import accumulate; import math, random, timeit
I = isinstance; S = lambda x: I(x, str);T = lambda x,y: I(x, tuple) and x[0]==y;atom = lambda x: I(x, (int, float, str))
_g = lambda f: lambda x: f(x) if atom(x) else list(map(_g(f), x))
_G = lambda f: (lambda x, y: f(x, y) if atom(x) and atom(y) else list(map(lambda yi: _G(f)(x, yi), y)) if atom(x) else list(map(lambda xi: _G(f)(xi, y), x)) if atom(y) else list(map(lambda xi, yi: _G(f)(xi, yi), x, y)))

sqr,sqrt,floor,neg,Not=_g(lambda x:x*x),_g(math.sqrt),_g(math.floor),_g(lambda x:-x),_g(lambda x:int(not x))
log,ln,exp,sin,cos,tanh,pi=_g(math.log2),_g(math.log),_g(math.exp),_g(math.sin),_g(math.cos),_g(math.tanh),math.pi
add,sub,mul,div,mod=_G(lambda x,y:x+y),_G(lambda x,y:x-y),_G(lambda x,y:x*y),_G(lambda x,y:x/y if y!=0 else float('inf')),_G(lambda x,y:x if y==0 else x%y)
max,min,less,more,eql=_G(max),_G(min),_G(lambda x,y:int(x<y)),_G(lambda x,y:int(x>y)),_G(lambda y,x:int(x==y))

cat, lst = lambda x, y: ([x] if atom(x) else x) + ([y] if atom(y) else y), lambda x:[x]
til, rev, first, count = lambda x: list(range(x)), lambda x: x if atom(x) else x[::-1], lambda x: x if atom(x) else x[0], lambda x: 1 if atom(x) else len(x)
where = lambda x: [i for i, v in enumerate(x) for _ in range(v if atom(v) else 1)]
match = lambda x,y:int(x==y)
Rand = lambda x,y: random.sample(range(x),y) if x==y else [random.randint(0,y-1) for _ in range(x)]
rand = lambda x: [random.random() for _ in range(x)]

take, drop = lambda x, y: y if atom(y) else y[:x], lambda x, y: y if atom(y) else y[x:]
over, scan = lambda f: lambda x: reduce(f, x), lambda f: lambda x: list(accumulate(x, f))
right, left = lambda f: lambda x, y: list(map(lambda yi: f(x, yi), y)) if not atom(y) else f(x, y), lambda f: lambda x, y: list(map(lambda xi: f(xi, y), x)) if not atom(x) else f(x, y)
fix = lambda f: lambda x, n: (g := lambda v, r=0: v if v == (res := f(v)) or (n and r >= n) else g(res, r + 1))(x)
Fix = lambda f: lambda x, n: (g := lambda v, r=0, acc=[]: acc + [v] if v == (res := f(v)) or (n and r >= n) else g(res, r + 1, acc + [v]))(x)

def each(f): return lambda *x: f(x[0]) if len(x) == 1 and atom(x[0]) else [f(item) for item in x[0]] if len(x) == 1 else [f(*args) for args in zip(*x)]
var = lambda x, y, z=globals(): z.update({x: y}) or y # var is not a good name

def apply(x,*y,env={}):
    if I(y[0], str) and y[0][0]=="[": y = p(t(y[0]))          # str
    if I(x, str) and x[0]=="{": x = p(t(x))[0]
    if T(y[0],"["): y = [eval(i,env) for i in y[0][1]]        # y's 
    elif y and callable(y[0]): return y[0](lambda *args: apply(x, *args, env=env))
    if callable(x): return x(*y)                              # x's
    elif I(x, list): return x[y[0]] if atom(y[0]) else [apply(x,i,env=env) for i in y[0]]
    elif T(x,"{"): fun = lambda *args: eval(x[1][0], env | dict(zip('xyz', args))); return fun if not y else fun(*y)
    else: return f(x)(*y) if len(y)==1 else F(x)(*y)

_V = " +-*&|<>=~!?@,:%#_'/\\"
_f = [None, None, neg, first, where, rev, None, None, None, Not, til, rand, None, lst, None, sqrt, count, floor, None, None, None]
_F = [None, add, sub, mul, min, max, less, more, eql, match, None, Rand, apply, cat, var, div, take, drop, each, over, scan]
f, F = lambda x: _f[_V.find(x)], lambda x: _F[_V.find(x)] # fx, Fxy
def QQ(x): raise ValueError(x)
def eval(x, env={}):
    i, r = len(x)-1, []; IV = lambda x: (not x and x != 0) or (S(x) and x in _V) or (x in (_f+_F))
    s = lambda x,y=True: globals().get(x, env.get(x, x if y else None)) if S(x) else x
    while i>-1:
        l, ll = s(x[i-1] if i>0 else None), s(x[i-2] if i>1 else None)
        if i == len(x)-1: r, i = eval(x[i][1][0], env=env) if T(x[i],"(") else x[i][1] if T(x[i],'"') else s(x[i],False), i-1
        elif S(x[i]) and (x[i] in "/\\"): 
            if I(ll, (list, tuple)): r, i = apply(apply(l, left if x[i] in "\\" else right, env=env), eval([ll],env=env), r, env=env), i-3
            elif I(ll, int): r, i = apply(apply(l, Fix if x[i] in "\\" else fix, env=env),r,ll), i-3
            else: r, i = apply(apply(l, scan if x[i] in "\\" else over, env=env), r, env=env), i-2
        elif IV(l): r, i = apply(s(x[i]),r,env=env), i-1
        else: 
            if x[i] in [":","var"]: r, i = QQ("reserved") if x[i-1] in globals() else apply(s(x[i]), x[i-1], r, env, env=env), i-2
            else: args = [ll,l] if T(l,"[") else [l]; r, i = apply(s(x[i]),eval(args,env=env),r,env=env), i-1-len(args)
    return r

# a:1 2 3
# [;...]
def p(t):
    x, current = [], []
    while t:
        c = t.pop(0)
        if c in ')}]': break
        elif c == ';': x.append(current) if current else None; current = []
        elif c in '({[': current.append((c, p(t)))
        elif c == '"': current.append(('"',''.join(iter(lambda: t.pop(0), '"'))))
        elif all(i.isdigit() or i == '.' for i in c): current.append(int(c) if '.' not in c else float(c))
        elif c.strip(): current.append(c.strip())
    if current: x.append(current)
    return x

#def t(x): return [i for i in ''.join(c if c.isalnum() or c == '.' else f' {c} ' for c in x).split()]
def t(x):
    t, c = [], ''
    for i in x:
        if i.isalnum() or i == '.': c+=i
        elif c: t.append(c); t.append(i); c=''
        else: t.append(i)
    if c: t.append(c)
    return t

k=lambda x:[eval(i)for i in p(t(x))][-1:][0]
def i():
  try:
      while True: print("",end="") if not (x:=input(" ")) or x.startswith("/") else print(timeit.timeit(lambda:k(x[2:]), number=10)) if x.startswith("\\t") else print(k(x))
  except EOFError: print("\n")
  except KeyboardInterrupt: print("\ninterrupted!")
  except Exception as ex: print(f" !{ex}");i()
print(f"mj's k 2024.10.25"),i()
