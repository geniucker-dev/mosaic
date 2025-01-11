# Mosaic

This is a simple Python script that creates a [photomosaic](https://en.wikipedia.org/wiki/Photographic_mosaic) of images from a given folder.

## Features

- Create a photomosaic of a target image using images from a given folder.
- Multithreading support for faster loading of images.

## Usage

Make sure you have Python 3 installed.

Install the package using pip:

```bash
pip install git+https://github.com/geniucker-dev/mosaic
```

or if you want to use ssh

```bash
pip install git+ssh://git@github.com/geniucker-dev/mosaic
```

### Use as a script

Run `python -m mosaic --help` to see the help message.

```
Usage: python -m mosaic [OPTIONS] TARGET_IMAGE_PATH TILES_DIR
                        OUTPUT_IMAGE_PATH NUM_TILES TILE_WIDTH

  Generate a mosaic image by tiling a target image using smaller images.

  TARGET_IMAGE_PATH: The path to the target image.
  TILES_DIR: The directory containing the tile images.
  OUTPUT_IMAGE_PATH: The path to save the mosaic image.
  NUM_TILES: The number of tiles to be placed along the shorter side of the target image.
  TILE_WIDTH: The width of each tile in pixels.

Options:
  -q, --quality INTEGER RANGE  The quality of the output image. From 1 (worst)
                               to 100 (best).  [1<=x<=100]
  --help                       Show this message and exit.
```

### Use as a module

Example usage:

```python
from mosaic import Mosaic


mosaic = Mosaic(
    num_tiles=100, # The number of tiles to be placed along the shorter side of the target image.
    tile_width=50 # The width of each tile in pixels.
)
mosaic.set_target_image("path/to/target/image.jpg")
mosaic.load_tiles("path/to/tiles/directory")
mosaic.create_mosaic()
mosaic.save_mosaic("path/to/output/image.jpg", quality=90) # The quality of the output image. From 1 (worst) to 100 (best).
```

## Example

target

![image](https://github.com/user-attachments/assets/9914ac18-0a63-4599-bd7f-2d49c0b09400)

mosaic

![image](https://github.com/user-attachments/assets/79655cfe-2a60-4890-8c71-c35913650f57)

detail

![image](https://github.com/user-attachments/assets/9497299d-0ab7-4d60-b6de-e441fc0e8ad7)
