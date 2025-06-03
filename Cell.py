class Cell:
    def __init__(self, piece=None) -> None:
        self.piece = piece #holds a piece

    def clone(self):
        cloned_cell = Cell()

        cloned_cell.piece = self.piece.clone() if self.piece else None

        return cloned_cell
 