#! python3
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import webbrowser
import re
from datetime import datetime
import time
#----------------------------------------------------------------------

main_link = 'https://www.telemagazyn.pl/'
links = []
contents = []
shows = []

with open('progs.txt', 'r') as progs:
    links = [main_link + prog.rstrip() for prog in progs.readlines()]

class TvShow:
    def __init__(self, title, time, info, canal):
        self.title = title
        self.time = time
        self.info = info
        self.canal = canal

class teleSoup:
    def __init__(self, main_link, links, contents, shows):
        self.main_link = main_link
        self.links = links
        self.contents = contents
        self.shows = shows


#---- Uzupełnia listę 'contents' danymi dla BeautifulSoup
    def make_content(self):
        for link in self.links:
            source = requests.get(link).text
            content = BeautifulSoup(source, features='html.parser')
            contents.append(content)
            print(f'Content for {link[27:]} made successfully.')
            return self.main_menu()



# ---- Znajduje każdy program (kanał, tytuł, godzinę i opis) i przypisuje go do klasy TvShow
    def get_day(self):
        canalRegex = re.compile(r'^[^-]*[^ -]')
        for soup in self.contents:
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

                    self.shows.append(TvShow(title_var, time_var, info_var, canal_var))
        print('getday succesful')

    def show_everything(self):
        startTime = time.time()
        for show in shows:
            print(f'{show.canal} - {show.time} - {show.title}')
        endTime = time.time()
        print('Took %s seconds to get this data.' % (endTime - startTime)) 

    def main_menu(self):
        print('------ T E L E S O U P -----')
        input('\n\n Press ENTER to start collecting data...')
        return self.make_content()

  
    def main(self):
        self.make_content()
        self.get_day()
        self.show_everything()


#---- Podaje program dla określonego kanału
def show_canal(canal):
    print(f'Program dla {canal} na dziś: \n')
    for show in shows:
        if show.canal == canal:
            print(str(show.time) + ' ' + show.title)

#---- Run:

run = teleSoup(main_link, links, contents, shows)

if __name__ == '__main__':
    run.main()


