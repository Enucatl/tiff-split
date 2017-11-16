import os
import click
import numpy as np
import libtiff
import glob
from tqdm import tqdm

@click.command()
@click.option("-n", type=int, default=5)
@click.argument("folder", type=click.Path(exists=True))
def main(n, folder):
    input_filenames = glob.glob(os.path.join(folder, "*.tif"))
    for f in tqdm(input_filenames):
        tif = libtiff.TIFF.open(f).read_image()
        print(tif.shape)


if __name__ == "__main__":
    main()
