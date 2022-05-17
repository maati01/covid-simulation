import matplotlib
import numpy as np
import pylab as pl

if __name__ == "__main__":
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue", "yellow", "red"])
    a = np.array([[0, 4000]])
    pl.figure(figsize=(1.5, 6))
    img = pl.imshow(a, cmap=cmap)
    pl.gca().set_visible(False)
    cax = pl.axes([0.2, 0.1, 0.4, 0.8])
    pl.colorbar(orientation="vertical", cax=cax)
    pl.title("infected")
    pl.savefig("../data/colorbar.jpg")