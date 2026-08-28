from PIL import Image

def encode(image_path: str, message: str, output_path: str):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    pixels = image.load()
    bits = ""
    # Turn the message into one long string of bits, e.g. "H" -> "01001000"
    delimiter = '1111111100000000'
    bits += delimiter
    for char in message:
        bits += format(ord(char), "08b")
    bits+=delimiter
    bit_index = 0  # which bit of `bits` we're currently placing

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            channels = [r, g, b]

            for i in range(3):  # R, G, B
                if bit_index < len(bits):
                    bit = int(bits[bit_index])
                    channels[i] = (channels[i] & ~1) | bit
                    bit_index += 1
                # once we run out of bits, channels[i] is just left as-is

            pixels[x, y] = tuple(channels)

    image.save(output_path, "PNG")
    print(f"Encoded {len(message)} characters into {output_path}")


if __name__ == "__main__":
    encode("bob.png", "SECRET MESSAGE: skynet is coming... beware... ", "bobE.png")