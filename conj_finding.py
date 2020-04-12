from reader import gettingData
from nltk_parser import parsing

testText = gettingData()
parsedTestText = parsing(testText)

def conjFinding(parsedText):
    for p in parsedText["paragraphs"]:
        for s in p["sentences"]:
            for l in s["lexems"]:
                break
# testing
conjFinding(parsedTestText)