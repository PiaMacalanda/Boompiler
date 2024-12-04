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

        # Define themes
        self.themes = {
            "light": {
                "bg": "#f7f4ef",
                "sidebar_bg": "#eaf3d9",
                "button_bg": "#f7f4ef",
                "button_fg": "#333",
                "text_bg": "white",
                "text_fg": "black",
                "result_bg": "lightyellow",
                "result_fg": "black",
            },
            "dark": {
                "bg": "#2b2b2b",
                "sidebar_bg": "#3c3c3c",
                "button_bg": "#4c4c4c",
                "button_fg": "white",
                "text_bg": "#1e1e1e",
                "text_fg": "white",
                "result_bg": "#2e2e2e",
                "result_fg": "white",
            }
        }
        self.current_theme = "light"  # Default theme

        # Initialize analyzers
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntax_analyzer = SyntaxAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer()

        # Create UI elements
        self.initialize_ui()

    def initialize_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.themes[self.current_theme]["sidebar_bg"], width=150)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        button_style = {"bg": self.themes[self.current_theme]["button_bg"],
                        "fg": self.themes[self.current_theme]["button_fg"],
                        "bd": 2, "relief": "groove", "font": ("Arial", 10, "bold")}

        self.open_file_button = tk.Button(self.sidebar, text="Open File", command=self.open_file, **button_style)
        self.lexical_analysis_button = tk.Button(self.sidebar, text="Lexical Analysis", command=self.lexical_analysis, state="disabled", **button_style)
        self.syntax_analysis_button = tk.Button(self.sidebar, text="Syntax Analysis", command=self.syntax_analysis, state="disabled", **button_style)
        self.semantic_analysis_button = tk.Button(self.sidebar, text="Semantic Analysis", command=self.semantic_analysis, state="disabled", **button_style)
        self.clear_button = tk.Button(self.sidebar, text="Clear", command=self.clear, **button_style)
        self.theme_toggle_button = tk.Button(self.sidebar, text="Dark Mode", command=self.toggle_theme, **button_style)

        # Pack buttons
        for button in [self.open_file_button, self.lexical_analysis_button, self.syntax_analysis_button,
                       self.semantic_analysis_button, self.clear_button, self.theme_toggle_button]:
            button.pack(fill="x", pady=5)
            self.add_hover_effect(button)

        # Main Content Area
        self.main_content = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.code_label = tk.Label(self.main_content, text="CODE:", bg=self.themes[self.current_theme]["bg"], font=("Arial", 10, "bold"))
        self.code_label.pack(anchor="w")

        self.code_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid",
                                 bg=self.themes[self.current_theme]["text_bg"], fg=self.themes[self.current_theme]["text_fg"])
        self.code_text.pack(fill="both", expand=True, pady=5)

        self.result_label = tk.Label(self.main_content, text="RESULT:", bg=self.themes[self.current_theme]["bg"], font=("Arial", 10, "bold"))
        self.result_label.pack(anchor="w")

        self.result_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid",
                                   bg=self.themes[self.current_theme]["result_bg"], fg=self.themes[self.current_theme]["result_fg"])
        self.result_text.pack(fill="both", expand=True, pady=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Java files", "*.java")])
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

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_toggle_button.config(text="Light Mode")
        else:
            self.current_theme = "light"
            self.theme_toggle_button.config(text="Dark Mode")

        theme = self.themes[self.current_theme]
        self.root.config(bg=theme["bg"])
        self.sidebar.config(bg=theme["sidebar_bg"])
        self.code_text.config(bg=theme["text_bg"], fg=theme["text_fg"])
        self.result_text.config(bg=theme["result_bg"], fg=theme["result_fg"])

        # Update button styles
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=theme["button_bg"], fg=theme["button_fg"])

    def add_hover_effect(self, button):
        def on_enter(event):
            button.config(bg="#d4e2c3", relief="raised")

        def on_leave(event):
            theme = self.themes[self.current_theme]
            button.config(bg=theme["button_bg"], relief="groove")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCompilerGUI(root)
    root.mainloop()
