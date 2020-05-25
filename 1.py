from nltk import tokenize
from rusenttokenize import ru_sent_tokenize
testText = "Я: она, ты."

# sent = tokenize.sent_tokenize(testText, language="russian")
# print(sent)
# sent = ru_sent_tokenize(testText)
# print(sent)
# words = tokenize.word_tokenize(sent[0], language="russian")
# print(words)
# print(ord("—"), ord("-"), ord(":"))

import MySQLdb

conn = MySQLdb.connect("localhost", "root", "SO08051897fya", "syntax_analyze", charset="utf8", init_command="SET NAMES UTF8")
cursor = conn.cursor()

cursor.execute("SELECT * FROM rule")

# Получаем данные.
row = cursor.fetchone()
while True:
    row = cursor.fetchone()
    if row is None:
        break
    print(row)

 
# Разрываем подключение.
conn.close()