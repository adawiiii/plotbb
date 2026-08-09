import matplotlib.pyplot as plt

from typing import Any
from cycler import cycler
from functools import wraps
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.dates import date2num
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

from numpy import linspace, column_stack, vstack, asarray

def _apply_style(fig: Figure) -> None:
    fig.set_facecolor("#000000")

    for ax in fig.get_axes():
        ax.set_facecolor("#000000")
        ax.tick_params(axis="both", colors="white")

        ax.set_prop_cycle(cycler(color=[
            "#00dbf4",
            "#ff4040",
            "#90fa75",
            "#ffd700",
        ]))
        
        ax.title.set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

        for spine in ax.spines.values():
            spine.set_color("#444444")

        ax.grid(
            color="#ffffff",
            linestyle=":",
            linewidth=1,
            alpha=0.35,
        )

        legend = ax.get_legend()

        if legend is not None:
            frame = legend.get_frame()
            frame.set_facecolor("#111111")
            frame.set_edgecolor("#222222")

            for text in legend.get_texts():
                text.set_color("white")

class PBBFigure(Figure):
    def draw(self, renderer):
        # Runs after the user adds artists but before they are rendered.
        _apply_style(self)
        super().draw(renderer)

@wraps(plt.subplots)
def subplots(*args, **kwargs):
    kwargs.setdefault("FigureClass", PBBFigure)
    kwargs.setdefault("layout", "tight")
    return plt.subplots(*args, **kwargs)

class PlotBB:
    def __init__(self, figure: Figure | None = None, axis: Axes | None = None) -> None:
        self.axis =  axis if axis is not None else plt.gca()

        if figure is not None:
            self.figure = figure
        elif figure is None:
            self.figure = plt.gcf()

        return
    
    def plot(self, *args, margin: float = 0.05, **kwargs) -> list[Line2D]:
        lines = self.axis.plot(*args, color="white", linewidth=0.5, **kwargs)

        for line in lines:
            x = asarray(line.get_xdata(orig=True), dtype=float)
            y = asarray(line.get_ydata(orig=False), dtype=float)    

            x_num = date2num(x)
            baseline = (min(y) * (1 - margin))
            gradient = linspace(0, 1, 512).reshape(-1, 1)
    
            # Polygon of area under the line
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
            
            # Gradient under chart
            bloomberg_cmap = LinearSegmentedColormap.from_list(
                "bloomberg_fill",
                [
                    (0.00, "#020250"),
                    (0.05, "#020250"),
                    (0.32, "#0058B1"),
                    (0.62, "#1086be"),
                    (0.80, "#27bef8"),
                    (0.92, "#00dbf4"),
                    (1.00, "#00dbf4"),
                ],
            )
    
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
    
            image.set_clip_path(clip_polygon)
            
            # Background gradient
            bloomberg_bgmap = LinearSegmentedColormap.from_list(
                        "bloomberg_bg",
                        [
                            "#000000",
                            "#91DCFF"
                        ],
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
    
            # Sizing 
            self.axis.set_xlim(x_num.min(), x_num.max())
            self.axis.set_ylim(baseline, (max(y) * (1 + margin)))
            self.axis.grid(alpha=0.35)

        self.figure.set_layout_engine("tight")

        return lines