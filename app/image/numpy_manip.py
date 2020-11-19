from io import BytesIO

import matplotlib.pyplot as plt
import skimage
from skimage import segmentation, future
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage.exposure import rescale_intensity
from skimage.feature import hog
from skimage.filters import sobel

from app.image.NumpyManip import NumpyManip, numpy
from app.image.PILManip import PILManip
from app.image.decorators import executor

__all__ = (
    "get_sobel",
    "hog_process",
    "rgb_graph",
    "triangle_manip"
)


@executor
def triangle_manip(byt: bytes) -> BytesIO:
    img = NumpyManip.image_read(byt)
    gimg = skimage.color.rgb2gray(img)
    labels = segmentation.slic(img, compactness=30, n_segments=400,
                               start_label=1)
    edges = sobel(gimg)
    edges_rgb = skimage.color.gray2rgb(edges)

    g = future.graph.rag_boundary(labels, edges)
    lc = future.graph.show_rag(labels, g, edges_rgb, img_cmap=None,
                               edge_cmap='viridis', edge_width=1.2)
    plt.colorbar(lc, fraction=0.03)
    plt.tight_layout()
    byt = BytesIO()
    plt.savefig(byt)
    byt.seek(0)
    return byt


@executor
@numpy
def get_sobel(img):
    # noinspection PyTypeChecker,PyUnresolvedReferences
    @adapt_rgb(each_channel)
    def _sobel_each(image):
        return skimage.filters.sobel(image)

    return rescale_intensity(1 - _sobel_each(img))


@executor
def hog_process(img: bytes) -> BytesIO:
    img = NumpyManip.image_read(img)
    fd, hog_image = hog(
        img,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        visualize=True,
        multichannel=True,
    )
    byt = BytesIO()
    plt.imsave(byt, hog_image, cmap=plt.cm.get_cmap("seismic"))
    byt.seek(0)
    return byt


@executor
def rgb_graph(img: bytes):
    def get_r(r):
        return "#%02x%02x%02x" % (r, 0, 0)

    def get_g(g):
        return "#%02x%02x%02x" % (0, g, 0)

    def get_b(b):
        return "#%02x%02x%02x" % (0, 0, b)

    im = PILManip.pil_image(img)
    dat = im.histogram()
    r_val = dat[0:256]
    g_val = dat[256:512]
    plt.figure()
    b_val = dat[512:768]
    axa = plt.subplot(2, 2, 1)
    axa.imshow(NumpyManip.image_read(img))
    axa.set_title("Image")
    axb = plt.subplot(2, 2, 2)
    for i in range(0, 256):
        axb.bar(i, r_val[i], color=get_r(i), alpha=0.3)
    axb.set_title("Red Values")
    axb.set_xlabel("Position")
    axb.set_ylabel("Red Intensity")
    axc = plt.subplot(2, 2, 3)
    for i in range(0, 256):
        axc.bar(i, g_val[i], color=get_g(i), alpha=0.3)
    axc.set_xlabel("Position")
    axc.set_ylabel("Green Intensity")
    axd = plt.subplot(2, 2, 4)
    for i in range(0, 256):
        axd.bar(i, b_val[i], color=get_b(i), alpha=0.3)
    axd.set_xlabel("Position")
    axd.set_ylabel("Blue Intensity")
    plt.tight_layout()
    byt = BytesIO()
    plt.savefig(byt)
    byt.seek(0)
    return byt
