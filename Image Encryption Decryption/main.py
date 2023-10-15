from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image

# Function to encrypt an image
def encrypt_image(input_image_path, output_image_path, password):
    # Generate a random salt
    salt = get_random_bytes(AES.block_size)

    # Derive a key using PBKDF2
    private_key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=1000000)
    # Print salt and private_key for debugging
    print("Salt:", salt)
    print("Private Key:", private_key)
    # Create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM)

    # Open and read the input image
    with Image.open(input_image_path) as image:
        # Convert the image to bytes
        image_bytes = image.tobytes()

        # Encrypt the image bytes
        ciphertext, tag = cipher.encrypt_and_digest(pad(image_bytes, AES.block_size))

    # Write the encrypted image data to the output file
    with open(output_image_path, 'wb') as image_file:
        image_file.write(salt + ciphertext)

# Function to decrypt an image
def decrypt_image(encrypted_image_path, output_image_path, password):
    # Read the salt and ciphertext
    with open(encrypted_image_path, 'rb') as image_file:
        salt = image_file.read(16)
        ciphertext = image_file.read()

    # Derive the private key using PBKDF2
    private_key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=1000000)
    # Print salt and private_key for debugging
    print("Salt:", salt)
    print("Private Key:", private_key)
    # Create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=salt)

    try:
        # Decrypt the image
        decrypted_image_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Create an Image object from the decrypted bytes
        with Image.frombytes("RGB", (image.width, image.height), decrypted_image_bytes) as image:
            image.save(output_image_path)
    except ValueError:
        print("Decryption failed. Padding is incorrect or the key is incorrect.")

# Example usage
input_image = "input.jpg"
encrypted_image = "encrypted.jpg"
decrypted_image = "decrypted.jpg"
password = "medhaMedha1"

# Encrypt the image
encrypt_image(input_image, encrypted_image, password)

# Decrypt the image
decrypt_image(encrypted_image, decrypted_image, password)
