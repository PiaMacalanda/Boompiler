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

# Functions to analyze code
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

# Function to run lexical analysis
def run_lexical_analysis():
    input_text = code_text.get("1.0", tk.END).strip()
    if input_text:
        output_text.config(state=tk.NORMAL)  # Enable editing to clear the text area
        output_text.delete("1.0", tk.END)
        result = analyze_code(input_text)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)  # Disable editing after inserting results
    else:
        messagebox.showwarning("Warning", "Please enter some code to analyze.")

# Funtion to load file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, code)

# Function to delete input file and result
def delete_functionality():
    # Clear both the code input and the output text areas
    code_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)  # Enable editing to clear the text area
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)  # Disable editing again

# Placeholder functions for other analyses NOT WORKING YET!
def syntax_analysis():
    messagebox.showinfo("Syntax Analysis", "Syntax analysis functionality not implemented yet.")

def semantic_analysis():
    messagebox.showinfo("Semantic Analysis", "Semantic analysis functionality not implemented yet.")

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

# Additional buttons for other analyses. FOR SYNTAX AND SEMANTIC. NOT WORKING YET!
syntax_button = tk.Button(root, text="Run Syntax Analysis", command=syntax_analysis)
syntax_button.pack(pady=5)

semantic_button = tk.Button(root, text="Run Semantic Analysis", command=semantic_analysis)
semantic_button.pack(pady=5)

#----------

# Delete functionality button
delete_button = tk.Button(root, text="Delete All", command=delete_functionality)
delete_button.pack(pady=5)

# Output label and text area
tk.Label(root, text="Analysis Output:").pack(anchor="w", padx=10, pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state="normal")
output_text.pack(padx=10, pady=5, fill="x")

root.mainloop()
