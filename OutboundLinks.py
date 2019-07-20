from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
import ssl
import requests


def getOutboundLink(url):
    headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #gcontext = ssl.SSLContext()  # Only for gangstars
    resp = requests.get(url, headers=headers,verify=False) #IMPORTANT : verify False for SSL 
    #resp = urlopen(url)
    soup = BeautifulSoup(resp.text,'lxml')
     # a set to get inly unique values 
    OutboundLinks = set([])
    for link in soup.find_all('a', href=re.compile("http")):
    # print(link['href'])
        OutboundLinks.add(link['href'])

    return(OutboundLinks)

def getURLbyPhrases(filname):
    #print("Reading file please wait ... ")

    data = pd.read_csv(filname)
    df = pd.DataFrame(data)
    allPharases =  set([])
   
    for index, row in df.iterrows():
       # print(index,row['Related Terms'])
        allPharases.add(row['Related Terms'])

    allPharases = list(allPharases)
    


    #print(URLsForPhrase.shape[0])
    #print(df.loc[df['Related Terms'] == allPharases[0], 'URL'].iloc[0])

    for phrase in allPharases:
        URLsForPhrase =df.loc[df['Related Terms'] == phrase, 'URL']
        for i in range((URLsForPhrase.shape[0])-1):
            url = df.loc[df['Related Terms'] == phrase, 'URL'].iloc[i]
            print(phrase,url)
            print(getOutboundLink(url))


if __name__ == '__main__':
    getURLbyPhrases("output.csv")