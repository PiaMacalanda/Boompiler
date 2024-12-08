class SyntaxAnalyzer:
    def parse_syntax(self, tokens):
        index = 0

        while index < len(tokens):
            if tokens[index]["type"] == "TYPE":
                index += 1 
                if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                    return False, "Syntax Error: Expected an identifier after type declaration. Aw sad :(."

                # This process variables in the same line first
                while index < len(tokens):
                    index += 1

                    if index < len(tokens) and tokens[index]["type"] == "ASSIGN":
                        index += 1 
                        if tokens[index]["type"] not in {
                            "INT_LITERAL", "FLOAT_LITERAL", "DOUBLE_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "IDENTIFIER", "CHAR_LITERAL"
                        }:
                            return False, f"Syntax Error: Invalid assignment value near token {index}. Aw sad :(."
                        index += 1 
                    
                    # Handle commas for mul var or semicolon to last dec
                    if index < len(tokens) and tokens[index]["type"] == "COMMA":
                        index += 1 
                        if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                            return False, "Syntax Error: Expected identifier after comma. Aw sad :(."
                    elif index < len(tokens) and tokens[index]["type"] == "SEMICOLON":
                        index += 1 
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
                index += 4
                continue

            else:
                return False, f"Syntax Error: Unexpected token '{tokens[index]['type']}' at position {index}. Aw sad :(."

        return True, None