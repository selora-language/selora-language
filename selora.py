import re

KEYWORDS = [
    "bloc","init","declare","render","react","func","var","dict","import","releaseEvent","filetype", "as", "while", "if", "else", "for", "elif", "out"

    
    ]

TYPE = [
    "int","float","str","bool","list","dict","glib","ulib"
]

SKIP_TOKENS = {"WHITESPACE", "COMMENT", "COMMENT_MULTILINE"}


TOKEN_TYPES = [
    ("COMMENT_MULTILINE", r"\*\*\*[\s\S]*?\*\*\*"),
    # Comments
    ("COMMENT", r"#.*"),
    # Events
    ("EVENT", r"@[A-Za-z_][A-Za-z0-9_]*(\.[A-Z]+)?|\bON[A-Z]+(\([^\)]*\))?\b"),
    # Numbers
    ("PATH", r"res://[A-Za-z0-9_/.]+"),
    # Operators
    ("NUMBER", r"\d+(\.\d+)?"),
    # Strings
    ("STRING", r'"[^"]*"|\'[^\']*\''),
    # Identifiers
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    # Hooks
    ("HOOK", r"\|\|\||\|\||\|"),
    # Comma
    ("COMMA", r","),
    # Symbols
    ("SYMBOL", r"->|[{}()\[\];=:.]|>|<"),
    # Paths
    ("OPERATOR", r"\+|\-|\*|/"),
    # Whitespace
    ("WHITESPACE", r"\s+"),
]

def lexer(code):
    tokens = []
    while code:
        matched = False

        # Skip whitespace first
        ws_match = re.match(r"\s+", code)
        if ws_match:
            code = code[ws_match.end():]
            continue

        for ttype, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                if ttype == "IDENT" and match.group() in KEYWORDS:
                    ttype = "KEYWORD"
                elif ttype == "IDENT" and match.group() in TYPE:
                    ttype = "TYPE"
                if ttype not in SKIP_TOKENS: 
                    tokens.append((ttype, match.group()))
                code = code[match.end():]
                matched = True
                break

        if not matched:
            raise SyntaxError(f"Unexpected token: {code[:10]!r}")

    return tokens

# Example usage
file = input("File path: ")

with open(file, "r") as f:
    selora_code = f.read()

tokens = lexer(selora_code)
print(tokens)
