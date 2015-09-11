import pymongo
from pymongo import MongoClient
from nltk.tokenize import wordpunct_tokenize

import json
import os
import itertools
import sys

NLPclient = MongoClient('localhost', 27017) # The client connects to a database
NLPdb = NLPclient.testNLPdb # The data base has collections

# Collections have elements:

#English
NLPcollectionUnigrams =  NLPdb.testNLPcollectionUnigrams
NLPcollectionBigrams =  NLPdb.testNLPcollectionBigrams

NLPcollectionUnigramFrequencies = NLPdb.testNLPcollectionUnigramFrequencies # This collection contains unigram frequencies
NLPcollectionBigramFrequencies = NLPdb.testNLPcollectionBigramFrequencies # This collection contains bigram frequencies
NLPcollectionBigramProbabilities = NLPdb.testNLPcollectionBigramProbabilities # This collection contains unigram probabilities

#Romanian
NLPcollectionUnigramsRO =  NLPdb.testNLPcollectionUnigramsRO
NLPcollectionBigramsRO =  NLPdb.testNLPcollectionBigramsRO

NLPcollectionUnigramFrequenciesRO = NLPdb.testNLPcollectionUnigramFrequenciesRO # This collection contains unigram frequencies
NLPcollectionBigramFrequenciesRO = NLPdb.testNLPcollectionBigramFrequenciesRO # This collection contains bigram frequencies
NLPcollectionBigramProbabilitiesRO = NLPdb.testNLPcollectionBigramProbabilitiesRO # This collection contains unigram probabilities

#Dictionary
NLPcollectionEnRoDict =  NLPdb.testNLPcollectionEnRoDict

def GetWordTranslationsAsList(word):
    translationRecord = NLPcollectionEnRoDict.find_one({"Word":word})
    translationDict = translationRecord["Dictionary"]
    return translationDict["Translations"]

def BackTrack(translationMatrix):
    startRow = 0
    endRow = len(translationMatrix)
    currentRow = startRow
    code = ""
    sentanceList = []
    while currentRow < endRow:
        code += "for word"+str(currentRow)+" in translationMatrix["+str(currentRow)+"]:"+"\n  " + "  "*currentRow
        currentRow += 1
    code += 'sentanceList.append(word0 + " " + word1 + " " + word2 + " " + word3 + " " + word4 + " " + word5)'
    exec(code)
    return sentanceList

def CheckGrammar(sentanceList):
    index = 0
    for index in range(0,len(sentanceList)-1):
        test = sentanceList[index]
        if test == "the":
            try:
                sentanceList[index+1] += "a"
            except:
                pass
            sentanceList.pop(index)
    return sentanceList

def BayesChainRule(sentanceList):
    sentanceProbability = 0
    for touple in zip(sentanceList,sentanceList[1:]):
        try:
            sentanceProbability += NLPcollectionBigramProbabilities.find_one({"fullBigram":touple[0]+"_"+touple[1]})["probability"]
        except:
            sentanceProbability += 0.001
    return sentanceProbability/len(sentanceList)

def ChooseBestTranslation(possibleTranslatedSentances):
    maxPosibility = 0
    bestTranslation = ""
    for sentance in possibleTranslatedSentances:
        gramaticallyCorrectSentance = CheckGrammar(wordpunct_tokenize(sentance))
        posibility = BayesChainRule(gramaticallyCorrectSentance)
        if posibility > maxPosibility:
            bestTranslation = sentance
            maxPosibility = posibility
    return bestTranslation

def Translate(toTranslate):

    import pymongo
    from pymongo import MongoClient
    from nltk.tokenize import wordpunct_tokenize

    import json
    import os
    import itertools
    import sys

    NLPclient = MongoClient('localhost', 27017) # The client connects to a database
    NLPdb = NLPclient.testNLPdb # The data base has collections

    # Collections have elements:

    #English
    NLPcollectionUnigrams =  NLPdb.testNLPcollectionUnigrams
    NLPcollectionBigrams =  NLPdb.testNLPcollectionBigrams

    NLPcollectionUnigramFrequencies = NLPdb.testNLPcollectionUnigramFrequencies # This collection contains unigram frequencies
    NLPcollectionBigramFrequencies = NLPdb.testNLPcollectionBigramFrequencies # This collection contains bigram frequencies
    NLPcollectionBigramProbabilities = NLPdb.testNLPcollectionBigramProbabilities # This collection contains unigram probabilities

    #Romanian
    NLPcollectionUnigramsRO =  NLPdb.testNLPcollectionUnigramsRO
    NLPcollectionBigramsRO =  NLPdb.testNLPcollectionBigramsRO

    NLPcollectionUnigramFrequenciesRO = NLPdb.testNLPcollectionUnigramFrequenciesRO # This collection contains unigram frequencies
    NLPcollectionBigramFrequenciesRO = NLPdb.testNLPcollectionBigramFrequenciesRO # This collection contains bigram frequencies
    NLPcollectionBigramProbabilitiesRO = NLPdb.testNLPcollectionBigramProbabilitiesRO # This collection contains unigram probabilities

    toTranslateList = (list(wordpunct_tokenize(toTranslate)))
    toTranslateDictionary = {}
    translationMatrix = []
    for word in toTranslateList:
        toTranslateDictionary[word] = GetWordTranslationsAsList(word)
        translationMatrix.append(toTranslateDictionary[word])
    possibleTranslatedSentances = BackTrack(translationMatrix)
    bestPossibleTranslation = ChooseBestTranslation(possibleTranslatedSentances)
    #print(bestPossibleTranslation)
    return bestPossibleTranslation

#print(Translate("the law for men is bad"))
