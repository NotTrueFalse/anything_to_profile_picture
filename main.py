import hashlib
import random
from PIL import Image
import re
uuid_regex = "^[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$"
current_str = input("Enter your id / uuid / usrename / password (anything): ")
PFP_SIZE = 64
if re.match(uuid_regex, current_str):
    current_str = int(current_str.replace("-", ""), 16)
token = hashlib.sha3_512(str(current_str).encode()).hexdigest()
pixels = []

for i in range(0, len(token), 8):
    pixels.append(int(token[i:i+8], 16))
img = Image.new("RGB", (PFP_SIZE, PFP_SIZE))
final_pixels = []
for i in range(PFP_SIZE*4):
    random.seed(i)
    random.shuffle(pixels)
    for j in pixels:
        final_pixels.append(j)
img.putdata(final_pixels)
block_img=img.resize((1,1))
block_img = block_img.resize((PFP_SIZE//4,PFP_SIZE//4))
img = Image.new("RGB", (PFP_SIZE*4, PFP_SIZE*4))
#each X represent a bloc of 16 x 16 pixels
pattern_list = ["x"+"-"*14+"x",
                "xx"+"-"*12+"xx",
                "x-x-x-x--x-x-x-x",
                "x--"*5+"x",
                "xx----x--x----xx",
                "x"*16,
                "x"*7+"-"*2+"x"*7,
                ]
for i in range(16):
    random.seed(i+final_pixels[0])
    pattern = random.choice(pattern_list)
    for j in range(16):
        if pattern[j] == "x":
            img.paste(block_img, (int(j*(PFP_SIZE/4)),int(i*(PFP_SIZE/4))))
img.save("final.png")
