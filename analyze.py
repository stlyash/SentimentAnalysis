import os
import pandas as pd
from nltk.tokenize import word_tokenize
import re

def get_CV_sequence(word):
    vowels = ["a","e","i","o","u"]
    clusters = ["ph","ng","ck"]
    prev_cons = None
    cv_seq = ""
    for char in word:
        if prev_cons and char in vowels:
            cv_seq += "CV"
            prev_cons = None
        elif char in vowels:
            cv_seq += "V"
        elif prev_cons and prev_cons+char in clusters:
            cv_seq += "C"
            prev_cons = None
        elif prev_cons:
            cv_seq += "C"
            prev_cons = char
        else:
            prev_cons = char

    if prev_cons:
        cv_seq += "C"

    return cv_seq

def get_syllable_sequence(word):
    """ Breaks a CV sequence into syllables.
    
    """
    if len(word) > 2 and word[-2]+wor[-1] == 'es':
        return 'aaaa'
    if len(word) > 2 and word[-2]+wor[-1] == 'ed':
        return 'aaaa'
    syl_seq = get_CV_sequence(word)

    while "VCC" in syl_seq:
        syl_seq = syl_seq.replace("VCC","VC-C")
    while "CVCV" in syl_seq:
        syl_seq = syl_seq.replace("CVCV","CV-CV")
    
    return syl_seq

stopWordList = []
stpFiles = ['StopWords_Auditor.txt','StopWords_Currencies.txt','StopWords_DatesandNumbers.txt','StopWords_Generic.txt','StopWords_GenericLong.txt','StopWords_Geographic.txt','StopWords_Names.txt']
for stp in stpFiles:
    with open('StopWords/'+stp,'r') as file:
        s = file.read()
        stopWordList = stopWordList + word_tokenize(s)

path = '---Path to the directory where text files containing articles is present---'
os.chdir(path)

positiveWords = []
negativeWords = []
negpath = '---path to negative words txt file---'
pospath = '---path to positive words txt file---'
with open(pospath,'r') as file:
    s = file.read()
    fileText = word_tokenize(s)   
    positiveWords += fileText
with open(negpath,'r') as file:
    s = file.read()
    fileText = word_tokenize(s)   
    negativeWords += fileText

df = pd.read_excel('---path to file ---/Input.xlsx',sheet_name='Sheet1')
urlList = df['URL'].tolist()
urlIdList = df['URL_ID'].tolist()

outputList = []
col = ['URL_ID','URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','SENTIMENT','AVERAGE SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVERAGE NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVERAGE WORD LENGTH']
for filNam in os.listdir():
    fileText = ''
    textString = ''
    with open(filNam,'r') as file:
        s = file.read()
        textString = s
        fileText = word_tokenize(s)
    filteredFileText = [k for k in fileText if not k in stopWordList]

    # Getting the URL of article

    url = ''
    for inde in range(len(urlIdList)):
        if str(urlIdList[inde]) == filNam[:-4]:
            url = urlList[inde]
            
    posScore = 0    # To be printed
    negScore = 0    # To be printed

    for word in filteredFileText:
        if word in positiveWords:
            posScore += 1
        if word in negativeWords:
            negScore += 1

    # Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
    polarityScore = (posScore-negScore)/((posScore+negScore)+0.000001)  #to be printed

    # Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
    subjectivityScore = (posScore+negScore)/((len(filteredFileText))+0.000001)    # to be printed
    
    # Finding URL ID
    urlid = ''
    for c in filNam:
        if c == '.':
            break
        else:
            urlid+=c

    # Finding Average Sentence Length
    total_words = len(filteredFileText)  # Total Words    To be printed
    total_stops = 0  # Total Sentences
    for c in textString:
        if c == '.':
            total_stops += 1
    
    avgSentLen = 0
    if total_stops == 0:
        avgSentLen = 0
    else:
        avgSentLen = total_words/total_stops

    # Sentiment Analysis
    sentiment = 0
    if total_words>0:
        sentiment = (posScore - negScore)/total_words
    # Finding Complex Words
    total_syllable = 0
    compWordCount = 0 # To be printed
    for wor in filteredFileText:
        dashCount = 0
        for ch in get_syllable_sequence(wor):
            if ch == '-':
                dashCount += 1
        dashCount += 1
        total_syllable += dashCount
        if dashCount > 2:
            compWordCount += 1

    # Finding Percentage Word Count
    percCompCount = 0
    if total_words != 0:
        percCompCount = compWordCount/total_words

    # Finding Fog Index 
    fogIndex = 0.4 * (avgSentLen + percCompCount)

    # Finding Syllable per Word
    syllPerWord = 0
    if total_words > 0:
        syllPerWord = total_syllable/total_words

    # Finding Average Word Length
    total_char = 0
    avgWorLen = 0
    for element in filteredFileText:
        total_char+=len(element)
    if total_words > 0:
        avgWorLen = total_char/total_words

    # Finding Number of Pronouns
    forPronounCount = re.compile(r'\b(I|we|ours|my|mine|(?-i:us))\b', re.I)
    pronCount = len(forPronounCount.findall(textString))
        
    outputList.append([urlid,url,posScore,negScore,polarityScore,subjectivityScore,sentiment,avgSentLen,percCompCount,fogIndex,avgSentLen,compWordCount,total_words,syllPerWord,pronCount,avgWorLen])

path = '---path to home directory---'
os.chdir(path)

df = pd.DataFrame(outputList,columns= col)
df.to_csv('outcome.csv') 

