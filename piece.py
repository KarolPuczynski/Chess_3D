class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Pawn(Piece):
    def __init__(self, color):
        self.moved = True
        super().__init__('pawn', color)

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