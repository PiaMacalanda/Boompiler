import re
from comment_remover import remove_comments

class LexicalAnalyzer:
    def tokenize(self, code):
        # Handle empty input early
        if not code.strip():
            return [], "Error: No input code provided."

        # Remove comments before processing
        code = remove_comments(code)

        tokens = []

        # Token specification (comment patterns should come first)
        token_spec = [
            # Comments
            ("COMMENT", r"//.*?$"),                                # Single-line comments
            ("MULTI_LINE_COMMENT", r"/\*.*?\*/"),                 # Multi-line comments

            # Keywords and identifiers
            ("ACCESS_MODIFIER", r"\b(?:public|private|protected)\b"),  # Access modifiers
            ("CLASS", r""),
            ("STATIC", r"\bstatic\b"),                                  # Static modifier
            ("METHOD", r"\b(?:void)\b"),                              # Method keyword (return type)
            ("TYPE", r"\b(?:int|float|double|String|boolean|char)\b"),   # Java types
            ("IDENTIFIER", r"[$a-zA-Z_][a-zA-Z0-9_$]*"),            # Java identifiers (allow $)

            # Literals and operators
            ("ASSIGN", r"="),                                     # Assignment operator
            ("NUMBER", r"\b\d+(\.\d+)?[fF]?\b"),                   # accept float literals with an optional 'f' suffix
            ("STRING_LITERAL", r'"(?:\\.|[^"\\])*"'),             # String literals (with escape sequences)
            ("CHAR_LITERAL", r"'(?:\\.|[^'\\])*'"),               # Char literals (with escape sequences)
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),           # Boolean literals

            # Punctuation and delimiters
            ("COMMA", r","),                                      # Comma
            ("SEMICOLON", r";"),                                  # End of statement
            ("LBRACE", r"{"),                                     # Left brace
            ("RBRACE", r"}"),                                     # Right brace
            ("LBRACKET", r"\["),                                  # Left bracket
            ("RBRACKET", r"\]"),                                  # Right bracket
            ("LPAREN", r"\("),                                    # Left parenthesis
            ("RPAREN", r"\)"),                                    # Right parenthesis

            # Whitespace and errors
            ("SKIP", r"[ \t\r\n]+"),                              # Skip all whitespace
            ("MISMATCH", r"."),                                   # Fallback for unexpected tokens
        ]

        # Compile regex for all tokens
        token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)

        # Tokenize the code
        for match in re.finditer(token_regex, code, re.DOTALL):
            kind = match.lastgroup
            value = match.group(kind)

            # Debug output for token matching
            print(f"Matched: {kind} -> {value}")

            if kind in {"COMMENT", "MULTI_LINE_COMMENT"}:
                continue  # Skip comments

            if kind == "MISMATCH" and value.strip():
                print(f"Unexpected token: {value}")  # Debugging line
                return [], f"Lexical Error: Unexpected token '{value}' huhuhu."


            if kind != "SKIP":  # Ignore whitespace
                tokens.append({"type": kind, "value": value})

        return tokens, None
