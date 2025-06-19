'''Really just an excuse for me to screw around with bogosort, thinking of sorting implementations and testing them'''

from random import shuffle
from typing import MutableSequence, Protocol, runtime_checkable, cast, List
import matplotlib.pyplot as plt
from time import time
# MutableSequence > Iterable because it's required for shuffle

# Can we run ordering comparisons?
@runtime_checkable
class Comparable(Protocol):
    def __le__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...

def bogo(list_in: MutableSequence[Comparable], reverse: bool = False) -> MutableSequence[Comparable]:
    def is_sorted() -> bool:
        it = iter(list_in)
        try: # Can we get another value?
            last = next(it) 
        except StopIteration: 
            return True # End of list means sorted
        
        for new in it:
            if reverse:
                # For reverse, each element should be <= previous
                if last <= new:
                    return False
            else:
                # For ascending, each element should be >= previous
                if last >= new:
                    return False
            last = new  # Update for next comparison
        return True
                
    while(True):
        if is_sorted():
            break
        shuffle(list_in)
    return list_in

'''
# Test for casting
my_list: MutableSequence[Comparable] = cast(MutableSequence[Comparable], list(range(1, 26)))
shuffle(my_list)
sorted_list: MutableSequence[Comparable] = bogo(my_list)
print(f'Done: {sorted_list}')
'''

def start_timer() -> float:
    return time()

def stop_timer(timer_start: float) -> float:
    return time() - timer_start

# Configuration
lengths_to_try = 13
trials = 5

# Data containers
raw_data: dict[int, List[float]] = {}
avg_times: List[float] = []
list_lengths: List[int] = []

# Execution
for length in range(1, lengths_to_try + 1):
    print(f'\nStarting test of length {length}')
    trial_times: List[float] = []
    for trial in range(trials):
        my_list: MutableSequence[Comparable] = cast(MutableSequence[Comparable], list(range(1, length + 1)))
        shuffle(my_list)
        start = start_timer()
        sorted_list = bogo(my_list)
        duration = stop_timer(start)
        trial_times.append(duration)
        print(f'  Trial {trial + 1}: {duration:.3f}s')
    average = sum(trial_times) / trials
    raw_data[length] = trial_times
    avg_times.append(average)
    list_lengths.append(length)
    print(f'Average time: {average:.3f}s')

# --- Plotting ---
plt.figure(figsize=(8, 5))                                              # type: ignore[reportUnknownMemberType]

# Plot individual trials at low opacity
for length, trial_times in raw_data.items():
    for time_val in trial_times:
        plt.scatter(length, time_val, color='gray', alpha=0.5, s=20)    # type: ignore[reportUnknownMemberType]           background points

# Plot average line
plt.plot(list_lengths, avg_times, label='Average Time', color='blue', marker='o')  # type: ignore[reportUnknownMemberType]

# Annotate average points
for x, y in zip(list_lengths, avg_times):
    plt.annotate(f"{y:.3f}s", (x, y), textcoords="offset points", xytext=(0, 5), ha='center')  # type: ignore[reportUnknownMemberType]

# Labels and title
plt.title('Bogosort: List Length vs. Execution Time')                   # type: ignore[reportUnknownMemberType]
plt.xlabel('List Length')                                               # type: ignore[reportUnknownMemberType]
plt.ylabel('Time (seconds)')                                            # type: ignore[reportUnknownMemberType]
plt.legend()                                                            # type: ignore[reportUnknownMemberType]
plt.grid(True)                                                          # type: ignore[reportUnknownMemberType]
plt.tight_layout()                                                      # type: ignore[reportUnknownMemberType]
plt.show()                                                              # type: ignore[reportUnknownMemberType]


'''
Starting test of length 1
  Trial 1: 0.000s
  Trial 2: 0.000s
  Trial 3: 0.000s
  Trial 4: 0.000s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 2
  Trial 1: 0.000s
  Trial 2: 0.000s
  Trial 3: 0.000s
  Trial 4: 0.000s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 3
  Trial 1: 0.000s
  Trial 2: 0.000s
  Trial 3: 0.000s
  Trial 4: 0.000s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 4
  Trial 1: 0.000s
  Trial 2: 0.000s
  Trial 3: 0.000s
  Trial 4: 0.000s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 5
  Trial 1: 0.000s
  Trial 2: 0.000s
  Trial 3: 0.000s
  Trial 4: 0.001s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 6
  Trial 1: 0.001s
  Trial 2: 0.000s
  Trial 3: 0.001s
  Trial 4: 0.000s
  Trial 5: 0.000s
Average time: 0.000s

Starting test of length 7
  Trial 1: 0.003s
  Trial 2: 0.002s
  Trial 3: 0.011s
  Trial 4: 0.000s
  Trial 5: 0.004s
Average time: 0.004s

Starting test of length 8
  Trial 1: 0.041s
  Trial 2: 0.119s
  Trial 3: 0.101s
  Trial 4: 0.076s
  Trial 5: 0.031s
Average time: 0.074s

Starting test of length 9
  Trial 1: 0.348s
  Trial 2: 0.030s
  Trial 3: 0.629s
  Trial 4: 1.033s
  Trial 5: 0.164s
Average time: 0.441s

Starting test of length 10
  Trial 1: 2.259s
  Trial 2: 3.342s
  Trial 3: 0.183s
  Trial 4: 0.668s
  Trial 5: 5.013s
Average time: 2.293s

Starting test of length 11
  Trial 1: 25.391s
  Trial 2: 9.817s
  Trial 3: 35.294s
  Trial 4: 160.886s
  Trial 5: 24.877s
Average time: 51.253s

Starting test of length 12
  Trial 1: 778.090s
  Trial 2: 365.707s
  Trial 3: 495.268s
  Trial 4: 1457.849s
  Trial 5: 375.958s
Average time: 694.574s
'''