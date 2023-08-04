import requests, logging, re
from bs4 import BeautifulSoup
from cachetools import cached, LRUCache, TTLCache

#define logger
logging.basicConfig(filename='app.log',filemode='a',format='%(asctime)s - %(filename)s / %(funcName)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S' ,level=logging.ERROR)

def remove_non_numeric_parentheses(string_val):
    if "("  in string_val:
        #Check for parentheses with non numeric values
        reg_ex_pattern = r'\([^0-9]*' 
        match = re.search(reg_ex_pattern,string_val)

        if match is not None:
            first_occurrence_index = match.start()
            filtered_val = string_val[0:first_occurrence_index] #get substring that will return the val w/o the parentheses
            return filtered_val.strip()
    else:
        return string_val.strip()
    
# cache anime list data for no longer than 4hrs
@cached(cache=TTLCache(maxsize=16, ttl=14400))
def get_anime_list():
    anime_list = []
    url = 'https://www.animefillerlist.com/shows/'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content,'html.parser')
            show_list = soup.find_all("div", id = "ShowList")
            soupTwo = BeautifulSoup(str(show_list),'html.parser')
            show_groups = soupTwo.find_all("div", class_="Group")

            for group in show_groups:
                show_name_list = group.select('li')
                for show in show_name_list:
                    show_name = show.select_one('a').get_text()
                    show_link = show.select_one('a')['href']
            
                    anime_dict = {'show_name': show_name,'link': show_link}
                    anime_list.append(anime_dict)
            return anime_list
        except Exception as e:
            logging.exception("Exception occurred")
    else:
        logging.error(f'Url error. We received the following response code: {response.status_code}')

 
def get_filler_eps(anime_name):
    filler_eps = []
    url = 'https://www.animefillerlist.com/'
    #request
    response = requests.get(url + anime_name + '/')
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content,'html.parser')

            filler_even = soup.find_all("tr", class_ = "filler even")
            filler_odd = soup.find_all("tr", class_ = "filler odd")
    
            #gather and order filler eps
            for filler in filler_even:
                ep_num = filler.select('td.Number')[0].get_text()
                filler_eps.append(int(ep_num))

            for filler in filler_odd:
                ep_num = filler.select('td.Number')[0].get_text()
                filler_eps.append(int(ep_num))
            
            filler_eps.sort()
            return  filler_eps
        except Exception as e:
            logging.exception("Exception occurred")  
    else:
        logging.error(f'Url error. We received the following response code: {response.status_code}')

# cache non filler eps data for no longer than 4hrs
@cached(cache=TTLCache(maxsize=16, ttl=14400))
def get_nonfiller_eps(anime_name):
    non_filler_eps = []
    url = 'https://www.animefillerlist.com/'
    #request
    response = requests.get(url + anime_name + '/')
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content,'html.parser')

            manga_canon_even = soup.find_all("tr", class_ = "manga_canon even")
            manga_canon_odd = soup.find_all("tr", class_ = "manga_canon odd")
            anime_canon_even = soup.find_all("tr", class_ = "anime_canon even")
            anime_canon_odd = soup.find_all("tr", class_ = "anime_canon odd")
            mixed_canon_even = soup.find_all("tr", class_ = "mixed_canon/filler even")
            mixed_canon_odd = soup.find_all("tr", class_ = "mixed_canon/filler odd")

            #gather and order non filler eps
            for canon in manga_canon_even:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))

            for canon in manga_canon_odd:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))

            for canon in anime_canon_even:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))

            for canon in anime_canon_odd:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))
            
            for canon in mixed_canon_even:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))

            for canon in mixed_canon_odd:
                ep_num = canon.select('td.Number')[0].get_text()
                non_filler_eps.append(int(ep_num))          
            
            non_filler_eps.sort()
            return non_filler_eps
        except Exception as e:
            logging.exception("Exception occurred")  
    else:
       logging.error(f'Url error. We received the following response code: {response.status_code}') 

