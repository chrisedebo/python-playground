#! /usr/bin/env python3.4

def fibp(n):
    """Print Fibonacci series up to n."""
    a,b = 0,1
    while a < n:
        print(a, end=' ')
        a,b = b, a+b
    print()

def fibr(n):
    """Return a list containing the Fibonacci series up to n."""
    result=[]
    a,b = 0,1
    while a < n:
        result.append(a)
        a,b = b, a+b
    return result

print(fibp.__doc__ + "(n = 20000)")
fibp(20000)

print(fibr.__doc__ + "(n = 100)")
f100 = fibr(100)
print(f100)


