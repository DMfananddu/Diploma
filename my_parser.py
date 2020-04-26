from pymorphy2 import MorphAnalyzer
from copy import deepcopy
from reader import gettingData
dataWordsList = []

inputData = gettingData()

# @profile
def wordExistingCheck(buf):
    wordCount = 0
    morph = MorphAnalyzer().parse(buf)
    for i in range(len(morph)):
        if (morph[i].normal_form == buf.lower() or len(morph[i].normal_form)//len(buf.lower()) < 3) and {'UNKN'} not in morph[i].tag:
            wordCount += 1
    return wordCount

# @profile
def wordProcessing(buf, stringList):
    if ord(buf[-1]) == 46:
        # print("точка", buf, stringList)
        if wordExistingCheck(buf[:-1]) != 0:
            # print("слово есть", buf, stringList)
            if len(buf[:-1]) > 1:
                stringList.append(buf)
                buf = ""
            elif len(buf[:-1]) == 1 and len(stringList[-1][:-1]) == 1 and len(stringList) > 0:
                stringList[-1] += buf
                buf = ""
        elif len(buf) == 1:
            stringList[-1] += buf
            buf = ""
    else:
        # print("не точка", buf, stringList)
        if wordExistingCheck(buf[:-1]) != 0 and wordExistingCheck(buf) == 0 or wordExistingCheck(buf) != 0 and len(buf) >= 1:
            # print("новое слово")
            stringList.append(buf)
            buf = ""
        elif len(stringList) > 0 and wordExistingCheck(stringList[-1]) == 0 and wordExistingCheck(stringList[-1][:-1]) == 0:
            stringList[-1] += buf
            buf = ""
        else:
            stringList.append(buf)
            buf = ""
    return buf, stringList

# @profile
def dataSlicing(inputData):
    buf = ""
    for dataStr in inputData:
        dataWordsList.append([])
        for symbol in dataStr:
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
                print(buf)
                buf, dataWordsList[-1] = wordProcessing(buf, dataWordsList[-1])
                print("\t", buf, dataWordsList[-1])
    if buf != "":
        buf, dataWordsList[-1] = wordProcessing(buf, dataWordsList[-1])
    if buf != "":
        dataWordsList[-1].append(buf)
        buf = ""
    return dataWordsList

dataWordsList = dataSlicing(inputData)
resultList = []
firstLetterIndex = 0
print(dataWordsList)

# @profile
def dataFinalPacking(dataWordsList):
    for stringList in dataWordsList:
        for stringElem in stringList:
            elemLength = len(stringElem)
            elem = deepcopy(stringElem)
            if len(elem) != 1:
                if 33 <= ord(elem[0]) <= 47 or 58 <= ord(elem[0]) <= 64 or \
                        91 <= ord(elem[0]) <= 96 or 123 <= ord(elem[0]) <= 127 and \
                        33 <= ord(elem[-1]) <= 47 or 58 <= ord(elem[-1]) <= 64 or \
                        91 <= ord(elem[-1]) <= 96 or 123 <= ord(elem[-1]) <= 127:
                    for i in range(elemLength-1):
                        if not (33 <= ord(elem[i]) <= 47 or 58 <= ord(elem[i]) <= 64 or 91 <= ord(elem[i]) <= 96 or 123 <= ord(elem[i]) <= 127):
                            resultList.append(elem[:i])
                            elem = elem[i:]
                            elemLength = len(elem)
                            for i in range(elemLength-1, 0, -1):
                                if not (33 <= ord(elem[i]) <= 47 or 58 <= ord(elem[i]) <= 64 or 91 <= ord(elem[i]) <= 96 or 123 <= ord(elem[i]) <= 127):
                                    resultList.append(elem[:i+1])
                                    resultList.append(elem[i+1:])
                                    break
                            break
                elif 33 <= ord(elem[0]) <= 47 or 58 <= ord(elem[0]) <= 64 or 91 <= ord(elem[0]) <= 96 or 123 <= ord(elem[0]) <= 127:
                    for i in range(elemLength-1):
                        if not (33 <= ord(elem[i]) <= 47 or 58 <= ord(elem[i]) <= 64 or 91 <= ord(elem[i]) <= 96 or 123 <= ord(elem[i]) <= 127):
                            resultList.append(elem[:i])
                            resultList.append(elem[i:])
                            break
                elif 33 <= ord(elem[-1]) <= 47 or 58 <= ord(elem[-1]) <= 64 or 91 <= ord(elem[-1]) <= 96 or 123 <= ord(elem[-1]) <= 127:
                    for i in range(elemLength-1, 0, -1):
                        if not (33 <= ord(elem[i]) <= 47 or 58 <= ord(elem[i]) <= 64 or 91 <= ord(elem[i]) <= 96 or 123 <= ord(elem[i]) <= 127):
                            resultList.append(elem[:i+1])
                            resultList.append(elem[i+1:])
                            break
                else:
                    resultList.append(elem)            
            else:
                resultList.append(elem)
    return resultList
resultList = dataFinalPacking(dataWordsList)
print(resultList)
