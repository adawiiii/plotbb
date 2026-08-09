"""Bloomberg-inspired plotting helpers built on Matplotlib."""

import matplotlib.pyplot as plt

from cycler import cycler
from functools import wraps
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.dates import date2num
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap

from numpy import linspace, column_stack, vstack, asarray

from .gradients import bloomberg_blue_map, bloomberg_bg_blue_map, bloomberg_orangemap, bloomberg_bg_orange_map
from .options import ChartFillOption, ChartBackgroundOption

# 0.6 alpha bg #85e2e8
FILL_GRADIENTS = {
    "none": None,
    "blue": bloomberg_blue_map,
    "orange": bloomberg_orangemap,
}

def _background_gradients(fill_map: LinearSegmentedColormap, bg: ChartBackgroundOption) -> LinearSegmentedColormap | None:
    if fill_map is "blue" and bg is "blue":
        return bloomberg_bg_blue_map
    elif fill_map is "orange" and bg is "blue":
        return bloomberg_bg_orange_map
    else:
        return None

FILL_ALPHA = {
    "none": 0.0,
    "blue": 0.35,
    "orange": 0.6,
}

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
    """Matplotlib figure that applies the PlotBB style before rendering."""

    def draw(self, renderer):
        """Apply the PlotBB style and render the figure.

        Args:
            renderer: Matplotlib renderer used to draw the figure.
        """
        _apply_style(self)
        super().draw(renderer)

@wraps(
    plt.subplots,
    assigned=("__module__", "__name__", "__qualname__", "__annotations__"),
)
def subplots(*args, **kwargs):
    """Create a figure and axes with the PlotBB figure class and styling.

    Positional and keyword arguments are passed to
    :func:`matplotlib.pyplot.subplots`. Unless explicitly supplied,
    ``FigureClass`` is set to :class:`PBBFigure` and ``layout`` is set to
    ``"tight"``.

    Args:
        *args: Positional arguments accepted by Matplotlib's ``subplots``.
        **kwargs: Keyword arguments accepted by Matplotlib's ``subplots``.

    Returns:
        A ``(figure, axes)`` tuple matching the return value of Matplotlib's
        ``subplots``.

    Example:
        >>> fig, ax = subplots(figsize=(10, 6))
    """
    kwargs.setdefault("FigureClass", PBBFigure)
    kwargs.setdefault("layout", "tight")
    return plt.subplots(*args, **kwargs)

class PlotBB:
    """Add Bloomberg-inspired plots to a Matplotlib figure and axes.

    Args:
        figure: Figure to draw on. The current figure is used when omitted.
        axis: Axes to draw on. The current axes are used when omitted.

    Example:
        >>> fig, ax = subplots()
        >>> chart = PlotBB(fig, ax)
        >>> chart.plot([1, 2, 3], [10, 15, 12])
    """

    def __init__(self, figure: Figure | None = None, axis: Axes | None = None) -> None:
        """Initialize a chart using the supplied or current figure and axes.

        Args:
            figure: Figure to draw on. The current figure is used when omitted.
            axis: Axes to draw on. The current axes are used when omitted.
        """
        self.axis =  axis if axis is not None else plt.gca()

        if figure is not None:
            self.figure = figure
        elif figure is None:
            self.figure = plt.gcf()

        return
    
    def plot(
        self,
        *args,
        margin: float = 0.05,
        fill: ChartFillOption = "blue",
        bg: ChartBackgroundOption = "light_blue",
        **kwargs) -> list[Line2D]:
        """Plot lines with optional fill and background gradients.

        Positional arguments are passed to :meth:`matplotlib.axes.Axes.plot`.

        Args:
            *args: Data and formatting arguments accepted by Matplotlib's
                ``Axes.plot`` method.
            margin: Fractional vertical margin added around the plotted data.
            fill: Gradient beneath the line. Supported values are ``"none"``,
                ``"blue"``, and ``"orange"``.
            bg: Background gradient. Supported values are ``"none"`` and
                ``"light_blue"``.
            **kwargs: Additional keyword arguments passed to ``Axes.plot``.

        Returns:
            The line objects created by Matplotlib.

        Raises:
            KeyError: If ``fill`` is not a supported fill option.

        Example:
            >>> chart.plot(x, y, fill="orange", bg="light_blue")
        """
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
            
            # Chart colors
            fill_map = FILL_GRADIENTS[fill]
            fill_alpha = FILL_ALPHA[fill]

            bg_map = _background_gradients(fill_map=fill_map, bg=bg)

            # Gradient under chart
            if fill_map is not None:
                image = self.axis.imshow(
                    gradient,
                    extent=(x_num.min(), x_num.max(), baseline, max(y)),
                    origin="lower",
                    aspect="auto",
                    cmap=fill_map,
                    alpha=fill_alpha,
                    interpolation="bicubic",
                    zorder=1,
                )
        
                image.set_clip_path(clip_polygon)
            
            # Background gradient
            if bg_map is not None:
                self.axis.imshow(
                    gradient,
                    extent=(x_num.min(), x_num.max(), baseline, (max(y) * (1 + margin))),
                    origin="lower",
                    aspect="auto",
                    cmap=bg_map,
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
