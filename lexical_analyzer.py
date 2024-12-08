import re
from comment_remover import remove_comments
import logging

# Configure logging. For debbuing purp only.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler("lexical_analyzer.log")  # Uncomment to log to file (for future reference)
    ]
)
logger = logging.getLogger("LexicalAnalyzer")

class LexicalAnalyzer:
    def tokenize(self, code):
        if not code.strip():
            return [], "Error: No input code provided."

        code = remove_comments(code)

        tokens = []

        token_spec = [
            # Comments
            ("COMMENT", r"//.*?$"),
            ("MULTI_LINE_COMMENT", r"/\*.*?\*/"),

            # Keywords and identifiers | Literals and operators
            ("ACCESS_MODIFIER", r"\b(?:public|private|protected)\b"),
            ("CLASS", r"class"),
            ("STATIC", r"\bstatic\b"),
            ("METHOD", r"\b(?:void)\b"),
            ("TYPE", r"\b(?:int|float|double|String|boolean|char|long|short|byte)\b"),
            ("BOOLEAN_LITERAL", r"\b(?:true|false)\b"),
            ("IDENTIFIER", r"[$a-zA-Z_][a-zA-Z0-9_$]*"),
            ("ASSIGN", r"="),
            ("FLOAT_LITERAL", r"\b\d+(\.\d*)?[fF]\b"),
            ("DOUBLE_LITERAL", r"\b\d+\.\d*(e[+-]?\d+)?[dD]?\b"),
            ("INT_LITERAL", r"\b\d+\b"),
            ("STRING_LITERAL", r'"(?:\\.|[^"\\])*"'),
            ("CHAR_LITERAL", r"'([^'\\])'"),

            # Punctuation and delimiters
            ("COMMA", r","),
            ("SEMICOLON", r";"),
            ("LBRACE", r"{"),
            ("RBRACE", r"}"),
            ("LBRACKET", r"\["),
            ("RBRACKET", r"\]"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),

            # Whitespace: SKIP and errors: Mismatch
            ("SKIP", r"[ \t\r\n]+"),
            ("MISMATCH", r"."),

        ]

        token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)

        for match in re.finditer(token_regex, code, re.DOTALL):
            kind = match.lastgroup
            value = match.group(kind)

            # DEBUG purp. ONLY: for token matching
            logger.debug(f"Matched: {kind} -> {value}")

            if kind in {"COMMENT", "MULTI_LINE_COMMENT"}:
                continue

            if kind == "MISMATCH" and value.strip():
                position = match.start()  # Error position
                logger.error(f"Unexpected token: '{value}' at position {position}")
                return [], f"Lexical Error: Unexpected token '{value}' at position {position} huhuhu."

            if kind != "SKIP":
                tokens.append({"type": kind, "value": value})

        return tokens, None
