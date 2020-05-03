from nltk import tokenize
from rusenttokenize import ru_sent_tokenize
testText = "Я: она, ты."

sent = tokenize.sent_tokenize(testText, language="russian")
print(sent)
sent = ru_sent_tokenize(testText)
print(sent)
words = tokenize.word_tokenize(sent[0], language="russian")
print(words)

# print(ord("—"), ord("-"), ord(":"))