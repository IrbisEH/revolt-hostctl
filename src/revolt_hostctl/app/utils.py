def to_snake(name: str) -> str:
    res = ""
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            res += "_"
        res += char.lower()
    return res


def to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def print_table(rows: list, headers: list) -> None:
    num_cols = len(rows[0])
    col_widths = [0] * num_cols

    for i, h in enumerate(headers[:num_cols]):
        col_widths[i] = len(str(h))

    for row in rows:
        for i, cell in enumerate(row[:num_cols]):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    if headers:
        print('  '.join(f"{h:<{w}}" for h, w in zip(headers, col_widths)))
        print('-' * sum(col_widths))

    for row in rows:
        print('  '.join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths)))
