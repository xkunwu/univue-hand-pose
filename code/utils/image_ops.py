import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.collections as mcoll
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
from args_holder import args_holder


def fig2data(fig, show_axis=False):
    """
    @brief Convert a Matplotlib figure to a 3D numpy array with RGBA channels
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    if not show_axis:
        plt.gcf().gca().axis('off')
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    ncols, nrows = fig.canvas.get_width_height()
    buf = np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf


def show_depth(file_name):
    """ show a depth image """
    img = mpimg.imread(file_name)
    plt.imshow(img, cmap='bone')
    plt.show()


def make_color_range(Color_beg, Color_end, step=10):
    return list(
        Color_beg.range_to(Color_end, step)
    )


def make_cmap_gradient(Color_beg, Color_end, step=10):
    color_range = [C.rgb for C in make_color_range(Color_beg, Color_end, step)]
    color_value = []
    for ci in range(3):
        cri = [c[ci] for c in color_range]
        color_value.append(
            zip(np.linspace(0.0, 1.0, step), cri, cri)
        )
    return dict(red=color_value[0], green=color_value[1], blue=color_value[2])


def make_segments(x, y):
    """
    Create list of line segments in the correct format for LineCollection.
    """
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), linewidth=2):
    """
    Plot a colored line.
    """
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, linewidth=linewidth)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


if __name__ == '__main__':
    argsholder = args_holder()
    argsholder.parse_args()
    # test(argsholder.args)