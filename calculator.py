import tkinter as tk
import time
import ttkbootstrap as ttk
import re
import ast
import operator
import math

# ------------------------
# Helper functions
# ------------------------

def format_number(num, for_display=False):
    """
    Format number for display or input.
    """
    try:
        n = float(num)
    except Exception:
        # Always return string for non-numeric input
        return str(num)

    # Very large numbers -> scientific notation
    if abs(n) >= 1e9:
        return f"{n:.2e}"

    if for_display:
        # Round to 8 decimal places for final results
        n = round(n, 8)
        s = f"{n:,.8f}".replace(",", " ")
        s = s.rstrip('0').rstrip('.')  # remove trailing zeros and dot if needed
        return s
    else:
        # Live input display — max 8 significant digits
        return f"{round(n, 8):.8g}"

def safe_calculate(expr):

    """Safely evaluate mathematical expressions."""
    expr = expr.replace('x', '*').strip()
    expr = expr.replace('^', '**').strip()
    
    try:
        # Create a safe namespace with only basic math operations
        safe_dict = {
            '__builtins__': {},
            'abs': abs,
            'round': round,
        }
        
        return eval(expr, safe_dict)
    
    except (SyntaxError, ValueError, ZeroDivisionError, NameError, TypeError) as e:
        raise ValueError(f"Calculation error: {str(e)}")

def science():
    """Toggle scientific calculator buttons beside the main keypad."""
    # First time setup
    if not hasattr(window, "science_buttons"):
        window.science_buttons = []
        window.science_visible = False

    # If currently visible → hide them
    if window.science_visible:
        for btn in window.science_buttons:
            btn.grid_forget()
        window.science_visible = False
        return

    # If currently hidden → show them
    window.science_buttons.clear()
    window.science_visible = True

    # Find the last used column in your keypad
    max_columns = max(len(row) for row in button_layout)

    sci_buttons = [
        ('sin', lambda: sci_insert('sin(')),
        ('cos', lambda: sci_insert('cos(')),
        ('tan', lambda: sci_insert('tan(')),
        ('√',   lambda: sci_insert('sqrt(')),
        ('x²',  lambda: sci_insert('^2')),
        ('xʸ',  lambda: sci_insert('^')),
        ('π',   lambda: sci_insert('3.1415926535')),
        ('e',   lambda: sci_insert('2.7182818284')),
        ('ln',  lambda: sci_insert('ln(')),
        ('log₁₀', lambda: sci_insert('log10(')),
        # Placeholder buttons
        ('a', lambda: sci_insert('a')),
        ('b', lambda: sci_insert('b')),
        ('c', lambda: sci_insert('c')),
        ('d', lambda: sci_insert('d')),
        ('e', lambda: sci_insert('e')),
        ('f', lambda: sci_insert('f')),
        ('g', lambda: sci_insert('g')),
        ('h', lambda: sci_insert('h')),
        ('i', lambda: sci_insert('i')),
        ('j', lambda: sci_insert('j')),
    ]

    # Create and place them to the right of the main keypad
    for i, (label, cmd) in enumerate(sci_buttons):
        btn = ttk.Button(
            master=input_frame,
            text=label,
            width=8,
            bootstyle="secondary",
            command=cmd
        )
        btn.grid(row=i % 5, column=max_columns + (i // 5), padx=15, pady=15)
        window.science_buttons.append(btn)

def sci_insert(text):
    """Insert scientific function text into the current expression."""
    global raw_expr, just_calculated
    if just_calculated:
        raw_expr = ""
        just_calculated = False
    raw_expr += str(text)
    update_display()

# ------------------------
# Calculator state
# ------------------------

just_calculated = False
last_result = None
calculation_count = 0
start_time = time.time()
raw_expr = ""  # unformatted input expression for calculations

# ------------------------
# Keyboard support
# ------------------------

def handle_key(event):
    key = event.keysym

    # Numbers
    if key.isdigit():
        number(key)

    # Operators
    elif key in ('plus', 'minus', 'asterisk', 'slash'):
        op_map = {'plus': '+', 'minus': '-', 'asterisk': 'x', 'slash': '/'}
        operator(op_map[key])

    # Decimal
    elif key in ('period', 'decimal'):
        number('.')

    # Enter / Return → =
    elif key in ('Return', 'KP_Enter'):
        calculate()

    # Backspace
    elif key == 'BackSpace':
        backspace()

    # +/- (map to some key, e.g., 'n' for negation)
    elif key == 'n':
        sign()

# ------------------------
# Display update
# ------------------------

def update_display():
    """Convert raw_expr to display string with formatted numbers and hide '*'."""
    if not raw_expr:
        display_var.set("")
        return

    # Replace internal '*' with nothing for display purposes
    expr_for_display = raw_expr.replace('*', '')

    tokens = expr_for_display.split(' ')
    display_tokens = []

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in '+-x/()':
            display_tokens.append(token)
        else:
            display_tokens.append(format_number(token, for_display=False))

    display_var.set(' '.join(display_tokens))

def update_ans_label():
    if last_result is not None:
        ans_label_var.set(f"ANS: {format_number(last_result, for_display=True)}")
    else:
        ans_label_var.set("ANS: ")

def update_runtime():
    elapsed = int(time.time() - start_time)
    runtime_var.set(f"Runtime: {elapsed}s | Calculations: {calculation_count}")
    window.after(1000, update_runtime)

# ------------------------
# Calculator functions
# ------------------------

def number(input_value):
    global just_calculated, raw_expr
    
    if just_calculated:
        raw_expr = ""
        just_calculated = False
    
    # If last character is an operator with space, don't add extra space
    if raw_expr and raw_expr[-1] == ' ':
        raw_expr += str(input_value)
    elif raw_expr and raw_expr[-1] in '+-x/':
        raw_expr += ' ' + str(input_value)
    else:
        raw_expr += str(input_value)
    
    update_display()


def clear():
    global just_calculated, raw_expr
    raw_expr = ""
    display_var.set("")
    just_calculated = False


def sign():
    global raw_expr, just_calculated, last_result

    # If just calculated, start new expression with negative last result
    if just_calculated and last_result is not None:
        raw_expr = format_number(-last_result, for_display=False)
        just_calculated = False
        update_display()
        return

    if not raw_expr.strip():
        raw_expr = "-"
        update_display()
        return

    # Split by operators (keeping spaces)
    tokens = raw_expr.split(' ')
    
    # Find the last number token
    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i] and tokens[i] not in '+-x/':
            # Found the last number
            if tokens[i].startswith('-'):
                tokens[i] = tokens[i][1:]  # Remove negative
            else:
                tokens[i] = '-' + tokens[i]  # Add negative
            break
    else:
        # No number found, add -1 at the end
        if tokens and tokens[-1] in '+-x/':
            tokens.append('-1')
    
    raw_expr = ' '.join(tokens)
    update_display()

def operator(op):
    global just_calculated, raw_expr, last_result

    if just_calculated:
        if last_result is not None:
            raw_expr = format_number(last_result, for_display=False)
        else:
            raw_expr = ""
        just_calculated = False

    # Don't allow operator at the start (except minus for negative numbers)
    if not raw_expr and op != '-':
        return
    
    # Don't allow consecutive operators (except minus after another operator)
    if raw_expr and raw_expr[-1] in '+-x/':
        if op == '-' and raw_expr[-1] != '-':
            # Allow minus after another operator (for negative numbers)
            raw_expr += ' ' + op
        else:
            # Replace the last operator
            raw_expr = raw_expr[:-1] + op
    else:
        # Normal case: add operator with spaces
        raw_expr += ' ' + op + ' '
    
    update_display()


def backspace():
    global raw_expr, just_calculated
    
    # If we just calculated, clear the result display and restore expression
    if just_calculated:
        if last_result is not None:
            raw_expr = format_number(last_result, for_display=False)
        else:
            raw_expr = ""
        just_calculated = False
        update_display()
        return
    
    # Normal backspace - remove last character
    if raw_expr:
        raw_expr = raw_expr[:-1].rstrip()  # Remove char and trailing spaces
        update_display()

def bracket():

    global raw_expr, just_calculated
    
    if just_calculated:
        raw_expr = ""
        just_calculated = False
    
    # Count current parenthesis balance
    open_count = raw_expr.count('(')
    close_count = raw_expr.count(')')
    
    # Determine what to insert next
    if open_count <= close_count:
        # Need to open a new parenthesis
        if not raw_expr:
            # Empty expression - just open
            raw_expr = "("
        elif raw_expr[-1] in '0123456789.)':
            # Number or closing bracket - implicit multiplication
            raw_expr += "*("
        else:
            # Operator or opening bracket - just open
            raw_expr += "("
    else:
        # Need to close an existing parenthesis
        if raw_expr and raw_expr[-1] in '(+-x/':
            # Don't close after operator or opening bracket
            # Insert 0 to make valid expression
            raw_expr += "0)"
        else:
            # Safe to close
            raw_expr += ")"
    
    update_display()


def calculate():
    global raw_expr, last_result, just_calculated, calculation_count
    if not raw_expr:
        return

    # Start from the current raw expression
    expression = raw_expr

    # Replace operators
    expression = expression.replace('x', '*')
    expression = expression.replace('^', '**')

    # Add math. prefix for trig and log functions
    functions = ['sin', 'cos', 'tan', 'sqrt', 'log10', 'ln']
    for f in functions:
        if f == 'ln':
            expression = expression.replace('ln', 'math.log')
        else:
            expression = expression.replace(f, f'math.{f}')

    # Strip trailing operators
    while expression and expression[-1] in '+-*/ ':
        expression = expression[:-1]

    try:
        total = eval(expression, {"__builtins__": None, "math": math})
        last_result = total
        calculation_count += 1
        just_calculated = True
    except Exception:
        total = 'Error'
        just_calculated = True
        raw_expr = ""

    # Update the display with the result
    lines = display_var.get().split('\n')
    if lines and lines[-1].startswith('='):
        lines = lines[:-1]
    lines.append(f"= {format_number(total, for_display=True)}")
    display_var.set('\n'.join(lines))

    update_ans_label()
    
def use_ans():
    global last_result, raw_expr, just_calculated
    if last_result is None:
        return

    # Always use the raw float value, not a formatted string
    ans_str = str(float(last_result))

    if just_calculated:
        raw_expr = ans_str
        just_calculated = False
        update_display()
        return

    if raw_expr and (raw_expr[-1].isdigit() or raw_expr[-1] == ')'):
        # Implicit multiply if ANS follows a number or bracket
        raw_expr += '*'
    elif raw_expr and raw_expr[-1] not in '+-x/ ':
        raw_expr += ' '

    raw_expr += ans_str
    update_display()


# ------------------------
# GUI Setup
# ------------------------

window = ttk.Window(themename='darkly')
window.bind('<Key>', handle_key)
window.title('Calculator')

style = ttk.Style()
style.configure("Custom.TLabel", foreground="white", background="darkgray")

title_label = ttk.Label(master=window, text='Calculator', font='Calibri 24 bold', style='Custom.TLabel')
title_label.pack(pady=20, padx=20)

top_frame = ttk.Frame(master=window)
top_frame.pack(anchor='center', pady=(0,10))
buttonscientific = ttk.Button(master=top_frame, text="Scientific", command=science, bootstyle="primary", width=8)
buttonquit = ttk.Button(master=top_frame, text="Quit", command=window.destroy, bootstyle="danger", width=8)
buttonclear = ttk.Button(master=top_frame, text="Clear", command=clear, bootstyle="info", width=8)
buttonscientific.pack(side='left', pady=10)
buttonquit.pack(side='right', pady=10)
buttonclear.pack(side='right', pady=10)

ans_label_var = tk.StringVar()
ans_label = ttk.Label(master=window, textvariable=ans_label_var, font=('Calibri', 14), foreground='gray')
ans_label.pack(anchor='w', padx=40)
update_ans_label()

display_frame = ttk.Frame(master=window)
display_frame.pack(pady=10, fill='x', expand=True)
display_var = tk.StringVar()
display_box = ttk.Label(master=display_frame,
                        textvariable=display_var,
                        font=('Calibri', 28),
                        justify='right',
                        anchor='e',
                        background='white',
                        foreground='black')
display_box.pack(ipadx=10, ipady=10, fill='x', padx=40, expand=True)

input_frame = ttk.Frame(master=window)
input_frame.pack(pady=20)

button_layout = [
    ['⌫', '( )', 'ANS', '/'],
    [7, 8, 9, 'x'],
    [4, 5, 6, '-'],
    [1, 2, 3, '+'],
    ['+/-', 0, '.', '=']
]

for r, row in enumerate(button_layout):
    for c, value in enumerate(row):
        if isinstance(value, str) and value not in ('x','-','+','=','+/-','.','/','ANS', "⌫", "( )"):
            btn = ttk.Button(master=input_frame, text=value, width=8, state='disabled')
        elif value == '+/-':
            btn = ttk.Button(master=input_frame, text=value, width=8, command=sign)
        elif value in ('+','-','x','/'):
            btn = ttk.Button(master=input_frame, text=value, width=8, command=lambda op=value: operator(op))
        elif value == "( )":
            btn = ttk.Button(master=input_frame, text=value, width=8, command=bracket)
        elif value == 'ANS':
            btn = ttk.Button(master=input_frame, text=value, width=8, command=use_ans)
        elif value == '=':
            btn = ttk.Button(master=input_frame, text='=', width=8, command=calculate)
        elif value == "⌫":
            btn = ttk.Button(input_frame, text='⌫', width=8, command=backspace)
        else:
            btn = ttk.Button(master=input_frame, text=str(value), width=8, command=lambda x=value: number(x))
        btn.grid(row=r, column=c, padx=15, pady=15)

runtime_var = tk.StringVar()
runtime_label = ttk.Label(master=window, textvariable=runtime_var, font=('Calibri', 12), foreground='gray')
runtime_label.pack(anchor='e', padx=40)
update_runtime()

window.mainloop()
