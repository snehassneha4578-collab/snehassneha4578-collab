import json
import math

INPUT_FILE = "data/contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

CELL = 13
GAP = 3
STEP = CELL + GAP

LEFT = 30
TOP = 30

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

days = data["days"]

# GitHub normally displays approximately 53 weeks × 7 days.
weeks = []

for i in range(0, len(days), 7):
    weeks.append(days[i:i + 7])

weeks = weeks[-53:]

width = LEFT + len(weeks) * STEP + 20
height = TOP + 7 * STEP + 55

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">'
)

svg.append("""
<style>
.cell {
    opacity: 0;
    animation: appear 0.35s ease-out forwards;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translate(-6px, -6px);
    }
    to {
        opacity: 1;
        transform: translate(0, 0);
    }
}
</style>
""")

svg.append("""
<rect width="100%" height="100%" rx="12"
      fill="#0d1117"/>
""")

svg.append("""
<text x="30" y="20"
      font-family="monospace"
      font-size="12"
      fill="#8b949e">
GitHub Contributions
</text>
""")

for week_index, week in enumerate(weeks):
    for day_index, day in enumerate(week):

        count = day.get("count", 0)

        if count == 0:
            level = 0
        elif count <= 2:
            level = 1
        elif count <= 5:
            level = 2
        elif count <= 10:
            level = 3
        elif count <= 20:
            level = 4
        else:
            level = 5

        x = LEFT + week_index * STEP
        y = TOP + day_index * STEP

        delay = (week_index + day_index) * 0.018

        svg.append(
            f'<rect class="cell" '
            f'x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" rx="3" '
            f'fill="{PALETTE[level]}" '
            f'style="animation-delay:{delay:.3f}s"/>'
        )

svg.append("""
<text x="30" y="140"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
Less
</text>
""")

legend_x = 60

for level in range(6):
    svg.append(
        f'<rect x="{legend_x + level * 18}" y="130" '
        f'width="13" height="13" rx="3" '
        f'fill="{PALETTE[level]}"/>'
    )

svg.append(f"""
<text x="{legend_x + 6 * 18 + 5}" y="140"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
More
</text>
""")

svg.append("</svg>")

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(svg))

print(f"Created {OUTPUT_FILE}")
