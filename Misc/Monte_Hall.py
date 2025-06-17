'''
Monty Hall problem Monte Carlo Simulation
Henry Rausch 2025
'''

from random import randint

def play_game(switch: bool, door_count: int = 3) -> bool:

    car_location = randint(1, door_count)
    choice = randint(1, door_count)

    doors_left = set([car_location, choice])
    other_door = car_location

    while len(doors_left) < 2:
        door = randint(1, door_count)
        doors_left.add(door)
        other_door = door
         
    if switch: 
        choice = other_door

    return car_location == choice

def simulation(trials: int, door_count: int) -> None:
    def run_simulation(wins, losses, switch, door_count):
        for _ in range(trials+1):
            result = play_game(switch, door_count)
            if result: wins += 1
            else: losses +=1

        return (wins, losses)

    switch_wins = 0
    switch_losses = 0
    stay_wins = 0
    stay_losses = 0

    switch_wins, switch_losses = run_simulation(switch_wins, switch_losses, True, door_count)
    stay_wins, stay_losses = run_simulation(stay_wins, stay_losses, False, door_count)

    print(f'Given {trials:,} attempts in either case, the results are as follows:')
    print(f'Switching gave: {switch_wins:,} wins and {switch_losses:,} losses, {(switch_wins/trials):0.3f} Win%')
    print(f'Staying gave: {stay_wins:,} wins and {stay_losses:,} losses, {(stay_wins/trials):0.3f} Win%')

simulation(1000000, 3)

"""
[Running] python -u "c:\\Users\\Henry\\OneDrive\\Documents\\Fun\\Misc\\Monte_Hall.py"
Given 1,000,000 attempts in either case, the results are as follows:
Switching gave: 666,210 wins and 333,791 losses, 0.666 Win%
Staying gave: 333,191 wins and 666,810 losses, 0.333 Win%
"""