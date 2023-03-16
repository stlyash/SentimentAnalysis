import pandas as pd
import urllib.request 
from bs4 import BeautifulSoup

df = pd.read_excel('Input.xlsx',sheet_name='Sheet1')
urlList = df['URL'].tolist()
urlIdList = df['URL_ID'].tolist()
#for i in range(1):
for i in range(len(urlList)):
    print(i,'/',len(urlIdList),sep='')
    try:
        URL = str(urlList[i])
        urlid = str(urlIdList[i])
        # opening the url for reading
        html = urllib.request.urlopen(URL)
        # parsing the html file
        htmlParse = BeautifulSoup(html, 'html.parser')

        # getting all the paragraphs
        text = ""
        for para in htmlParse.find_all("p"):
            text += para.get_text()+'\n'
        with open('readData/'+ urlid+'.txt','w') as file:
            file.write(text)
    except:
        print('Error in file: ',i,sep='')
        with open('readData/'+ urlid+'.txt','w') as file:
            file.write('8540904380')      ## 8540904380 is a code which represents webpage is unreadable, and it also represents my contact number


    