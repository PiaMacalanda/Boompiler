class SyntaxAnalyzer:
    def parse_syntax(self, tokens):
        if len(tokens) < 3:
            return False, "Syntax Error: Incomplete variable declaration."

        # Check starting with a TYPE and followed by IDENTIFIER
        if tokens[0]["type"] != "TYPE" or tokens[1]["type"] != "IDENTIFIER":
            return False, "Syntax Error: Declaration must start with a type and identifier."
        
        # Check for optional assignment and semicolon
        if tokens[2]["type"] == "ASSIGN":
            if tokens[-2]["type"] not in {"NUMBER", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER"}:
                return False, "Syntax Error: Invalid assignment expression."
            if tokens[-1]["type"] != "SEMICOLON":
                return False, "Syntax Error: Missing semicolon at end of declaration."
        elif tokens[2]["type"] == "SEMICOLON":
            # Direct declaration without assignment
            return True, None
        else:
            return False, "Syntax Error: Unexpected token after identifier."

        # If all checks pass
        return True, None