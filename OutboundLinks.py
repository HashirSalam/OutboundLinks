from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
import ssl
import requests
from collections import Counter
pd.options.mode.chained_assignment = None # Removes warning for copied dataframe





RESERVED = ["gov","wiki"]


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

def scrapeURLS(filname):
    #print("Reading file please wait ... ")

    data = pd.read_csv(filname)
    df = pd.DataFrame(data)
    allPharases =  set([])
   
    for index,row in df.iterrows():   #dont remove index
       # print(index,row['Related Terms'])
        allPharases.add(row['Related Terms'])

    
    allPharases = list(allPharases)
    

    LinkPerURL = pd.DataFrame(columns=['Related Terms','URL', 'Outbound Links'])

    for phrase in allPharases:
        URLsForPhrase =df.loc[df['Related Terms'] == phrase, 'URL']
        for i in range((URLsForPhrase.shape[0])-1):
            url = df.loc[df['Related Terms'] == phrase, 'URL'].iloc[i]
            #print("Processing for : " + phrase + url)
            
            if any(x in url for x in RESERVED):
              
                LinkPerURL = LinkPerURL.append({'Related Terms': phrase,'URL':url, 'Outbound Links' : url}, ignore_index=True)
            else:
                link = ' , '.join(getOutboundLink(url))
                LinkPerURL = LinkPerURL.append({'Related Terms': phrase,'URL':url, 'Outbound Links' : link}, ignore_index=True)
        
    LinkPerURL.to_csv("outbound.csv", encoding='utf-8',index=False)


def calculateOutboundLinks():

    data = pd.read_csv("outbound.csv")
    df = pd.DataFrame(data)
    
    #Get those rows with  keywords
    reserveWordString = '|'.join(RESERVED)
    
    reservedRecords = df[df['URL'].str.contains(reserveWordString)==True]
    
    diff = df[~df.apply(tuple,1).isin(reservedRecords.apply(tuple,1))]
   

    allPharases =  set([])
    dfObj = pd.DataFrame(columns = ['Related Terms' , 'Outbound Links'])
    
    for index,row in diff.iterrows():
       # print(index,row['Related Terms'])
        allPharases.add(row['Related Terms'])
    allPharases = list(allPharases)
    
    for phrase in allPharases:
        LinksPerTerm  = []
        OutboundLinksForPhrase =diff.loc[diff['Related Terms'] == phrase, 'Outbound Links']
      
        for i in range((OutboundLinksForPhrase.shape[0])-1):
            links = diff.loc[diff['Related Terms'] == phrase, 'Outbound Links'].iloc[i]
           
            LinksPerTerm.append(links)
  
        my_lst_str = ''.join(map(str, LinksPerTerm))
        mylist = my_lst_str.split (",")
       
        dictPerPhrase = Counter(mylist) #Counts the occurences of each element
       
        for link, freq in dictPerPhrase.items(): 
            if any(x in link for x in RESERVED): #check for wiki and gov 
                
                dfObj = dfObj.append({'Related Terms': phrase, 'Outbound Links': link}, ignore_index=True)
              
            elif (freq == 2):
                dfObj = dfObj.append({'Related Terms': phrase, 'Outbound Links': link}, ignore_index=True)

    #print(dfObj)
    #dfObj.drop_duplicates(subset ="Related Terms", keep = 'first' , inplace = True) #removing duplicates (Keeping first occurance)  
    result= dfObj.append(reservedRecords, ignore_index = True, sort=False) 
    
    result = result[result['Outbound Links'].str.contains('http')]   
    result.to_csv("Result.csv",encoding='utf-8-sig', index=False, header=True)
if __name__ == '__main__':
    #scrapeURLS("output.csv")
    calculateOutboundLinks()