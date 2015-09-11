import urllib.request
from urllib.request import Request, urlopen

import json
import io
import time

def ExtractUsefulInformation(translationsJSON):
    dictionaryEntry = {}
    sentencesList = translationsJSON["sentences"]
    sentencesDictionary = sentencesList[0]
    dictionaryList = []
    try:
        dictionaryList = translationsJSON["dict"]
    except:
        pass
    translations = []
    dictionaryEntry.update({'EnglishWord': sentencesDictionary["orig"]})
    dictionaryEntry.update({'BestTranslation': sentencesDictionary["trans"] })
    if len(dictionaryList) > 0:
        dictionaryDict = dictionaryList[0]
        otherPossibleTranslations = dictionaryDict["terms"]
        utf8otherPossibleTranslations = [ otherPossibleTranslation for otherPossibleTranslation in otherPossibleTranslations ]
        dictionaryEntry.update({'OtherTranslations': otherPossibleTranslations})
        try:
            pos = dictionaryDict["pos"]
            dictionaryEntry.update({'PartOfSpeech': pos})
        except:
            pass
    return dictionaryEntry

def GenerateDictionaryEntry(word, sourceLanguage, targetLanguage):
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    link = 'https://translate.google.com/translate_a/t?client=mt&sl=%s&tl=%s&hl=en&q=%s' % (sourceLanguage, targetLanguage, word)
    request = Request(link,headers=agents)
    response = urlopen(request).read().decode('utf-8')
    jsonVersion1 = json.dumps(response, ensure_ascii=False)
    jsonVersion2 = json.loads(jsonVersion1)
    jsonFinal = json.loads(jsonVersion2)
    return ExtractUsefulInformation(jsonFinal)

def MessagePerMinute(startTime,timeBetweenMessages):
	if time.time() > startTime + timeBetweenMessages:
		startTime = time.time()
		Message = "The script is working at: " + str(startTime) + "\n"
		print (Message)
	return startTime

def GetTranslations():
    startTime = time.time()
    minuteTime = startTime
    batchSaveTime = 300
    batchNumber = 48
    batchName = "RoEnDictionaryBatch" + str(batchNumber) + ".txt"
    englishWords = open('EnglishWords.txt', 'r')
    RoEnDictionary = io.open(batchName, 'w', encoding='utf8')
    for englishWord in englishWords:

        if time.time() > startTime + batchSaveTime:
            startTime = time.time()
            Message1 = "Batch " + str(batchNumber) + " finished. Closing file."
            print (Message1)
            RoEnDictionary.close()
            Message2 = "Closed file belonging to batch " + str(batchNumber) + "."
            print (Message2)
            batchNumber += 1
            batchName = "RoEnDictionaryBatch" + str(batchNumber) + ".txt"
            RoEnDictionary = io.open(batchName, 'w', encoding='utf8')
            Message3 = "Opened file belonging to batch " + str(batchNumber) + "."
            print (Message3)

        for attempt in range(0,10):
            try:
                RoEnDictionaryEntry = GenerateDictionaryEntry(englishWord, 'en', 'ro')
                json.dump(RoEnDictionaryEntry, RoEnDictionary, ensure_ascii=False)
            except:
                print("Error getting dictionary entry for word: ",englishWord,". Attempt ",attempt," out of 10. Time: ",time.time())
                time.sleep(60)
            else:
                break

        minuteTime = MessagePerMinute(minuteTime,60)

def main():
    print("Starting Requests.")
    GetTranslations()
    print("Ending Requests.")

if __name__ == '__main__':
	main()
