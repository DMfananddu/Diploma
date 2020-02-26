from pymorphy2 import MorphAnalyzer
# ввод текста вручную в командной строке
inputStr = input("Введите текст, оканчивающийся символом переноса строки (или нажмите Enter): ").strip("\n")

# ввод текста чтением из файла

stringList = []
buf = ""

def wordExistingCheck(buf):
    wordCount = 0
    morph = MorphAnalyzer().parse(buf)
    for i in range(len(morph)):
        if morph[i].normal_form == buf.lower():
            wordCount += 1
    return wordCount

for symbol in inputStr:
    buf += symbol
    if 48 <= ord(symbol) <= 57:
        print("цифра:", symbol)
    elif 33 <= ord(symbol) <= 47 or 58 <= ord(symbol) <= 64 or 91 <= ord(symbol) <= 96 or 123 <= ord(symbol) <= 127:
        print("знак препинания:", symbol)
    elif 65 <= ord(symbol) <= 90:
        print("Прописная латинская:", symbol)
    elif 97 <= ord(symbol) <= 122:
        print("Строчная латинская:", symbol)
    elif 1040 <= ord(symbol) <= 1071 or ord(symbol) == 1025:
        print("Прописная русская:", symbol)
    elif 1072 <= ord(symbol) <= 1103 or ord(symbol) == 1105:
        print("Строчная русская:", symbol)
    elif ord(symbol) == 32:
        buf = buf[:-1]
        if buf != "" and ord(buf[-1]) != 46:
            print(buf)
            stringList.append(buf)
            buf = ""
        elif len(buf) >= 1:
            if wordExistingCheck(buf[:-1]) != 0:
                stringList.append(buf)
                buf = ""
if buf != "":
    stringList.append(buf)
print(stringList)