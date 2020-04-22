from tile import Tile, EMPTY, SPRING

class Board:

    def __init__(self):
        self.grid = [[Tile() for _ in range(9)] for _ in range(5)]
        self.at(4, 0).tile_type = SPRING
        self.at(5, 2).tile_type = SPRING
        self.at(4, 4).tile_type = SPRING

    def at(self, x, y):
        return self.grid[y][x]

    def render(self):
        render_rows = []
        for y, row in enumerate(self.grid):
            row_lines = ['   '],[f'{5-y}  '],['   ']
            for tile in row:
                if tile.tile_type == SPRING:
                    row_lines[0].append('.@@.')
                    row_lines[1].append('@@@@')
                    row_lines[2].append('.@@.')
                else:
                    row_lines[0].append('....')
                    row_lines[1].append('....')
                    row_lines[2].append('....')
            render_rows.append('\n'.join(map(' '.join, row_lines)))
        return '\n\n'.join(render_rows)+'\n\n      A    B    C    D    E    F    G    H    I'