# utils/matplotlib_style.py

import matplotlib.pyplot as plt


def apply_dark_theme():
    plt.style.use("dark_background")
    plt.rcParams.update(
        {
            "axes.edgecolor": "#FFFFFF",
            "axes.labelcolor": "#FFFFFF",
            "axes.titlecolor": "#FFFFFF",
            "xtick.color": "#FFFFFF",
            "ytick.color": "#FFFFFF",
            "text.color": "#FFFFFF",
            "grid.color": "#555555",
            "legend.facecolor": "#2e2e2e",
            "legend.edgecolor": "#FFFFFF",
        }
    )
