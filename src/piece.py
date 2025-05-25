class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)
        self.moved = False
        self.dir = -1 if color == 'white' else 1
        self.moves = []

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color)
        self.moves = []

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color)
        self.moves = []

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color)
        self.moves = []

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color)
        self.moves = []

class King(Piece):
    def __init__(self, color):
        self.moved = False
        super().__init__('king', color)
        self.moves = []