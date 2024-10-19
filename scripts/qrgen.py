import qrcode 
from PIL import Image

qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0.
        )
qr.add_data("https://leekspin.co/")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
resizedimg = img.resize((64,64), Image.NEAREST)
midsized= img.resize((32,32), Image.NEAREST)

img.save("og.bmp", "BMP")
resizedimg.save("64pixel.bmp", "BMP")
midsized.save("32.bmp", "BMP")
