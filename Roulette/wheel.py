'''Creation of the Roulette Wheel'''

from random import choice

class RouletteWheel:

    def __init__(self, table_type):
        legal_types = ['0', '00', '000']
        
        if table_type not in legal_types:
            raise ValueError("Table must be one of the following types: '0', '00', '000'.")
        
        self.table_type = table_type
        
        # Define payouts
        self.payout_table = {
            "straight_up": 35,  # Single number
            "split": 17,        # Two adjacent numbers
            "street": 11,       # Three numbers in a row
            "corner": 8,        # Four numbers in a square
            "line": 5,          # Six numbers
            "column": 2,        # Column of 12 numbers
            "dozen": 2,         # Dozen bet (1-12, 13-24, 25-36)
            "red_or_black": 1,  # Red or Black
            "odd_or_even": 1,   # Odd or Even
            "low_or_high": 1    # Low (1-18) or High (19-36)
        }

        # Remove five-number bet for European tables
        if table_type != "00":
            self.payout_table.pop("five_number", None)
        else:
            self.payout_table["five_number"] = 6

        # Define spaces (numbers + colors)
        self.spaces = [
            ("1", "red"), ("2", "black"), ("3", "red"), ("4", "black"),
            ("5", "red"), ("6", "black"), ("7", "red"), ("8", "black"),
            ("9", "red"), ("10", "black"), ("11", "black"), ("12", "red"),
            ("13", "black"), ("14", "red"), ("15", "black"), ("16", "red"),
            ("17", "black"), ("18", "red"), ("19", "red"), ("20", "black"),
            ("21", "red"), ("22", "black"), ("23", "red"), ("24", "black"),
            ("25", "red"), ("26", "black"), ("27", "red"), ("28", "black"),
            ("29", "black"), ("30", "red"), ("31", "black"), ("32", "red"),
            ("33", "black"), ("34", "red"), ("35", "black"), ("36", "red")
        ]

        # Add correct number of green spaces based on table type
        for i in range(len(table_type)):  
            self.spaces.append(("0" * (i + 1), "green"))

    def place_bet(self, bet_type, amount, details=None):
        """
        Place a bet on the roulette wheel.

        Parameters:
        - bet_type (str): The type of bet (e.g., "straight_up", "red_or_black").
        - amount (float): The amount of money being wagered.
        - details: Additional info about the bet (e.g., specific number(s), group, etc.).

        Returns:
        - None
        """
        # Validate bet type
        if bet_type not in self.payout_table:
            raise ValueError(f"Invalid bet type: {bet_type}")

        # Validate bet amount
        if amount <= 0:
            raise ValueError("Bet amount must be greater than 0.")

        # Use a match-case for better readability
        match bet_type:
            case "straight_up":
                if details not in [num for num, _ in self.spaces]:
                    raise ValueError("For 'straight_up' bets, details must be a valid number (e.g., '17').")

            case "split":
                if not isinstance(details, tuple) or len(details) != 2:
                    raise ValueError("For 'split' bets, details must be a tuple of two adjacent numbers (e.g., (1, 2)).")
                if not all(num in [num for num, _ in self.spaces] for num in details):
                    raise ValueError("Each number in a 'split' bet must be valid numbers on the wheel.")

            case "street":
                if not isinstance(details, tuple) or len(details) != 3:
                    raise ValueError("For 'street' bets, details must be a tuple of three numbers in the same row.")
                rows = [
                    [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12],
                    [13, 14, 15], [16, 17, 18], [19, 20, 21],
                    [22, 23, 24], [25, 26, 27], [28, 29, 30],
                    [31, 32, 33], [34, 35, 36]
                ]
                if details not in rows:
                    raise ValueError(f"Invalid 'street' bet. Must be a row of three numbers (e.g., (1, 2, 3)).")

            case "corner":
                if not isinstance(details, tuple) or len(details) != 4:
                    raise ValueError("For 'corner' bets, details must be a tuple of four numbers in a square.")
                squares = [
                    [1, 2, 4, 5], [2, 3, 5, 6], [4, 5, 7, 8], [5, 6, 8, 9],
                    # Extend this to include all valid corner groups
                ]
                if sorted(details) not in squares:
                    raise ValueError(f"Invalid 'corner' bet. Must be four numbers in a square (e.g., (1, 2, 4, 5)).")

            case "line":
                if not isinstance(details, tuple) or len(details) != 6:
                    raise ValueError("For 'line' bets, details must be a tuple of six numbers in two rows.")
                lines = [
                    [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12],
                    # Extend to include all valid lines
                ]
                if sorted(details) not in lines:
                    raise ValueError(f"Invalid 'line' bet. Must be six numbers in two rows (e.g., (1, 2, 3, 4, 5, 6)).")

            case "column":
                if details not in [1, 2, 3]:
                    raise ValueError("For 'column' bets, details must be 1, 2, or 3 (for the respective column).")

            case "dozen":
                if details not in [1, 2, 3]:
                    raise ValueError("For 'dozen' bets, details must be 1 (1-12), 2 (13-24), or 3 (25-36).")

            case "red_or_black" | "odd_or_even" | "low_or_high":
                valid_details = {
                    "red_or_black": ["red", "black"],
                    "odd_or_even": ["odd", "even"],
                    "low_or_high": ["low", "high"]
                }
                if details not in valid_details[bet_type]:
                    raise ValueError(f"For '{bet_type}' bets, details must be one of {valid_details[bet_type]}.")

            case "five_number":
                if self.table_type != "00":
                    raise ValueError("The 'five_number' bet is only valid on American roulette tables.")
                if details is not None:
                    raise ValueError("The 'five_number' bet does not require details.")

            case _:
                raise ValueError(f"Unrecognized bet type: {bet_type}")

        # Add the bet to the list of bets
        self.bets.append({
            "bet_type": bet_type,
            "amount": amount,
            "details": details
        })

        print(f"Bet placed: {bet_type} | Amount: {amount} | Details: {details}")


    def spin_wheel(self):
        """
        Simulate a spin of the roulette wheel.

        Returns:
        - winning_number (str): The winning number (as a string).
        - winning_color (str): The color of the winning number (red/black/green).
        """
        # Randomly choose a space (index) from the wheel
        winning_space = choice(self.spaces)
        winning_number, winning_color = winning_space
        print(f"The winning number is {winning_number} ({winning_color})")

        return winning_number, winning_color

    def resolve_bets(self):
        """
        Resolve all the bets placed on the wheel.

        Returns:
        - None
        """
        # Spin the wheel and get the result
        winning_number, winning_color = self.spin_wheel()

        for bet in self.bets:
            bet_type = bet["bet_type"]
            amount = bet["amount"]
            details = bet["details"]
            
            # Resolve each bet type
            match bet_type:
                case "straight_up":
                    if details == winning_number:
                        payout = self.payout_table["straight_up"]
                        winnings = amount * payout
                        print(f"Straight-up bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Straight-up bet on {details} loses.")
                
                case "split":
                    if details[0] == winning_number or details[1] == winning_number:
                        payout = self.payout_table["split"]
                        winnings = amount * payout
                        print(f"Split bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Split bet on {details} loses.")
                
                case "street":
                    if winning_number in details:
                        payout = self.payout_table["street"]
                        winnings = amount * payout
                        print(f"Street bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Street bet on {details} loses.")
                
                case "corner":
                    if sorted(details) == sorted([winning_number, winning_number + 1, winning_number + 2, winning_number + 3]):
                        payout = self.payout_table["corner"]
                        winnings = amount * payout
                        print(f"Corner bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Corner bet on {details} loses.")
                
                case "line":
                    if winning_number in details:
                        payout = self.payout_table["line"]
                        winnings = amount * payout
                        print(f"Line bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Line bet on {details} loses.")
                
                case "column":
                    if (details == 1 and int(winning_number) % 3 == 1) or (details == 2 and int(winning_number) % 3 == 2) or (details == 3 and int(winning_number) % 3 == 0):
                        payout = self.payout_table["column"]
                        winnings = amount * payout
                        print(f"Column bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Column bet on {details} loses.")
                
                case "dozen":
                    if (details == 1 and 1 <= int(winning_number) <= 12) or (details == 2 and 13 <= int(winning_number) <= 24) or (details == 3 and 25 <= int(winning_number) <= 36):
                        payout = self.payout_table["dozen"]
                        winnings = amount * payout
                        print(f"Dozen bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Dozen bet on {details} loses.")
                
                case "red_or_black":
                    if winning_color == details:
                        payout = self.payout_table["red_or_black"]
                        winnings = amount * payout
                        print(f"Red/Black bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Red/Black bet on {details} loses.")
                
                case "odd_or_even":
                    if (winning_number % 2 == 1 and details == "odd") or (winning_number % 2 == 0 and details == "even"):
                        payout = self.payout_table["odd_or_even"]
                        winnings = amount * payout
                        print(f"Odd/Even bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Odd/Even bet on {details} loses.")
                
                case "low_or_high":
                    if (1 <= int(winning_number) <= 18 and details == "low") or (19 <= int(winning_number) <= 36 and details == "high"):
                        payout = self.payout_table["low_or_high"]
                        winnings = amount * payout
                        print(f"Low/High bet on {details} wins! Payout: {winnings}")
                    else:
                        print(f"Low/High bet on {details} loses.")
                
                case "five_number":
                    if self.table_type == "00" and winning_number in ['0', '00', '1', '2', '3']:
                        payout = self.payout_table["five_number"]
                        winnings = amount * payout
                        print(f"Five-number bet wins! Payout: {winnings}")
                    else:
                        print(f"Five-number bet loses.")
                        