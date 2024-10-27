import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# Define keywords and relational operators
keywords = {"auto", "break", "case", "char", "const", "while", "endl", "cin", "cout", "string", "sizeof", 
            "continue", "default", "catch", "try", "bool", "using", "sort", "unsigned", "void", "do", 
            "double", "else", "enum", "extern", "float", "for", "goto", "typedef", "union", "if", "int", 
            "long", "register", "return", "short", "signed", "struct", "switch", "static"}

relational_ops = {">", ">=", "<", "<=", "==", "!="}

def is_keyword(word):
    return word in keywords

def is_relational(op):
    return op in relational_ops

def analyze_code(input_text):
    result = []
    keystring = ""
    opstring = ""
    idstring = ""

    for ch in input_text:
        if ch in "(){}[]":
            result.append(f"Parenthesis: {ch}")
        
        if ch.isalpha():
            keystring += ch
            idstring += ch
        else:
            if keystring and is_keyword(keystring):
                result.append(f"Keyword: {keystring}")
            keystring = ""
            
            if idstring and not is_keyword(idstring):
                result.append(f"Identifier: {idstring}")
            idstring = ""
        
        if ch in "<>=!":
            opstring += ch
        else:
            if opstring and is_relational(opstring):
                result.append(f"Relational Operator: {opstring}")
            opstring = ""
    
    return "\n".join(result)

def run_lexical_analysis():
    input_text = code_text.get("1.0", tk.END).strip()
    if input_text:
        output_text.delete("1.0", tk.END)
        result = analyze_code(input_text)
        output_text.insert(tk.END, result)
    else:
        messagebox.showwarning("Warning", "Please enter some code to analyze.")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, code)

# GUI setup
root = tk.Tk()
root.title("Lexical Analyzer")
root.geometry("600x400")

# Input label and text area
tk.Label(root, text="Enter code here or load a file:").pack(anchor="w", padx=10, pady=5)
code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8)
code_text.pack(padx=10, fill="x")

# Load file button
load_button = tk.Button(root, text="Load File", command=load_file)
load_button.pack(pady=5)

# Run lexical analysis button
analyze_button = tk.Button(root, text="Run Lexical Analysis", command=run_lexical_analysis)
analyze_button.pack(pady=5)

# Output label and text area
tk.Label(root, text="Analysis Output:").pack(anchor="w", padx=10, pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state="normal")
output_text.pack(padx=10, pady=5, fill="x")

root.mainloop()
