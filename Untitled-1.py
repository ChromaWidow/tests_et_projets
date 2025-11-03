from random import randint
'''
L=[]
max= 100
n=50
for i in range(n):
    L.append(randint(0,max))
print(L)
'''
n=50

L=[randint(0,max)for i in range(n)]
print(L)

for i in range(0,len(L)-1):
     min=L[i]
     min_index = i

for j in range(i + 1, n):
    if L[j] < L[i]:
            min=L[j]
            min_index = j
            L[i], L[min_index] = L[min_index], L[i]

print(L)