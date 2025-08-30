"""
Encryptor Module
This module embeds a hidden message into an image using a custom steganography algorithm with a Kuwahara filter preprocessing.
"""

import numpy as np
from PIL import Image
from filters import kuwahara

def encrypt_image(image_path, message):
    """
    Encrypts a message into the provided image.

    Parameters:
        image_path (str): Path to the base image.
        message (str): Message to hide in the image.

    Returns:
        PIL.Image: Encrypted image containing the hidden message.
    """
    letters = [
        "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
        "q","r","s","t","u","v","w","x","y","z"," ",".",",","?","!","¿","¡",
        "(",")",":",";","-","\"","'","á","é","í","ó","ú","ü","ñ"
    ]
    codes = list(range(1, 48))
    
    # Convert message to numeric representation
    message_numbers = []
    message = message.lower()
    for letter in message:
        number = codes[letters.index(letter)]
        if number < 10:
            message_numbers.append(number + 1)
            message_numbers.append(-1)
        else:
            message_numbers.extend([int(d) + 1 for d in str(number)])
            message_numbers.append(-1)
    message_numbers.append(0)

    # Load image and apply Kuwahara filter
    image = Image.open(image_path)
    filtered_image = kuwahara(image)
    pixels = np.array(filtered_image)
    height, width, channels = pixels.shape

    message_index = 0
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            block = pixels[y:y+2, x:x+2, :]
            selected_pixels = np.array([
                block[:, :, 0].flatten()[0:3],
                block[:, :, 1].flatten()[0:3],
                block[:, :, 2].flatten()[0:3]
            ])
            variances = np.var(selected_pixels, axis=1)
            channel_min_var = np.argmin(variances)

            avg_channel = np.mean(selected_pixels[channel_min_var])
            val_encrypted = (avg_channel + message_numbers[message_index]) % 256
            pixels[y+1, x+1, channel_min_var] = int(val_encrypted)
            message_index += 1
            if message_index >= len(message_numbers):
                break
        if message_index >= len(message_numbers):
            break

    return Image.fromarray(pixels.astype('uint8'))

def main():
    print("≡≡ Image Encryptor ≡≡")
    image_exists = False
    while not image_exists:
        file_name = input("Enter base image filename (.png): ")
        if file_name.lower().endswith(".png"):
            try:
                _ = Image.open(file_name)
                image_exists = True
            except FileNotFoundError:
                print(f"File {file_name} not found.")
        else:
            print("File must have .png extension.")

    message_to_hide = input("Enter message to hide: ")
    output_file = input("Enter output filename (.png): ")
    while not output_file.lower().endswith(".png"):
        print("Output file must have .png extension.")
        output_file = input("Enter output filename (.png): ")

    encrypted_image = encrypt_image(file_name, message_to_hide)
    encrypted_image.save(output_file)
    print(f"Encrypted image saved as {output_file}")

if __name__ == "__main__":
    main()
