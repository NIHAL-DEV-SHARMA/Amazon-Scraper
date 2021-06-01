from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

class Scraper:
    
    def __init__(self , driver ,search_term , pages ,name_of_file='amazon-scarped-data'):
        self.search_term = search_term
        self.driver = driver
        self.pages = pages
        self.url_template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2f' 
        self.name_of_file = name_of_file
        
    def get_url(self , search):
        search = search.replace(' ' , '+')
        self.url = self.url_template.format(search)
        self.url += '&page={}'

    @staticmethod
    def card_data(card):
        atag = card.h2.a
        
        # link of the  card
        link = 'https://www.amazon.in' + atag.get('href')
        
        # tittle of the card
        tittle = atag.text.strip()
        
        # price of the card
        try:
            price_parent = card.find('span','a-price')
            price = price_parent.find('span','a-offscreen').text
        except AttributeError:
            return

        # rating of the card
        try:
            rating = card.find('span','a-icon-alt').text
        except AttributeError:
            return
        
        #returning the data
        results = (tittle,price,rating,link)
        return results
    
    
    def data_of_cards(self):
        cards_data = []
        search_term = self.search_term
        self.get_url(search_term)
        
        for page in range(0,self.pages):            
            self.driver.get(self.url.format(page))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            cards = soup.find_all('div',{'data-component-type' :'s-search-result'})

            for card in cards:
                record = self.card_data(card)
                if record:
                    cards_data.append(record)
        self.driver.close()
        
        # saving the data into csv file
        with open(f'{self.name_of_file}.csv','w',newline='',encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['tittle','price','rating','link'])
            writer.writerows(cards_data)

# I am using brave you are free to user chrome , firefox i dont care

driver_path = "driver/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

userSearch = input('Enter your search item: ')
userPage = int(input('Enter how many page of data you want: '))
userFileName = input('Enter your name of file: ')

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito")

driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

# start time
start_time = time.time()

scraper = Scraper(driver , userSearch , userPage , userFileName)
scraper.data_of_cards()

print('\nScraped data successfuly!\n')
print(f"Total time taken by scraping is {time.time()-start_time}")
