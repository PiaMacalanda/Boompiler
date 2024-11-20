import tkinter as tk
from tkinter import filedialog, messagebox
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer


class MiniCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Boompiler")
        self.root.configure(bg="#f7f4ef")
        self.root.geometry("700x500")

        # Initialize analyzers
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntax_analyzer = SyntaxAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer()

        # Create UI elements
        self.initialize_ui()

    def initialize_ui(self):
        # Left Sidebar for Buttons
        self.sidebar = tk.Frame(self.root, bg="#eaf3d9", width=150)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        button_style = {"bg": "#f7f4ef", "fg": "#333", "bd": 2, "relief": "groove", "font": ("Arial", 10, "bold")}

        self.open_file_button = tk.Button(self.sidebar, text="Open File", command=self.open_file, **button_style)
        self.lexical_analysis_button = tk.Button(self.sidebar, text="Lexical Analysis", command=self.lexical_analysis, state="disabled", **button_style)
        self.syntax_analysis_button = tk.Button(self.sidebar, text="Syntax Analysis", command=self.syntax_analysis, state="disabled", **button_style)
        self.semantic_analysis_button = tk.Button(self.sidebar, text="Semantic Analysis", command=self.semantic_analysis, state="disabled", **button_style)
        self.clear_button = tk.Button(self.sidebar, text="Clear", command=self.clear, **button_style)

        self.open_file_button.pack(fill="x", pady=5)
        self.lexical_analysis_button.pack(fill="x", pady=5)
        self.syntax_analysis_button.pack(fill="x", pady=5)
        self.semantic_analysis_button.pack(fill="x", pady=5)
        self.clear_button.pack(fill="x", pady=5)

        # Main Content Area
        self.main_content = tk.Frame(self.root, bg="#f7f4ef")
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.code_label = tk.Label(self.main_content, text="CODE:", bg="#f7f4ef", font=("Arial", 10, "bold"))
        self.code_label.pack(anchor="w")

        self.code_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid")
        self.code_text.pack(fill="both", expand=True, pady=5)

        self.result_label = tk.Label(self.main_content, text="RESULT:", bg="#f7f4ef", font=("Arial", 10, "bold"))
        self.result_label.pack(anchor="w")

        self.result_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid", bg="lightyellow")
        self.result_text.pack(fill="both", expand=True, pady=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.display_code(code)
            self.enable_button(self.lexical_analysis_button)
        else:
            messagebox.showinfo("No file selected", "Please select a valid file.")

    def display_code(self, code):
        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", code)
        self.code_text.config(state="disabled")

    def display_result(self, result):
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, result + "\n")
        self.result_text.config(state="disabled")

    def clear(self):
        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        self.code_text.config(state="disabled")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        self.disable_all_buttons()
        self.enable_button(self.open_file_button)

    def disable_all_buttons(self):
        self.lexical_analysis_button.config(state="disabled")
        self.syntax_analysis_button.config(state="disabled")
        self.semantic_analysis_button.config(state="disabled")

    def enable_button(self, button):
        button.config(state="normal")

    def lexical_analysis(self):
        code = self.code_text.get("1.0", tk.END).strip()
        tokens, error = self.lexical_analyzer.tokenize(code)
        if error:
            self.display_result(error)
            return
        self.display_result("Lexical Analysis Success. Tokens:")
        for token in tokens:
            self.display_result(f"{token['type']}: {token['value']}")
        self.enable_button(self.syntax_analysis_button)
        self.lexical_analysis_button.config(state="disabled")

    def syntax_analysis(self):
        tokens = self.lexical_analyzer.tokenize(self.code_text.get("1.0", tk.END).strip())[0]
        result, error = self.syntax_analyzer.parse_syntax(tokens)
        if not result:
            self.display_result(error)
            return
        self.display_result("Syntax Analysis Success. Syntax Free.")
        self.enable_button(self.semantic_analysis_button)
        self.syntax_analysis_button.config(state="disabled")

    def semantic_analysis(self):
        tokens = self.lexical_analyzer.tokenize(self.code_text.get("1.0", tk.END).strip())[0]
        result, error = self.semantic_analyzer.check_semantics(tokens)
        if not result:
            self.display_result(error)
            return
        self.display_result("Semantic Analysis Success. Semantics Valid.")
        self.semantic_analysis_button.config(state="disabled")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCompilerGUI(root)
    root.mainloop()
