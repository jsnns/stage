import colorsys


class Color:
    def __init__(self, hex: str = None, xy: list = None):
        self.hex = hex
        self._xy = xy

    def xy(self):
        """conversion of RGB colors to CIE1931 XY colors
        Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
        Args:
            red (float): a number between 0.0 and 1.0 representing red in the RGB space
            green (float): a number between 0.0 and 1.0 representing green in the RGB space
            blue (float): a number between 0.0 and 1.0 representing blue in the RGB space
        Returns:
            xy (list): x and y
        """

        red, green, blue = self.rgb()

        # gamma correction
        red = (
            pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
        )
        green = (
            pow((green + 0.055) / (1.0 + 0.055), 2.4)
            if green > 0.04045
            else (green / 12.92)
        )
        blue = (
            pow((blue + 0.055) / (1.0 + 0.055), 2.4)
            if blue > 0.04045
            else (blue / 12.92)
        )

        # convert rgb to xyz
        x = red * 0.649926 + green * 0.103455 + blue * 0.197109
        y = red * 0.234327 + green * 0.743075 + blue * 0.022598
        z = green * 0.053077 + blue * 1.035763

        # convert xyz to xy
        x = x / (x + y + z)
        y = y / (x + y + z)

        # TODO check color gamut if known

        return [x, y]

    def bri(self):
        return colorsys.rgb_to_hsv(*self.rgb())[2] * 255

    def rgb(self):
        """
        Convert a hex string to an rgb tuple
        :param hex:
        :return:
        """
        return tuple(
            int(self.hex[i : i + 2], 16) / 255.0 for i in (1, 3, 5)
        )  # skip '#'

    def __repr__(self) -> str:
        return f"<Color: {self.hex}>"
