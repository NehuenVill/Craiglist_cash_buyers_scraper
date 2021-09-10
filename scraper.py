import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import time

#set variables:
total_output = []

#function to get the URL ready to search for:
def get_url(term, results):

    if results == 0:

        base_url = 'https://newyork.craigslist.org/search/hhh?&query='

        nterm = term.replace(' ', '+')

        URL = base_url+nterm+'&availabilityMode=0&sale_date=all+dates'

        get_html(URL, True, nterm)

    elif results > 120:

        pags = math.floor(results/120) + 1

        cont = 0

        for i in range(pags):

            base_url = 'https://newyork.craigslist.org/search/hhh?'+'s=%s' % (cont) +'&query='

            nterm = term.replace(' ', '+')

            URL = base_url+nterm+'&availabilityMode=0&sale_date=all+dates'

            print("getting %s  ..." % (URL))

            get_html(URL, False, nterm)            

            cont+=120

    else:

        base_url = 'https://newyork.craigslist.org/search/hhh?&query='

        nterm = term.replace(' ', '+')

        URL = base_url+nterm+'&availabilityMode=0&sale_date=all+dates'

        print("getting %s  ..." % (URL))

        get_html(URL, False, nterm)

#function to get the HTML respose:
def get_html(url, cond, term):

    if cond:

        req = requests.get(url).text

        soup = BeautifulSoup(req, 'html.parser')

        time.sleep(2)

        results = int(soup.find('span', class_ = 'totalcount').text)

        get_url(term, results)

    else:
        
        req = requests.get(url).text

        soup = BeautifulSoup(req, 'html.parser')

        time.sleep(2)
        
        parse(soup)


#function to parse the HTML:
def parse(soup):

    cards = soup.find_all('li', class_='result-row')

    PT = ['we buy', 'WE BUY', 'cash buyers', 'CASH', 'CASH BUYER', 'CASH BUYERS', 'cash buyer']

    #iterate through all the results: 

    for i in cards:

        time.sleep(2)

        title = i.find('a', class_='result-title hdrlnk').text

        #if there's any coincidence of the common terms in the title get into that result's URL: 

        if PT[0] in title or PT[1] in title or PT[2] in title or PT[3] in title or PT[4] in title or PT[5] in title or PT[6] in title:

            time.sleep(0.5)

            title_link = i.find('a', class_='result-title hdrlnk')

            link = title_link['href']

            req = requests.get(link).text

            print('getting info from %s' % (link))

            soup = BeautifulSoup(req, 'html.parser')

            time.sleep(0.5)

            try:

                img_gall = soup.find('div', class_= 'swipe-wrap')

                print(img_gall)

                imgs = img_gall.find_all('a', class_ = 'thumbs')

                print(imgs)

                imgs_links = ''

                for i in imgs:

                    imgs_links += ', ' + i['href']

                print(imgs_links)

                if len(imgs_links) == 0:

                    imgs = img_gall.find_all('img')

                    print(imgs)

                    for i in imgs:

                        imgs_links += ', ' + i['src']

                    print(imgs_links)

            except:

                imgs_links = "---No images---"

            raw_Info = soup.find('section', {'id' : 'postingbody'}).text

            Raw_info = raw_Info.replace('\n', '-----')
            info =  Raw_info.replace('QR Code Link to This Post', '')

            #sort the results into a json output:

            output = {

                'Link': link,

                'Title': soup.find('span', id = 'titletextonly').text,

                'Info': info,

                'Images links': imgs_links,

            }

            print('data retrieved: %s' % (output))

            time.sleep(0.5)

            total_output.append(output)

            time.sleep(0.5)

        else:

            pass

#function to save the results in an excel file:
def save(OP):

    print('saving data...')

    df = pd.DataFrame(OP, columns= ["Link", "Title", "Info", "Images links"])
    df.to_excel('CASH_BUYERS.xls', index= True, columns= ["Link", "Title", "Info", "Images links"])
    
get_url('we buy', 0)

save(total_output)

