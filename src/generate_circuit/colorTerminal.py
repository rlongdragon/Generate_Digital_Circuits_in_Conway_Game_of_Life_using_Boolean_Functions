def color(text: str, fgcol=9, bgcol=9):
    """
    text: str
    color code:
    0:gary, 1: red, 2: green, 3: yellow, 4: blue, 5: purple, 6: cyan, 7: white
    """
    fgcode = 30 + fgcol
    bgcode = 40 + bgcol

    return f"\033[{fgcode};{bgcode}m{text}\033[0m"