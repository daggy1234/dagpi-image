from .WandManip import wand
from .decorators import executor


@executor
@wand
def sepia(image):
    image.sepia_tone(threshold=0.8)
    return image


@executor
@wand
def grayscale(image):
    image.transform_colorspace("gray")
    return image


@executor
@wand
def charcoal(image):
    image.transform_colorspace("gray")
    image.sketch(0.5, 0.0, 98.0)
    return image


@executor
@wand
def solar(image):
    image.solarize(threshold=0.5 * image.quantum_range)
    return image


@executor
@wand
def paint(image):
    image.oil_paint(sigma=3)
    return image


@executor
@wand
def poster(image):
    image.posterize(2)
    return image


@executor
@wand
def floor(image):
    print('floor')
    image.virtual_pixel = 'tile'
    image.resize(300, 300)
    x, y = image.width, image.height
    arguments = (0, 0, 77, 153,
                 x, 0, 179, 153,
                 0, y, 51, 255,
                 x, y, 204, 255)
    image.distort('perspective', arguments)
    return image


@executor
@wand
def swirl(image):
    image.swirl(degree=-90)
    return image


@executor
@wand
def polaroid(image):
    image.polaroid()
    return image


@executor
@wand
def edge(image):
    image.alpha_channel = False
    image.transform_colorspace('gray')
    image.edge(2)
    return image


@executor
@wand
def night(image):
    image.blue_shift(factor=1.25)
    return image
