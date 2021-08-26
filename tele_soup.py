#! python3
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import webbrowser
import re
from datetime import datetime
import time
#----------------------------------------------------------------------


class TvShow:
    def __init__(self, title, time, info, canal):
        self.title = title
        self.time = time
        self.info = info
        self.canal = canal


links = ['https://www.telemagazyn.pl/fokus_tv', 'https://www.telemagazyn.pl/tvp_historia', 'https://www.telemagazyn.pl/ttv/',
         'https://www.telemagazyn.pl/stopklatka/', 'https://www.telemagazyn.pl/discovery/', 'https://www.telemagazyn.pl/discovery_science/',
         'https://www.telemagazyn.pl/discovery_historia/', 'https://www.telemagazyn.pl/discovery_life/', 'https://www.telemagazyn.pl/national_geographic/',
         'https://www.telemagazyn.pl/nat_geo_wild/', 'https://www.telemagazyn.pl/history/', 'https://www.telemagazyn.pl/nat_geo_people/',
         'https://www.telemagazyn.pl/animal_planete_hd/', 'https://www.telemagazyn.pl/polsat_doku/', 'https://www.telemagazyn.pl/polsat_viasat_history/',
         'https://www.telemagazyn.pl/polsat_viasat_nature/', 'https://www.telemagazyn.pl/polsat_viasat_explorer/',
         'https://www.telemagazyn.pl/crime_investigation_network_polsat/', 'https://www.telemagazyn.pl/bbc_earth/', 'https://www.telemagazyn.pl/bbc_lifestyle/',
         'https://www.telemagazyn.pl/bbc_brit/', 'https://www.telemagazyn.pl/water_planet/']

contents = []
shows = []


#---- Uzupełnia listę 'contents' danymi dla BeautifulSoup
def makeContent():
    for link in links:
        source = requests.get(link).text
        content = BeautifulSoup(source, features='html.parser')
        contents.append(content)


# ---- Znajduje każdy program (kanał, tytuł, godzinę i opis) i przypisuje go do klasy TvShow
def showDay():
    canalRegex = re.compile(r'^[^-]*[^ -]')
    for soup in contents:
        mo = canalRegex.search(soup.title.text)
        canal_var = mo.group()  # canal
        for div in soup.find_all("div", class_='lista'):
            for li_tag in div.find_all('li'):
                for span in li_tag.find_all('span'):  # title
                    title_var = span.text
                for em_tag in li_tag.find_all('em'):  # time
                    time_obj = datetime.strptime(
                        em_tag.text, ' %H:%M ').time()  # time object
                    time_var = time_obj
                for p_tag in li_tag.find_all('p'):  # info
                    if 'Odcinek: ' in p_tag.text:
                        pass
                    else:
                        info_var = p_tag.text

                shows.append(TvShow(title_var, time_var, info_var, canal_var))


#---- Podaje program dla określonego kanału
def showCanal(canal):
    print(f'Program dla {canal} na dziś: \n')
    for show in shows:
        if show.canal == canal:
            print(str(show.time) + ' ' + show.title)

# def show3hrs(canal):
#     for show in shows:
#         if show.time


#---- Run:
startTime = time.time()

makeContent()
#showDay()
#showCanal('Viasat Nature HD')
for show in shows:
    print(f'{show.canal} - {show.time} - {show.title}')
endTime = time.time()
print('Took %s seconds to get this data.' % (endTime - startTime))
