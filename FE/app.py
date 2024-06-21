import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Mental Assistant")
    root.geometry("375x667")  # Size of an iPhone screen
    root.configure(bg='white')

    # Load the custom font
    inter_semi_bold = font.Font(family="Inter", size=24, weight="bold")

    # Add the image
    image_path = "/Users/klaudia/Documents/Mental_health_assistant/FE/resources/image_brain.png"
    image = Image.open(image_path)
    image = image.resize((450, 450), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Create a canvas to place the image and text
    canvas = tk.Canvas(root, width=375, height=500, bg='white', highlightthickness=0)
    canvas.pack()

    # Center the image on the canvas
    canvas.create_image(187.5, 380, image=photo)  # Center position for the image

    # Add the text above the image
    canvas.create_text(187.5, 180, text="Mental Assistant", font=inter_semi_bold, fill="#1DB981")

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
