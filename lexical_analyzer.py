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
            ("COMMENT", r"//.*?$"),
            ("MULTI_LINE_COMMENT", r"/\*.*?\*/"),

            # Keywords and identifiers | Literals and operators
            ("ACCESS_MODIFIER", r"\b(?:public|private|protected)\b"),
            ("CLASS", r"class"),
            ("STATIC", r"\bstatic\b"),
            ("METHOD", r"\b(?:void)\b"),
            ("TYPE", r"\b(?:int|float|double|String|boolean|char)\b"),
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),
            ("IDENTIFIER", r"[$a-zA-Z_][a-zA-Z0-9_$]*"),
            ("ASSIGN", r"="),

            # Literals
            ("FLOAT_LITERAL", r"\b\d+(\.\d*)?[fF]\b"),
            ("DOUBLE_LITERAL", r"\b\d+\.\d*(e[+-]?\d+)?[dD]?\b"),
            ("INT_LITERAL", r"\b\d+\b"),
            ("STRING_LITERAL", r'"(?:\\.|[^"\\])*"'),
            ("CHAR_LITERAL", r"'([^'\\])'"),
            #("CHAR_LITERAL_MISMATCH", r"'([^'\\].*)'"), will delete soon

            # Punctuation and delimiters
            ("COMMA", r","),
            ("SEMICOLON", r";"),
            ("LBRACE", r"{"),
            ("RBRACE", r"}"),
            ("LBRACKET", r"\["),
            ("RBRACKET", r"\]"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),

            # Whitespace and errors
            ("SKIP", r"[ \t\r\n]+"),
            ("MISMATCH", r"."),

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
