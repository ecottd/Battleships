import pytest
from battleships import Player, coords_within_board, valid_ship_coords, valid_bomb_drop

@pytest.fixture
def player():
    player = Player("Player")
    player.piece_locations = {
        'carrier': [(6, 3), (6, 4), (6, 5), (6, 6), (6, 7)],
        'battleship': [(2, 8), (3, 8), (4, 8), (5, 8)],
        'cruiser': [(6, 12), (7, 12), (8, 12), (9, 12)],
        'submarine': [(11, 1), (11, 2), (11, 3)],
        'destroyer': [(1, 2), (1, 3)]
    }
    player.bombs_dropped = [(5, 8), (9, 3), (12, 12)]
    return player

@pytest.fixture
def opponent():
    opponent = Player("Opponent")
    opponent.piece_locations = {
            'carrier': [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
            'battleship': [(2, 5), (3, 5), (4, 5), (5, 5)],
            'cruiser': [(6, 3), (7, 3), (8, 3), (9, 3)],
            'submarine': [(8, 1), (8, 2), (8, 3)],
            'destroyer': [(10, 2), (10, 3)]
    }
    opponent.bombs_dropped = [(3, 11), (5, 4), (6, 6)]
    return opponent
    
@pytest.fixture
def board_size():
    board_size = 10
    return board_size

def test_coords_within_board(board_size):
    assert coords_within_board(board_size, 3, 6) == True
    assert coords_within_board(board_size, 8, 27) == False
    assert coords_within_board(board_size, 16, 4) == False
    assert coords_within_board(board_size, 13, 13) == False
    assert coords_within_board(board_size, 0, 0) == False

def test_valid_ship_coords(player, opponent):
    assert valid_ship_coords(player, [(3, 6)]) == True
    assert valid_ship_coords(player, [(7, 12)]) == False    
    assert valid_ship_coords(opponent, [(3, 3)]) == True
    assert valid_ship_coords(opponent, [(8, 3)]) == False

def test_valid_bomb_drop(player, opponent):
    assert valid_bomb_drop(player, (5, 8)) == False
    assert valid_bomb_drop(player, (4, 5)) == True
    assert valid_bomb_drop(opponent, (3, 11)) == False
    assert valid_bomb_drop(opponent, (4, 5)) == True