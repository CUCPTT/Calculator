import tkinter as tk
from tkinter import ttk
import pandas as pd
from lexicalAnalyse import lexer

def calculate():
    current_input = entry.get()
    if current_input:
        print(lexer(current_input))
        history_text.insert(1.0, current_input + "=\n")
        entry.delete(0, tk.END)

def toggle_sign():
    current_input = entry.get()
    if current_input:
        if current_input[0] == "-":
            entry.delete(0)
        else:
            entry.insert(0, "-")

def create_calculator_gui():
    global entry 
    window = tk.Tk()
    window.title("https://github.com/CUCPTT/Calculator")
    window.resizable(False, False)

    # 设置窗口图标
    window.iconbitmap("misc/favicon.ico")

    global history_text
    history_text = tk.Text(window, width=30, height=5, font=("Arial", 16), bg="white", relief="flat")
    history_text.grid(row=0, column=0, columnspan=6)

    entry = tk.Entry(window, width=30, font=("Arial", 16), relief="flat")
    entry.grid(row=1, column=0, columnspan=6)

    # 加载CSV文件
    data = pd.read_csv("misc/GUI.csv", header=None)
    button_texts = data.values.flatten()

    # 设置按钮样式
    style = ttk.Style(window)
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
            button = ttk.Button(window, text=button_text, command=lambda: entry.delete(len(entry.get())-1), style="Custom.TButton")
        elif button_text == "C":
            # 创建清空按钮
            button = ttk.Button(window, text=button_text, command=lambda: entry.delete(0, tk.END), style="Custom.TButton")
        elif button_text == "=":
            # 创建特殊样式的按钮
            button = ttk.Button(window, text=button_text, command=lambda: [calculate(), entry.delete(0, tk.END)], style="Equal.TButton")
        elif button_text == "+/-":
            # 创建切换正负号按钮
            button = ttk.Button(window, text=button_text, command=toggle_sign, style="Custom.TButton")
        else:
            # 创建普通按钮
            button = ttk.Button(window, text=button_text, command=lambda txt=button_text: entry.insert(tk.END, txt), style="Custom.TButton")
        
        button.grid(row=row_count, column=(i % 5))

        # 判断是否需要换行
        if (i + 1) % 5 == 0:
            row_count += 1

    window.mainloop()

if __name__ == "__main__":
    create_calculator_gui()