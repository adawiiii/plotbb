import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.dates import date2num
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon

from numpy import linspace, column_stack, vstack

from pandas import Series

class PlotBB:
    def __init__(self, axis: Axes) -> None:
        self.axis = axis
        return

    def plot(self, x: Series, y: Series, margin: float = 0.05):
        x_num = date2num(x)
        baseline = (min(y) * (1 - margin))

        # Polygon describing the area under the line
        vertices = column_stack([x_num, y])
        vertices = vstack([
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
        self.axis.add_patch(clip_polygon)

        bloomberg_cmap = LinearSegmentedColormap.from_list(
            "bloomberg_fill",
            [
                (0.00, "#020250"),
                (0.32, "#0058B1"),
                (0.62, "#1086be"),
                (0.80, "#27bef8"),
                (0.92, "#00dbf4"),
                (1.00, "#00dbf4"),
            ],
        )

        bloomberg_bgmap = LinearSegmentedColormap.from_list(
            "bloomberg_bg",
            [
                "#000000",
                "#91DCFF"
            ],
        )

        gradient = linspace(0, 1, 512).reshape(-1, 1)

        image = self.axis.imshow(
            gradient,
            extent=(x_num.min(), x_num.max(), baseline, max(y)),
            origin="lower",
            aspect="auto",
            cmap=bloomberg_cmap,
            alpha=0.35,
            interpolation="bicubic",
            zorder=1,
        )

        self.axis.imshow(
                    gradient,
                    extent=(x_num.min(), x_num.max(), baseline, (max(y) * (1 + margin))),
                    origin="lower",
                    aspect="auto",
                    cmap=bloomberg_bgmap,
                    alpha=0.197,
                    interpolation="bicubic",
                    zorder=0,
                )

        image.set_clip_path(clip_polygon)

        self.axis.set_xlim(x_num.min(), x_num.max())
        self.axis.set_ylim(baseline, (max(y) * (1 + margin)))
        self.axis.plot(x, y, color="white", linewidth=0.5)
        self.axis.grid(alpha=0.3)