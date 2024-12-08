import tkinter as tk
from tkinter import filedialog, messagebox
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer

class MiniCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Boompiler")
        self.root.geometry("1050x750")

        # Initialize analyzers
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntax_analyzer = SyntaxAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer()

        # Default mode is Light
        self.is_dark_mode = False

        # Setup UI (☞ﾟヮﾟ)☞
        self.initialize_ui()

    def initialize_ui(self):
        # Header setup
        self.header = tk.Frame(self.root, width=150)
        self.header.pack(side="top", fill="y", padx=10, pady=10)

        head_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 28, "bold")}
        self.headLabel = tk.Label(self.header, text="ִ ⸜(｡˃ ᵕ ˂ )⸝♡  BOOMPILER  ദ്ദി(˵ •̀ ᴗ - ˵ )", **head_style)
        self.headLabel.pack(pady=10)

        desc_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 12, "italic")}
        self.descLabel = tk.Label(self.header, text="---------- By Pia Macalanda, Juliana Mancera, & Thoby Ralleta ----------", **desc_style)
        self.descLabel.pack(pady=5)

        # Sidebar setup with buttons
        self.sidebar = tk.Frame(self.root, width=150)
        self.sidebar.pack(side="top", fill="y", padx=10, pady=10)

        button_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 12, "bold")}
        self.open_file_button = tk.Button(self.sidebar, text="Open File", command=self.open_file, **button_style, width=15)
        self.lexical_analysis_button = tk.Button(self.sidebar, text="Lexical Analysis", command=self.lexical_analysis, state="disabled", **button_style, width=15)
        self.syntax_analysis_button = tk.Button(self.sidebar, text="Syntax Analysis", command=self.syntax_analysis, state="disabled", **button_style, width=15)
        self.semantic_analysis_button = tk.Button(self.sidebar, text="Semantic Analysis", command=self.semantic_analysis, state="disabled", **button_style, width=15)
        self.clear_button = tk.Button(self.sidebar, text="Clear", command=self.clear, **button_style, width=15)
        self.toggle_mode_button = tk.Button(self.sidebar, text="࣪ ִֶָ☾.", command=self.toggle_mode, **button_style, width=5)

        # Pack buttons
        buttons = [
            self.open_file_button, self.lexical_analysis_button, self.syntax_analysis_button,
            self.semantic_analysis_button, self.clear_button, self.toggle_mode_button
        ]
        for button in buttons:
            button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
            self.add_hover_effect(button)

        # Main Content Area displaying code and results
        self.main_content = tk.Frame(self.root, padx=10, pady=10)
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.code_label = tk.Label(self.main_content, text="CODE:", font=("Arial", 12, "bold"))
        self.code_label.pack(anchor="w")
        self.code_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid", font=("Courier", 12, "normal"), state="disabled")
        self.code_text.pack(fill="both", expand=True, pady=5)

        self.result_label = tk.Label(self.main_content, text="RESULT:", font=("Arial", 12, "bold"))
        self.result_label.pack(anchor="w")
        self.result_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid", font=("Courier", 12, "normal"), state="disabled")
        self.result_text.pack(fill="both", expand=True, pady=5)

        self.apply_styles()

    def add_hover_effect(self, button):
        def on_enter(e):
            button['bg'] = "#cccccc" if not self.is_dark_mode else "#555555"

        def on_leave(e):
            button['bg'] = "#f5f5f5" if not self.is_dark_mode else "#333333"

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def apply_styles(self):
        if self.is_dark_mode:
            bg_color = "#191919"
            fg_color = "#ffffff"
            self.root.configure(bg=bg_color)
            self.header.configure(bg=bg_color)
            self.sidebar.configure(bg=bg_color)
            self.main_content.configure(bg=bg_color)
        else:
            bg_color = "#f5f5f5"
            fg_color = "#191919"
            self.root.configure(bg=bg_color)
            self.header.configure(bg=bg_color)
            self.sidebar.configure(bg=bg_color)
            self.main_content.configure(bg=bg_color)

        self.update_ui_colors(bg_color, fg_color)

    def update_ui_colors(self, bg_color, fg_color):

        self.headLabel.config(bg=bg_color, fg=fg_color)
        self.descLabel.config(bg=bg_color, fg=fg_color)

        button_style = {"bg": "#f5f5f5" if not self.is_dark_mode else "#333333", "fg": fg_color, "bd": 0, "font": ("Arial", 12, "bold")}
        for button in [self.open_file_button, self.lexical_analysis_button, self.syntax_analysis_button, self.semantic_analysis_button, self.clear_button, self.toggle_mode_button]:
            button.config(**button_style)

        self.code_text.config(bg="#ffffff" if not self.is_dark_mode else "#333333", fg=fg_color)
        self.result_text.config(bg="#ffffff" if not self.is_dark_mode else "#333333", fg=fg_color)

        self.code_label.config(bg=bg_color, fg=fg_color)
        self.result_label.config(bg=bg_color, fg=fg_color)

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_styles()

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
        self.display_result("Lexical Analysis Success! BOOM! \n--- Tokens ---")
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
        self.display_result("Syntax Analysis Success! BOOM! Syntax Free.")
        self.enable_button(self.semantic_analysis_button)
        self.syntax_analysis_button.config(state="disabled")

    def semantic_analysis(self):
        tokens = self.lexical_analyzer.tokenize(self.code_text.get("1.0", tk.END).strip())[0]
        result, error = self.semantic_analyzer.check_semantics(tokens)
        if not result:
            self.display_result(error)
            return
        self.display_result("Semantic Analysis Success! BOOM! Semantics Valid.")
        self.semantic_analysis_button.config(state="disabled")

# ╰(*°▽°*)╯
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCompilerGUI(root)
    root.mainloop()