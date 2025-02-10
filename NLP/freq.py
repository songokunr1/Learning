import nltk
from nltk.corpus import brown
from collections import Counter
nltk.download('brown')
words = brown.words()
word_freq = Counter(words)
most_common_words = word_freq.most_common(100000)
print(most_common_words)