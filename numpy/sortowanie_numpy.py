import numpy as np

dtype = [('name', 'S10'), ('height', float), ('age', int)]
values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),
          ('Galahad', 1.7, 38)]
a = np.array(values, dtype=dtype)       # create a structured array
np.sort(a, order='height')

np.sort(a, order=['age', 'height'])

#https://thispointer.com/delete-elements-from-a-numpy-array-by-value-or-conditions-in-python/

