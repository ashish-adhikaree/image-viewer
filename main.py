import tkinter as tk
from app import App
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    root = tk.Tk()
    app = App(root)
    root.mainloop()