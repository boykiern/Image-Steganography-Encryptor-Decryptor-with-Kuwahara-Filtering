"""
Decryptor Module
This module provides functionality to decrypt a hidden message embedded in an image using a custom steganography technique.
"""

import numpy as np
from PIL import Image

def decrypt_image(encrypted_image):
    """
    Extracts the hidden message from an encrypted image.
    
    Parameters:
        encrypted_image (PIL.Image): Image containing the hidden message.
    
    Returns:
        str: The decrypted hidden message.
    """
    letters = [
        "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
        "q","r","s","t","u","v","w","x","y","z"," ",".",",","?","!","¿","¡",
        "(",")",":",";","-","\"","'","á","é","í","ó","ú","ü","ñ"
    ]
    codes = list(range(1, 48))

    pixels = np.array(encrypted_image)
    height, width, channels = pixels.shape

    encoded_values = []

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
            val_encrypted = (block[1, 1, channel_min_var] - int(avg_channel)) % 256
            if val_encrypted != -1 and val_encrypted < 0:
                val_encrypted += 256
            encoded_values.append(val_encrypted)
            if val_encrypted == 0:
                break
        if val_encrypted == 0:
            break

    adjusted_values = [(n - 1) if n != -1 and n != 0 else n for n in encoded_values]

    hidden_message = ''
    i = 0
    while i < len(adjusted_values):
        num = adjusted_values[i]

        # Combine digits if needed
        if i + 1 < len(adjusted_values):
            combined = num * 10 + adjusted_values[i + 1]
            if combined in codes:
                hidden_message += letters[codes.index(combined)]
                i += 2
                continue

        if num in codes:
            hidden_message += letters[codes.index(num)]
        i += 1

    return hidden_message

def main():
    print("≡≡ Image Decryptor ≡≡")
    image_exists = False
    while not image_exists:
        file_name = input("Enter the encrypted image filename (.png): ")
        if file_name.lower().endswith(".png"):
            try:
                encrypted_image = Image.open(file_name)
                image_exists = True
            except FileNotFoundError:
                print(f"File {file_name} not found.")
        else:
            print("File must have .png extension.")

    message = decrypt_image(encrypted_image)
    print(f"Hidden message: {message}")

if __name__ == "__main__":
    main()
