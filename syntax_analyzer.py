class SyntaxAnalyzer:
    def parse_syntax(self, tokens):
        index = 0
        while index < len(tokens):
            # Ensure enough tokens to process a statement
            if len(tokens) - index < 3:
                return False, f"Syntax Error: Incomplete statement starting at token {index}."

            # Multi-variable declaration with commas
            if tokens[index]["type"] == "TYPE":
                index += 1  # Skip TYPE
                while index < len(tokens) and tokens[index]["type"] == "IDENTIFIER":
                    index += 1  # Skip IDENTIFIER
                    if index < len(tokens) and tokens[index]["type"] == "COMMA":
                        index += 1  # Skip COMMA for multi-variable declaration
                    elif index < len(tokens) and tokens[index]["type"] == "SEMICOLON":
                        index += 1  # Skip SEMICOLON, end of declaration
                        break
                    else:
                        return False, "Syntax Error: Missing comma or semicolon in variable declaration."
                else:
                    return False, "Syntax Error: Declaration did not end correctly."

            # Assignment statement
            elif tokens[index]["type"] == "IDENTIFIER" and tokens[index + 1]["type"] == "ASSIGN":
                if index + 3 >= len(tokens) or tokens[index + 2]["type"] not in {"NUMBER", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER"}:
                    return False, f"Syntax Error: Invalid assignment expression near token {index}."
                if tokens[index + 3]["type"] != "SEMICOLON":
                    return False, "Syntax Error: Missing semicolon after assignment."
                index += 4  # Move past IDENTIFIER, ASSIGN, value, and SEMICOLON

            else:
                return False, f"Syntax Error: Unexpected token '{tokens[index]['type']}' at position {index}."

        # If all statements are valid
        return True, None
