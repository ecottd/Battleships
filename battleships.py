"""
battleships.py
Python Code that allows two players to play Battleships on a computer
"""

class Player():
    """
    A class that defines a battleship player and their game state
    """
    

    def __init__(self, name):
        """
        Args:
            name (str): The player's name
        """
        # Initialize the object with a name, a remaining piece count of 5, dictionaries containing piece locations and piece sizes,
        # an array representing the board and a list for storing where bombs have been dropped on their board
        self.name = name
        self.remaining_pieces = 5
        self.piece_locations = {
            'carrier': [],
            'battleship': [],
            'cruiser': [],
            'submarine': [],
            'destroyer': []
        }
        self.piece_sizes = {
            'carrier': 5,
            'battleship': 4,
            'cruiser': 3,
            'submarine': 3,
            'destroyer': 2
        }
        self.pieces = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]
        # I realize I am storing board state twice here. I need to refactor to just use one. 
        self.bombs_dropped = []
        self.board = [
                [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['9', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['10', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]


def place_pieces(board_size: int) -> None:
    """
    Args:
        board_size (int): An integer representing the size of the playing board

    Raises:
        ValueError: If pieces are not placed correctly on the board, either diagonally, overlapping, off the playing board etc.
        
    Returns:
        None
    """
    # This function populates the player objects with state peratining to ship locations
    print(f"Today's board is {board_size} positions square.")
    print("You will be asked to supply two sets of coordinates to place each piece.")
    print("Those coordinates should be the extremeties of the piece in question.")
    print("If you supply coordinates that don't match the size of the piece you are laying,")
    print("an error will be thrown and you will be asked for coordinates again.")
    
    # Loop through each player and each piece to successfully lay each ship on the board
    for player in players:
        draw_board(player)
        for piece in player.pieces:
            # Instantiate a while loop to keep prompting the user for valid coordinates until successful
            while True:
                # Use try catch to ensure given coords are within the boundaries of the playing surface   
                try:
                    print(f"OK, {player.name}, time to lay your {piece}.")
                    # TODO Boil down the gathering of coords from the user into a single function
                    # Gather the ship's starting coordinates from the player
                    x1, y1 = [int(x) for x in input(f"Enter two starting coordinate values for your {piece}, separated by a 'space': ").split()]
                    
                    # Are the supplied coordinates within the limits of the board
                    if coords_within_board(board_size, x1, y1):
                        pass
                    else:
                        raise ValueError("Incorrect coordinates were supplied. Try again.")
                    
                    # Gather the ship's ending coordinates from the player
                    x2, y2 = [int(x) for x in input(f"Enter two ending coordinate values for your {piece}, separated by a space: ").split()]
                    
                    # Are the supplied coordinates within the limits of the board
                    if coords_within_board(board_size, x2, y2):
                        pass
                    else:
                        raise ValueError("Incorrect coordinates were supplied. Try again.")

                    # Put both x anc y coordinates into respective lists for further computation
                    x_s = [x1, x2]
                    y_s = [y1, y2]
                    
                    # TODO Boil down the code for placing a ship on the board into a single function to avoid this repetition
                    if (x1 != x2) and (y1 == y2):
                        print(f"{piece} has been laid horizontally.")
                        # Build a list of tuples representing all coordinates occupied by the piece
                        piece_coords = [(x,y1) for x in range(sorted(x_s)[0], sorted(x_s)[1] + 1)]

                        # Check to make sure the supplied coordinates are equal to the size of the ship being laid
                        if ((sorted(x_s)[1] - sorted(x_s)[0]) + 1) != player.piece_sizes[piece]:
                            raise ValueError(f"It looks like your supplied coordinates do not match the length of your ship, which should be {player.piece_sizes[piece]}")
                       
                        # Check to make sure the supplied coordinates do not already exist on the player's board                        
                        if valid_ship_coords(player, piece_coords):
                                for item in piece_coords:
                                    player.piece_locations[piece].append(item)
                        else:
                            raise ValueError("You can't lay a piece there, something is already in one of those spots.")
                                                                        
                    elif (y1 != y2) and (x1 == x2):
                        print(f"{piece} has been laid vertically.")
                        # Build a list of tuples representing all coordinates occupied by the piece
                        piece_coords = [(x1,y) for y in range(sorted(y_s)[0], sorted(y_s)[1] + 1)]

                        # Check to make sure the supplied coordinates are equal to the size of the ship being laid
                        if ((sorted(y_s)[1] - sorted(y_s)[0])  + 1) != player.piece_sizes[piece]:
                            raise ValueError(f"It looks like your supplied coordinates do not match the length of your ship, which should be {player.piece_sizes[piece]}")
                        
                        # Check to make sure the supplied coordinates do not already exist on the player's board
                        if valid_ship_coords(player, piece_coords):
                            for item in piece_coords:
                                player.piece_locations[piece].append(item)
                        else:
                            raise ValueError("You can't lay a piece there, something is already in one of those spots.")
                        
                    else:
                        # Error out of a piece is not laid horizontally or vertically
                        raise ValueError("It looks like you tried to lay a piece in a funky way, try again. ")
                    
                except ValueError as e:
                    print(f"Whoops: {e}")
                    continue
                
                else:
                    break


def drop_bomb(player, opponent, board_size: int) -> None:
    """
    Args:
        player (object): An object derived from a class that describes a player and their board
        opponent (object): An object derived from a class that describes a player and their board
        board_size (int): An integer representing the size of the playing board

    Raises:
        ValueError: If a bomb is dropped in an invalid location
        
    Returns:
        None
    """
    
    # Draw the board so that the player can see what their board looks like before they drop a bomb
    draw_board(player)
    
    # Use a while loop to run through tests on supplied coordinates until valid ones have been supplied
    while True:
        try:
            # Prompt the user for coordinates to drop the bomb
            xb,yb = [int(x) for x in input(f"Enter the coordinates to drop your bomb: ").split()]
            # Put the coordinated into a tuple for further calculation
            coords = (xb, yb)
            
            # Perform checks to validate the bomb placement is good
            if coords_within_board(board_size, xb, yb):
                if valid_bomb_drop(player, coords):
                    player.bombs_dropped.append(coords)
                    # Check that the supplied coordinates relate to hitting a player's ship
                    for ship, placement in opponent.piece_locations.items():
                        # If the coordinates supplied DO match an opponent's ship, decrement the number of remaining coords for that ship
                        if coords in placement:
                            print(f"You hit their {ship}!")
                            opponent.piece_sizes[ship] -= 1
                            print("Dropping an X on the board at those coordinates")
                            player.board[yb][xb] = 'X'
                            # Check to see if there are any more remaining coords for this ship, if not, ship is destroyed
                            if opponent.piece_sizes[ship] == 0:
                                print(f"You destroyed their {ship}!")
                                opponent.remaining_pieces -= 1
                                # If we reach a successful bomb drop and a ship is destroyed, break out of the while loop
                                break
                            # If we reach a successful bomb drop and did NOT destroy a ship, break out of the while loop                        
                            break
                        else:
                            ####################################
                            # TODO This is crappy, I only want to say that the bomb missed once.
                            ####################################
                            print("Dropping an O on the board at those coordinates")
                            player.board[yb][xb] = 'O'
                            print(f"Missed the {ship}!")      
                #If the player laid a valid bomb, break out of the while loop to pass the turn to the next player
                    break
            
                # Raise an error if the bomb placement doesn't meet the tests
                else:
                    raise ValueError("Invalid bomb drop location, try again.")

        
        # Standardized error message for try catch
        except ValueError as e:
            print(f"You didn't supply correct coordinates: {e}")
        

def coords_within_board(board_size: int, *args: int) -> bool:
    """
    Args:
        board_size (int): An integer representing the size of the playing board

    Returns:
        bool: The supplied coordinates arte within the limits of the board, or not
    """
    # Check to see if the supplied coordinates are within the limits of the board size
    if 0 < args[0] <= board_size and 0 < args[1] <= board_size:
        return True
    else:
        return False


def valid_ship_coords(player, coords: list) -> bool:
    """
    Args:
        player (object): An object derived from a class that describes a player and their board
        coords (list): A list of coordinates(tuples) representing a given ship

    Returns:
        bool: _description_
    """
    # Check to see if the player has already laid a ship in any one of the supplied coordinates, if so, return False
    position_taken = []
    for coord in coords:
        for ship, placement in player.piece_locations.items():
            if coord in placement:
                position_taken.append(coord)
    if len(position_taken) > 0:
        return False
    else:
        return True


def valid_bomb_drop(player, coords: tuple) -> bool:
    """
    Args:
        player (object): An object derived from a class that describes a player and their board
        coords (tuple): A tuple representing the coordinates of a dropped bomb

    Returns:
        bool: Returns true if the bomb coordinates have not already been supplied
    """
    # Check to see if the player has already laid a bomb at this coordinate
    return coords not in player.bombs_dropped


def draw_board(player) -> None:
    """
    _summary_

    Args:
        player (object): An object derived from a class that describes a player and their board
        
    Returns: Prints out the player's board to the screen
    """
    print('\n'.join([''.join(['{:2}'.format(item) for item in row]) for row in player.board]))


if __name__ == '__main__':
    # This is the main game function that runs when this file is executed
    # Fix the board size to be the same as the physical Battleship board
    board_size = 10

    # Create the player objects
    player1 = Player("Dan")
    player2 = Player("Finley")
    players = [player1, player2]
    
    # Start the first part of the game, laying the pieces
    place_pieces(board_size)

    # Start the main game, droppin' bombs
    # Provided both players have pieces remaining, the game is not over, stay in while loop
    while player1.remaining_pieces > 0 and player2.remaining_pieces > 0:
        if player1.remaining_pieces > 0:
            print(f"{player1.name}, It's your turn.")
            drop_bomb(player1, player2, board_size)
        if player2.remaining_pieces > 0:
            print(f"{player2.name}, It's your turn.")
            drop_bomb(player2, player1, board_size)

    # When we drop out of the while loop, let the winner know that they won.    
    print("Game over!")
    for player in players:
        if player.remaining_pieces > 0:
            print(f"{player.name}, you won the game!")

