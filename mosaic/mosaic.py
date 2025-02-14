import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL.Image import registered_extensions
from tqdm import tqdm

from .image import Image, Tile, TilesCollection


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

    def __init__(self, num_tiles: int, tile_width: int):
        # load the target image
        self.__num_tiles = num_tiles
        self.__tile_width = tile_width

        self.__target_image: Image = None
        self.__tiles: list[Tile] = []
        self.__tiles_collection: TilesCollection = None
        self.__mosaic: Image = None

    def set_target_image(self, target_image_path: str):
        if not os.path.isfile(target_image_path):
            raise ValueError(f"File '{target_image_path}' not found.")
        self.__target_image = Image()
        self.__target_image.read(target_image_path)
        # resize the target image with shorter side equal to num_tiles
        if self.__target_image.width < self.__target_image.height:
            self.__target_image.resize(self.__num_tiles, int(self.__num_tiles * self.__target_image.height / self.__target_image.width))
        else:
            self.__target_image.resize(int(self.__num_tiles * self.__target_image.width / self.__target_image.height), self.__num_tiles)


    def load_tiles(self, tiles_dir: str):
        """Load the tile images from the directory."""
        if not os.path.isdir(tiles_dir):
            raise ValueError(f"Directory '{tiles_dir}' not found.")

        self.__tiles.clear()
        print(f"Loading tiles from '{tiles_dir}'...")
        paths = [os.path.join(tiles_dir, filename) for filename in os.listdir(tiles_dir) if filename.lower().endswith(tuple(registered_extensions().keys()))]
        def load_tile(tile_path):
            tile = Tile()
            tile.read(tile_path, self.__tile_width)
            return tile
        MAX_WORKERS = os.cpu_count()
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
        self.__mosaic = Image(self.__target_image.width*self.__tile_width, self.__target_image.height*self.__tile_width)
        for i in range(self.__target_image.height):
            for j in range(self.__target_image.width):
                color = self.__target_image[i, j]
                tile = self.__tiles_collection.get_nearest(color)
                # place the tile in the mosaic
                self.__mosaic[i*self.__tile_width:(i+1)*self.__tile_width, j*self.__tile_width:(j+1)*self.__tile_width] = tile[:, :]

    def save_mosaic(self, output_image_path: str, quality: int = 100):
        """Save the mosaic image."""
        print(f"Saving mosaic to '{output_image_path}'...")
        self.__mosaic.save(output_image_path, quality=quality)
