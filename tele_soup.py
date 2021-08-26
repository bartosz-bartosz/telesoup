#! python3
import os
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
canals = []

with open('progs.txt', 'r') as progs:
    links = [main_link + prog.rstrip() for prog in progs.readlines()]

class TvShow:
    def __init__(self, title, time, info, canal):
        self.title = title
        self.time = time
        self.info = info
        self.canal = canal

class teleSoup:
    def __init__(self, main_link, links, contents, shows, canals):
        self.main_link = main_link
        self.links = links
        self.contents = contents
        self.shows = shows
        self.canals = canals


#---- Uzupełnia listę 'contents' danymi dla BeautifulSoup
    def make_content(self):
        startTime = time.time()
        for link in self.links:
            source = requests.get(link).text
            content = BeautifulSoup(source, features='html.parser')
            contents.append(content)
            print(f'Content for {link[27:]} made successfully.')
        endTime = time.time()
        print('Took %s seconds to get this data.' % (endTime - startTime))
        return self.get_day()

# ---- Znajduje każdy program (kanał, tytuł, godzinę i opis) i przypisuje go do klasy TvShow
    def get_day(self):
        canalRegex = re.compile(r'^[^-]*[^ -]')
        for soup in self.contents:
            mo = canalRegex.search(soup.title.text)
            canal_var = mo.group()  # canal
            for div in soup.find_all('div', class_='lista'):
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
            self.canals.append(canal_var)
        print('getday succesful')
        input('Press ENTER to go back to main menu...')
        return self.main_menu()

    def show_everything(self):
        for show in shows:
            print(f'{show.canal} - {show.time} - {show.title}')
        input('\n Press ENTER to go back to main menu')
        return self.main_menu()

    def show_canals(self):
        for canal in canals:
            print(str(canals.index(canal)) + ' - ' + canal)
        x = input('Type number of canal to show.')
        x=int(x)

        if x <= len(canals) and x >= 0:
            return self.show_single(x)
        else:
            return self.main_menu()

    def show_single(self, canal_index=1):
        for show in shows:
            if canals[canal_index] == show.canal:
                print(f'{show.canal} - {show.time} - {show.title}')

    def main_menu(self):
        os.system('cls')
        print('------ T E L E S O U P -----')
        if self.contents == []:

            print('\nNo data available.\n Collecting data...\n')
            return self.make_content()
        else:
            options = ['0', '1', '2']
            print('\nData collected.\n')
            print(r'''--- OPTIONS

                1 - View all available data
                2 - Show available canals
                0 - Exit''')

            choice = input('\nChoose option:')
            if choice not in options:
                return self.main_menu()
            elif choice == "0":
                return exit()
            elif choice == "1":
                return self.show_everything()
            elif choice == "2":
                return self.show_canals()

  
    def main(self):
        self.main_menu()


#---- Run:

run = teleSoup(main_link, links, contents, shows, canals)

if __name__ == '__main__':
    run.main()


