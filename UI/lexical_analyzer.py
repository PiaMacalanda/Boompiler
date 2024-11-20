import re

class LexicalAnalyzer:
    def tokenize(self, code):
        tokens = []
        keywords = {"int", "float", "double", "String", "boolean"}
        
        # Token specification
        token_spec = [
            ("TYPE", r"\b(?:int|float|double|String|boolean)\b"),  # Java types
            ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z_0-9]*"),            # Variable names
            ("ASSIGN", r"="),                                     # Assignment operator
            ("NUMBER", r"\b\d+(\.\d+)?\b"),                       # Integer or decimal numbers
            ("STRING_LITERAL", r'"[^"]*"'),                       # String literals
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),           # Boolean literals
            ("SEMICOLON", r";"),                                  # End of statement
            ("SKIP", r"[ \t]+"),                                  # Skip whitespace
            ("MISMATCH", r"."),                                   # Any other character
        ]
        
        # Compile regex for all tokens
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)
        
        # Match each token in code
        for mo in re.finditer(token_regex, code):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == "MISMATCH":
                return [], f"Lexical Error: Unexpected token '{value}'"
            if kind != "SKIP":  # Ignore whitespace
                tokens.append({"type": kind, "value": value})
        
        return tokens, None