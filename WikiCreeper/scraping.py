'''Methods for scraping actual data from wikipedia'''

from requests import get
from bs4 import BeautifulSoup # type: ignore
import tools, database_tools
from time import sleep

def scrape_page(CONFIG: dict, conn, page: str, defer: bool = True, update: bool = False, sleep_timer: float = 0.01, debug: bool = False, ) -> tuple[list, bool]: 
    '''Return list of links on page'''
    sleep(sleep_timer)

    base_url = 'https://en.wikipedia.org/wiki/'

    if defer: 
        try:
            #links = graph[page]
            links = database_tools.retrieve_links(page, conn)
            if debug and links:
                print(f"Retrieved links from memory for {page}")
                return (links, False)
            elif debug: print(f"Requesting links from Wikipedia for {page}")
        except:
            if debug:
                print(f"Requesting links from Wikipedia for {page}")
            pass


    try:
        if page:
            full_url = base_url + page
            response = get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == 429:
                print("Oh we fucked up my bad wikipedia")
                quit()

            links = []

            for tag in soup.find_all('a', href=True):
                href = tag['href'] # /wiki/[link]
                if href.startswith('/wiki/') and ':' not in href and '#' not in href and "List_of_" not in href and "disambiguation" not in href: # links and not namespaces or lists
                    href = href[6:]
                    if href not in CONFIG['global_pages'] and href != page:
                        links.append(href)

            if links == ['Case_sensitivity']: 
                print(f"Page ({page}) does not exist")
                
            links = list(dict.fromkeys(links))
            if update:
                tools.write_file(page, links)
            #graph[page] = links
            return (links, True)

        else: raise ValueError
    except Exception as e:
        print(f"An error has occurred: {e}")

def scrape_page_in_memory(CONFIG: dict, graph: dict, page: str, defer: bool = True, update: bool = False, sleep_timer: float = 0.01, debug: bool = False, ) -> tuple[list, bool]: 
    '''Return list of links on page'''
    sleep(sleep_timer)

    base_url = 'https://en.wikipedia.org/wiki/'

    if defer: 
        try:
            links = graph[page]
            if links:
                if debug:
                    print(f"Retrieved links from memory for {page}")
                return (links, False)
            elif debug: print(f"Requesting links from Wikipedia for {page}")
        except:
            if debug:
                print(f"Requesting links from Wikipedia for {page}")
            pass


    try:
        if page:
            full_url = base_url + page
            response = get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == 429:
                print("Oh we fucked up my bad wikipedia")
                quit()

            links = []

            for tag in soup.find_all('a', href=True):
                href = tag['href'] # /wiki/[link]
                if href.startswith('/wiki/') and ':' not in href and '#' not in href and "List_of_" not in href and "disambiguation" not in href: # links and not namespaces or lists
                    href = href[6:]
                    if href not in CONFIG['global_pages'] and href != page:
                        links.append(href)

            if links == ['Case_sensitivity']: 
                print(f"Page ({page}) does not exist")
                
            links = list(dict.fromkeys(links))
            if update:
                tools.write_file(page, links)
            graph[page] = links
            return (links, True)

        else: raise ValueError
    except Exception as e:
        print(f"An error has occurred: {e}")

