'''Tools for graph memory and storage'''

import json, os, re

def initialize_configs(config_file: str = 'config.json') -> dict:
    """Initialize configuration from a JSON file."""
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON in configuration file: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred: {e}")

CONFIG = initialize_configs()

def write_file(page: str, data: list[str]) -> None:
    try:
        file_name = f"{CONFIG['memory']}\{page}.lnk"
        with open(file_name, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(item + '\n')
        print(f"File successfully written to {file_name}")
    except Exception as e:
        print(f"An error occurred while writing {page}: {e}")

def generate_map(path: str = CONFIG['memory']) -> dict:
    map = {}
    for filename in os.listdir(path):
        try:
            file_path = os.path.join(path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                filename = filename[:-4]
                data = file.readlines()
                data = [link.rstrip() for link in data]
                map[filename] = data
        except Exception as e:
            print(f"An error has occurred: {e}")
    
    return map

MAP = {}

def log_map() -> None:
    global MAP

    for key in MAP.keys():
        write_file(key, MAP[key])

def folder_to_file(path: str = CONFIG['memory']) -> None:
    global CONFIG
    graph = generate_map(path)

    with open(CONFIG['master_memory'], 'w', encoding='utf-8') as file:
        for line in graph.keys():
            file.write(f"{line}, {graph[line]}\n")

def map_to_file(graph: dict = None, dest: str = None) -> None:
    graph = graph or MAP
    dest = dest or CONFIG['master_memory']
    with open(dest, 'w', encoding='utf-8') as file:
        for line in graph.keys():
            file.write(f"{line}, {graph[line]}\n")


def read_file(path: str = CONFIG['master_memory']) -> dict:
    map = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            key = line.split(',')[0]
            try:
                data = [item.replace('\\', '') for item in re.findall(r"'(.*?)'", line)]
            except:
                data = []
            map[key] = data
            
    return map

def display_time(seconds:float) -> str:
    hour = int(seconds // 3600)
    minute = int((seconds % 3600) // 60)
    second = seconds % 60

    return f"{hour}h {minute}m {second:0.2f}s"
