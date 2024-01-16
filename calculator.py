#Impoorting for GUI
import tkinter as tk
"""The following function handles button clicks. 
It takes the value of the clicked button and updates the display accordingly. 
It uses the eval function to evaluate the mathematical expression when the "=" button is clicked."""
def on_click(button_value):
    current_text = entry_var.get()
    
    if button_value == '=':
        try:
            result = eval(current_text)
            entry_var.set(result)
        except Exception as e:
            entry_var.set("Error")
    elif button_value == 'C':
        entry_var.set('')
    else:
        entry_var.set(current_text + str(button_value))

# Create main window
root = tk.Tk()
root.title("Calculator using tkinter and python")

# Entry widget for display
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, justify="left", font=('Arial', 20))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
    'C'
]

row_val = 1
col_val = 0

for button in buttons:
    tk.Button(root, text=button, width=5, height=3,
              command=lambda b=button: on_click(b)).grid(row=row_val, column=col_val, padx=5, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Function to handle keyboard input
def on_key(event):
    key = event.char
    if key.isdigit() or key in ['+', '-', '*', '/']:
        on_click(key)
    elif key == '\r':
        on_click('=')
    elif key == '\x08':
        on_click('C')

# Bind keyboard events to on_key function
root.bind('<Key>', on_key)

root.mainloop()
