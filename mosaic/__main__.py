import click

from mosaic import Mosaic


@click.command()
@click.argument("target_image_path", type=click.Path(exists=True))
@click.argument("tiles_dir", type=click.Path(exists=True))
@click.argument("output_image_path", type=click.Path())
@click.argument("num_tiles", type=int)
@click.argument("tile_width", type=int)
@click.option("--quality", "-q", type=click.IntRange(1, 100), default=60, help="The quality of the output image. From 1 (worst) to 100 (best).")
def main(target_image_path, tiles_dir, output_image_path, num_tiles, tile_width, quality):
    """
    Generate a mosaic image by tiling a target image using smaller images.

    \b
    TARGET_IMAGE_PATH: The path to the target image.
    TILES_DIR: The directory containing the tile images.
    OUTPUT_IMAGE_PATH: The path to save the mosaic image.
    NUM_TILES: The number of tiles to be placed along the shorter side of the target image.
    TILE_WIDTH: The width of each tile in pixels.
    """
    mosaic = Mosaic(num_tiles, tile_width)
    mosaic.set_target_image(target_image_path)
    mosaic.load_tiles(tiles_dir)
    mosaic.create_mosaic()
    mosaic.save_mosaic(output_image_path, quality=quality)


if __name__ == "__main__":
    main()
