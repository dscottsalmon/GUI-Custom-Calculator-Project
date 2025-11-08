#using tutorial https://youtu.be/mop6g-c5HEY?si=IoHiZNpIlG9HckNe as an example to learn GUI basics in python

import tkinter as tk
import math
#from tkinter import ttk
import ttkbootstrap as ttk

def convert():
    mile = entry_int.get()
    conversion = 1.60934
    km = mile*conversion

    rinks = km/(61/1000) #61m per rink NA standard
    fields = km/(109.7/1000) #109.7m per football field
    tacobell = round(km*mile*math.pi) #something i randomly made up for fun

    input_string.set("You've given me a distance of %0.2f miles, which can be converted to: %0.2f km"%(mile, km))
    output_string.set("You silly Yankee. If we're going to use stupid units, lets use fun ones like how\nthis distance is also equal to:\n\n\t\t\t- %i football fields\n\n\t\t\t- %i hockey rinks,\n\n\t\t\t- %i taco bells."%(fields,rinks,tacobell))

# window
window = ttk.Window(themename= 'journal')
window.title('Imperial Measurements are stupid')
window.geometry('1080x800')

# title
title_label = ttk.Label(master= window, text= 'Convert from American to Canadian', font = 'Calibri 24 bold')
title_label.pack()

# input field and button
input_frame = ttk.Frame(master= window)
entry_int = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable = entry_int)
button = ttk.Button(master=input_frame, text = "Convert", command = convert)
entry.pack(side='left', padx = 15)
button.pack(side='left')
input_frame.pack(pady = 20)

# input label
input_string = tk.StringVar()
input_label = ttk.Label(master=window, text= 'Input', font = 'Calibri 18', textvariable = input_string)
input_label.pack(pady = 10)

# output
output_string = tk.StringVar()
output_label = ttk.Label(
    master=window, 
    text= 'Output:', 
    font = 'Calibri 18', 
    textvariable = output_string)
output_label.pack()

# run
window.mainloop()