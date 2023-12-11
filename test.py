import tkinter as tk
from tkinter import ttk

def change_button_color():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_create("custom_theme", parent="alt", settings={
        "TButton": {
            "configure": {"background": "white"},
            "map": {
                "background": [("active", "grey")],
                "brodercolor": "black"
            }
        }
    })
    style.theme_use("custom_theme")

    button = ttk.Button(root, text="Custom Button")
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    change_button_color()