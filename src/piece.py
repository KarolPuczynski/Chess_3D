class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)
        self.dir = -1 if color == 'white' else 1

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color)
