import requests, sqlite3, time, bs4, flatten

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ADDRESS_STUB = 'https://www.hockey-reference.com/players/'
DATABASE = 'database.db'
conn = sqlite3.connect(DATABASE)
DELAY = 3 # Delay in seconds to match 20 requests/min

for letter in ALPHABET:
    address = f'{ADDRESS_STUB}{letter}/'

    try:
        request = requests.get(address)
        if request.status_code == 200:
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
    except Exception as e:
        print(f'An unexpected error occured and {letter} could not be handled: {e}')

    for tag in soup.find_all('p', class_ = 'nhl'):
        href = tag.find('a')['href']  # "/players/a/aaltoan01.html"
        reference_id = href.split('/')[-1].replace('.html', '')

        tag_split = tag.text.split(' ')

        name = f'{tag_split[0]} {tag_split[1]}'.encode('utf-8') # Separates first and last name
        name_flat = flatten.flatten(f'{tag_split[0]} {tag_split[1]}') # Flattens diacritics

        hof = 1 if tag.find('*') else 0     # This would work but they don't actually
                                                                     # Correctly tag HOFers

        position = tag_split[-1].strip(')')

        years = tag_split[-2].strip('(').replace(',', '').split('-')
        first_year = years[0]
        last_year = years[1]

        insert = '''
        INSERT INTO Player_List (reference_id, name, name_flat, position, first_year, last_year, hof)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''

        try:
            conn.execute(insert, (reference_id, name, name_flat, position, first_year, last_year, hof))
            conn.commit()
            print(f'{name_flat} added to the database under id {reference_id}')
        except sqlite3.IntegrityError as e:
            print(f"Error: IntegrityError occurred, {name_flat} is already in the database with id {reference_id}: {e}")
        except Exception as e:
            print(f'An unexpected error occured: {e}')

    time.sleep(DELAY)