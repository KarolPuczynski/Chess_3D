from objloader import OBJ

class ModelInfo:
    def __init__(self, obj_model, position):
        self.obj_model = obj_model
        self.position = position

def load_model(file_path, position=(0, 0, 0)):
    try:
        obj_model = OBJ(file_path, swapyz=True)
        print(f"Successfully loaded: {file_path}")
        return ModelInfo(obj_model, list(position))
    except Exception as e:
        print(f"Error loading model {file_path}: {e}")
        return None

def get_chess_position(square):
    positions = {
        'A1': (-16.8, -16.8, 0), 'A2': (-16.8, -12.0, 0), 'A3': (-16.8, -7.2, 0), 'A4': (-16.8, -2.4, 0),
        'A5': (-16.8, 2.4, 0), 'A6': (-16.8, 7.2, 0), 'A7': (-16.8, 12.0, 0), 'A8': (-16.8, 16.8, 0),
        'B1': (-12.0, -16.8, 0), 'B2': (-12.0, -12.0, 0), 'B3': (-12.0, -7.2, 0), 'B4': (-12.0, -2.4, 0),
        'B5': (-12.0, 2.4, 0), 'B6': (-12.0, 7.2, 0), 'B7': (-12.0, 12.0, 0), 'B8': (-12.0, 16.8, 0),
        'C1': (-7.2, -16.8, 0), 'C2': (-7.2, -12.0, 0), 'C3': (-7.2, -7.2, 0), 'C4': (-7.2, -2.4, 0),
        'C5': (-7.2, 2.4, 0), 'C6': (-7.2, 7.2, 0), 'C7': (-7.2, 12.0, 0), 'C8': (-7.2, 16.8, 0),
        'D1': (-2.4, -16.8, 0), 'D2': (-2.4, -12.0, 0), 'D3': (-2.4, -7.2, 0), 'D4': (-2.4, -2.4, 0),
        'D5': (-2.4, 2.4, 0), 'D6': (-2.4, 7.2, 0), 'D7': (-2.4, 12.0, 0), 'D8': (-2.4, 16.8, 0),
        'E1': (2.4, -16.8, 0), 'E2': (2.4, -12.0, 0), 'E3': (2.4, -7.2, 0), 'E4': (2.4, -2.4, 0),
        'E5': (2.4, 2.4, 0), 'E6': (2.4, 7.2, 0), 'E7': (2.4, 12.0, 0), 'E8': (2.4, 16.8, 0),
        'F1': (7.2, -16.8, 0), 'F2': (7.2, -12.0, 0), 'F3': (7.2, -7.2, 0), 'F4': (7.2, -2.4, 0),
        'F5': (7.2, 2.4, 0), 'F6': (7.2, 7.2, 0), 'F7': (7.2, 12.0, 0), 'F8': (7.2, 16.8, 0),
        'G1': (12.0, -16.8, 0), 'G2': (12.0, -12.0, 0), 'G3': (12.0, -7.2, 0), 'G4': (12.0, -2.4, 0),
        'G5': (12.0, 2.4, 0), 'G6': (12.0, 7.2, 0), 'G7': (12.0, 12.0, 0), 'G8': (12.0, 16.8, 0),
        'H1': (16.8, -16.8, 0), 'H2': (16.8, -12.0, 0), 'H3': (16.8, -7.2, 0), 'H4': (16.8, -2.4, 0),
        'H5': (16.8, 2.4, 0), 'H6': (16.8, 7.2, 0), 'H7': (16.8, 12.0, 0), 'H8': (16.8, 16.8, 0)
    }
    return positions.get(square, (0, 0, 0))

def setup_scene():
    models = []
    chess_board = load_model('assets/models/chess_board.obj')
    if chess_board:
        models.append(chess_board)
    
    # Black pieces
    for file in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        pawn = load_model('assets/models/pawn_black.obj', get_chess_position(f"{file}7"))
        if pawn: models.append(pawn)
    
    pieces = [
        ('A8', 'rook_black.obj'), ('H8', 'rook_black.obj'),
        ('B8', 'knight_black.obj'), ('G8', 'knight_black.obj'),
        ('C8', 'bishop_black.obj'), ('F8', 'bishop_black.obj'),
        ('D8', 'queen_black.obj'), ('E8', 'king_black.obj')
    ]
    
    for pos, model in pieces:
        piece = load_model(f'assets/models/{model}', get_chess_position(pos))
        if piece: models.append(piece)
    
    # White pieces
    for file in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        pawn = load_model('assets/models/pawn_white.obj', get_chess_position(f"{file}2"))
        if pawn: models.append(pawn)
    
    pieces = [
        ('A1', 'rook_white.obj'), ('H1', 'rook_white.obj'),
        ('B1', 'knight_white.obj'), ('G1', 'knight_white.obj'),
        ('C1', 'bishop_white.obj'), ('F1', 'bishop_white.obj'),
        ('D1', 'queen_white.obj'), ('E1', 'king_white.obj')
    ]
    
    for pos, model in pieces:
        piece = load_model(f'assets/models/{model}', get_chess_position(pos))
        if piece: models.append(piece)
    
    return models