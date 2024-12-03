import re

class LexicalAnalyzer:
    def tokenize(self, code):
        tokens = []
        keywords = {"int", "float", "double", "String", "boolean", "char"}
        
        # Token specification (comment patterns should come first)
        token_spec = [
            ("COMMENT", r"//.*?$"),                               # Single-line comments
            ("MULTI_LINE_COMMENT", r"/\*.*?\*/"),                  # Multi-line comments
            ("TYPE", r"\b(?:int|float|double|String|boolean|char)\b"),  # Java types
            ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_$]*\b"),        # Java variable names (letters, digits, _, $)
            ("ASSIGN", r"="),                                     # Assignment operator
            ("NUMBER", r"\b\d+(\.\d+)?\b"),                       # Integer or decimal numbers
            ("STRING_LITERAL", r'"(?:\\.|[^"\\])*"'),              # String literals (with escape sequences)
            ("CHAR_LITERAL", r"'(?:\\.|[^'\\])*'"),                # Char literals (with escape sequences)
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),           # Boolean literals
            ("SEMICOLON", r";"),                                  # End of statement
            ("SKIP", r"[ \t]+"),                                  # Skip whitespace
            ("MISMATCH", r"."),                                   # Any other character (fallback for unexpected tokens)
        ]
        
        # Compile regex for all tokens
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)
        
        # Match each token in code
        for mo in re.finditer(token_regex, code, re.DOTALL):  # Used re.DOTALL to handle multi-line comments
            kind = mo.lastgroup
            value = mo.group(kind)

            if kind in {"COMMENT", "MULTI_LINE_COMMENT"}:
                continue  # Skip the whole comment

            if kind == "MISMATCH":
                # Log the mismatch token and continue
                print(f"Lexical Error: Unexpected token '{value}'")

            if kind != "SKIP":  # Ignore whitespace
                tokens.append({"type": kind, "value": value})
        
        return tokens, None