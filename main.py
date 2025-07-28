from PIL import Image
import os

def encode(image_path, message, output_path=None):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size

    message += chr(0)  # Mark end of message with null char
    binary_message = ''.join(format(ord(c), '08b') for c in message)

    if len(binary_message) > width * height:
        raise ValueError("Message is too long for this image.")

    pixels = encoded.load()

    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_message[idx])  # Replace LSB of red channel
                pixels[x, y] = (r, g, b)
                idx += 1
            else:
                break

    if not output_path:
        base, _ = os.path.splitext(image_path)
        output_path = base + "_encoded.png"

    encoded.save(output_path)
    print(f"Message hidden! Saved as: {output_path}")

def decode(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    binary_message = ''
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)

    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''
    for c in chars:
        char = chr(int(c, 2))
        if char == chr(0):
            break
        message += char

    return message

def main():
    print("Hey! Welcome to the Steganography Tool.")
    while True:
        mode = input("What do you want to do? (encode / decode / exit): ").strip().lower()
        if mode == 'encode':
            image_path = input("Path to your image file: ").strip()
            message = input("What message do you want to hide? ")
            output_path = input("Where should I save the new image? (leave blank to auto-save): ").strip()
            if output_path == '':
                output_path = None
            try:
                encode(image_path, message, output_path)
            except Exception as e:
                print("Oops! Something went wrong:", e)
        elif mode == 'decode':
            image_path = input("Path to the image to decode: ").strip()
            try:
                hidden_message = decode(image_path)
                print("Here's the hidden message:")
                print(hidden_message)
            except Exception as e:
                print("Couldn't decode the message:", e)
        elif mode == 'exit':
            print("Thanks for using the tool! Bye!")
            break
        else:
            print("Please type either 'encode', 'decode', or 'exit'.")

if __name__ == "__main__":
    main()