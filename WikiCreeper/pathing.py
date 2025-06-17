'''Methods for pathing through graph'''

from collections import deque
from scraping import scrape_page, scrape_page_in_memory
import tools, database_tools
from time import time
import threading, os
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

CONFIG = tools.initialize_configs()

def bfs(start_page: str, goal_page: str, update: bool = False, defer: bool = True, sleep_timer: float = 0.01, debug: bool = False) -> list:
    global CONFIG

    conn = database_tools.create_connection()

    queue = deque([start_page])
    parents = {start_page: None}

    print(f"Pathing from {start_page} to {goal_page}")

    try:
        while queue:
            pop = queue.popleft()
            if debug:
                print(f"Visiting: {pop}")

            if pop == goal_page:

                path = []
                while pop:
                    path.append(pop)
                    pop = parents[pop]
                return path[::-1] 

            links, new_flag = scrape_page(CONFIG, conn, pop, update=update, defer=defer, sleep_timer=sleep_timer, debug=debug)

            if links:
                if new_flag: 
                    database_tools.insert_page(pop, links, conn, debug)
                for link in links:
                    if link not in parents:
                        queue.append(link)
                        parents[link] = pop
        return []
    except KeyboardInterrupt:

        raise
    
def bfs_in_memory(start_page: str, goal_page: str, update: bool = False, defer: bool = True, sleep_timer: float = 0.01, debug: bool = False) -> list:
    global  CONFIG

    graph = database_tools.make_dict()
    print(f"Data loaded to memory")
    conn = database_tools.create_connection()

    queue = deque([start_page])
    parents = {start_page: None}

    print(f"Pathing from {start_page} to {goal_page}")

    try:
        while queue:
            pop = queue.popleft()
            if debug:
                print(f"Visiting: {pop}")

            if pop == goal_page:

                path = []
                while pop:
                    path.append(pop)
                    pop = parents[pop]
                return path[::-1] 

            links, new_flag = scrape_page_in_memory(CONFIG, graph, pop, update=update, defer=defer, sleep_timer=sleep_timer, debug=debug)

            if links:
                if new_flag: 
                    database_tools.insert_page(pop, links, conn, debug)
                for link in links:
                    if link not in parents:
                        queue.append(link)
                        parents[link] = pop
        return []
    except KeyboardInterrupt:
        raise

def bfs_in_memory_with_threading(start_page: str, goal_page: str, update: bool = False, defer: bool = True, sleep_timer: float = 0.01, debug: bool = False, max_workers: int = 4) -> list:
    global CONFIG

    graph = database_tools.make_dict()
    print("Data loaded to memory")
    conn = database_tools.create_connection()

    seen = set()

    queue = Queue()
    queue.put(start_page)
    parents = {start_page: None}
    sql_lock = threading.Lock()

    print(f"Pathing from {start_page} to {goal_page} using {max_workers} threads")

    def process_page():
        while not queue.empty():
            pop = queue.get()

            if debug:
                print(f"Visiting: {pop}")

            if pop == goal_page:
                # Reconstruct the path
                path = []
                while pop:
                    path.append(pop)
                    pop = parents[pop]
                return path[::-1]

            links, new_flag = scrape_page_in_memory(CONFIG, graph, pop, update=update, defer=defer, sleep_timer=sleep_timer, debug=debug)

            if links:
                with sql_lock:  # Ensure safe update to shared resources
                    if new_flag:
                        database_tools.insert_page(pop, links, conn, debug)
                for link in links:
                    if link not in seen and link not in parents:
                        seen.add(link)
                        queue.put(link)
                        parents[link] = pop

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Use a pool of threads to process the queue
            futures = [executor.submit(process_page) for _ in range(max_workers)]
            for future in futures:
                result = future.result()
                if result:  # If any thread finds the goal, return the path
                    return result
        return []
    except KeyboardInterrupt:
        raise
    finally:
        conn.close()

def optimal_worker_count():
    cpu_cores = os.cpu_count()
    return cpu_cores * 2 if cpu_cores else 4

def metric_test(start_page: str, goal_page: str, worker_range: list):
    database_tools.database_analysis()
    for item in worker_range:
        try:
            print('----------------------------------------------------------')
            print('Begin Timer')
            start_time = time()
            result = bfs_in_memory_with_threading(start_page, goal_page, max_workers=item)
            print(f"Found with {item} workers: {result}")  # Or a more meaningful result
            print(f"Found in {tools.display_time(time() - start_time)} Seconds")
        except Exception as e:
            print(f"Error with {item} workers: {e}")


 



