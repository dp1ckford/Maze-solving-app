import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import random

MAZE_WIDTH, MAZE_HEIGHT = (22, 24)
LINE_WIDTH = 6
IMAGE_COUNT = 10


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.searched = False
        self.connected_from = None
        self.connected_to = []
        self.neighbours = []
        self.walls = [False]*4

    def recursive_dfs(self):
        random.shuffle(self.neighbours)
        for neighbour in self.neighbours:
            if not neighbour.searched:
                neighbour.searched = True
                neighbour.connected_from = self
                self.connected_to.append(neighbour)
                neighbour.recursive_dfs()
        self.wall_non_connections()

    def wall_non_connections(self):
        sides = [0, 1, 2, 3]
        if self.connected_from:
            sides.remove(self.get_direction_of_neighbour(self.connected_from))
        for neighbour in self.connected_to:
            sides.remove(self.get_direction_of_neighbour(neighbour))
        for i in sides:
            self.add_wall(i)
        return self

    def get_direction_of_neighbour(self, neighbour):
        if neighbour.x == self.x:
            return 1 + (neighbour.y - self.y)
        else:
            return 2 + (self.x - neighbour.x)

    def add_wall(self, side):
        try:
            if type(side) == str:
                side = {"top": 0, "right": 1, "bottom": 2, "left": 3}[side.lower()]
            self.walls[side] = True
        except Exception as e:
            print(e, f"- ({self.x}, {self.y}) Wall {side} not placed")
        return self

    def remove_wall(self, side):
        try:
            if type(side) == str:
                side = {"top": 0, "right": 1, "bottom": 2, "left": 3}[side.lower()]
            self.walls[side] = False
        except Exception as e:
            print(e, f"- ({self.x}, {self.y}) Wall {side} not removed")
        return self


def from_grid_coords(grid, pos):
    try:
        return grid[pos[1]][pos[0]]
    except Exception as e:
        print(e, pos)
    return grid[pos[1]][pos[0]]


def main():
    images = []
    for i in range(IMAGE_COUNT):
        # Create grid of tiles
        grid = []
        for y in range(MAZE_HEIGHT):
            row = []
            for x in range(MAZE_WIDTH):
                row.append(Tile(x, y))
            grid.append(row)

        # Give tiles neighbours, forming a graph that can be traversed

        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if x:
                    grid[y][x].neighbours.append(from_grid_coords(grid,(x-1, y)))
                if y:
                    grid[y][x].neighbours.append(from_grid_coords(grid,(x, y-1)))
                if x < MAZE_WIDTH-1:
                    grid[y][x].neighbours.append(from_grid_coords(grid,(x+1, y)))
                if y < MAZE_HEIGHT - 1:
                    grid[y][x].neighbours.append(from_grid_coords(grid,(x, y+1)))

        # DFS

        start_node = grid[random.randint(0, MAZE_HEIGHT-1)][random.randint(0, MAZE_WIDTH-1)]
        start_node.searched = True

        start_node.recursive_dfs()

        # Create exits

        grid[0][0].remove_wall("top")
        grid[MAZE_HEIGHT-1][MAZE_WIDTH-1].remove_wall("bottom")

        # Create image of maze
        canvas_dims = (794, 1123)
        img = PIL.Image.new(mode="RGB", size=canvas_dims, color=(255, 255, 255))

        maze_width_px = 750
        tile_size = maze_width_px/MAZE_WIDTH
        maze_height_px = tile_size*MAZE_HEIGHT
        maze_start = ((canvas_dims[0]-maze_width_px-LINE_WIDTH)/2, (canvas_dims[1]-maze_height_px-LINE_WIDTH)/2)
        draw = PIL.ImageDraw.Draw(img)

        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if grid[y][x].walls[0]:
                    points = [
                        (x*tile_size+maze_start[0], y*tile_size+maze_start[1]),
                        ((x+1)*tile_size+maze_start[0], y*tile_size+maze_start[1]),
                        ((x+1)*tile_size+maze_start[0], y*tile_size+LINE_WIDTH+maze_start[1]),
                        (x * tile_size+maze_start[0], y * tile_size+LINE_WIDTH+maze_start[1])
                    ]
                    draw.polygon(tuple(points), fill=(0, 0, 0, 255))
                if grid[y][x].walls[2]:
                    points = [
                        (x*tile_size+maze_start[0], (y+1)*tile_size+maze_start[1]),
                        ((x+1)*tile_size+maze_start[0]+LINE_WIDTH, (y+1)*tile_size+maze_start[1]),
                        ((x+1)*tile_size+maze_start[0]+LINE_WIDTH, (y+1)*tile_size+LINE_WIDTH+maze_start[1]),
                        (x * tile_size+maze_start[0], (y+1)*tile_size+LINE_WIDTH+maze_start[1])
                    ]
                    draw.polygon(tuple(points), fill=(0, 0, 0, 255))

                if grid[y][x].walls[1]:
                    points = [
                        ((x+1)*tile_size+maze_start[0], y*tile_size+maze_start[1]),
                        ((x+1)*tile_size+maze_start[0], (y+1)*tile_size+maze_start[1]+LINE_WIDTH),
                        ((x+1)*tile_size+maze_start[0]+LINE_WIDTH, (y+1)*tile_size+maze_start[1]+LINE_WIDTH),
                        ((x+1) * tile_size+maze_start[0]+LINE_WIDTH, y*tile_size+maze_start[1])
                    ]
                    draw.polygon(tuple(points), fill=(0, 0, 0, 255))

                if grid[y][x].walls[3]:
                    points = [
                        (x*tile_size+maze_start[0], y*tile_size+maze_start[1]),
                        (x*tile_size+maze_start[0], (y+1)*tile_size+maze_start[1]+LINE_WIDTH),
                        (x*tile_size+maze_start[0]+LINE_WIDTH, (y+1)*tile_size+maze_start[1]+LINE_WIDTH),
                        (x * tile_size+maze_start[0]+LINE_WIDTH, y*tile_size+maze_start[1])
                    ]
                    draw.polygon(tuple(points), fill=(0, 0, 0, 255))
        images.append(img)
    images[0].save("out.pdf", save_all=True, append_images=images[1:])


if __name__ == "__main__":
    main()
