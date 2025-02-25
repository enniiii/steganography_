import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_message(image_path, message, output_path):
    try:
        image = Image.open(image_path).convert('RGB')
        pixels = list(image.getdata())

        message += "\0"
        bits = ''.join(f'{ord(c):08b}' for c in message)
        if len(bits) > len(pixels):
            raise ValueError("Message is too long to fit in the image.")

        encoded_pixels = [
            (r & ~1 | int(bit), g, b) if i < len(bits) else (r, g, b)
            for i, ((r, g, b), bit) in enumerate(zip(pixels, bits))
        ] + pixels[len(bits):]

        image.putdata(encoded_pixels)
        image.save(output_path)
    except Exception as e:
        raise ValueError(f"Failed to encode message: {e}")


def decode_message(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        bits = ''.join(str(r & 1) for r, _, _ in image.getdata())

        message = ''.join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8))
        return message.split('\0', 1)[0]
    except Exception as e:
        raise ValueError(f"Failed to decode message: {e}")


def select_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)


def save_encoded_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    return file_path


def encode_action():
    image_path = image_path_var.get()
    message = message_var.get()
    
    if not image_path:
        messagebox.showerror("Error", "Please select an image.")
        return

    if not message:
        messagebox.showerror("Error", "Please enter a message to encode.")
        return

    output_path = save_encoded_image()
    if not output_path:
        return

    try:
        encode_message(image_path, message, output_path)
        messagebox.showinfo("Success", f"Message encoded and saved to {output_path}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def decode_action():
    image_path = image_path_var.get()
    
    if not image_path:
        messagebox.showerror("Error", "Please select an image.")
        return

    try:
        decoded_message = decode_message(image_path)
        if decoded_message:
            messagebox.showinfo("Decoded Message", f"The message is: {decoded_message}")
        else:
            messagebox.showwarning("No Message Found", "No hidden message found in the selected image.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x200")
root.configure(bg="#f0f0f0")

image_path_var = tk.StringVar()
message_var = tk.StringVar()

# Image Selection
frame1 = tk.Frame(root, bg="#f0f0f0")
frame1.pack(pady=10)

tk.Label(frame1, text="Image Path:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame1, textvariable=image_path_var, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame1, text="Browse", command=select_image).grid(row=0, column=2, padx=5, pady=5)

# Message Input
frame2 = tk.Frame(root, bg="#f0f0f0")
frame2.pack(pady=10)

tk.Label(frame2, text="Message:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame2, textvariable=message_var, width=40).grid(row=1, column=1, padx=5, pady=5)

# Buttons
frame3 = tk.Frame(root, bg="#f0f0f0")
frame3.pack(pady=20)

tk.Button(frame3, text="Encode Message", command=encode_action, width=20, bg="#0078D7", fg="white").grid(row=0, column=0, padx=10)
tk.Button(frame3, text="Decode Message", command=decode_action, width=20, bg="#0078D7", fg="white").grid(row=0, column=1, padx=10)

root.mainloop()