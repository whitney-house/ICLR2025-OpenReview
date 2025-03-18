"""
To plot the bar chart.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from constants import X_LABEL
import os


class BarPlot:
    def __init__(self, xlabel=X_LABEL):
        self.xlabel = xlabel

    def plot(self, data, title, save_path=None):
        names, counts = zip(*data)  # separate two lists
        names, counts = names[::-1], counts[::-1]  # top is on top

        # theme
        sns.set_style("white")
        colors = sns.color_palette("BuGn", len(names))  # soft color

        # create fig
        fig, ax = plt.subplots(figsize=(12, 6))

        # bar
        bars = ax.barh(names, counts, color=colors, edgecolor="gray", linewidth=0.5)

        # x-axis setting
        ax.set_xlim(0, max(counts) * 1.1)

        # fonts
        ax.set_xlabel(self.xlabel, fontsize=14, fontweight="bold", fontfamily="serif")
        ax.set_title(title, fontsize=16, fontweight="bold", color="seagreen", fontfamily="serif")

        # show value and spare space
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() - 1,  # Shift inside the bar
                    bar.get_y() + bar.get_height() / 2,
                    f"{count}", ha="right", va="center", fontsize=12, color="white",
                    bbox=dict(facecolor="none", edgecolor="none", alpha=0.7))  # Transparent box

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        # option: save plot
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {save_path}")

        plt.show()



if __name__ == "__main__":
    bar_plot = BarPlot()
    test_data = [("Institution A", 50), ("Institution B", 40), ("Institution C", 30)]
    bar_plot.plot(test_data, "Top 3 Institutions", save_path="plots/fig1.png")


