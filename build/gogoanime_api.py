import requests, json, logging
from datetime import datetime, timedelta
from cachetools import cached, LRUCache, TTLCache

#define logger
logging.basicConfig(filename='app.log',filemode='a',format='%(asctime)s - %(filename)s / %(funcName)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S' ,level=logging.ERROR)

base_url = "https://api.consumet.org/anime/gogoanime/"

# cache anime id data for no longer than 4hrs
@cached(cache=TTLCache(maxsize=16, ttl=14400))
def get_anime_id(anime_name, version = 'sub'):
    filtered_results = []
    url = base_url + str(anime_name)
    response = requests.get(url, params={"page": 1})
    if response.status_code == 200:
        try:
            data = response.json()

            #parse json for sub or dub result
            for result in  data['results']:
                if result['subOrDub'] == version:
                    filtered_results.append(result)
            return filtered_results[0]['id']
        except Exception as e:
            logging.exception("Exception Occurred")
    else:
        logging.error(f'Url error. We received the following response code: {response.status_code}')

def get_all_canon_eps_links(anime_id, canon_eps_list):
    canon_eps_links = []
    if len(canon_eps_list) > 0:
        for ep in canon_eps_list:
            url = base_url + "watch/" + anime_id + "-episode-" + str(ep) 
            response = requests.get(url, params={"server": "vidstreaming"})  
            if response.status_code == 200:
                try:
                    data = response.json()
                    for result in data['sources']:
                        if result['quality'] == 'default':
                            canon_eps_links.append({"episode" : str(ep) , "link": result['url']})
                    return canon_eps_links
                except Exception as e:
                    logging.exception("Exception Occurred")
            else:
                logging.error(f'Url error. We received the following response code: {response.status_code}')

# cache ep link data for no longer than 4hrs
@cached(cache=TTLCache(maxsize=16, ttl=14400))         
def get_ep_link(anime_id, episode):
    ep_link = []
    url = base_url + "watch/" + anime_id + "-episode-" + str(episode) 
    response = requests.get(url, params={"server": "vidstreaming"})   
    if response.status_code == 200:
        try:
            data = response.json()
            for result in data['headers']:
                ep_link.append({ "episode" : episode, "link" : data['headers']['Referer']})
            return ep_link
        except Exception as e:
            logging.exception("Exception Occurred")
    else:
        logging.error(f'Url error. We received the following response code: {response.status_code}')

def get_anime_info(anime_id):
    url = "https://api.consumet.org/anime/gogoanime/info/" + anime_id
    response = requests.get(url)
    if response.status_code == 200:
        try:
            anime_info = response.json()
            return(anime_info)
        except Exception as e:
            logging.exception("Exception Occurred")
    else:
        logging.error(f'Url error. We received the following response code: {response.status_code}')
