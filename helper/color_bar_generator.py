import matplotlib
import numpy as np
import pylab as pl

SCALE = 4
PATH_TO_EXTENDED_COLOR_BAR = "../data/extended_color_bar.jpg"
PATH_TO_COLOR_BAR = "../data/color_bar.jpg"


def generate_color_bar(path: str, scale: int):
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue", "yellow", "red"])
    array = np.array([[0, 4000*(scale**2)]])
    pl.figure(figsize=(1.5, 6))
    pl.imshow(array, cmap=cmap)
    pl.gca().set_visible(False)
    cax = pl.axes([0.2, 0.1, 0.4, 0.8])
    pl.colorbar(orientation="vertical", cax=cax)
    pl.title("infected")

    pl.savefig(path)


if __name__ == "__main__":
    generate_color_bar(PATH_TO_EXTENDED_COLOR_BAR, SCALE)
    generate_color_bar(PATH_TO_COLOR_BAR, 1)
