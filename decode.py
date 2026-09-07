from PIL import Image

def decode(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    pixels = image.load()

    delimiter = '1111111100000000'
    bits = ""
    started = False   # have we found the START delimiter yet?
    found = False      # have we found the END delimiter yet? (used to break out)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            for value in (r, g, b):
                bits += str(value & 1)

                if bits.endswith(delimiter):
                    if not started:
                        started = True
                        bits = ""
                    else:
                        bits = bits[:-len(delimiter)]
                        found = True
                        break

                if found:
                    break
            if found:
                break   # exits `for x`
        if found:
            break       # exits `for y` -- this one was missing

    # Convert the collected message bits back into text, 8 bits at a time
    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))

    return message


if __name__ == "__main__":
    result = decode("bobE.png")
    print("Decoded message:", result)