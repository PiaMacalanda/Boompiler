class SemanticAnalyzer:
    def __init__(self):
        # Define type mappings for allowed assignments
        self.type_mappings = {
            "int": "NUMBER",
            "float": "NUMBER",
            "double": "NUMBER",
            "String": "STRING_LITERAL",
            "boolean": "BOOLEAN_LITERAL",
            "char": "CHAR_LITERAL"
        }
    
    def check_semantics(self, tokens):
        if not tokens or len(tokens) < 2:
            return False, "Semantic Error: Invalid syntax or incomplete tokens. Aw sad :( "

        # Get declared type and assignment token
        type_decl = tokens[0].get("value")
        assigned_token = tokens[3] if len(tokens) > 3 and tokens[2].get("type") == "ASSIGN" else None

        # Validate declared type
        if type_decl not in self.type_mappings:
            return False, f"Semantic Error: Unsupported type '{type_decl}'. Aw sad :( ."

        # If there's an assignment, check compatibility
        if assigned_token:
            value_type = assigned_token.get("type")
            expected_type = self.type_mappings[type_decl]

            if value_type != expected_type:
                return (
                    False,
                    f"Semantic Error: Type mismatch. '{type_decl}' expects '{expected_type}', but got '{value_type}'. Aw sad :( ."
                )
        
        # If no assignment or compatible assignment, return success
        return True, None
