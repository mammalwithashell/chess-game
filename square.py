from PIL import Image
import arcade

SCREEN_HEIGHT = 512

SQUARE_SIZE = int(SCREEN_HEIGHT/8)


img = Image.new("RGB", (SQUARE_SIZE,SQUARE_SIZE), color=arcade.color.AMAZON)
img.save("sprites/greenSquare.png")
