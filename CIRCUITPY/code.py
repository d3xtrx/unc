import board
#import os 
import json
from wifi import radio
from socketpool import SocketPool
from busio import I2C
import displayio
from time import monotonic, sleep
import adafruit_displayio_sh1106
from adafruit_imageload import load
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Pull
import terminalio

displayio.release_displays()

WIFI_SSID = "wustl-guest-2.0"
radio.connect(WIFI_SSID)
print(radio.ipv4_address)
server_ip = "172.27.188.83"

pins = (board.IO9, board.IO18, board.IO11, board.IO7) # up, down, left, right
buttons = []   # will hold list of Debouncer objects
for pin in pins:   # set up each pin
    tmp_pin = DigitalInOut(pin) # defaults to input
    tmp_pin.pull = Pull.UP      # turn on internal pull-up resistor
    buttons.append( Debouncer(tmp_pin) )
print(pins)

WIDTH = 130
HEIGHT = 64
BORDER = 0
i2c = I2C(board.SCL, board.SDA) # create the I2C interface.
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT) # Create the SH1106 OLED class.
group = displayio.Group() # create a group to hold TileGrid
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF #black

qrcodeimg = "sprites/64pixel.bmp"

slime0 = "sprites/0unshaded24.bmp"
slime1 = "sprites/1unshaded12.bmp"
slime2 = "sprites/2unshaded12.bmp"
slime3 = "sprites/3unshaded12.bmp"
slime4 = "sprites/4unshaded16.bmp"

alt0 = "sprites/0AltUnshaded19.bmp"
alt1 = "sprites/1AltUnshaded12.bmp"
alt2 = "sprites/2AltUnshaded22.bmp"
alt3 = "sprites/3AltUnshaded25.bmp"
alt4 = "sprites/4AltUnshaded12.bmp"

active_avatar = slime0 
sentiment_verbage = ""

def get_frames(image):
  numberstr = image[-6:-4]
  framenum = int(numberstr)
  return framenum

def displayanimatedonce(image):
  pointer = 0 # current frame
  timer = 0 
  frames = get_frames(image)
  SPRITE_SIZE = (64, 64)
  icon_bit, icon_pal = load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)
  icon_grid = displayio.TileGrid(icon_bit, pixel_shader=color_palette,
  width=1, height=1, tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0], default_tile=0, x=32, y=0)
  group.append(icon_grid)
  display.show(group)
  while True:
    if (timer + 0.1) <  monotonic():
        icon_grid[0] = pointer
        pointer = (pointer + 1) % frames
        timer =  monotonic()
    for i, button in enumerate(buttons):
        button.update()
        if button.fell:
            print(f"{['up', 'down', 'left', 'right'][i]} button pressed!")
            group.remove(icon_grid)
            group.pop()
            display.show(group)
            return i
    sleep(0.01)

def displaystaticimage(image):
  frames = get_frames(image)
  background = displayio.OnDiskBitmap(image) 
  background_grid= displayio.TileGrid(background, pixel_shader=color_palette) 
  group.append(background_grid) 

  imagething = displayio.OnDiskBitmap(qrcodeimg)
  image_grid = displayio.TileGrid(imagething, pixel_shader=color_palette)
  group.append(image_grid)

  display.show(group) 
  while True:
    if (timer + 0.1) <  monotonic():
        icon_grid[0] = pointer
        pointer = (pointer + 1) % frames
        timer =  monotonic()
    for i, button in enumerate(buttons):
        button.update()
        if button.fell:
            print(f"{['up', 'down', 'left', 'right'][i]} button pressed!")
            group.remove(icon_grid)
            group.pop()
            display.show(group)
            return i
    sleep(0.01)
    
def displayanimatedhud(background, animatedimage):
    pointer = 0
    timer = 0
    print("qr code stuff")
    frames = get_frames(animatedimage)
    imagething = displayio.OnDiskBitmap(background)
    image_grid = displayio.TileGrid(imagething, pixel_shader=color_palette)
    group.append(image_grid)    
    SPRITE_SIZE = (64, 64)
    icon_bit, icon_pal = load(animatedimage, bitmap=displayio.Bitmap, palette=displayio.Palette)
    icon_grid = displayio.TileGrid(icon_bit, pixel_shader=color_palette,
    width=1, height=1, tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0], default_tile=0, x=64, y=0)
    group.append(icon_grid)
    display.show(group)

    loop_count = 0

    while loop_count >= 2:
        if (timer + 0.1) < monotonic():
            icon_grid[0] = pointer
            pointer = (pointer + 1) % frames
            timer = monotonic()
            if pointer == 0:
                loop_count += 1
    group.remove(icon_grid)
    group.remove(image_grid)
    display.show(group)
    return None

def displayqrcode(background):
    pointer = 0
    timer = 0
    button.update()
    print("qr code stuff")
    imagething = displayio.OnDiskBitmap(background)
    image_grid = displayio.TileGrid(imagething, pixel_shader=color_palette)
    group.append(image_grid)    
    display.show(group)
    sleep(1)
    group.remove(image_grid)
    display.show(group)
    return 0


def displayanimatedhudwithstats(animatedimage):
    pointer = 0
    timer = 0
    frames = get_frames(animatedimage)
    global sentiment_verbage

    calories_eaten = get_calories(server_ip)
    sentiment = get_sentiment(server_ip)
    if sentiment == 0:
        sentiment_verbage = "Very Upset"
    elif sentiment == 1:
        sentiment_verbage = "Upset"
    elif sentiment == 2:
        sentiment_verbage = "Neutral"
    elif sentiment == 3:
        sentiment_verbage = "Happy"
    elif sentiment == 4:
        sentiment_verbage = "Very Happy"
    avatar = get_avatar(server_ip)
    avatar_name = get_avatar_name(server_ip)

    bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    palette = displayio.Palette(2)
    palette[0] = 0x000000  # Black
    palette[1] = 0xFFFFFF  # White

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(tile_grid)

    text_area = label.Label(terminalio.FONT, text=f"Sentiment: {sentiment_verbage}\nCalories: {calories_eaten}\nAvatar: {avatar_name}", color=0xFFFFFF)
    text_area.x = 5
    text_area.y = 5
    group.append(text_area)

    SPRITE_SIZE = (64, 64)
    icon_bit, icon_pal = load(animatedimage, bitmap=displayio.Bitmap, palette=displayio.Palette)
    icon_grid = displayio.TileGrid(icon_bit, pixel_shader=color_palette,
    width=1, height=1, tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0], default_tile=0, x=64, y=0)
    group.append(icon_grid)
    display.show(group)

    while True:
        if (timer + 0.1) < monotonic():
            icon_grid[0] = pointer
            pointer = (pointer + 1) % frames
            timer = monotonic()
        for i, button in enumerate(buttons):
            button.update()
            if button.fell:
                print(f"{['up', 'down', 'left', 'right'][i]} button pressed!")
                group.remove(icon_grid)
                group.remove(text_area)
                group.remove(tile_grid)
                display.show(group)
                return i
        sleep(0.01)

def displayhomescreen(image):
    pointer = 0  # current frame
    timer = 0
    frames = get_frames(image)
    print(f"Detected frames: {frames}")
    SPRITE_SIZE = (64, 64) #change
    icon_bit, icon_pal = load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)
    print(f"Loaded image dimensions: {icon_bit.width}x{icon_bit.height}")
    icon_grid = displayio.TileGrid(icon_bit, pixel_shader=color_palette,
                                   width=1, height=1, 
                                   tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0],
                                   default_tile=0, x=32, y=0)
    group.append(icon_grid)
    display.show(group)
    while True:
        if (timer + 0.1) <  monotonic():
            icon_grid[0] = pointer
            pointer = (pointer + 1) % frames
            timer =  monotonic()
        for i, button in enumerate(buttons):
            button.update()
            if button.fell:
                print(f"{['up', 'down', 'left', 'right'][i]} button pressed!")
                group.remove(icon_grid)
                display.show(group)
                return i
        sleep(0.01)

def check_ip_online(ip_address, port=3000):
    try:
        socket = SocketPool(radio).socket()
        socket.connect((ip_address, port))
        socket.close()
        return True
    except Exception as e:
        print(f"Error checking IP: {e}")
        return False

def get_sentiment(server_ip):
    try:
        socket = SocketPool(radio).socket()
        socket.connect((server_ip, 3000))
        request = f"GET /get_sentiment HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        socket.send(request.encode())
        response = bytearray(4096)  # Adjust buffer size as needed
        received = 0
        while True:
            chunk = socket.recv_into(memoryview(response)[received:])
            if chunk == 0:
                break
            received += chunk
        socket.close()
        full_response = response[:received].decode()
        try:
            headers, body = full_response.split("\r\n\r\n", 1)
            data = json.loads(body)
            return data['sentiment']
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return None
    except Exception as e:
        print(f"Error fetching sentiment: {e}")
        return None

def get_avatar(server_ip):
    try:
        socket = SocketPool(radio).socket()
        socket.connect((server_ip, 3000))
        request = f"GET /get_avatar HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        socket.send(request.encode())
        response = bytearray(4096)  # Adjust buffer size as needed
        received = 0
        while True:
            chunk = socket.recv_into(memoryview(response)[received:])
            if chunk == 0:
                break
            received += chunk
        socket.close()
        full_response = response[:received].decode()
        try:
            headers, body = full_response.split("\r\n\r\n", 1)
            data = json.loads(body)
            return data['avatar']
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return None
    except Exception as e:
        print(f"Error fetching sentiment: {e}")
        return None

def get_avatar_name(server_ip):
    try:
        socket = SocketPool(radio).socket()
        socket.connect((server_ip, 3000))
        request = f"GET /get_avatar_name HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        socket.send(request.encode())
        response = bytearray(4096)  # Adjust buffer size as needed
        received = 0
        while True:
            chunk = socket.recv_into(memoryview(response)[received:])
            if chunk == 0:
                break
            received += chunk
        socket.close()
        full_response = response[:received].decode()
        try:
            headers, body = full_response.split("\r\n\r\n", 1)
            data = json.loads(body)
            return data['avatar_name']
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return None
    except Exception as e:
        print(f"Error fetching avatar_name: {e}")
        return None

def get_calories(server_ip):
    try:
        socket = SocketPool(radio).socket()
        socket.connect((server_ip, 3000))
        request = f"GET /get_calories HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        socket.send(request.encode())
        response = bytearray(4096)  # Adjust buffer size as needed
        received = 0
        while True:
            chunk = socket.recv_into(memoryview(response)[received:])
            if chunk == 0:
                break
            received += chunk
        socket.close()
        full_response = response[:received].decode()
        try:
            headers, body = full_response.split("\r\n\r\n", 1)
            data = json.loads(body)
            return data['calories_eaten']
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return None
    except Exception as e:
        print(f"Error fetching sentiment: {e}")
        return None

def set_slime(active_avatar):
    current_sentiment = get_sentiment(server_ip)
    avatar = get_avatar(server_ip)
    print(f"current sentiment is: {current_sentiment}")
    print(f"current avatar is: {avatar}")

    if avatar == 0:
        if current_sentiment == 0:
            active_avatar = slime0
        elif current_sentiment == 1:
            active_avatar = slime1
        elif current_sentiment == 2:
            active_avatar = slime2
        elif current_sentiment == 3:
            active_avatar = slime3
        elif current_sentiment == 4:
            active_avatar = slime4
        else:
            active_avatar = slime0
    elif avatar == 1:
        if current_sentiment == 0:
            active_avatar = alt0 
        elif current_sentiment == 1:
            active_avatar = alt1 
        elif current_sentiment == 2:
            active_avatar = alt2
        elif current_sentiment == 3:
            active_avatar = alt3
        elif current_sentiment == 4:
            active_avatar = alt4 
        else:
            active_avatar = alt0
    else:
        active_avatar = slime0
    return(active_avatar)

is_online = check_ip_online(server_ip)
if is_online:
    print(f"{server_ip} is reachable")
else:
    print(f"{server_ip} is offline")

active_avatar = set_slime(active_avatar)    

while True:
    pressed_button = displayhomescreen(active_avatar) #change to x=0 when he finishes the home thing
    if pressed_button == 0: #up
        active_avatar = set_slime(active_avatar)
        displayanimatedonce(active_avatar)
    elif pressed_button == 1:#down
        active_avatar = set_slime(active_avatar)
        displayhomescreen(active_avatar)
    elif pressed_button == 2:#left
        active_avatar = set_slime(active_avatar)
        displayanimatedhud(qrcodeimg, active_avatar) 
    elif pressed_button == 3:#right
        active_avatar = set_slime(active_avatar)
        displayanimatedhudwithstats(active_avatar)
    elif pressed_button == None: continue

    