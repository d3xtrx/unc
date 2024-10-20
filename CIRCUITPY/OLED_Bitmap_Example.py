from board import SCL, SDA
import busio
import displayio
import adafruit_framebuf
from adafruit_display_text import label
import adafruit_displayio_sh1106

displayio.release_displays()

IMAGE = "/goofnug.bmp" # The path to the .BMP image you want to display
WIDTH = 130 # Change these to the right size for your display!
HEIGHT = 64
BORDER = 1

i2c = busio.I2C(SCL, SDA) # Create the I2C interface.
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT) # Create the SH1106 OLED class.

bitmap = displayio.OnDiskBitmap(IMAGE) # Setup the file as the bitmap data source
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader) # Create a TileGrid to hold the bitmap
group = displayio.Group() # Create a Group to hold the TileGrid
group.append(tile_grid) # Add the TileGrid to the Group
display.show(group) # Add the Group to the Display

while True: # Loop forever so you can enjoy your image
    pass # Write more code here :-)
