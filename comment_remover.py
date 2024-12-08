import re

def remove_comments(code): # Used in Lexical Analyzer Line 22. Dyslexic problem.

    # Single-line comments (//...)
    code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)
    
    # Multi-line comments (/*...*/)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    return code
