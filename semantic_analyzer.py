class SemanticAnalyzer:
    def __init__(self):
        self.type_mappings = {
            "int": "INT_LITERAL",
            "float": "FLOAT_LITERAL",
            "double": "DOUBLE_LITERAL",
            "String": "STRING_LITERAL",
            "boolean": "BOOLEAN_LITERAL",
            "char": "CHAR_LITERAL",
        }
        self.variable_types = {}

    def check_semantics(self, tokens):

        self.variable_types = {}
        # DEBUGGING purp. ONLY: print the tokens being processed. 'Di na nag logging lol.
        print(f"Tokens in semantic analysis: {tokens}")

        if not tokens or len(tokens) < 2:
            return False, "Semantic Error: Invalid syntax or incomplete tokens. Aw sad :(. "

        index = 0
        while index < len(tokens):
            if tokens[index]["type"] == "TYPE":
                type_token = tokens[index]["value"]
                index += 1

                if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                    return False, "Semantic Error: Expected an identifier after type declaration. Aw sad :(."

                # Process same line (handles multiple declarations like 'int x, y, z;')
                while index < len(tokens) and tokens[index]["type"] == "IDENTIFIER":
                    identifier = tokens[index]["value"]

                    # Check for redeclaration of a var
                    if identifier in self.variable_types:
                        return False, f"Semantic Error: Variable '{identifier}' already declared. Aw sad :("

                    self.variable_types[identifier] = type_token  # For Var type tracker
                    index += 1

                    # Check for assignment
                    if index < len(tokens) and tokens[index]["type"] == "ASSIGN":
                        index += 1
                        if tokens[index]["type"] not in {
                            "INT_LITERAL", "FLOAT_LITERAL", "DOUBLE_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "CHAR_LITERAL", "IDENTIFIER"
                        }:
                            return False, f"Semantic Error: Invalid assignment value near token {index}. Aw sad :("

                        # Validate based on var type
                        value_type = tokens[index]["type"]
                        if value_type != self.type_mappings.get(self.variable_types[identifier], None):
                            return False, f"Semantic Error: Type mismatch for '{identifier}'. Expected {self.variable_types[identifier]} but got {value_type}. Aw sad :("

                        index += 1
                    
                    # Handle commas for mul var or semicolon to end dec
                    if index < len(tokens) and tokens[index]["type"] == "COMMA":
                        index += 1
                        if index >= len(tokens) or tokens[index]["type"] != "IDENTIFIER":
                            return False, "Semantic Error: Expected identifier after comma. Aw sad :(."
                    elif index < len(tokens) and tokens[index]["type"] == "SEMICOLON":
                        index += 1
                        break
                    else:
                        return False, "Semantic Error: Missing comma or semicolon in variable declaration. Aw sad :("

            # Handle assignment statement (e.g., x = 0;)
            elif tokens[index]["type"] == "IDENTIFIER":
                identifier = tokens[index]["value"]
                if identifier not in self.variable_types:
                    return False, f"Semantic Error: Variable '{identifier}' used before declaration. Aw sad :("

                if index + 1 >= len(tokens) or tokens[index + 1]["type"] != "ASSIGN":
                    return False, f"Semantic Error: Missing '=' after identifier '{identifier}' at token {index}. Aw sad :("
                
                index += 2 

                if index < len(tokens) and tokens[index]["type"] in {
                    "INT_LITERAL", "FLOAT_LITERAL", "DOUBLE_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL", "CHAR_LITERAL"
                }:
                    value_type = tokens[index]["type"]
                    expected_type = self.variable_types[identifier]
                    if value_type != self.type_mappings.get(expected_type, None):
                        return False, f"Semantic Error: Type mismatch for variable '{identifier}'. Expected {expected_type}, got {value_type}. Aw sad :("

                    index += 1
                    
                    if index < len(tokens) and tokens[index]["type"] != "SEMICOLON":
                        return False, f"Semantic Error: Missing semicolon after assignment for '{identifier}'. Aw sad :("
                    index += 1
                else:
                    return False, f"Semantic Error: Invalid assignment value for '{identifier}' at token {index}. Aw sad :("
            
            else:
                return False, f"Semantic Error: Unexpected token '{tokens[index]['type']}' at position {index}. Aw sad :("

        return True, "Semantics Valid. BOOM!"