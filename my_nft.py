from PIL import Image 
from IPython.display import display 
import random
import json
import os

# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%
# IPFS: https://gateway.pinata.cloud/ipfs/QmfHXRWSkUrHJgMNGZCwUUhSu5vMKuoh45vAuNQsur4LEa

body = ["Pink", "White", "Blue"]
body_weights = [30, 60, 10]

eyes = ["Blue", "Black", "Red", "Yellow", "Green", "Pink", "Orange"]
eyes_weights = [5, 45, 20, 4, 11, 4, 11]

horn = ["Yellow", "Orange", "Pink", "Multi", "White"]
horn_weights = [3, 31, 30, 1, 35]

hair = ['Blue Hair', 'Pink Hair', 'White Hair', 'Multicolor']
hair_weights = [20, 38, 38, 4]

tail = ["Pink", "Gold", "Multicolor", "White"]
tail_weights = [50, 35, 10, 5]

wings = ['Pink', "Multicolor", "Gold", "Blue", "Red"]
wings_weights = [52, 24, 4, 14, 6]


# Classify traits

body_files = {
    "Pink": "body1",
    "White": "body2",
    "Blue": "body3"
}

eyes_files = {
    "Blue": "eyes1",
    "Black": "eyes2",
    "Red": "eyes3",
    "Yellow": "eyes4",
    "Green": "eyes5",
    "Pink": "eyes6",
    "Orange": "eyes7"
}

horn_files = {
    "Yellow": "horn1",
    "Orange": "horn2",
    "Pink": "horn3",
    "Multi": "horn4",
    "White": "horn5"
}

hair_files = {
    "Blue Hair": "hair1",
    "Pink Hair": "hair2",
    "White Hair": "hair3",
    "Multicolor": "hair4"
}


tail_files = {
    "Pink": "tail1",
    "Gold": "tail2",
    "Multicolor": "tail3",
    "White": "tail4"
}

wings_files = {
    "Pink": "wings1",
    "Multicolor": "wings2",
    "Gold": "wings3",
    "Blue": "wings4",
    "Red": "wings5"
}

# Generate Traits

TOTAL_IMAGES = 10  # Number of random unique images we want to generate

all_images = []


# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {}  #

    # For each trait category, select a random trait based on the weightings
    new_image["Body"] = random.choices(body, body_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Horn"] = random.choices(horn, horn_weights)[0]
    new_image["Hair"] = random.choices(hair, hair_weights)[0]
    new_image["Tail"] = random.choices(tail, tail_weights)[0]
    new_image["Wings"] = random.choices(wings, wings_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


print("Are all images unique?", all_images_unique(all_images))
# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)

# Get Trait Counts

body_count = {}
for item in body:
    body_count[item] = 0

eyes_count = {}
for item in eyes:
    eyes_count[item] = 0

horn_count = {}
for item in horn:
    horn_count[item] = 0

hair_count = {}
for item in hair:
    hair_count[item] = 0

tail_count = {}
for item in tail:
    tail_count[item] = 0

wings_count = {}
for item in wings:
    wings_count[item] = 0

for image in all_images:
    body_count[image["Body"]] += 1
    eyes_count[image["Eyes"]] += 1
    horn_count[image["Horn"]] += 1
    hair_count[image["Hair"]] += 1
    tail_count[image["Tail"]] += 1
    wings_count[image["Wings"]] += 1

print(body_count)
print(eyes_count)
print(horn_count)
print(hair_count)
print(tail_count)
print(wings_count)

# Generate Images

os.mkdir(f'./images')

for item in all_images:
    im1 = Image.open(f'./unicorn_parts/body/{body_files[item["Body"]]}.png').convert('RGBA')
    im2 = Image.open(f'./unicorn_parts/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
    im3 = Image.open(f'./unicorn_parts/horn/{horn_files[item["Horn"]]}.png').convert('RGBA')
    im4 = Image.open(f'./unicorn_parts/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')
    im5 = Image.open(f'./unicorn_parts/tail/{tail_files[item["Tail"]]}.png').convert('RGBA')
    im6 = Image.open(f'./unicorn_parts/wings/{wings_files[item["Wings"]]}.png').convert('RGBA')

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)

    # Convert to RGB
    rgb_im = com5.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)

os.mkdir(f'./metadata')
METADATA_FILE_NAME = './metadata/all-traits.json'
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

