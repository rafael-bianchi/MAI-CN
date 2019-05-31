
#%%
import requests 
from bs4 import BeautifulSoup
import pandas
import re
import datetime


#%%
base_url = 'https://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?Pagina=**PAGENUMBER**&dt_inicial=11%2F04%2F1960&dt_final=11%2F04%2F2019&parlamentar=&filiacaoPartidaria=1&ordenarPor=2&Pesquisar=Pesquisar'
regexPattern = re.compile(r'(?P<MovDate>(?P<Day>\d{1,2})/(?P<Month>\d{1,2})/(?P<Year>(?:\d{4}|\d{2})))\s*-\s*Comunicação\s*de\s*Mudança\s*de\s*Partido:\s*do\s*(?P<PartyFrom>.*)\s+para\s+o\s+(?P<PartyTo>.*)(:?\(\))')


#%%
r = requests.get(base_url.replace('**PAGENUMBER**', '1'))
c = r.content


#%%
soup = BeautifulSoup(c,"html.parser")


#%%
paging = soup.find("div",{"class":"listingBar"}).find_all("a")
start_page = 1#paging[1].text
last_page = paging[len(paging)-1].text


#%%
print ( f'First page:{start_page} and last page:{last_page}')


#%%
deputiesMovements = []
#last_page = 2
for page_number in range(int(start_page),int(last_page) + 1):
    i = i + 1
    # To form the url based on page numbers
    url = base_url.replace('**PAGENUMBER**', f'{page_number}')
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    
    deputiesPanels = soup.find("div",{"id":"content"}).find_all("div",{"class":"panel panel-default"})
    
    for deputy in deputiesPanels:
        i = i + 1
        depName = deputy.find("h4", {"class":"panel-heading"}).find("a").text
                
        depName = None
        depMovements = None
        
        depName = deputy.find("h4", {"class":"panel-heading"})                                   .find("a").text

        depMovements = []
        depMovementsLi = deputy.find("div", {"class":"panel-body"})                                      .find("ul")                                      .find_all("li")

        for movLi in depMovementsLi: 
            for m in re.finditer(regexPattern, movLi.text.strip()):
                movDic = {}
                movDic['Date'] = datetime.date(int(m.group('Year')), int(m.group('Month')), int(m.group('Day'))) 
                movDic['From'] = m.group('PartyFrom')
                movDic['To'] = m.group('PartyTo')
                depMovements.append(movDic)

        depDic ={}
        depDic['Name'] = depName
        depDic['Movements'] = depMovements
        depDic['MovementsCount'] = len(depMovements)
        deputiesMovements.append(depDic)

        # To make a dataframe with the list
df = pandas.DataFrame(deputiesMovements)

# To write the dataframe to a csv file
#df.to_csv("Output2.csv")


#%%
df.sort_values("MovementsCount", axis = 0, ascending = False, 
                 inplace = True, na_position ='last') 


#%%
df


