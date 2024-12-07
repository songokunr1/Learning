import numpy as np

# %%timeit
import numpy as np

all_files = range(0, int(1e7))  # just a few more to be sure
old_files = np.random.randint(0, 1e7, size=int(1e5))  # random old "files"

new_files = set(all_files) - set(old_files)
len(new_files)

np.setdiff1d(a,b)