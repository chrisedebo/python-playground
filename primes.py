#! /usr/bin/env python3.3
primes=[]
nonprimes=[]
for n in range(2,1000):
	for x in range(2,n):
		if n % x == 0:
			nonprimes.append(n)
			break
	else:
		primes.append(n)

print('Primes:')
for p in primes :
    print(p,end=',')
print('\nNon-primes:')
for np in nonprimes :
    print(np,end=',')
print('\n')


