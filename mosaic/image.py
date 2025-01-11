import numpy as np
from PIL import Image as PILImage
from pillow_heif import register_avif_opener, register_heif_opener
from scipy.spatial import KDTree

register_heif_opener()
register_avif_opener()

class Image:
    def __init__(self, width: int = 0, height: int = 0):
        self.__width = width
        self.__height = height
        self.__pixels = np.zeros((height, width, 3), dtype=np.uint8)

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

    def read(self, path):
        image = PILImage.open(path).convert("RGB")
        self.__pixels = np.array(image)
        self.__height, self.__width, _ = self.__pixels.shape

    def from_array(self, array):
        self.__pixels = array
        self.__height, self.__width, _ = self.__pixels.shape

    def __getitem__(self, key) -> np.ndarray:
        return self.__pixels[key]

    def __setitem__(self, key, value):
        self.__pixels[key] = value

    def resize(self, width, height):
        self.__pixels = np.array(PILImage.fromarray(self.__pixels).resize((width, height)))
        self.__height, self.__width, _ = self.__pixels.shape

    def save(self, path, **kwargs):
        image = PILImage.fromarray(self.__pixels)
        image.save(path, **kwargs)

class Tile(Image):
    def __init__(self, width: int = 0, height: int = 0):
        super().__init__(width, height)
        self.__average_color = np.zeros(3)

    @property
    def average_color(self):
        return self.__average_color

    def read(self, path, tile_width):
        super().read(path)
        # crop the image to a square
        if self.width > self.height:
            start = (self.width - self.height) // 2
            self.from_array(self[:, start:start+self.height])
        elif self.height > self.width:
            start = (self.height - self.width) // 2
            self.from_array(self[start:start+self.width, :])

        # resize
        self.resize(tile_width, tile_width)
        # calculate average color
        self.__average_color = np.mean(self[:, :, :], axis=(0, 1))

    def __set_item__(self, key, value):
        super().__setitem__(key, value)
        self.__average_color = np.mean(self[:, :, :], axis=(0, 1))



# tiles collection
class TilesCollection:
    """
    A collection of images that can be queried for the nearest image to a given color.
    """
    def __init__(self, tiles: list[Tile]):
        self.__images = tiles
        self.__kdtree = KDTree([image.average_color for image in tiles])

    def get_nearest(self, color) -> Tile:
        _, index = self.__kdtree.query(color)
        return self.__images[index]
