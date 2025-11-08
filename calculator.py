

import tkinter as tk
import math
#from tkinter import ttk
import ttkbootstrap as ttk

# window
window = ttk.Window(themename= 'darkly')
window.title('Calculator')
window.geometry('1080x800')

style = ttk.Style()
style.configure("Custom.TLabel", foreground="white", background="darkgray")

# title
title_label = ttk.Label(master= window, text= 'Calculator', font = 'Calibri 24 bold', style='Custom.TLabel')
title_label.pack(pady=20, padx=20)

# run
window.mainloop()