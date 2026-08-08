import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon

import numpy as np

x_num = mdates.date2num(spx["Date"])
y = spx["Close"]
baseline = min(y) - 20

# Polygon describing the area under the line
vertices = np.column_stack([x_num, y])
vertices = np.vstack([
    vertices,
    [x_num[-1], baseline],
    [x_num[0], baseline],
])

clip_polygon = Polygon(
    vertices,
    closed=True,
    facecolor="none",
    edgecolor="none",
)
axes[1].add_patch(clip_polygon)

# Dark at the bottom, light cyan at the top
bloomberg_cmap = LinearSegmentedColormap.from_list(
    "bloomberg_fill",
    [
        "#061432",  # bottom
        "#073765",
        "#087b91",
        "#55cddd",  # top
    ],
)

gradient = np.linspace(0, 1, 512).reshape(-1, 1)

image = axes[1].imshow(
    gradient,
    extent=[x_num.min(), x_num.max(), baseline, max(y)],
    origin="lower",
    aspect="auto",
    cmap=bloomberg_cmap,
    alpha=0.85,
    interpolation="bicubic",
    zorder=0,
)

# Show the gradient only beneath the price line
image.set_clip_path(clip_polygon)

axes[1].set_xlim(x_num.min(), x_num.max())
axes[1].set_ylim(baseline, max(y) + 20)
# axes[1].xaxis_date()
# axes[1].grid(color="#6391a3", linestyle=":", alpha=0.6)