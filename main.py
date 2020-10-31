"""
Chess

"""
import arcade
from PIL import Image
# Screen title and size
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Chess"

SQUARE_SIZE = SCREEN_WIDTH/8

"""
TODO
Snap to place
Only allow possible moves for each piece
Show possible moves when a piece is selected
Implement castling
"""

class Square(arcade.Sprite):
    def __init__(self, bw: str = "black", x: float = 0, y: float = 0):
        """Used for snap to place 

        Args:
            bw (str, optional): black or white. Defaults to "black".
            x (float, optional): x location. Defaults to 0.
            y (float, optional): y location. Defaults to 0.
        """
        super().__init__(f"sprites/{bw}Square.png", 1, center_x=x, center_y=y)


class Piece(arcade.Sprite):
    def __init__(self, bw="white", value="Pawn", x: int = 0, y: int = 0,  scale=1):
        """ Piece Constructor """
        self.bw = bw
        self.value = value
        self.cstl_bool = None

        self.image_file_name = f"sprites/{self.bw}{self.value}.png"
        super().__init__(self.image_file_name, scale)
        self.position = (x,y)


class MyGame(arcade.Window):
    def __init__(self):
        """Initial settings of the game
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Set background color
        arcade.set_background_color(arcade.color.ANTIQUE_WHITE)
        self.turn = True
        self.piece_in_hand: Piece = None
        self.original_location = None

        self.white_set = arcade.SpriteList()
        self.black_set = arcade.SpriteList()
        self.board = arcade.SpriteList()

    def draw_board(self):
        """
        :return: Creates board for snap to place feature
        """
        x, y = SQUARE_SIZE / 2, SQUARE_SIZE / 2
        colors = ["green","white"]
        for _ in range(8):
            x = SQUARE_SIZE/2
            for i in range(8):
                if i % 2 == 0:
                    self.board.append(Square(colors[0], x, y))
                    # arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.BLACK)
                else:
                    self.board.append(Square(colors[1], x, y))
                    # arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.WHITE)
                x += SQUARE_SIZE
            colors.reverse()
            y += SQUARE_SIZE

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Set up variables for pieces
        half_square, stop = SQUARE_SIZE/2, 8*SQUARE_SIZE
        x_list = [i for i in range(int(half_square), int(stop), int(SQUARE_SIZE))]
        y_list = [SQUARE_SIZE/2, SQUARE_SIZE * 1.5, SQUARE_SIZE * 6.5, SQUARE_SIZE * 7.5]
        y_list = [int(i) for i in y_list]
        back_row = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
        
        # White Side
        [self.white_set.append(Piece("white", "Pawn", x, y_list[1], 1)) for x in x_list]
        [self.white_set.append(Piece("white", title, x, y_list[0], 1)) for x, title in zip(x_list, back_row)]

        # Black Side
        [self.black_set.append(Piece("black", "Pawn", x, y_list[2], 1)) for x in x_list]
        [self.black_set.append(Piece("black", title, x, y_list[3], 1)) for x, title in zip(x_list, back_row)]

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.draw_board()
        arcade.start_render()
        self.board.draw()
        
        self.white_set.draw()
        self.black_set.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button. """
        if self.turn:
            piece = arcade.get_sprites_at_point((x, y), self.white_set)
        else:
            piece = arcade.get_sprites_at_point((x, y), self.black_set)

        if len(piece) > 0:
            self.piece_in_hand = piece[0]
            self.original_location = self.piece_in_hand.position

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.piece_in_hand is not None:
            self.piece_in_hand.center_x += dx
            self.piece_in_hand.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Who's turn is it
        # arcade.get_sprites_at_point() returns a python list of sprites at the cursors location
        if self.turn:
            piece = arcade.get_sprites_at_point((x, y), self.black_set)
        else:
            piece = arcade.get_sprites_at_point((x, y), self.white_set)

        # if there is no sprite at my mouse location
        if len(piece) == 0:
            # drop the sprite
            if self.piece_in_hand is not None:
                mat = arcade.get_closest_sprite(self.piece_in_hand, self.board)
                self.piece_in_hand.position = mat[0].position
                self.turn = not self.turn
                self.piece_in_hand = None
            return
        
        # if there is a sprite at my mouse location
        elif len(piece) == 1:
            # If piece at current position is a dif color then kill it
            if piece[0].bw != self.piece_in_hand.bw:
                mat = arcade.get_closest_sprite(self.piece_in_hand, self.board)
                self.piece_in_hand.position = mat[0].position
                self.turn = not self.turn
                self.piece_in_hand = None
                piece[0].kill()

def main():
    """ Main method """
    window = MyGame()
    window.draw_board()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
