# Copyright (C) z03h https://github.com/z03h
# 2021 - Present

import io

import numpy as np

from wand.image import Image as wImage
from PIL import Image, ImageSequence, ImageFilter, ImageChops, ImageEnhance, ImageDraw

from app.exceptions.errors import BadImage, ParameterError, ManipulationError

__all__ = ('neon', 'a_neon')


def gif_a_neon(oim, **kwargs):
    """Specific function for animated source and animated gradient
    kwargs are similar to neon_static
    """
    kwargs = default_neon_kwargs(kwargs)
    # getting options
    sharp = kwargs.get('sharp', True)
    soft = kwargs.get('soft', True)
    if not (sharp or soft):
        raise ParameterError('sharp and soft both cannot be False')
    overlay = kwargs.get('overlay', False)
    single = False
    try:
        colors = kwargs['colors']
        colors_per_frame = kwargs.get('colors_per_frame') or 3
        gradient_direction = kwargs.get('gradient_direction', 1)
    except KeyError:
        raise ParameterError('Must set "colors"')

    if not all(isinstance(c, (tuple, list)) for c in colors):
        raise ParameterError('colors must be a tuple/list of RGB tuples')

    horizontal = gradient_direction % 2
    # create the gradient
    paste = create_gradient(oim, colors, single, gradient_direction,
                            horizontal, colors_per_frame)
    if gradient_direction in (0, 1):
        # reverse gradient to reverse direction
        paste = paste.rotate(180)

    # starting position of gradient
    position = 0
    num_frames = oim.n_frames

    # calculate pixel to move per frame
    if gradient_direction == 5:
        step = 360
        paste = paste.resize((oim.width * 2, oim.height * 2))
    elif horizontal:
        # set step based on width if horizontal gradient
        # or height for vertical gradient
        step = int((paste.width if horizontal else paste.height) / 2)
    # divmod to get as equal steps as possible while
    # summing to original size
    step, rem = divmod(step, num_frames)
    iter_steps = iter(([step + 1] * rem) + ([step] * (num_frames - rem)))

    if gradient_direction in (1, 2):
        # reverse the position for reversed gradient
        position = -paste.width + oim.width if horizontal else -paste.height + oim.height
    frames = []
    durations = []
    for im in ImageSequence.Iterator(oim):
        # Processing per frame
        durations.append(oim.info.get('duration', 10))
        im = preprocess_neon(im, single=single, **kwargs)

        # create sharp outline
        outline = create_sharp_outline(im, single, **kwargs)

        # create mask when pasting end result colors
        with im, outline, Image.new('L', im.size, 0) as mask:
            if soft:
                # create soft outline
                mask = create_soft_outline(outline, single, **kwargs)

            if sharp:
                # paste sharp outline
                mask.paste(outline, mask=outline)

            # start pasting gradient
            temp = im.copy() if overlay else Image.new('RGBA', im.size,
                                                       (0, 0, 0, 255))
            with process_gradient(paste, mask, position,
                                  gradient_direction) as temp_paste:
                temp.paste(temp_paste, mask=mask)
        frames.append(temp)

        # reverse the step for reverse gradients
        position -= -next(iter_steps) if gradient_direction in (
            1, 2) else next(iter_steps)

    return frames, durations


def default_neon_kwargs(kwargs):
    defaults = {
        'sharp': True,
        'soft': True,
        'overlay': False,
        'brightness': 1.0,
        'saturation': 1.0,
        'gradient': 0,
        'gradient_direction': 3,
        'colors_per_frame': 3,
    }
    for kwarg, value in kwargs.items():
        if value is None and kwarg in defaults:
            kwargs[kwarg] = defaults[kwarg]

    return kwargs


def neon_static(oim, **kwargs):
    """neon colors for single images

    Parameters
    ----------
    sharp: :class:`bool`
        Whether to include the sharp outline. Default is ``True``.
        sharp and soft both cannot be ``False``.
    sharp_brightness: :class:`float`
        How much to adjust the sharp outline brghtneess.
        Default is 3 for static and 2 for animated
    soft: :class:`bool`
        Whether to include the soft outline. Default is ``True``.
        soft and sharp both cannot be ``False``.
    soft_brightness: :class:`float`
        How much to adjust the sharp outline brghtneess.
        Default is 3 for static and 2 for animated
    soft_softness: :class:`float`
        How much to blur the soft outline by
    overlay: :class:`bool`
        Whether outline is overlaid on top of the original image.
        Default is ``False``.
    brightness: :class:`float`
        Brightness of original image if overlaid. Default is ``0.85``
    colors: Union[List[Tuple]]
        List of RGB tuples.
        Ex.  ``[(255,0,0), (0,0,255)]``
    per_color: :class:`int`
        How many frames per color OR % of image to move per frame for
        animated gradient. Does nothing for single color/static gradient.
    gradient: :class:`int`
        0: no gradient
        1: static gradient
        2: animated gradient
        Default is ``0``.
    gradient_direction: :class:`int`
        direction of the gradient and animation
        left:3
        down:2
        right:1
        up:0
    colors_per_frame: :class:`int`
        How many colors are visible in the starting gradient frame.
        Default is ``3``.
    multi: :class:`bool`
        whether this should be treated as an animated image regardless of
        input. Defaults to ``False``
    saturation: :class:`float`
        How much to saturate or desaturate the image by. Default is ``None``
        for no change. ``0.0`` for grayscale, values > ``1.0`` to increase
        saturation. Does nothing unless overlay is ``True``.

        Passed to preprocessing.
    sharpen: :class:`int`
        -1 for smooth, -2 for smooth more, -3 or lower for gauss blur of radius -(x+2)
        0 for detail, 1 for sharpen, 2 for enhance edges, 3 for enhance edges more.
        Default is ``None`` for no sharpening.

        Passed to preprocessing
    """
    kwargs = default_neon_kwargs(kwargs)
    # getting options
    sharp = kwargs.get('sharp', True)
    soft = kwargs.get('soft', True)
    if not (sharp or soft):
        raise ParameterError('sharp and soft both cannot be False')
    overlay = kwargs.get('overlay', False)
    gradient = kwargs.get('gradient', 0)
    try:
        colors = kwargs['colors']
    except KeyError:
        raise ParameterError('Must set "colors"')
    else:
        per_color = kwargs.get('per_color') or 6
        if all(isinstance(c, (tuple, list)) for c in colors):
            # tuple of rgb tuples
            if len(colors) == 1:
                # passed single color, switch to single neon
                gradient = 0
                # single color, statis neon
                single = True
                colors = tuple(colors[0])
            else:
                if gradient not in (0, 1, 2):
                    raise ParameterError('gradient must be 0, 1, or 2')

                # 0 no gradient, animated
                # 1 static gradient
                # 2 animated gradient, animated
                single = gradient == 1
                colors_per_frame = kwargs.get('colors_per_frame') or 3
                gradient_direction = kwargs.get('gradient_direction', 1)
        elif all(isinstance(c, int) for c in colors) and len(colors) == 3:
            # colors is tuple of (r,g,b) instead of nested tuple ((r,g,b),)
            gradient = 0
            single = True
        else:
            raise ParameterError(
                'colors must be a tuple/list of RGB tuples or RGB tuple')

    # Actual processing
    im = preprocess_neon(oim, single=single, **kwargs)

    # create sharp outline
    outline = create_sharp_outline(im, single, **kwargs)

    # create mask when pasting end result colors
    with Image.new('L', im.size, (0)) as mask:
        if soft:
            # create soft outline
            mask = create_soft_outline(outline, single, **kwargs)

        if sharp:
            # paste sharp outline
            mask.paste(outline, mask=outline)
            outline.close()

        # set effect kwargs
        options = {'overlay': overlay, 'per_color': per_color}
        # set to neon static
        effect = neon_static_breathing
        if gradient:
            # add gradient options
            options['colors_per_frame'] = colors_per_frame
            options['gradient_direction'] = gradient_direction
            # switch to gradient function
            effect = neon_static_gradient
        return effect(im, mask, colors, single, **options)


def preprocess_neon(im, *, single, **kwargs):
    sharpen = kwargs.get('sharpen', None)
    saturation = kwargs.get('saturation', None)
    overlay = kwargs.get('overlay', False)

    # convert to RGB
    im = im.convert('RGB')

    # get kwargs max size or use arg single to determine size
    maxsize = kwargs.get('maxsize', 512 if single else 256)
    size = max(im.size)
    if size > maxsize:
        # resize image while trying to keep ratio
        ratio = size / maxsize
        im = im.resize((int(im.width / ratio), int(im.height / ratio)))

    # Apply sharpening or smoothing to edges before getting edges
    if sharpen is not None:
        if sharpen >= 0:
            filters = (
                ImageFilter.DETAIL,
                ImageFilter.SHARPEN,
                ImageFilter.EDGE_ENHANCE,
                ImageFilter.EDGE_ENHANCE_MORE,
            )
        else:
            sharpen = -sharpen
            filters = (
                ImageFilter.DETAIL,
                ImageFilter.SMOOTH,
                ImageFilter.SMOOTH_MORE,
                ImageFilter.GaussianBlur(sharpen - 2),
            )
            sharpen = min(
                3, sharpen)  # allow for blur but overflow just blurs more

        try:
            im = im.filter(filters[sharpen])
        except IndexError:
            pass
    # Darken to slightly enhance outline colors
    if overlay:
        enhance = ImageEnhance.Brightness(im)
        im = enhance.enhance(kwargs.get('brightness') or 1.0)

        # Apply saturation
        if saturation is not None:
            enhancer = ImageEnhance.Color(im)
            im = enhancer.enhance(saturation)

    return im


def create_sharp_outline(im, single, **kwargs):
    multi = kwargs.get('multi')
    # get edges, convert to L mode
    countour_outline = ImageChops.invert(
        im.filter(ImageFilter.CONTOUR).convert('L'))

    # contour creates white lines along the edges of the image
    # remove outer edge with a mask

    # Can potentially clip the image but removes the resulting edge glow
    width, height = countour_outline.size
    width -= 1
    height -= 1
    draw = ImageDraw.Draw(countour_outline)
    # draw black lines along edges
    draw.line((0, 0, 0, height), 0, 1)
    draw.line((0, 0, width, 0), 0, 1)
    draw.line((width, height, 0, height), 0, 1)
    draw.line((width, height, width, 0), 0, 1)

    # birghten to enhance sharp outline
    enhancer = ImageEnhance.Brightness(countour_outline)
    countour_outline = enhancer.enhance(
        kwargs.get('sharp_brightness')
        or (3.0 if single and not multi else 2.0))

    return countour_outline


def create_soft_outline(outline, single, **kwargs):
    # multi = kwargs.get('multi')
    # blur to create soft effect
    brightness = kwargs.get('soft_brightness') or (1.0)
    radius = kwargs.get('soft_softness') or 13

    steps = max(int(radius//5), 1)
    step = radius/steps

    # blur to create soft effect
    # enhance to brighten soft outline colors
    frames = (ImageEnhance.Brightness(outline.filter(ImageFilter.GaussianBlur(radius+1-step*i))).enhance(brightness) for i in range(steps))
    arr = np.zeros((outline.height, outline.width))
    for i, frame in enumerate(frames, 1):
        arr += np.array(frame).astype(np.float64)/i
    amax = np.amax(arr)
    if amax:
        arr = arr/(amax / 200)
        arr = arr.astype(np.uint8)
    else:
        arr = np.zeros(arr.shape, dtype=np.uint8)

    # soft = ImageEnhance.Brightness(soft).enhance(brightness)
    return Image.fromarray(arr)


def neon_static_breathing(im, mask, colors, single, *, overlay, per_color):
    """handles single color or breathing effect"""
    if single:
        # single color
        with Image.new('RGB', im.size, colors) as paste:
            # use original if overlay or new image
            temp = im if overlay else Image.new('RGBA', im.size,
                                                (0, 0, 0, 255))
            temp.paste(paste, mask=mask)
        return temp

    # animated breathing
    frames = []
    # add first color to cycle back to original
    iter_colors = iter(colors + type(colors)((colors[0], )))
    next_color = next(iter_colors)
    while True:
        try:
            # get current and next color
            current = next_color
            next_color = next(iter_colors)
        except StopIteration:
            break
        # get range of colors between current and next
        for color in color_range(current, next_color, per_color):
            with Image.new('RGB', im.size, color) as paste:
                # copy original if overlay else new image
                temp = im.copy() if overlay else Image.new(
                    'RGBA', im.size, (0, 0, 0, 255))
                temp.paste(paste, mask=mask)
            frames.append(temp)
    return frames


# code from Mark Ransom
# https://stackoverflow.com/a/49321304
def to_sRGB(x):
    ''' Returns a sRGB value in the range [0,255]
        for linear input in [0,1]
    '''
    return int(255.9999 * (12.92 * x if x <= 0.0031308 else
                           (1.055 * (x**(1 / 2.4))) - 0.055))


def from_sRGB(x):
    ''' Returns a linear value in the range [0,1]
        for sRGB input in [0,255].
    '''
    x /= 255.0
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055)**2.4


def lerp(color1, color2, frac):
    return color1 * (1 - frac) + color2 * frac


def color_range(color1, color2, steps):
    gamma = .43
    color1_lin = [from_sRGB(c) for c in color1]
    bright1 = sum(color1_lin)**gamma
    color2_lin = [from_sRGB(c) for c in color2]
    bright2 = sum(color2_lin)**gamma
    for step in range(steps):
        intensity = lerp(bright1, bright2, step / steps)**(1 / gamma)
        color = tuple(
            lerp(cl1, cl2, step / steps)
            for cl1, cl2 in zip(color1_lin, color2_lin))
        if sum(color) != 0:
            color = [c * intensity / sum(color) for c in color]
        color = tuple(to_sRGB(c) for c in color)
        yield color


def neon_static_gradient(im, mask, colors, single, gradient_direction, *,
                         overlay, per_color, colors_per_frame):
    """handles static or animated gradient effect"""
    horizontal = gradient_direction % 2
    # create gradient to paste
    paste = create_gradient(im, colors, single, gradient_direction, horizontal,
                            colors_per_frame)

    if single:
        # static image
        if paste.size != mask.size:
            # resize incase of rounding error
            paste = paste.resize(mask.size)
        temp = im if overlay else Image.new('RGBA', im.size, (0, 0, 0, 255))
        with paste, mask:
            temp.paste(paste, mask=mask)
        return temp

    # animated gradient
    frames = []
    position = 0
    if gradient_direction == 5:
        # radial gradient
        step = int(360 * per_color)
        min_pos = -360
        # make sure paste fits the mask when rotated
        paste = paste.resize((mask.width * 2, mask.height * 2))
    else:
        # get the step based on width if horizontal gradient
        # or height if vertical gradient
        attr = 'width' if horizontal else 'height'
        # horizontal
        step = int(getattr(im, attr) * per_color)
        min_pos = -int(getattr(paste, attr) / 2)

    step, rem = divmod(step, 100)
    steps = iter([step + 1] * rem)

    while position > min_pos:
        # copy if overlay else new image
        temp = im.copy() if overlay else Image.new('RGBA', im.size,
                                                   (0, 0, 0, 255))
        temp_paste = process_gradient(paste, mask, position,
                                      gradient_direction)
        with temp_paste, mask:
            temp.paste(temp_paste, mask=mask)
        frames.append(temp)
        try:
            # move position step+1 rem times
            position -= next(steps)
        except StopIteration:
            # use step after StopIteration
            position -= step
    return frames


def create_gradient(im, colors, single, gradient_direction, horizontal,
                    colors_per_frame):
    arrays = []
    # add first color to rotate back
    iter_colors = iter(colors + type(colors)(
        (colors[0], ))) if not single or gradient_direction == 5 else iter(
            colors)
    next_color = next(iter_colors)
    # single gradient fits in original image
    # moving gradient is extended part original image
    ratio = len(
        colors
    ) - 1 if single or gradient_direction == 5 else colors_per_frame - 1
    while True:
        # create gradients with 2 colors
        try:
            current = next_color
            next_color = next(iter_colors)
        except StopIteration:
            break
        with wImage() as wim:
            # use ImageMagick pseudo scripts to create gradients
            wim.clear()
            pseudo = f'gradient:rgb{tuple(current)}-rgb{tuple(next_color)}'
            if horizontal:
                # horizontal gradient
                wim.options['gradient:direction'] = 'east'
                wim.pseudo(int(im.width / ratio), im.height, pseudo)
            else:
                # vertical gradient
                wim.options['gradient:direction'] = 'north'
                wim.pseudo(im.width, int(im.height / ratio), pseudo)
            # image to array, add array to a list
            arrays.append(np.array(wim))
    if not horizontal:
        # uh idk why, I think it's backwards
        arrays.reverse()
    # use numpy to combine arrays
    # hstack for horizontal // vstack for vertical gradient
    stack = np.hstack if horizontal else np.vstack

    # get pil image from stacked arrays
    if gradient_direction == 5:
        # create radial gradient
        with wImage.from_array(stack(arrays)) as wim:
            wim.virtual_pixel = 'edge'
            wim.distort('arc', (360, ))
            paste = Image.fromarray(np.array(wim))
    else:
        # combine into horizontal/vertical gradient
        paste = Image.fromarray(
            stack(arrays if single else [*arrays, *arrays]))

    if (single and gradient_direction in (1, 2)) or gradient_direction == 5:
        # reverse the gradient for correct direction
        paste = paste.rotate(180)
    return paste


def process_gradient(paste, mask, position, gradient_direction):
    """Helper method to crop the gradient to correct sizes"""
    horizontal = gradient_direction % 2
    if gradient_direction == 5:
        coords = (int(paste.width / 4), int(paste.height / 4),
                  int(paste.width / 4) + mask.width,
                  int(paste.height / 4) + mask.height)
        return paste.rotate(-position).crop(coords)
    elif horizontal:
        # horizontal
        return paste.crop((-position, 0, -position + mask.width, mask.height))
    else:
        # vertical
        return paste.crop((0, -position, mask.width, -position + mask.height))


def neon(oim, colors, **kwargs):
    """Handles static source neon images

    Parameters
    ----------
    sharp: :class:`bool`
        Whether to include the sharp outline. Default is ``True``.
        sharp and soft both cannot be ``False``.
    sharp_brightness: :class:`float`
        How much to adjust the sharp outline brghtneess.
        Default is 3 for static and 2 for animated
    soft: :class:`bool`
        Whether to include the soft outline. Default is ``True``.
        soft and sharp both cannot be ``False``.
    soft_brightness: :class:`float`
        How much to adjust the sharp outline brghtneess.
        Default is 3 for static and 2 for animated
    soft_softness: :class:`int`
        How much to blur soft outline
    overlay: :class:`bool`
        Whether outline is overlaid on top of the original image.
        Default is ``False``.
    brightness: :class:`float`
        Brightness of original image if overlaid. Default is ``0.85``
    colors: Union[List[Tuple]], Tuple[Tuple]]
        List of RGB tuples.
        Ex.  ``[(255,0,0), (0,0,255)]``
    per_color: :class:`int`
        How many frames per color OR % of image to move per frame for
        animated gradient. Does nothing for single color/static gradient.
    gradient: :class:`int`
        0: no gradient
        1: static gradient
        2: animated gradient
        Default is ``0``.
    direction: :class:`str`
        direction of the gradient and animation
        [L]eft, [R]ight, [U]p, [D]own, Radial
    colors_per_frame: :class:`int`
        How many colors are visible in the starting gradient frame.
        Default is ``3``.
    saturation: :class:`float`
        How much to saturate or desaturate the image by. Default is ``None``
        for no change. ``0.0`` for grayscale, values > ``1.0`` to increase
        saturation. Does nothing unless overlay is ``True``.

        Passed to preprocessing.
    sharpen: :class:`int`
        -1 for smooth, -2 for smooth more, -3 or lower for gauss blur of radius -(x+2)
        0 for detail, 1 for sharpen, 2 for enhance edges, 3 for enhance edges more.
        Default is ``None`` for no sharpening.

        Passed to preprocessing
    """

    gradient = kwargs.pop('gradient', 0)
    overlay = kwargs.pop('overlay', False)

    directions = {
        'l': 3,
        'left': 3,
        'd': 2,
        'down': 2,
        'r': 1,
        'right': 1,
        'u': 0,
        'up': 0,
        'radial': 5
    }
    gradient_direction = directions.get(kwargs.pop('direction', '').lower(), 3)

    per_color = kwargs.pop('per_color', None)
    saturation = kwargs.pop('saturation', None)
    image = neon_static(oim,
                        colors=colors,
                        per_color=per_color or (10 if gradient else 8),
                        saturation=saturation or 0.7,
                        overlay=overlay,
                        gradient=gradient,
                        gradient_direction=gradient_direction,
                        **kwargs)
    final = io.BytesIO()
    if isinstance(image, list):
        ext = 'gif'
        if gradient == 2 and gradient_direction in (1, 2):
            # reverse images to simulate moving the opposite direction
            image.reverse()
        image[0].save(final,
                      format=ext,
                      save_all=True,
                      dispose=2,
                      append_images=image[1:],
                      loop=0)
    else:
        # single image, save normally
        ext = 'png'
        image.save(final, format=ext)
    final.seek(0)
    return final


def a_neon(oim, colors, **kwargs):
    """Handles animated source to neon images
    Refer to :func:`neon` for kwarg info
    """
    gradient = kwargs.pop('gradient', 0)
    overlay = kwargs.pop('overlay', False)

    directions = {
        'l': 3,
        'left': 3,
        'd': 2,
        'down': 2,
        'r': 1,
        'right': 1,
        'u': 0,
        'up': 0,
        'radial': 5
    }
    gradient_direction = directions.get(kwargs.pop('direction', '').lower(), 3)

    # start neon process after getting image bytes
    image = []
    durations = []

    try:
        # another animated check
        total_frames = oim.n_frames
        if total_frames < 2:
            raise BadImage('Image not animated')
    except AttributeError:
        raise BadImage('Image not animated')

    if not gradient and len(colors) > 1:
        # create the colors for breathing

        # check # of colors to frames
        if len(colors) >= total_frames:
            raise ParameterError('Too many colors')

        # divmod to evenly distribute frames per colors
        # and match original frame count
        per, remainder = divmod(total_frames, len(colors))
        _frames_per_color = ([per + 1] *
                             remainder) + ([per] * (len(colors) - remainder))
        iter_colors = []
        ic = iter(colors + type(colors)((colors[0], )))
        next_color = next(ic)
        for num_frames in _frames_per_color:
            try:
                current = next_color
                next_color = next(ic)
            except StopIteration:
                break
            iter_colors.extend(color_range(current, next_color, num_frames))
        iter_colors = iter(iter_colors)
    per_color = kwargs.pop('per_color', None)
    saturation = kwargs.pop('saturation', None)
    colors_per_frame = kwargs.pop('colors_per_frame', None)
    if gradient != 2:
        # static/breathing/static gradient
        for im in ImageSequence.Iterator(oim):
            if not gradient and len(colors) > 1:
                # swap color per frame to simluate animated
                # breathing effect
                color = next(iter_colors)
            else:
                # static/static gradient
                # use all normal colors
                color = colors

            durations.append(im.info.get('duration', 10))
            frame = neon_static(im,
                                colors=color,
                                per_color=per_color or (10 if gradient else 8),
                                saturation=saturation or 0.7,
                                overlay=overlay,
                                gradient=gradient,
                                gradient_direction=gradient_direction,
                                maxsize=256,
                                multi=True,
                                **kwargs)
            image.append(frame)
    else:
        # animated gradient with animated source
        image, durations = gif_a_neon(oim,
                                      colors=colors,
                                      saturation=saturation or 0.7,
                                      overlay=overlay,
                                      gradient=gradient,
                                      gradient_direction=gradient_direction,
                                      colors_per_frame=colors_per_frame or 2,
                                      maxsize=256,
                                      **kwargs)
    final = io.BytesIO()
    if not isinstance(image, list):
        raise ManipulationError(
            f'Got {type(image)} instead of list of PIL.Image')
    ext = 'gif'
    image[0].save(final,
                  format=ext,
                  save_all=True,
                  dispose=2,
                  append_images=image[1:],
                  duration=durations,
                  loop=0)
    final.seek(0)
    return final
