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
        if (morph[i].normal_form == buf.lower() or len(morph[i].normal_form)//len(buf.lower()) < 3) and {'UNKN'} not in morph[i].tag:
            wordCount += 1
    return wordCount

for symbol in inputStr:
    buf += symbol
    # if 48 <= ord(symbol) <= 57:
    #     print("цифра:", symbol)
    # elif 33 <= ord(symbol) <= 47 or 58 <= ord(symbol) <= 64 or 91 <= ord(symbol) <= 96 or 123 <= ord(symbol) <= 127:
    #     print("знак препинания:", symbol)
    # elif 65 <= ord(symbol) <= 90:
    #     print("Прописная латинская:", symbol)
    # elif 97 <= ord(symbol) <= 122:
    #     print("Строчная латинская:", symbol)
    # elif 1040 <= ord(symbol) <= 1071 or ord(symbol) == 1025:
    #     print("Прописная русская:", symbol)
    # elif 1072 <= ord(symbol) <= 1103 or ord(symbol) == 1105:
    #     print("Строчная русская:", symbol)
    if ord(symbol) == 32:
        buf = buf[:-1]
        if buf == "":
            continue
        if ord(buf[-1]) != 46:
            print("не точка", stringList)
            if wordExistingCheck(buf) != 0:
                stringList.append(buf)
                buf = ""
        elif wordExistingCheck(buf[:-1]) != 0:
            print("точка", stringList)
            if len(buf) > 2:
                stringList.append(buf)
                buf = ""
            elif len(buf) == 1:
                stringList[-1] += buf
                buf = ""
        else:
            if len(buf) == 1:
                stringList[-1] += buf
                buf = ""
if buf != "":
    if ord(buf[-1]) != 46 and wordExistingCheck(buf) != 0:
        stringList.append(buf)
        buf = ""
    elif wordExistingCheck(buf[:-1]) != 0:
        if len(buf) > 2:
            stringList.append(buf)
            buf = ""
        elif len(buf) == 1:
            stringList[-1] += buf
            buf = ""
    else:
        if len(buf) == 1:
            stringList[-1] += buf
            buf = ""
print(stringList)