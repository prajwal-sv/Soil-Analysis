import base64

# Path to the image file
image_path = "./Black_5_hOjoxxW.jpg"

# Convert the image to Base64
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

print(base64_image)