import os
import click
import numpy as np
import libtiff
import glob
from tqdm import tqdm

@click.command()
@click.option("-n", type=int, default=5)
@click.option("-m", type=int, default=3)
@click.argument("folder", type=click.Path(exists=True))
def main(n, m, folder):
    """Split all the tiff files in a folder into n chunks with m different
    offsets"""
    input_filenames = glob.glob(os.path.join(folder, "*.tif"))
    example_tif = libtiff.TIFF.open(input_filenames[0]).read_image()
    total_length = example_tif.shape[1]
    chunk_length = total_length // n
    offset = chunk_length // m
    offset_indices = chunk_length // offset
    number_of_splits = total_length // chunk_length
    number_of_offsets = chunk_length // offset
    indices = [
        [offset * (i - offset_indices // 2)
         + (j + 1) * chunk_length
         for j in range(number_of_splits - 1)]
        for i in range(number_of_offsets)
    ]
    offset_folder = os.path.join(folder, "offset_{}")
    split_folder = os.path.join(offset_folder, "split_{}")

    #create folders
    for i in range(number_of_offsets):
        for j in range(number_of_splits):
            os.makedirs(split_folder.format(i, j), exist_ok=True)

    #split files
    for f in tqdm(input_filenames):
        tif = libtiff.TIFF.open(f).read_image()
        for i, offset in enumerate(indices):
            splits = np.array_split(tif, offset, axis=1)
            for j, split in enumerate(splits):
                output_filename = os.path.join(
                    split_folder.format(i, j),
                    os.path.basename(f))
                output_tif = libtiff.TIFF.open(output_filename, "w")
                output_tif.write_image(split)
                output_tif.close()


if __name__ == "__main__":
    main()
