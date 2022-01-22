from PIL import Image, ImageSequence
from PIL.ImageFilter import BoxBlur
#  Elmo Burn
# o = Image.open('a.png').resize((150, 150)).convert('RGBA')
# elmo_gif = Image.open('elmo_burn.gif')
# frames = []
# for frame in ImageSequence.Iterator(elmo_gif):
#     new_elmo = frame.convert('RGBA')
#     new_elmo.paste(o, (175, 125))
#     frames.append(new_elmo)
# frames[0].save('elmo_p.gif', format='GIF', append_images=frames[1:], save_all=True, loop=0)


#  RAIN
# image = Image.open('a.png').resize((330, 330)).convert("RGBA")
# gif = Image.open('rain.gif')
# print(gif.size)
# frames = []
# for frame in ImageSequence.Iterator(gif):
#     im_c = image.copy()
#     frame = frame.convert('RGBA')
#     mask_im = Image.new('RGBA', frame.size, (255, 255, 255, 175))
#     im_c.paste(frame, (0, 0), mask_im)
#     frames.append(im_c)
# frames[0].save(
#     'rain_m.gif',
#     format='gif',
#     save_all=True,
#     append_images=frames[1:],
#     loop=0,
#     duration=100,
#     optimize=True)


# image = Image.open('a.png').resize((330, 330)).convert("RGBA")
# gif = Image.open('tv_static.gif')
# print(gif.size)
# frames = []
# for frame in ImageSequence.Iterator(gif):
#     im_c = image.copy()
#     frame = frame.convert('RGBA')
#     mask_im = Image.new('RGBA', frame.size, (255, 255, 255, 200))
#     im_c.paste(frame, (0, 0), mask_im)
#     frames.append(im_c)
# frames[0].save(
#     'rain_m.gif',
#     format='gif',
#     save_all=True,
#     append_images=frames[1:],
#     loop=0,
#     duration=100,
#     optimize=True)

# Remove Bg

# DAOA16
# gif = Image.open('eq.gif')
# frames = []
# for frame in ImageSequence.Iterator(gif):
#     frame = frame.convert('RGBA')
#     wi, hi = frame.size
#     pix = frame.load()
#     for w in range(wi):
#         for h in range(hi):
#             if pix[w, h] == (0, 0, 0, 255):
#                 pix[w, h] = (0, 0, 0, 0)
#     frames.append(frame)
# frames[0].save('math.gif',
#                format='gif',
#                save_all=True,
#                append_images=frames[1:],
#                loop=0)

# print(frames[0].size)


# Math GIf
# image = Image.open('a.png').resize((330, 330)).convert("RGBA")
# gif = Image.open('math.gif')
# print(gif.size)
# frames = []
# for frame in ImageSequence.Iterator(gif):
#     im_c = image.copy()
#     frame = frame.convert('RGBA')
#     mask_im = Image.new('RGBA', frame.size, (255, 255, 255, 50))
#     im_c.paste(frame, (0, 0), mask_im)
#     frames.append(im_c)
# frames[0].save(
#     'm_m.gif',
#     format='gif',
#     save_all=True,
#     append_images=frames[1:],
#     loop=0,
#     duration=100,
#     optimize=True)


# Code to make Album Cover over Image
# image = Image.open('hitler.jpg').convert("RGBA")
# pa = Image.open('parental_advisory.jpg').convert("RGBA")
# pten = 0.10
# w, h = image.size
# pa_resized = pa.resize((int(w * 0.18), int(h * 0.12)))
# newimg = image.resize(((w - int(w * pten * 2)), h - int(h * pten * 2)))
# image = image.filter(BoxBlur(radius=10))
# image.paste(newimg, (int(w * pten), int(h * pten)), newimg)
# image.paste(pa_resized, (int(w * pten) + int(pa_resized.width / 2), h - int(h * pten * 2) - int(h * pten)), pa_resized)
# image.save('exp.png')

# Glitchthis

# glitcher = ImageGlitcher()
# im = Image.open('a.png')
# gl = glitcher.glitch_image(im, 2, color_offset=True, gif=True)
# gl[0].save(
#     'm_m.gif',
#     format='gif',
#     save_all=True,
#     append_images=gl[1:],
#     loop=0,
#     duration=100,
#     optimize=True)
