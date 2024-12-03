import re
from comment_remover import remove_comments

class LexicalAnalyzer:
    def tokenize(self, code):

        if not code.strip():  # Handle empty input early
            return [], "Error: No input code provided."
        
        # Remove comments before processing
        code = remove_comments(code)

        tokens = []
        
        # Token specification (comment patterns should come first)
        token_spec = [
            ("COMMENT", r"//.*?$"),                               # Single-line comments
            ("MULTI_LINE_COMMENT", r"/\*.*?\*/"),                  # Multi-line comments
            ("CLASS", r"\bclass\b"),                              # Class keyword
            ("METHOD", r"\b(?:public|private|protected|static|void)\b"),  # Method modifiers and return types
            ("TYPE", r"\b(?:int|float|double|String|boolean|char)\b"),  # Java types
            ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_$]*\b"),       # Java identifiers
            ("ASSIGN", r"="),                                     # Assignment operator
            ("NUMBER", r"\b\d+(\.\d+)?\b"),                       # Integer or decimal numbers
            ("STRING_LITERAL", r'"(?:\\.|[^"\\])*"'),              # String literals (with escape sequences)
            ("CHAR_LITERAL", r"'(?:\\.|[^'\\])*'"),                # Char literals (with escape sequences)
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),           # Boolean literals
            ("SEMICOLON", r";"),                                  # End of statement
            ("LBRACE", r"{"),                                     # Left brace
            ("RBRACE", r"}"),                                     # Right brace
            ("LBRACKET", r"\["),                                   # Left bracket
            ("RBRACKET", r"\]"),                                    # Right bracket
            ("LPAREN", r"\("),                                    # Left parenthesis
            ("RPAREN", r"\)"),                                    # Right parenthesis
            ("SKIP", r"[ \t\r\n]+"),                              # Skip all whitespace, including newlines
            ("MISMATCH", r"."),                                   # Any other character (fallback for unexpected tokens)
        ]
        
        # Compile regex for all tokens
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)
        
        # Match each token in code
        for mo in re.finditer(token_regex, code, re.DOTALL):  # Used re.DOTALL to handle multi-line comments
            kind = mo.lastgroup
            value = mo.group(kind)
            print(f"Matched: {kind} -> {value}")  # Debug print to check each match


            if kind in {"COMMENT", "MULTI_LINE_COMMENT"}:
                continue  # Skip the whole comment

            if kind == "MISMATCH" and value.strip():
                # Log the mismatch token and continue
                return [], f"Lexical Error: Unexpected token '{value}'"

            if kind != "SKIP":  # Ignore whitespace
                tokens.append({"type": kind, "value": value})

        return tokens, None