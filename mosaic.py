from image import Image, Tile, TilesCollection

from PIL.Image import registered_extensions

import os
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class Mosaic:
    """A class to create a mosaic image from a target image and a collection of tile images.

    Parameters
    ----------
    target_image_path : str
        The path to the target image.
    tiles_dir : str
        The directory containing the tile images.
    output_image_path : str
        The path to save the mosaic image.
    num_tiles : int
        The number of tiles to be placed along the shorter side of the target image.
    tile_width : int
        The width of each tile in pixels.
    quality : int, optional
    """

    def __init__(self, target_image_path: str, tiles_dir: str, output_image_path: str, num_tiles: int, tile_width: int, quality: int = 100):
        # load the target image
        self.__target_image = Image()
        self.__target_image.read(target_image_path)
        # resize the target image with shorter side equal to num_tiles
        if self.__target_image.width < self.__target_image.height:
            self.__target_image.resize(num_tiles, int(num_tiles * self.__target_image.height / self.__target_image.width))
        else:
            self.__target_image.resize(int(num_tiles * self.__target_image.width / self.__target_image.height), num_tiles)
        
        self.__tiles_dir = tiles_dir
        self.__tiles: list[Tile] = []
        self.__tiles_collection: TilesCollection = None
        self.__output_image_path = output_image_path
        self.__tile_width = tile_width
        self.__quality = quality

        self.__mosaic = Image(tile_width * self.__target_image.width, tile_width * self.__target_image.height)

    def load_tiles(self):
        """Load the tile images from the directory."""
        print(f"Loading tiles from '{self.__tiles_dir}'...")
        if not os.path.isdir(self.__tiles_dir):
            raise ValueError(f"Directory '{self.__tiles_dir}' not found.")

        paths = [os.path.join(self.__tiles_dir, filename) for filename in os.listdir(self.__tiles_dir) if filename.lower().endswith(tuple(registered_extensions().keys()))]
        def load_tile(tile_path):
            tile = Tile()
            tile.read(tile_path, self.__tile_width)
            return tile
        MAX_WORKERS = 16
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # submit tasks
            futures = [executor.submit(load_tile, path) for path in paths]
            # get results
            for future in tqdm(as_completed(futures), total=len(paths), desc="Loading tiles"):
                self.__tiles.append(future.result())
        self.__tiles_collection = TilesCollection(self.__tiles)


    def create_mosaic(self):
        """Create the mosaic image."""
        print("Creating mosaic...")
        for i in range(self.__target_image.height):
            for j in range(self.__target_image.width):
                color = self.__target_image[i, j]
                tile = self.__tiles_collection.get_nearest(color)
                # place the tile in the mosaic
                self.__mosaic[i*self.__tile_width:(i+1)*self.__tile_width, j*self.__tile_width:(j+1)*self.__tile_width] = tile[:, :]

    def save_mosaic(self):
        """Save the mosaic image."""
        print(f"Saving mosaic to '{self.__output_image_path}'...")
        self.__mosaic.save(self.__output_image_path, quality=self.__quality)
