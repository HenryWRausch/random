import random
import matplotlib.pyplot as plt
import scipy.stats as stats
from collections import Counter

def simulate(sides: int, n_list: int | list[int], bias: list[float] = None) -> list | dict:
    '''
    Simulates a given die for random number generation over a given number of trials

    Parameters:
    sides (int)             : Number of sides on the die
    n_list (int | list[int]): Either a single trial size or a list of trial sizes
    bias (list[float])      : List of probabilities for the die. Default is a fair die with even distribution

    Returns:
    Either a single list if only one trial is performed, or a dictionary where keys are trial sizes and values are the simulated trials

    Raises:
    ValueError if the size of bias is not equal to the number of sides, or n_list is not an accepted type
    '''

    if bias and len(bias) != sides:
        raise ValueError("The length of 'bias' must match the number of sides.")

    if isinstance(n_list, int):
        return random.choices(range(1, sides+1), bias, k = n_list)
    elif isinstance(n_list, list):
        return {n: random.choices(range(1, sides+1), bias, k=n) for n in n_list}

    else: 
        raise ValueError(f"'n_list' must be a list of integers or a single integer, got {type(n_list)}")

def simulation_to_stats(sides: int, simulation: list[int] | list[list[int]] | dict, bias_threshold: float = 0.05) -> dict:
    '''
    Translates a simulation from simulate() into statistics for analysis

    Parameters: 
    sides (int)                                         : Number of sides on the simulated die
    simulation (list[int] or list[list[int]] or dict)   : Either a single trial (list[int]), a list of trials (list[list[int]]), or a dictionary output from simulate()
    bias_threshold (float)                              : Alpha value for "fairness"

    Returns:
    A dictionary of statistics for a single trial or a list of dictionaries for multiple trials with the following values:
        'sides'                 : Number of sides on simulated die
        'number_of_rolls'       : Number of times the die roll was simulated
        'counts'                : Number of times each face was rolled
        'probabilities'         : List of probability representation of counts; counts[number]/number of rolls
        'expected_probability'  : Probability of each side assuming a fair die
        'bias_threshold'        : Directly bias_threshold
        'simple_fair'           : Boolean of whether any individual probability is more than bias_threshold away from a theoretical distribution
        'chi2_fair'             : Result of Chi-Squared test on given alpha

    
    Raises:
    ValueError if simulation is of incorrect type
    '''

    def get_stats(sides: int, simulation: list[int], bias_threshold: float) -> dict:
        '''
        Helper operation to simplify gathering stats to only the case of one trial
        
        Parameters: 
        sides (int)                                         : Number of sides on the simulated die
        simulation (list[int])                              : A single trial (list[int])
        bias_threshold (float)                              : Alpha value for "fairness"

        
        Returns:
        A dictionary of statistics for a single trial or a list of dictionaries for multiple trials with the following values:
            'sides'                 : Number of sides on simulated die (int)
            'number_of_rolls'       : Number of times the die roll was simulated (int)
            'counts'                : Number of times each face was rolled (list[tuple[int, int]])
            'probabilities'         : List of probability representation of counts; counts[number]/number of rolls (list[tuple[int, float]])
            'expected_probability'  : Probability of each side assuming a fair die (float)
            'bias_threshold'        : Directly bias_threshold (float)
            'simple_fair'           : Determines whether all probabilities are within bias_threshold of their expected theoretical values (bool)
            'chi2_fair'             : Result of Chi-Squared test on given alpha tuple[bool, float]
        '''

        data = {}

        # Sides
        data['sides'] = sides

        # Number of Rolls
        data['number_of_rolls'] = len(simulation)

        # Counts
        count_helper = Counter(simulation)
        data['counts'] = [(i, count_helper.get(i, 0)) for i in range(1, sides+1)]

        # Probabilities
        data['probabilities'] = [(side, count / data['number_of_rolls']) for side, count in data['counts']]

        # Expected Probability
        data['expected_probability'] = 1/sides

        # Bias Threshold
        data['bias_threshold'] = bias_threshold

        # Simple Fair
        data['simple_fair'] = all(abs(probability - data['expected_probability']) <= bias_threshold for _, probability in data['probabilities'])

        # Chi-Squared Fair
        counts = [count for _, count in data['counts']]
        _, p = stats.chisquare(counts)
        data['chi2_fair'] = (bool(p > bias_threshold), float(p))

        return data
                

    if isinstance(simulation, list) and all(isinstance(i, int) for i in simulation):
        # Single Trial
        data =  get_stats(sides, simulation, bias_threshold)
    elif isinstance(simulation, list) and all(isinstance(i, list) for i in simulation):
        # List of Trials
        data = {}
        for trial_number, trial in enumerate(simulation, 1):
            data[f'Trial {trial_number}'] = get_stats(sides, trial, bias_threshold)
    elif isinstance(simulation, dict):
        # Dictionary of Trials
        data = {f'{key} rolls' : get_stats(sides, simulation[key], bias_threshold) for key in simulation.keys()}
    else:
        raise ValueError(f"Invalid type for 'simulation'. Expected list[int], list[list[int]], or dict, got {type(simulation)}")
    
    return data

def print_simulation_stats(stats: dict, verbose: bool = False, probability_precision: int = 5, p_precision: int = 3, min_width: int = 0) -> str:
    '''
    Creates a formatted string for displaying simulation statistics.

    Parameters:
    stats (dict)                : Dictionary containing simulation data.
    verbose (bool)              : If True, prints the output to terminal.
    probability_precision (int) : Number of decimal places for probabilities, default is 5.
    p_precision (int)           : Number of decimal places for p-value, default is 3.
    min_width (int)             : Minimum width of output

    Returns:
    str : A formatted string with simulation statistics.

    Raises:
    ValueError if the stats dictionary is missing expected keys.
    '''

    expected_keys = [
            'sides',                 # Number of sides on simulated die (int)
            'number_of_rolls',       # Number of times the die roll was simulated (int)
            'counts',                # Number of times each face was rolled (list[tuple[int, int]])
            'probabilities',         # List of probability representation of counts; counts[number]/number of rolls (list[tuple[int, float]])
            'expected_probability',  # Probability of each side assuming a fair die (float)
            'bias_threshold',        # Directly bias_threshold (float)
            'simple_fair',           # Determines whether all probabilities are within bias_threshold of their expected theoretical values (bool)
            'chi2_fair'              # Result of Chi-Squared test on given alpha tuple[bool, float]
    ]
    
    # Check for missing keys
    missing_keys = [key for key in expected_keys if key not in stats]
    if missing_keys:
        raise ValueError(f"Missing expected keys: {', '.join(missing_keys)}")

    # Header
    summary = f"{stats['sides']} sides tested on {stats['number_of_rolls']:,} rolls"
    expected_prob_str = f"We expect to see a probability of {stats['expected_probability']:0.{probability_precision}f} in a fair die with {stats['sides']} sides"

    # Probabilities
    max_count_length = len(str(max(count for _, count in stats['counts'])))
    max_count_length += 2 + max_count_length//3 # account for commas
    max_count_length = 5 if max_count_length < 5 else max_count_length
    
    probabilities_header = f"|{'Face #':^8}|{'Count':^{max_count_length}}|{'Probability':^13}|"
    probabilities_breaker = f"|{'':-^8}|{'':-^{max_count_length}}|{'':-^13}|"
    probabilities_rows = [
        f"|{i:^8}|{count:^{max_count_length},}|{probability:^13.{probability_precision}f}|"
        for (i, count), (_, probability) in zip(stats['counts'], stats['probabilities'])
    ]
    
    # Fairness
    fairness_header = f"We used an alpha of {stats['bias_threshold']:.{p_precision}f} for the following fairness tests:"
    simple_fairness = f"We evaluated the die to be {'fair' if stats['simple_fair'] else 'unfair'} using the simple test"
    chi2_fairness = f"At p={stats['chi2_fair'][1]:.{p_precision}f} we evaluated the die to be {'fair' if stats['chi2_fair'][0] else 'unfair'} using a Chi^2 test"
    
    # Finding widest line for width
    width = max(
        len(summary), 
        len(expected_prob_str), 
        len(probabilities_header),
        len(probabilities_rows[0]), 
        len(simple_fairness), 
        len(chi2_fairness),
        min_width-6 # -6 because we add 4 whitespace and 2 edgelines
    ) + 4

    formatted_sections = {
        'summary': f'{summary:^{width}}',
        'expected_prob_str': f'{expected_prob_str:^{width}}',
        'probabilities_header': f'{probabilities_header:-^{width}}',
        'probabilities_breaker': f'{probabilities_breaker:-^{width}}',
        'fairness_header': f'{fairness_header:-^{width}}',
        'simple_fairness': f'{simple_fairness:-^{width}}',
        'chi2_fairness': f'{chi2_fairness:-^{width}}',
    }

    breaker = '-' * width

    output = f"""|{breaker}|
|{formatted_sections['summary']}|
|{breaker}|
|{formatted_sections['expected_prob_str']}|
|{breaker}|
|{formatted_sections['probabilities_header']}|
|{formatted_sections['probabilities_breaker']}|
"""
    
    for row in probabilities_rows:
        output += f'|{row:-^{width}}|\n'
    
    output += f"""|{breaker}|
|{formatted_sections['fairness_header']}|
|{formatted_sections['simple_fairness']}|
|{formatted_sections['chi2_fairness']}|
|{breaker}|"""

    
    if verbose:
        print(output)

    return output
