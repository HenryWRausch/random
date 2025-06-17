import sqlite3, tools, os, scraping
from collections import Counter

CONFIG = tools.initialize_configs()

def create_table(database_name: str = CONFIG['database_file']):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS pages (
            page_name VARCHAR PRIMARY KEY,
            links STRING
        );
        """

        cursor.execute(create_table_query)

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def populate_from_csv(database_name: str = CONFIG['database_file'], csv_source: str = CONFIG['master_memory']):
    csv_source = tools.read_file()
    for key in csv_source.keys():
        insert_page(key, csv_source[key], database_name)

def pack_list(lst: list) -> str:
    return '|'.join(str(item) for item in lst)

def unpack_list(string: str) -> list[str]:
    list_ = [item for item in string.split('|') if item]

    return list_
    
def insert_page(page_name: str, links: list, connection, debug:bool = False) -> None:
    insert_query = "INSERT OR REPLACE INTO pages (page_name, links) VALUES (?, ?);"
    try:
        links_packed = pack_list(links)

        cursor = connection.cursor()

        cursor.execute(insert_query, (page_name, links_packed))

        connection.commit()
        if debug:
            print(f"Inserted {page_name} and {len(links)} links successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def retrieve_links(page_name: str, connection) -> list:
    try:
        cursor = connection.cursor()
        select_query = '''
        SELECT links
        FROM pages
        WHERE page_name = ?;
        '''

        cursor.execute(select_query, (page_name,))
        
        links_packed = cursor.fetchone()[0]
        links = unpack_list(links_packed)

        return links

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def create_connection(database_name: str = CONFIG['database_file']):
    try:
        conn = sqlite3.connect(database_name, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def database_analysis(database_name: str = CONFIG['database_file']) -> dict:
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        data = {}

        get_size = 'SELECT COUNT(*) FROM pages;'
        cursor.execute(get_size)
        data['count'] = cursor.fetchone()[0]

        bytes = os.path.getsize(database_name)

        data['file_size_b'] = bytes
        data['file_size_kb'] = bytes / 1024
        data['file_size_mb'] = bytes / (1024 * 1024)
        data['file_size_gb'] = bytes / (1024 * 1024 * 1024)

        print(f"File size: {int(data['file_size_kb'])} KB")
        print(f"File size: {data['file_size_mb']:0.2f} MB")
        print(f"File size: {data['file_size_gb']:0.2f} GB")

        print(f"{data['count']} entries")

        return data


    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def adv_database_analysis(database_name: str = CONFIG['database_file'], verbose: bool = True) -> dict:
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        data = {}

        get_size = 'SELECT COUNT(*) FROM pages;'
        cursor.execute(get_size)
        data['count'] = cursor.fetchone()[0]

        get_links = 'SELECT links FROM pages;'
        get_paired_page = 'SELECT page_name FROM pages WHERE links = ?'
        cursor.execute(get_links)
        links_unique = set()
        links =[]
        data['most_links'] =('', 0)
        all_links = cursor.fetchall()
        for string in all_links:
            help_links = unpack_list(string[0])
            links.extend(help_links)
            links_unique.update(help_links)
            if len(help_links) > data['most_links'][1]:
                cursor.execute(get_paired_page, (string[0],))
                data['most_links'] = (cursor.fetchone()[0], len(help_links))

        data['visits'] = len(links_unique)
        data['average_links'] = len(links) / data['count']

        counter = Counter(links)
        data['most_common'] = counter.most_common(1)[0]

        bytes = os.path.getsize(database_name)

        data['file_size_b'] = bytes
        data['file_size_kb'] = bytes / 1024
        data['file_size_mb'] = bytes / (1024 * 1024)
        data['file_size_gb'] = bytes / (1024 * 1024 * 1024)

        if verbose:
            print(f"File size: {int(data['file_size_kb'])} KB")
            print(f"File size: {data['file_size_mb']:0.2f} MB")
            print(f"File size: {data['file_size_gb']:0.2f} GB")
            print(f'----------------------------------------------------')
            print(f"{data['count']} entries fully logged")
            print(f"{data['visits']} pages have been seen on other pages")
            print(f'----------------------------------------------------')
            print(f"The average page has {data['average_links']:0.2f} links")
            print(f"The page with the most links is {data['most_links'][0]} with {data['most_links'][1]} links")
            print(f"The most visited page is {data['most_common'][0]} with {data['most_common'][1]} links to it")
        return data

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

def make_dict(database_name: str = CONFIG['database_file']) -> None:
    graph = {}
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        select = "SELECT * FROM pages;"
        cursor.execute(select)

        for item in cursor.fetchall():
            graph[item[0]] = unpack_list(item[1])
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally: 
        conn.close()
        return graph
        
adv_database_analysis()