class SyntaxAnalyzer:
    def parse_syntax(self, tokens):
        index = 0
        while index < len(tokens):
            # Ensure enough tokens to process a statement
            if len(tokens) - index < 3:
                return False, f"Syntax Error: Incomplete statement starting at token {index}."

            # Handle variable declarations (both single and multi-variable declarations)
            if tokens[index]["type"] == "TYPE":
                index += 1  # Skip TYPE
                if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                    return False, "Syntax Error: Expected an identifier after type declaration."

                # Handle single-variable or multi-variable declaration
                while index < len(tokens) and tokens[index]["type"] == "IDENTIFIER":
                    index += 1  # Skip IDENTIFIER

                    # Check for assignment to the variable (optional)
                    if index < len(tokens) and tokens[index]["type"] == "ASSIGN":
                        index += 1  # Skip ASSIGN
                        if tokens[index]["type"] not in {"NUMBER", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER", "CHAR_LITERAL"}:
                            return False, f"Syntax Error: Invalid assignment value near token {index}."
                        index += 1  # Skip the assigned value
                    
                    # Handle either comma (for multi-variable declaration) or semicolon (end of declaration)
                    if index < len(tokens) and tokens[index]["type"] == "COMMA":
                        index += 1  # Skip COMMA for multi-variable declaration
                    elif index < len(tokens) and tokens[index]["type"] == "SEMICOLON":
                        index += 1  # Skip SEMICOLON, end of declaration
                        break
                    else:
                        return False, "Syntax Error: Missing comma or semicolon in variable declaration."
                
                continue  # Move to the next statement or token

            # Handle assignment statement (e.g., x = 0;)
            elif tokens[index]["type"] == "IDENTIFIER":
                if index + 1 >= len(tokens) or tokens[index + 1]["type"] != "ASSIGN":
                    return False, f"Syntax Error: Missing '=' after identifier at token {index}."
                if index + 2 >= len(tokens) or tokens[index + 2]["type"] not in {"NUMBER", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER", "CHAR_LITERAL"}:
                    return False, f"Syntax Error: Invalid assignment value near token {index + 2}."
                if index + 3 >= len(tokens) or tokens[index + 3]["type"] != "SEMICOLON":
                    return False, "Syntax Error: Missing semicolon after assignment."
                index += 4  # Move past IDENTIFIER, ASSIGN, value, and SEMICOLON
                continue

            else:
                return False, f"Syntax Error: Unexpected token '{tokens[index]['type']}' at position {index}."

        # If all statements are valid
        return True, None
