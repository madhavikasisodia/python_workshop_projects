import tkinter as tk
from tkinter import ttk
import math

class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calculator")
        self.root.geometry("400x580")
        self.mode = 'light'
        self.expression = ''

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.create_top_bar()
        self.create_widgets()
        self.apply_theme()

    def create_top_bar(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5, anchor='ne')

        self.toggle_var = tk.IntVar(value=0)
        self.toggle_slider = tk.Checkbutton(
            top_frame,
            text="🌞",  # Default to sun
            variable=self.toggle_var,
            onvalue=1, offvalue=0,
            command=self.toggle_mode,
            font=("Arial", 12),
            indicatoron=False,
            width=4,
            bg="#ffffff",
            bd=0,
            relief="flat"
        )
        self.toggle_slider.pack(side='right')

    def create_widgets(self):
        self.input_field = tk.Entry(self.root, font=('Arial', 20), bd=5, relief=tk.FLAT, justify='right')
        self.input_field.pack(fill='x', padx=10, pady=10)

        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.history_box = tk.Text(self.history_frame, height=8, state='disabled', wrap='word')
        self.scrollbar = ttk.Scrollbar(self.history_frame, command=self.history_box.yview)
        self.history_box.configure(yscrollcommand=self.scrollbar.set)

        self.history_box.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        button_layout = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '√'],
            ['1', '2', '3', '-', '^'],
            ['0', '.', '=', '+', 'log'],
            ['sin', 'cos', 'tan', '(', ')']
        ]

        for row in button_layout:
            row_frame = tk.Frame(self.root)
            row_frame.pack(pady=2)
            for label in row:
                btn = tk.Button(
                    row_frame, text=label, width=6, height=2, font=('Arial', 12),
                    command=lambda val=label: self.handle_click(val)
                )
                btn.pack(side='left', padx=2)

        self.close_button = ttk.Button(self.root, text="Close Calculator", command=self.root.destroy)
        self.close_button.pack(pady=10)

    def apply_theme(self):
        bg_color = '#2e2e2e' if self.mode == 'dark' else '#ffffff'
        text_color = '#ffffff' if self.mode == 'dark' else '#000000'
        entry_color = '#3e3e3e' if self.mode == 'dark' else '#f0f0f0'

        self.root.configure(bg=bg_color)
        self.input_field.configure(bg=entry_color, fg=text_color, insertbackground=text_color)
        self.history_box.configure(bg=entry_color, fg=text_color)
        self.history_frame.configure(bg=bg_color)
        self.toggle_slider.configure(
            bg=bg_color,
            fg=text_color,
            activebackground=bg_color,
            text="🌙" if self.mode == 'dark' else "🌞"
        )

    def toggle_mode(self):
        self.mode = 'dark' if self.toggle_var.get() == 1 else 'light'
        self.apply_theme()

    def handle_click(self, value):
        if value == 'C':
            self.expression = ''
            self.input_field.delete(0, tk.END)
        elif value == '=':
            try:
                result = str(eval(self.transform_expression(self.expression)))
                self.update_history(self.expression + " = " + result)
                self.input_field.delete(0, tk.END)
                self.input_field.insert(tk.END, result)
                self.expression = result
            except Exception:
                self.input_field.delete(0, tk.END)
                self.input_field.insert(tk.END, "Error")
                self.expression = ''
        else:
            self.expression += value
            self.input_field.delete(0, tk.END)
            self.input_field.insert(tk.END, self.expression)

    def transform_expression(self, expr):
        expr = expr.replace('√', 'math.sqrt')
        expr = expr.replace('^', '**')  # Power operator
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('sin', 'math.sin(math.radians')
        expr = expr.replace('cos', 'math.cos(math.radians')
        expr = expr.replace('tan', 'math.tan(math.radians')

        for fn in ['sin', 'cos', 'tan']:
            expr = expr.replace(f'math.{fn}(math.radians', f'math.{fn}(math.radians(')

        return expr

    def update_history(self, text):
        self.history_box.configure(state='normal')
        self.history_box.insert(tk.END, text + '\n')
        self.history_box.configure(state='disabled')
        self.history_box.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCalculator(root)
    root.mainloop()
