# PlotBB
![Latest Release](https://img.shields.io/github/v/release/adawiiii/plotbb) ![License](https://img.shields.io/github/license/adawiiii/plotbb) [![PyPi](https://img.shields.io/pypi/v/plotbb)](https://pypi.org/project/plotbb/)

[![GitHub issues](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/adawiiii/plotbb/issues) [![Contributing](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg?)](https://github.com/adawiiii/plotbb/fork)

A Python package to be used in conjunction with Matplotlib to emulate the look of the [Bloomberg](#disclaimers) charts, because not all of us have $31,980 to spare.

## Examples
```PlotBB.plot(x, y, fill="blue", bg="light_blue")```

![blue_bg_blue_example](https://github.com/adawiiii/plotbb/blob/main/figures/blue_example.png)

---

```PlotBB.plot(x, y, fill="orange", bg="light_blue")```

![orange_bg_blue_example](https://github.com/adawiiii/plotbb/blob/main/figures/orange_blue_bg_example.png)

---

```PlotBB.plot(x, y, fill="orange", bg="none")```

![orange_bg_none_example](https://github.com/adawiiii/plotbb/blob/main/figures/orange_example.png)

## Usage
> [!NOTE]
> All functions like `subplots()` and `PlotBB.plot()` are wrappers for their Matplotlib respective underlying function and all `*args` and `**kwargs` are passed. This allows users to modify any styling or behavior. 

### Single plot setup:
```py
from plotbb import PlotBB
import matplotlib as plt
import pandas as pd

chart_data = pd.read_csv("time_series_data.csv")

chart = PlotBB()
chart.plot(chart_data["Date"], chart_data["Price"])

plt.show()
```

### Multiplot setup with `subplots()`:
```py
from plotbb import PlotBB, subplots
import matplotlib as plt
import pandas as pd

chart_data = pd.read_csv("time_series_data.csv")

fig, axes = subplots(
    nrows=3,
    ncols=1,
    figsize=(12, 8),
    sharex=True
)

chart1 = PlotBB(axis=axes[0])
chart1.plot(chart_data["Date"], chart_data["Price"])

plt.show()
```
> [!WARNING]
> Ensure `plotbb.subplots()` is used and NOT `matplotlib.pyplot.subplots()`. Also ensure the correct `Axes` is used. This allows PlotBB to style the Matplotlib correctly and draw on the correct subplot. 

### Different plot styles:
```py
from plotbb import PlotBB, subplots
import matplotlib as plt
import pandas as pd

chart_data = pd.read_csv("time_series_data.csv")

fig, axes = subplots(
    nrows=3,
    ncols=1,
    figsize=(12, 8),
    sharex=True
)

chart1 = PlotBB(axis=axes[0])
chart1.plot(chart_data["Date"], chart_data["Price"], fill="orange", bg="none")

plt.show()
```
## Contributing
Feel free to contribute by either giving more references of the Terminal charts (as I don't have access to the actual terminal and am limited to photos from Google), submitting issues on the [repository's page](https://github.com/adawiiii/plotbb/issues), or forking and creating pull requests. Any help is appreciated! 

## Disclaimers
This service has been developed independently from and is not endorsed by the Bloomberg L.P. "Bloomberg" and "Bloomberg Terminal" are trademarks and service marks of Bloomberg Finance L.P., a Delaware limited partnership, or its subsidiaries.
