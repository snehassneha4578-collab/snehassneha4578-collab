import json
import html

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
TOP = 35

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

days = data.get("days", [])

# Group days into weeks.
weeks = []

for i in range(0, len(days), 7):
    week = days[i:i + 7]

    if len(week) == 7:
        weeks.append(week)

weeks = weeks[-53:]

width = LEFT + len(weeks) * STEP + 30
height = TOP + 7 * STEP + 45

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    
    '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',

    '''
    <text x="30" y="20"
          font-family="monospace"
          font-size="12"
          fill="#8b949e">
        GitHub Contributions
    </text>
    ''',
]

# Draw contribution cells.
for week_index, week in enumerate(weeks):

    for day_index, day in enumerate(week):

        count = int(day.get("count", 0))

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

        delay = (week_index + day_index) * 0.025

        svg.append(
            f'''
            <rect x="{x}" y="{y}"
                  width="{CELL}" height="{CELL}"
                  rx="3"
                  fill="{PALETTE[level]}">
                
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.35s"
                    begin="{delay:.3f}s"
                    fill="freeze"/>
                
            </rect>
            '''
        )

# Legend.
legend_y = TOP + 7 * STEP + 10

svg.append(
    f'''
    <text x="30" y="{legend_y + 10}"
          font-family="monospace"
          font-size="11"
          fill="#8b949e">
        Less
    </text>
    '''
)

legend_x = 60

for level in range(6):

    svg.append(
        f'''
        <rect x="{legend_x + level * 18}"
              y="{legend_y}"
              width="13"
              height="13"
              rx="3"
              fill="{PALETTE[level]}"/>
        '''
    )

svg.append(
    f'''
    <text x="{legend_x + 6 * 18 + 5}"
          y="{legend_y + 10}"
          font-family="monospace"
          font-size="11"
          fill="#8b949e">
        More
    </text>
    '''
)

svg.append("</svg>")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print(f"Created {OUTPUT_FILE}")
