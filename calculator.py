import tkinter as tk
import math
import ttkbootstrap as ttk

def number(input):
    print(input)
    current = display_var.get()
    display_var.set(current + str(input))

def clear():
    print("cleared input")
    display_var.set("")

def sign():
    print("flipped sign")
    current = display_var.get()
    if current[0] == '-':
        display_var.set(current[1:])
    else:
        display_var.set("-" + current)

# window
window = ttk.Window(themename= 'darkly')
window.title('Calculator')

style = ttk.Style()
style.configure("Custom.TLabel", foreground="white", background="darkgray")


# title
title_label = ttk.Label(master= window, text= 'Calculator', font = 'Calibri 24 bold', style='Custom.TLabel')
title_label.pack(pady=20, padx=20)

top_frame = ttk.Frame(master=window)
top_frame.pack(anchor='center', pady=(0,10))

buttonquit = ttk.Button(master=top_frame, text = "Quit", command = window.destroy, bootstyle="danger", width=8)
buttonclear = ttk.Button(master=top_frame, text = "Clear", command = clear, bootstyle="info",width=8)
buttonquit.pack(side='right', pady=10)
buttonclear.pack(side='right', pady=10)

display_frame = ttk.Frame(master=window)
display_frame.pack(pady=20)
display_var = tk.StringVar()
display_box = ttk.Label(master=display_frame, textvariable=display_var, font=('Calibri', 28), justify='right')
display_box.pack(ipadx=10, ipady=10, fill='x', padx=40)
display_box.configure(background='white',foreground='black')

# input field and button
input_frame = ttk.Frame(master= window)
input_frame.pack(pady = 20)

# Create 3x3 grid of buttons
buttons = []
num = 1
for row in range(3):
    for col in range(3):
        btn = ttk.Button(
            master=input_frame,
            text=str(num),
            command=lambda x=num: number(x),
            width=8
        )
        btn.grid(row=row, column=col, padx=15, pady=15)
        buttons.append(btn)
        num += 1

# === 4th row: +/-  0  . ===
ttk.Button(input_frame, text="+/-", command=lambda: sign(), width=8).grid(row=3, column=0, padx=15, pady=15)
ttk.Button(input_frame, text="0", command=lambda: number(0), width=8).grid(row=3, column=1, padx=15, pady=15)
ttk.Button(input_frame, text=".", command=lambda: number('.'), width=8).grid(row=3, column=2, padx=15, pady=15)

# run
window.mainloop()