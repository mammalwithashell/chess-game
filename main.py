"""
Chess

"""
import arcade

# Screen title and size
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Chess"

SQUARE_SIZE = 64

"""
TODO:
Snap to place 
Only allow possible moves for each piece
Show possible moves when a piece is selected
Implement castling
"""


def draw_board():
    """
    :return: Draws a the black squares onto a white background to make a chess board
    """
    x, y = SQUARE_SIZE / 2, SQUARE_SIZE / 2

    for i in range(8):
        for _ in range(8):
            if i % 2 == 0:
                arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.ONYX)
            else:
                arcade.draw_rectangle_filled(x - SQUARE_SIZE, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.ONYX)
            x += SQUARE_SIZE * 2
        y += SQUARE_SIZE
        x = SQUARE_SIZE / 2


class Piece(arcade.Sprite):
    """ Piece sprite """

    def __init__(self, bw, value, scale):
        """ Piece Constructor """

        self.bw = bw
        self.value = value
        self.cstl_bool = None

        self.image_file_name = f"Sprites/{self.bw}{self.value}.png"
        super().__init__(self.image_file_name, scale)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.ANTIQUE_WHITE)
        self.turn = True
        self.piece_in_hand = None
        self.original_location = None

        self.white_set = None
        self.black_set = None

        self.white_pawns = None
        self.white_rook1 = None
        self.white_rook2 = None
        self.white_knight1 = None
        self.white_knight2 = None
        self.white_bishop1 = None
        self.white_bishop2 = None
        self.white_queen = None
        self.white_king = None

        self.black_pawns = None
        self.black_rook1 = None
        self.black_rook2 = None
        self.black_knight1 = None
        self.black_knight2 = None
        self.black_bishop1 = None
        self.black_bishop2 = None
        self.black_queen = None
        self.black_king = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.white_set = arcade.SpriteList()
        self.black_set = arcade.SpriteList()

        # White Pawns, create and append to sprite lists
        self.white_pawns = [Piece("white", "Pawn", 1) for _ in range(8)]
        [self.white_set.append(i) for i in self.white_pawns]

        # White Rooks, create and append to sprite lists
        self.white_rook1, self.white_rook2 = [Piece("white", "Rook", 1) for _ in range(2)]
        self.white_set.append(self.white_rook1)
        self.white_set.append(self.white_rook2)
        self.white_rook1.cstl_bool = True
        self.white_rook2.cstl_bool = True

        # White Bishops, create and append to sprite lists
        self.white_bishop1, self.white_bishop2 = [Piece("white", "Bishop", 1) for _ in range(2)]
        self.white_set.append(self.white_bishop1)
        self.white_set.append(self.white_bishop2)

        # White Knights, create and append to sprite lists
        self.white_knight1, self.white_knight2 = [Piece("white", "Knight", 1) for _ in range(2)]
        self.white_set.append(self.white_knight1)
        self.white_set.append(self.white_knight2)

        # White King & Queen
        self.white_king = Piece("white", "King", 1)
        self.white_queen = Piece("white", "Queen", 1)
        self.white_set.append(self.white_king)
        self.white_set.append(self.white_queen)
        self.white_king.cstl_bool = True

        # Assign all the positions
        back_row = [self.white_rook1, self.white_knight1, self.white_bishop1, self.white_queen, self.white_king,
                    self.white_bishop2, self.white_knight2, self.white_rook2]
        x, y = SQUARE_SIZE / 2, SQUARE_SIZE / 2
        for piece in back_row:
            piece.position = x, y
            x += SQUARE_SIZE
        self.white_king.cstl_bool = False
        self.white_rook1.cstl_bool = False
        self.white_rook2.cstl_bool = False

        x, y = SQUARE_SIZE / 2, (SQUARE_SIZE / 2 + SQUARE_SIZE)
        for i in self.white_pawns:
            i.center_x = x
            i.center_y = y
            x += SQUARE_SIZE

        # -------------------- BLACK STARTS HERE --------------------
        # Black Pawns
        self.black_pawns = [Piece("black", "Pawn", 1) for _ in range(8)]
        [self.black_set.append(i) for i in self.black_pawns]

        # Black Rooks, create and append to sprite lists
        self.black_rook1, self.black_rook2 = [Piece("black", "Rook", 1) for _ in range(2)]
        self.black_set.append(self.black_rook1)
        self.black_set.append(self.black_rook2)

        # Black Bishops, create and append to sprite lists
        self.black_bishop1, self.black_bishop2 = [Piece("black", "Bishop", 1) for _ in range(2)]
        self.black_set.append(self.black_bishop1)
        self.black_set.append(self.black_bishop2)

        # Black Knights, create and append to sprite lists
        self.black_knight1, self.black_knight2 = [Piece("black", "Knight", 1) for _ in range(2)]
        self.black_set.append(self.black_knight1)
        self.black_set.append(self.black_knight2)

        # Black King & Queen
        self.black_king = Piece("black", "King", 1)
        self.black_queen = Piece("black", "Queen", 1)
        self.black_set.append(self.black_king)
        self.black_set.append(self.black_queen)

        # Position back row of black pieces
        back_row = [self.black_rook1, self.black_knight1, self.black_bishop1, self.black_queen, self.black_king,
                    self.black_bishop2, self.black_knight2, self.black_rook2]
        x, y = SQUARE_SIZE / 2, SQUARE_SIZE / 2 + 7 * SQUARE_SIZE
        for piece in back_row:
            piece.position = x, y
            x += SQUARE_SIZE

        self.black_king.cstl_bool = False
        self.black_rook1.cstl_bool = False
        self.black_rook2.cstl_bool = False

        x, y = SQUARE_SIZE / 2, (SQUARE_SIZE / 2 + 6 * SQUARE_SIZE)
        for i in self.black_pawns:
            i.center_x = x
            i.center_y = y
            x += SQUARE_SIZE

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()
        draw_board()
        self.white_set.draw()
        self.black_set.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        if self.turn:
            piece = arcade.get_sprites_at_point((x, y), self.white_set)
        else:
            piece = arcade.get_sprites_at_point((x, y), self.black_set)

        if len(piece) > 0:
            self.piece_in_hand = piece[0]
            self.original_location = self.piece_in_hand.position

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        self.piece_in_hand.center_x += dx
        self.piece_in_hand.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        # arcade.get_sprites_at_point() returns a python list of sprites at the cursors location
        # who's turn is it
        if self.turn:
            cur = arcade.get_sprites_at_point((x, y), self.black_set)
        else:
            cur = arcade.get_sprites_at_point((x, y), self.white_set)

        # if there is a sprite at my mouse location
        if len(cur) > 0:
            # If piece at current position is a dif color then kill it
            if cur[0].bw != self.piece_in_hand.bw:
                cur[0].kill()

            """elif cur[0].value == "Rook" and self.piece_in_hand.value == "King" and self.piece_in_hand.cstl_bool is True:
                if cur[0].position[0] < self.piece_in_hand.position[0]:  # Left castle
                    # Position rook and then king
                    cur[0].center_x = self.piece_in_hand + 3 * SQUARE_SIZE
                    self.piece_in_hand.center_x -= 2 * SQUARE_SIZE
                else:  # Right castle white
                    cur[0].center_x = self.piece_in_hand.center_x + SQUARE_SIZE
                    self.piece_in_hand.center_x += SQUARE_SIZE * 2
            else:
                self.piece_in_hand.position = self.original_location"""

        if self.piece_in_hand is not None:
            self.turn = not self.turn
            self.piece_in_hand = None


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
