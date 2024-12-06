class SyntaxAnalyzer:
    def parse_syntax(self, tokens):
        index = 0
        while index < len(tokens):
            # Check for type declaration
            if tokens[index]["type"] == "TYPE":
                index += 1  # Skip TYPE
                if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                    return False, "Syntax Error: Expected an identifier after type declaration. Aw sad :(."

                # Process variables in the same line
                while index < len(tokens):
                    index += 1  # Skip IDENTIFIER

                    # Check for assignment
                    if index < len(tokens) and tokens[index]["type"] == "ASSIGN":
                        index += 1  # Skip ASSIGN
                        if tokens[index]["type"] not in {
                            "INT_LITERAL", "FLOAT_LITERAL", "DOUBLE_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER", "CHAR_LITERAL"
                        }:
                            return False, f"Syntax Error: Invalid assignment value near token {index}. Aw sad :(."
                        index += 1  # Skip assigned value
                    
                    # Handle commas for multiple variables or semicolon to end declaration
                    if index < len(tokens) and tokens[index]["type"] == "COMMA":
                        index += 1  # Skip COMMA
                        if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                            return False, "Syntax Error: Expected identifier after comma. Aw sad :(."
                    elif index < len(tokens) and tokens[index]["type"] == "SEMICOLON":
                        index += 1  # Skip SEMICOLON, end of declaration
                        break
                    else:
                        return False, "Syntax Error: Missing comma or semicolon in variable declaration. Aw sad :(."

            # Assignment statement (e.g., x = 0;)
            elif tokens[index]["type"] == "IDENTIFIER":
                if index + 1 >= len(tokens) or tokens[index + 1]["type"] != "ASSIGN":
                    return False, f"Syntax Error: Missing '=' after identifier at token {index}. Aw sad :(."
                if index + 2 >= len(tokens) or tokens[index + 2]["type"] not in {
                    "INT_LITERAL", "FLOAT_LITERAL", "DOUBLE_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER", "CHAR_LITERAL"
                }:
                    return False, f"Syntax Error: Invalid assignment value near token {index + 2}. Aw sad :(."
                if index + 3 >= len(tokens) or tokens[index + 3]["type"] != "SEMICOLON":
                    return False, "Syntax Error: Missing semicolon after assignment. Aw sad :(."
                index += 4  # Move past IDENTIFIER, ASSIGN, value, and SEMICOLON
                continue

            # Unexpected token
            else:
                return False, f"Syntax Error: Unexpected token '{tokens[index]['type']}' at position {index}. Aw sad :(."

        return True, None
