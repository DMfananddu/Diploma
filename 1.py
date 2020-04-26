from nltk import tokenize
from rusenttokenize import ru_sent_tokenize
testText = "Н.Р. Брысина, М. А. Кучеренко и пр., м. б. и д. б. задолбали, заколебали и т.д., и т. п."

sent = tokenize.sent_tokenize(testText, language="russian")
print(sent)
sent = ru_sent_tokenize(testText)
print(sent)
words = tokenize.word_tokenize(sent[0], language="russian")
print(words)