'''Script for creation of the database if the file does not already exist'''

import sqlite3, json
from pathlib import Path

# Load config for database location
try:
    with open('config.json', 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    print("Error: config.json file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: config.json is not a valid JSON file.")
    exit(1)

# Check if the database file exists
file_path = Path(config["database_name"])
if file_path.exists():
    print(f'{file_path} already exists, skipping creation')
else:
    tables = [
        # traits
        '''
        CREATE TABLE traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species INTEGER NOT NULL,
            FOREIGN KEY (species) REFERENCES species(id) ON DELETE CASCADE
                CONSTRAINT fk_traits_species
        );
        ''',

        # trait_variants
        '''
        CREATE TABLE trait_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phenotype_expression TEXT NOT NULL,
            allele_expression TEXT NOT NULL,
            is_dominant INTEGER NOT NULL,
            trait INTEGER NOT NULL,
            co_dominance INTEGER,
            FOREIGN KEY (trait) REFERENCES traits(id) ON DELETE CASCADE
                CONSTRAINT fk_trait_variants_traits,
            FOREIGN KEY (co_dominance) REFERENCES trait_variants(id) ON DELETE SET NULL
                CONSTRAINT fk_trait_variants_trait_variants
        );
        ''',

        # species
        '''
        CREATE TABLE species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scientific_name TEXT UNIQUE,
            name TEXT
        );
        ''',

        # specimens
        '''
        CREATE TABLE specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            genotype TEXT NOT NULL,
            species INTEGER NOT NULL,
            parent_a INTEGER,
            parent_b INTEGER,
            FOREIGN KEY (species) REFERENCES species(id) ON DELETE CASCADE
                CONSTRAINT fk_specimens_species,
            FOREIGN KEY (parent_a) REFERENCES specimens(id) ON DELETE SET NULL
                CONSTRAINT fk_specimens_specimens_a,
            FOREIGN KEY (parent_b) REFERENCES specimens(id) ON DELETE SET NULL
                CONSTRAINT fk_specimens_specimens_b
        );
        '''
    ]

    # Create the database and tables
    try:
        conn = sqlite3.connect(config["database_name"])
        cursor = conn.cursor()

        for table in tables:
            cursor.execute(table)

        # Commit changes and close the connection
        conn.commit()
        print(f'{file_path} created with all tables')
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()


