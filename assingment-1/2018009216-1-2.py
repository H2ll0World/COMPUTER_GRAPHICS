import numpy as np
m = np.array(range(2,27))
print(m)
m = m.reshape(5,5)
print(m)

for i in range(5):
    m[0][i] = 0
print(m)

m = m.dot(m)
print(m)

sum = 0.0
for i in range(25):
    temp = m.reshape(25)
    sum = sum + temp[i]*temp[i]
print(np.sqrt(sum))


