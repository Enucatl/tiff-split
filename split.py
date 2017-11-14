import click
import numpy as np
import libtiff
import glob

@click.command()
@click.option("-n", type=int, default=5)
@click.argument("folder", type=click.Path(exists=True))
def main(n, folder):
    pass


if __name__ == "__main__":
    main()
