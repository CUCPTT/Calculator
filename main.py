import tkinter as tk
from tkinter import ttk
import pandas as pd
from lexicalAnalyse import lexer

def toggle_sign(entry):
    current_input = entry.get()
    if current_input:
        if current_input[0] == "-":
            entry.delete(0)
        else:
            entry.insert(0, "-")

def create_calculator_gui():
    root = tk.Tk()
    root.title("github.com/CUCPTT/Calculator")
    root.resizable(False, False)

    # 设置窗口图标
    root.iconbitmap("misc/favicon.ico")

    history_list = tk.Listbox(root, width=30, height=5, font=("Arial", 16), bg="white", relief="flat")
    history_list.grid(row=0, column=0, columnspan=6)

    entry = tk.Entry(root, width=30, font=("Arial", 16), relief="flat")
    entry.grid(row=1, column=0, columnspan=6)

    # 加载CSV文件
    data = pd.read_csv("misc/GUI.csv", header=None)
    button_texts = data.values.flatten()

    # 设置按钮样式
    style = ttk.Style(root)
    style.theme_create("custom_theme", parent="alt", settings={
        "Custom.TButton": {
            "configure": {"background": "white", "width": 4, "font": ("Arial", 16),
                           "bordercolor": "black", "relief": tk.FLAT, "borderwidth": 10, "borderradius": 0}
        },
        "Equal.TButton": {
            "configure": {"background": "light gray", "width": 4, "font": ("Arial", 16),
                           "bordercolor": "black", "relief": tk.FLAT, "borderwidth": 10, "borderradius": 0}
        }
    })
    style.theme_use("custom_theme")

    # 生成按钮
    row_count = 2
    for i, button_text in enumerate(button_texts):
        if button_text == "CE":
            # 创建删除按钮
            button = ttk.Button(root, text=button_text, command=lambda: entry.delete(len(entry.get())-1), style="Custom.TButton")
        elif button_text == "C":
            # 创建清空按钮
            button = ttk.Button(root, text=button_text, command=lambda: entry.delete(0, tk.END), style="Custom.TButton")
        elif button_text == "=":
            button = ttk.Button(root, text=button_text, command=lambda: calculate(entry, history_list), style="Equal.TButton")
        elif button_text == "+/-":
            button = ttk.Button(root, text=button_text, command=lambda: toggle_sign(entry), style="Custom.TButton")
        else:
            button = ttk.Button(root, text=button_text, command=lambda txt=button_text: entry.insert(tk.END, txt), style="Custom.TButton")
        
        button.grid(row=row_count, column=(i % 5))

        # 判断是否需要换行
        if (i + 1) % 5 == 0:
            row_count += 1

    root.mainloop()

from ReversePN import RPN
from analysis import analyse, show

def calculate(entry, history_list):
    current_input = entry.get()
    if not current_input.startswith("Error"):
        token = lexer(current_input)
        if str(token).startswith("Error"):
            entry.delete(0, tk.END)
            entry.insert(0, token)
            return
        tokens = token.copy()
        table_text, string, info = analyse(tokens)
        if str(info).startswith("Error"):
            entry.delete(0, tk.END)
            entry.insert(0, info)
            show(table_text, string)
            return
        result = RPN(token)
        if str(result).startswith("Error"):
            entry.delete(0, tk.END)
            entry.insert(0, result)
        else:
            history_list.insert(0, current_input + "=\n")
            history_list.insert(1, str(result) + "\n")
            entry.delete(0, tk.END)
            entry.insert(0, str(result))
            show(table_text, string)
    else:
        entry.delete(0, tk.END)

if __name__ == "__main__":
    create_calculator_gui()