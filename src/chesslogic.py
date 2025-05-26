from scenesetup import get_chess_position

class ChessLogic:
    def __init__(self, models):
        self.models = models
        self.selected_piece = None
        self.selected_square = None

    def find_closest_square(self, world_x, world_y):
        squares = {
            'A1': (-16.8, -16.8), 'A2': (-16.8, -12.0), 'A3': (-16.8, -7.2), 'A4': (-16.8, -2.4),
            'A5': (-16.8, 2.4), 'A6': (-16.8, 7.2), 'A7': (-16.8, 12.0), 'A8': (-16.8, 16.8),
            'B1': (-12.0, -16.8), 'B2': (-12.0, -12.0), 'B3': (-12.0, -7.2), 'B4': (-12.0, -2.4),
            'B5': (-12.0, 2.4), 'B6': (-12.0, 7.2), 'B7': (-12.0, 12.0), 'B8': (-12.0, 16.8),
            'C1': (-7.2, -16.8), 'C2': (-7.2, -12.0), 'C3': (-7.2, -7.2), 'C4': (-7.2, -2.4),
            'C5': (-7.2, 2.4), 'C6': (-7.2, 7.2), 'C7': (-7.2, 12.0), 'C8': (-7.2, 16.8),
            'D1': (-2.4, -16.8), 'D2': (-2.4, -12.0), 'D3': (-2.4, -7.2), 'D4': (-2.4, -2.4),
            'D5': (-2.4, 2.4), 'D6': (-2.4, 7.2), 'D7': (-2.4, 12.0), 'D8': (-2.4, 16.8),
            'E1': (2.4, -16.8), 'E2': (2.4, -12.0), 'E3': (2.4, -7.2), 'E4': (2.4, -2.4),
            'E5': (2.4, 2.4), 'E6': (2.4, 7.2), 'E7': (2.4, 12.0), 'E8': (2.4, 16.8),
            'F1': (7.2, -16.8), 'F2': (7.2, -12.0), 'F3': (7.2, -7.2), 'F4': (7.2, -2.4),
            'F5': (7.2, 2.4), 'F6': (7.2, 7.2), 'F7': (7.2, 12.0), 'F8': (7.2, 16.8),
            'G1': (12.0, -16.8), 'G2': (12.0, -12.0), 'G3': (12.0, -7.2), 'G4': (12.0, -2.4),
            'G5': (12.0, 2.4), 'G6': (12.0, 7.2), 'G7': (12.0, 12.0), 'G8': (12.0, 16.8),
            'H1': (16.8, -16.8), 'H2': (16.8, -12.0), 'H3': (16.8, -7.2), 'H4': (16.8, -2.4),
            'H5': (16.8, 2.4), 'H6': (16.8, 7.2), 'H7': (16.8, 12.0), 'H8': (16.8, 16.8)
        }
        
        closest_square = None
        min_distance = float('inf')
        
        for square, (sq_x, sq_y) in squares.items():
            distance = ((world_x - sq_x)**2 + (world_y - sq_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_square = square
        
        return closest_square if min_distance < 4.0 else None

    def get_piece_at_square(self, square):
        if not square:
            return None
        
        square_pos = get_chess_position(square)
        for model in self.models:
            if (abs(model.position[0] - square_pos[0]) < 0.1 and \
               abs(model.position[1] - square_pos[1]) < 0.1 and \
               model.obj_model != self.models[0].obj_model):  # ignorowanie planszy do klikania 
                return model
        return None

    def move_piece(self, piece, new_square):
        if piece and new_square:
            new_pos = get_chess_position(new_square)
            piece.position = list(new_pos)
            print(f"Przeniesiono figure na pole {new_square}")
            return True
        return False

    def handle_click(self, world_x, world_y):
        clicked_square = self.find_closest_square(world_x, world_y)
        
        if clicked_square:
            print(f"Kliknieto pole: {clicked_square}")
            
            if self.selected_piece is None:
                self.selected_piece = self.get_piece_at_square(clicked_square)
                self.selected_square = clicked_square
                if self.selected_piece:
                    print(f"Wybrano figure na polu {clicked_square}")
                else:
                    print("Brak figury na wybranym polu")
            else:
                target_piece = self.get_piece_at_square(clicked_square)
                
                if clicked_square == self.selected_square:
                    print("Odznaczono figure")
                    self.selected_piece = None
                    self.selected_square = None
                elif target_piece is None:
                    if self.move_piece(self.selected_piece, clicked_square):
                        self.selected_piece = None
                        self.selected_square = None
                else:
                    print("Nie mozna przeniesc figury - pole zajete")
        else:
            print("Kliknieto poza plansza")
            self.selected_piece = None
            self.selected_square = None