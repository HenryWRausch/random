'''Classes and methods'''

import sqlite3, time

class DBObject:

    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def create_connection(db_path, max_retries=5, initial_wait=1, max_wait=60):
        retries = 0
        conn = None

        while retries < max_retries:
            try:
                conn = sqlite3.connect(db_path)
                print("Connection established.")
                return conn
            except sqlite3.Error as e:
                print(f"SQLite error occurred: {e}")
                retries += 1
                wait_time = min(initial_wait * (2 ** (retries - 1)), max_wait)  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Wait before retrying

        print("Failed to establish connection after several attempts.")
        return None
    
    conn: sqlite3.Connection = create_connection("database.db")
    cursor: sqlite3.Cursor = conn.cursor()

    def close_connection(self):
        """Close the database connection gracefully."""
        if DBObject.conn:
            DBObject.conn.close()
            print("Connection closed.")

class Specimen(DBObject):
    def __init__(self, genotype: str, species: int, **kwargs):
        self.genotype = genotype
        self.species = species

        # Default to None if not passed
        self.name = kwargs.get('name', None)
        self.parent_a = kwargs.get('parent_a', None)
        self.parent_b = kwargs.get('parent_b', None)

    def add_to_database(self):
        query = '''
        INSERT INTO specimens (name, genotype, species, parent_a, parent_b)
        VALUES (?, ?, ?, ?, ?);
        '''

        DBObject.cursor.execute(query, (self.name, self.genotype, self.species, self.parent_a, self.parent_b))
        DBObject.conn.commit()

class Species(DBObject):
    pass

class Trait(DBObject):
    def get_id(self):
        query = '''
        SELECT id FROM trait 
        WHERE name = ?
        AND species = ?
        '''
        DBObject.cursor.execute(query, (self.trait_name, self.species))

class TraitVariant(DBObject):
    def __init__(self, phenotype_expression: str, allele_expression: str, is_dominant: bool, trait: Trait, co_dominance: "TraitVariant" = None):
        self.phenotype_expression = phenotype_expression
        self.allele_expression = allele_expression
        self.is_dominant = is_dominant
        self.trait = trait
        self.co_dominance = co_dominance

    def add_to_database(self):
        query = '''
        INSERT INTO trait_variants (phenotype_expression, allele_expression, is_dominant, trait, co_dominance)
        '''

'''
id INTEGER PRIMARY KEY AUTOINCREMENT,
phenotype_expression TEXT NOT NULL,
allele_expression TEXT NOT NULL,
is_dominant INTEGER NOT NULL,
trait INTEGER NOT NULL,
co_dominance INTEGER,
    '''