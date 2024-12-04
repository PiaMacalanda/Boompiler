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

        # Default mode (Light Mode)
        self.is_dark_mode = False

        # Create UI elements
        self.initialize_ui()

    def initialize_ui(self):
        # Header
        self.header = tk.Frame(self.root, width=150)
        self.header.pack(side="top", fill="y", padx=10, pady=10)

        head_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 28, "bold")}
        self.headLabel = tk.Label(self.header, text="ִ ⸜(｡˃ ᵕ ˂ )⸝♡  BOOMPILER  ദ്ദി(˵ •̀ ᴗ - ˵ )", **head_style)
        self.headLabel.pack(pady=10)

        desc_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 12, "italic")}
        self.descLabel = tk.Label(self.header, text="---------- By Pia Macalanda, Juliana Mancera, & Thoby Ralleta ----------", **desc_style)
        self.descLabel.pack(pady=5)

        # Left Sidebar for Buttons
        self.sidebar = tk.Frame(self.root, width=150)
        self.sidebar.pack(side="top", fill="y", padx=10, pady=10)

        button_style = {"bg": "#f5f5f5", "fg": "#191919", "bd": 0, "font": ("Arial", 12, "bold")}
        self.open_file_button = tk.Button(self.sidebar, text="Open File", command=self.open_file, **button_style, width=15)
        self.lexical_analysis_button = tk.Button(self.sidebar, text="Lexical Analysis", command=self.lexical_analysis, state="disabled", **button_style, width=15)
        self.syntax_analysis_button = tk.Button(self.sidebar, text="Syntax Analysis", command=self.syntax_analysis, state="disabled", **button_style, width=15)
        self.semantic_analysis_button = tk.Button(self.sidebar, text="Semantic Analysis", command=self.semantic_analysis, state="disabled", **button_style, width=15)
        self.clear_button = tk.Button(self.sidebar, text="Clear", command=self.clear, **button_style, width=15)
        self.toggle_mode_button = tk.Button(self.sidebar, text="࣪ ִֶָ☾.", command=self.toggle_mode, **button_style, width=5)

        self.open_file_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
        self.lexical_analysis_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
        self.syntax_analysis_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
        self.semantic_analysis_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
        self.clear_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)
        self.toggle_mode_button.pack(side=tk.LEFT, fill="y", pady=10, padx=10)

        # Main Content Area
        self.main_content = tk.Frame(self.root, padx=10, pady=10)
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.code_label = tk.Label(self.main_content, text="CODE:", font=("Arial", 12, "bold"))
        self.code_label.pack(anchor="w")
        self.code_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid", font=("Courier", 12, "normal"))
        self.code_text.pack(fill="both", expand=True, pady=5)
        self.code_text.bind("<<Modified>>", self.on_code_change)

        self.result_label = tk.Label(self.main_content, text="RESULT:", font=("Arial", 12, "bold"))
        self.result_label.pack(anchor="w")
        self.result_text = tk.Text(self.main_content, height=10, wrap="word", borderwidth=2, relief="solid", font=("Courier", 12, "normal"), state="disabled")
        self.result_text.pack(fill="both", expand=True, pady=5)

        # Apply default styles (Light Mode)
        self.apply_styles()

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

        # Update button, label, and text colors
        self.update_ui_colors(bg_color, fg_color)

    def update_ui_colors(self, bg_color, fg_color):
        # Update header text
        self.headLabel.config(bg=bg_color, fg=fg_color)
        self.descLabel.config(bg=bg_color, fg=fg_color)

        # Update buttons
        button_style = {"bg": "#f5f5f5" if not self.is_dark_mode else "#333333", "fg": fg_color, "bd": 0, "font": ("Arial", 12, "bold")}
        self.open_file_button.config(**button_style)
        self.lexical_analysis_button.config(**button_style)
        self.syntax_analysis_button.config(**button_style)
        self.semantic_analysis_button.config(**button_style)
        self.clear_button.config(**button_style)
        self.toggle_mode_button.config(**button_style)

        # Update code text and result text
        self.code_text.config(bg="#ffffff" if not self.is_dark_mode else "#333333", fg=fg_color)
        self.result_text.config(bg="#ffffff" if not self.is_dark_mode else "#333333", fg=fg_color)

        self.code_label.config(bg=bg_color, fg=fg_color)
        self.result_label.config(bg=bg_color, fg=fg_color)

    def toggle_mode(self):
        """Toggle between light and dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_styles()

    def on_code_change(self, event):
        """Enable buttons when code is manually typed."""
        self.code_text.edit_modified(False)  # Reset the modified flag
        code = self.code_text.get("1.0", tk.END).strip()
        if code:
            self.enable_button(self.lexical_analysis_button)
        else:
            self.disable_all_buttons()
        self.enable_button(self.open_file_button)

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
        self.display_result("Lexical Analysis Success! \n--- Tokens ---")
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
        self.display_result("Syntax Analysis Success! Syntax Free.")
        self.enable_button(self.semantic_analysis_button)
        self.syntax_analysis_button.config(state="disabled")

    def semantic_analysis(self):
        tokens = self.lexical_analyzer.tokenize(self.code_text.get("1.0", tk.END).strip())[0]
        result, error = self.semantic_analyzer.check_semantics(tokens)
        if not result:
            self.display_result(error)
            return
        self.display_result("Semantic Analysis Success! Semantics Valid.")
        self.semantic_analysis_button.config(state="disabled")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCompilerGUI(root)
    root.mainloop()
