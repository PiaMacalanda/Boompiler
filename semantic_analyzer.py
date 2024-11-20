class SemanticAnalyzer:
    def check_semantics(self, tokens):
        type_decl = tokens[0]["value"]   # Get the declared type
        assigned_token = tokens[3] if len(tokens) > 3 and tokens[2]["type"] == "ASSIGN" else None
        
        # Check if the type and value are compatible
        if assigned_token:
            value_type = assigned_token["type"]
            if type_decl == "int" and value_type != "NUMBER":
                return False, "Semantic Error: 'int' type can only be assigned integer values."
            elif type_decl == "float" and value_type != "NUMBER":
                return False, "Semantic Error: 'float' type can only be assigned numeric values."
            elif type_decl == "double" and value_type != "NUMBER":
                return False, "Semantic Error: 'double' type can only be assigned numeric values."
            elif type_decl == "String" and value_type != "STRING_LITERAL":
                return False, "Semantic Error: 'String' type can only be assigned string literals."
            elif type_decl == "boolean" and value_type != "BOOLEAN_LITERAL":
                return False, "Semantic Error: 'boolean' type can only be assigned 'true' or 'false'."
        
        # If no assignment or compatible assignment, return success
        return True, None
