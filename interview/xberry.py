# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

# [1,2,3,4,5]
# 5
# 4
# 3
# 2
# 1


def naopak(values):
    gen = (print(value) for value in values[::-1])
    [val for val in gen]


naopak([1, 2, 3, 4, 5])


def remove_dublicats(values):
    #cache = [] + iteracja plus if i gi
    # lub set

    working_values = values.copy()
    dicta = {}
    for index, element in enumerate(working_values, start=0):
        dicta[element] = 1 if dicta.get(element, None) else values.pop()

    return values


print(remove_dublicats([1, 1, 3, 2, 3, 3]))


class AdressMails(db.Modle):
    __tablename__ = 'AdressMails'

    id = db.column(db.intiger, primary_key=True)
    mail = db.columns(db.string, default='guest @ cos.pl')


class User(db.Model):
    __tablename__

    id = db.column(db.intiger, primary_key=True)
    username = db.columns(db.string, default=guest)
    mail = db.relationship('AdressMails'