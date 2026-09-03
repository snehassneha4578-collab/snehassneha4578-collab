from pathlib import Path
from html import escape

INPUT_FILE = Path("ascii-portrait.txt")
OUTPUT_FILE = Path("ascii-portrait.svg")

text = INPUT_FILE.read_text(encoding="utf-8")

lines = text.splitlines()

font_size = 8
line_height = 10
padding = 20

max_length = max((len(line) for line in lines), default=1)

width = max_length * 5 + padding * 2
height = len(lines) * line_height + padding * 2

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',

    '<rect width="100%" height="100%" rx="14" fill="#0d1117"/>',

    '<text x="15" y="18" '
    'font-family="monospace" '
    'font-size="10" '
    'fill="#8b949e">sneha@github:~$ cat ascii-portrait.txt</text>'
]

start_y = padding + 15

for index, line in enumerate(lines):
    y = start_y + index * line_height

    svg.append(
        f'<text x="{padding}" y="{y}" '
        f'font-family="monospace" '
        f'font-size="{font_size}px" '
        f'fill="#39d353">'
        f'{escape(line)}'
        f'</text>'
    )

svg.append("</svg>")

OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")

print(f"Created {OUTPUT_FILE}")
