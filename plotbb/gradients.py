from matplotlib.colors import LinearSegmentedColormap

bloomberg_orangemap = LinearSegmentedColormap.from_list(
    "bloomberg_orange",
    [
        (0.00, "#0a0a0a"),
        (0.85, "#b46200"),
        (1.00, "#b46200"),
    ]
)

bloomberg_bg_orange_map = LinearSegmentedColormap.from_list(
    "bloomberg_bg",
    [
        "#000000",
        "#85e2e8"
    ],
)

bloomberg_blue_map = LinearSegmentedColormap.from_list(
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

bloomberg_bg_blue_map = LinearSegmentedColormap.from_list(
    "bloomberg_bg",
    [
        "#000000",
        "#91DCFF"
    ],
)