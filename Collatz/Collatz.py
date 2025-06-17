'''Fun with Collatz Conjecture demo, with the intent of using no preconstructed algorithms'''

SOLVED_LIST = []

def merge_sort(target: list) -> list:
    '''Sorts a list in ascending order using the merge sort algorithm.
    
    Args:
        target (list): The list to sort.
    
    Returns:
        list: A new sorted list.
    
    Raises:
        ValueError: If the input list is None.
    '''
    def merge(left: list, right: list) -> list:
        '''Merges two sorted lists into a single sorted list.
        
        Args:
            left (list): A sorted list.
            right (list): Another sorted list.
        
        Returns:
            list: A merged sorted list.
        '''
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result

    if target is None:
        raise ValueError("List to sort must not be None")
    
    if len(target) <= 1:
        return target
    
    mid_point = len(target) // 2
    left = merge_sort(target[:mid_point])
    right = merge_sort(target[mid_point:])

    return merge(left, right)


def find_in_sorted(search_pool: list, search_piece) -> int:
    '''Finds the index of a given element in a sorted list using binary search.
    
    Args:
        search_pool (list): The sorted list to search.
        search_piece: The element to find.
    
    Returns:
        int: The index of the element in the list.
    
    Raises:
        ValueError: If the element is not found.
    '''
    def helper(low, high):
        if low > high:
            return None
        
        mid_point = (low + high) // 2
        mid_search = search_pool[mid_point]
        
        if mid_search == search_piece:  # Found
            return mid_point
        
        if mid_search > search_piece:  # Too high
            return helper(low, mid_point - 1)
        
        # Too low
        return helper(mid_point + 1, high)

    return helper(0, len(search_pool) - 1)

def insert_into_sorted(sorted_list: list, item) -> list:
    '''Inserts an item into a sorted list while maintaining sorted order.
    
    Args:
        sorted_list (list): The sorted list to insert into.
        item: The item to insert.
    
    Returns:
        list: A new sorted list with the item inserted.
    '''
    def find_insert_position(low, high):
        if low > high:
            return low

        mid = (low + high) // 2
        if sorted_list[mid] < item:
            return find_insert_position(mid + 1, high)
        else:
            return find_insert_position(low, mid - 1)

    insert_position = find_insert_position(0, len(sorted_list) - 1)
    return sorted_list[:insert_position] + [item] + sorted_list[insert_position:]


def populate_list(file_name: str = 'Collatz_Prefound.txt', destination: list = None) -> list:
    '''Reads a file of values, sorts them, and populates a given list or returns a sorted list.
    
    Args:
        file_name (str): The name of the file to read from. Defaults to 'Collatz_Prefound.txt'.
        destination (list, optional): A list to populate with sorted values. If None, a new sorted list is returned.
    
    Returns:
        list: The sorted list of values from the file.
    
    Raises:
        ValueError: If the file is empty or cannot be read.
    '''
    if destination is None:
        destination = []
    
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        cleaned_lines = [int(line.strip()) for line in lines if line.strip()]

        if not cleaned_lines:
            raise ValueError(f"The file '{file_name}' is empty or has no valid content.")

        sorted_lines = merge_sort(cleaned_lines)

        destination.extend(sorted_lines)
        return destination

    except FileNotFoundError as e:
        raise ValueError(f"File not found: {file_name}") from e

def write_file(file_name: str = 'Collatz_Prefound.txt', source: list = None) -> None:
    '''Writes a list of unique values to a file.
    
    Args:
        file_name (str): The name of the file to write to. Defaults to 'Collatz_Prefound.txt'.
        source (list, optional): The list of values to write to the file. Each value will be converted to a string.
    
    Raises:
        ValueError: If the source is None or not iterable.
        IOError: If there are issues writing to the file.
    '''
    if source is None or not isinstance(source, (list, tuple)):
        raise ValueError("Source must be a non-empty list or tuple of values to write.")

    try:
        unique_source = set(source)
        with open(file_name, 'w') as file:
            for item in unique_source:
                file.write(f"{str(item)}\n")

    except IOError as e:
        raise ValueError(f"Could not write to file: {file_name}") from e


def check_collatz(number: int, sequence: list[int] = None) -> bool:
    '''Checks if a number satisfies the Collatz Conjecture.
    
    Args:
        number (int): The starting number to check.
        sequence (list[int], optional): The sequence of numbers in the current Collatz path. Defaults to None.
    
    Returns:
        bool: True if the Collatz Conjecture holds for the number, False if a loop is detected.
    '''
    global SOLVED_LIST 
    if sequence is None:
        sequence = []

    if find_in_sorted(SOLVED_LIST, number) or number == 1:
        for item in sequence:
            SOLVED_LIST = insert_into_sorted(SOLVED_LIST, item)  
        return True

    if number in sequence:
        return False

    sequence.append(number)

    if number % 2 == 0:  # Even
        next_number = number // 2
    else:  # Odd
        next_number = 3 * number + 1

    return check_collatz(next_number, sequence)

def test():
    '''Main function to test the Collatz Conjecture for sequential numbers.'''
    global SOLVED_LIST  

    result = True
    try:
        try:
            populate_list('Collatz.txt', SOLVED_LIST)
        except ValueError: 
            print('Could not find file')

        number = 1
        while number in SOLVED_LIST and number + 1 in SOLVED_LIST:
            number += 1

        while result:
            number += 1
            result = check_collatz(number)
            if result:
                print(f"{number:,} passes the test.")
                if not find_in_sorted(SOLVED_LIST, number):
                    SOLVED_LIST = insert_into_sorted(SOLVED_LIST, number)

        print(f"{number} disproves the Collatz Conjecture!")

    except ValueError as e:
        print(f"Error occurred: {e}. Saving progress...")
        write_file('Collatz.txt', SOLVED_LIST)
        print("Progress saved. Exiting.")

    except Exception as e:
        print(f"Unexpected error: {e}. Saving progress...")
        write_file('Collatz.txt', SOLVED_LIST)
        print("Progress saved. Exiting.")

    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Saving progress...")
        write_file('Collatz.txt', SOLVED_LIST)
        print("Progress saved. Exiting.")

def stats():
    global SOLVED_LIST

    try:
        populate_list('Collatz.txt', SOLVED_LIST)
    except ValueError:
        print('Could not find or read the file properly.')

    if not SOLVED_LIST:
        print("No data loaded into SOLVED_LIST. Exiting statistics computation.")
        return

    number = 1
    while number in SOLVED_LIST and number + 1 in SOLVED_LIST:
        number += 1

    print(f"Tested values up to {number:,}.")
    print(f"Maximum value is {max(SOLVED_LIST):,}")

if __name__ == '__main__':
    method = 'test'

    if method == 'test':
        test()

    if method == 'stats':
        stats()