import colorsys as cs

__all__ = ['Color']

class Color:
    RED         = (  1,    0,    0,    1)
    GREEN       = (  0,    1,    0,    1)
    BLUE        = (  0,    0,    1,    1)

    CYAN        = (  0,    1,    1,    1)
    MAGENTA     = (  1,    0,    1,    1)
    YELLOW      = (  1,    1,    0,    1)

    WHITE       = (  1,    1,    1,    1)
    BLACK       = (  0,    0,    0,    1)
    GRAY        = ( .5,   .5,   .5,    1)

    GRAY_P01    = ( .6,   .6,   .6,    1)
    GRAY_P02    = ( .7,   .7,   .7,    1)
    GRAY_P03    = ( .8,   .8,   .8,    1)
    GRAY_P04    = ( .9,   .9,   .9,    1)

    GRAY_M01    = ( .4,   .4,   .4,    1)
    GRAY_M02    = ( .3,   .3,   .3,    1)
    GRAY_M03    = ( .2,   .2,   .2,    1)
    GRAY_M04    = ( .1,   .1,   .1,    1)

    @staticmethod
    def convert_from_255_to_01(col: tuple):
        if len(col) == 4:
            return col[0] / 255, col[1] / 255, col[2] / 255, col[3] / 255
        else:
            return col[0] / 255, col[1] / 255, col[2] / 255

    @staticmethod
    def convert_from_hex_to_01(col: str):
        col = col.lstrip('#')

        if len(col) == 8:
            return int(col[0:2], 16) / 255, int(col[2:4], 16) / 255, int(col[4:6], 16) / 255, int(col[6:], 16) / 255
        else:
            return int(col[0:2], 16) / 255, int(col[2:4], 16) / 255, int(col[4:6], 16) / 255

    @staticmethod
    def from_rgba(r, g, b, a):
        return (r, g, b, a)

    def rgb_to_hsv(r, g, b):
        return cs.rgb_to_hsv(r, g, b)

    def hsv_to_rgb(h, s, v):
        return cs.hsv_to_rgb(h, s, v)

    def rgb_setValue(rgb, value):
        h, s, v = cs.rgb_to_hsv(*rgb)
        return cs.hsv_to_rgb(h, s, value)

    @staticmethod
    def change(color,byAmount,hue=False,val=False,sat=False):
        r,g,b = color[:-1]
        h,s,v = cs.rgb_to_hsv(r,g,b)

        if hue:
            h += byAmount
            h = h - int(h)

        if sat: s += byAmount
        if val: v += byAmount

        r,g,b = cs.hsv_to_rgb(h, s, v)

        return (r,g,b,color[3])

    @staticmethod
    def hue_p01(color): return Color.change(color,    .1,     hue=True)

    @staticmethod
    def hue_p02(color): return Color.change(color,    .2,     hue=True)

    @staticmethod
    def hue_p03(color): return Color.change(color,    .3,     hue=True)

    @staticmethod
    def hue_p04(color): return Color.change(color,    .4,     hue=True)

    @staticmethod
    def hue_m01(color): return Color.change(color,    -.1,    hue=True)

    @staticmethod
    def hue_m02(color): return Color.change(color,    -.2,    hue=True)

    @staticmethod
    def hue_m03(color): return Color.change(color,    -.3,    hue=True)

    @staticmethod
    def hue_m04(color): return Color.change(color,    -.4,    hue=True)

    @staticmethod
    def sat_p01(color): return Color.change(color,    .1,     sat=True)

    @staticmethod
    def sat_p02(color): return Color.change(color,    .2,     sat=True)

    @staticmethod
    def sat_p03(color): return Color.change(color,    .3,     sat=True)

    @staticmethod
    def sat_p04(color): return Color.change(color,    .4,     sat=True)

    @staticmethod
    def sat_m01(color): return Color.change(color,    -.1,    sat=True)

    @staticmethod
    def sat_m02(color): return Color.change(color,    -.2,    sat=True)

    @staticmethod
    def sat_m03(color): return Color.change(color,    -.3,    sat=True)

    @staticmethod
    def sat_m04(color): return Color.change(color,    -.4,    sat=True)

    @staticmethod
    def val_p01(color): return Color.change(color,    .1,     val=True)

    @staticmethod
    def val_p02(color): return Color.change(color,    .2,     val=True)

    @staticmethod
    def val_p03(color): return Color.change(color,    .3,     val=True)

    @staticmethod
    def val_p04(color): return Color.change(color,    .4,     val=True)

    @staticmethod
    def val_m01(color): return Color.change(color,    -.1,    val=True)

    @staticmethod
    def val_m02(color): return Color.change(color,    -.2,    val=True)

    @staticmethod
    def val_m03(color): return Color.change(color,    -.3,    val=True)

    @staticmethod
    def val_m04(color): return Color.change(color,    -.4,    val=True)

    @staticmethod
    def complementary(col):
        r,g,b,a = col
        hsv = cs.rgb_to_hsv(r, g, b)
        return cs.hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2]) + (a,)

