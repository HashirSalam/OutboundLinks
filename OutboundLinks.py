from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
import ssl
import requests


# def CountFrequency(my_list): 
#     l=[]
#     l=my_list.split(' , ')
#     wordfreq=[l.count(p) for p in l]
#     print(dict(zip(l,wordfreq)))

def getOutboundLink(url):
    headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #gcontext = ssl.SSLContext()  # Only for gangstars
    resp = requests.get(url, headers=headers,verify=False) #IMPORTANT : verify False for SSL error
    #resp = urlopen(url)
    soup = BeautifulSoup(resp.text,'lxml')
     # a set to get inly unique values 
    OutboundLinks = set([])
    for link in soup.find_all('a', href=re.compile("http")):
    # print(link['href'])
        OutboundLinks.add(link['href'])
    
    OutboundLinks = list(OutboundLinks)
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
    

    LinkPerURL = pd.DataFrame(columns=['Related Terms','URL', 'Outbound Links'])

    for phrase in allPharases:
        URLsForPhrase =df.loc[df['Related Terms'] == phrase, 'URL']
        for i in range((URLsForPhrase.shape[0])-1):
            url = df.loc[df['Related Terms'] == phrase, 'URL'].iloc[i]
            print("Processing for : " + phrase + url)
            #print(getOutboundLink(url))
            link = ' , '.join(getOutboundLink(url))
            LinkPerURL = LinkPerURL.append({'Related Terms': phrase,'URL':url, 'Outbound Links' : link}, ignore_index=True)
    
    
  
    #print(LinkPerURL)
    
   
    #result = pd.merge(df, LinkPerURL, on='Related Terms') #adding extra rows 
    #print(result)
    LinkPerURL.to_csv("outbound.csv", encoding='utf-8',index=False)


def calculateOutboundLinks():

    data = pd.read_csv("outbound.csv")
    df = pd.DataFrame(data)
   
    allPharases =  set([])
   
    for index, row in df.iterrows():
       # print(index,row['Related Terms'])
        allPharases.add(row['Related Terms'])
    allPharases = list(allPharases)

    for phrase in allPharases:
        LinksPerTerm  = []
        OutboundLinksForPhrase =df.loc[df['Related Terms'] == phrase, 'Outbound Links']
        for i in range((OutboundLinksForPhrase.shape[0])-1):
            links = df.loc[df['Related Terms'] == phrase, 'Outbound Links'].iloc[i]
            #print(links)
            LinksPerTerm.append(links)
            # #print(getOutboundLink(url))
            # link = ' , '.join(getOutboundLink(url))
            # LinkPerURL = LinkPerURL.append({'Related Terms': phrase,'URL':url, 'Outbound Links' : link}, ignore_index=True)
        
        #print(phrase)
        #print(*LinksPerTerm, sep = "\n") 
        my_lst_str = ''.join(map(str, LinksPerTerm))
        mylist = my_lst_str.split (",")
        print(mylist)

if __name__ == '__main__':
    #getURLbyPhrases("output.csv")
    calculateOutboundLinks()