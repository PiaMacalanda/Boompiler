class SemanticAnalyzer:
    def __init__(self):
        # Define type mappings for allowed assignments
        self.type_mappings = {
            "int": "INT_LITERAL",
            "float": "FLOAT_LITERAL",
            "double": "DOUBLE_LITERAL",
            "String": "STRING_LITERAL",
            "boolean": "BOOLEAN_LITERAL",
            "char": "CHAR_LITERAL",
        }

    def check_semantics(self, tokens):
        # Debugging: print the tokens being processed
        print(f"Tokens in semantic analysis: {tokens}")

        if not tokens or len(tokens) < 2:
            return False, "Semantic Error: Invalid syntax or incomplete tokens. Aw sad :(. "

        # The first token should be the type
        type_decl = tokens[0].get("value")

        # Validate the declared type
        if type_decl not in self.type_mappings:
            return False, f"Semantic Error: Unsupported type '{type_decl}'. Aw sad :(. "

        # Check for multiple variable declarations on the same line (e.g., `int x, y, z;`)
        declared_variables = []
        index = 1
        if tokens[index]["type"] == "IDENTIFIER":
            while index < len(tokens) and tokens[index]["type"] == "IDENTIFIER":
                declared_variables.append(tokens[index]["value"])
                index += 1  # Move past the identifier(s)

        # Now we need to check if each variable gets assigned after its declaration.
        # Initialize a dictionary to track which variables were assigned
        assignments = {var: False for var in declared_variables}

        # Iterate through the rest of the tokens and check for assignments
        while index < len(tokens):
            if tokens[index]["type"] == "ASSIGN":
                # Get the variable to assign to
                if index - 1 >= 0 and tokens[index - 1]["type"] == "IDENTIFIER":
                    var = tokens[index - 1]["value"]
                    if var in assignments:
                        # Check the assigned value's type
                        assigned_token = tokens[index + 1] if index + 1 < len(tokens) else None
                        if assigned_token:
                            value_type = assigned_token["type"]
                            expected_type = self.type_mappings[type_decl]

                            # Type mismatch checks
                            if type_decl == "int" and value_type in ["FLOAT_LITERAL", "DOUBLE_LITERAL"]:
                                return False, f"Semantic Error: Cannot assign a float or double literal to an int variable '{var}'. Aw sad :(. Please use integer values."
                            if type_decl == "float" and value_type == "DOUBLE_LITERAL":
                                return False, f"Semantic Error: Cannot assign a double literal to a float variable '{var}'. Aw sad :(. Please use the 'f' suffix for float values."
                            if value_type != expected_type:
                                return False, f"Semantic Error: Type mismatch. '{type_decl}' expects '{expected_type}', but got '{value_type}' for variable '{var}'. Aw sad :("

                            assignments[var] = True  # Mark variable as assigned
                            index += 2  # Skip assignment and value

            index += 1  # Move to the next token

        # Check if all declared variables are assigned
        for var, assigned in assignments.items():
            if not assigned:
                return False, f"Semantic Error: Variable '{var}' declared but never assigned. Aw sad :("

        return True, "Semantics Valid. BOOM!"
