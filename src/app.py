import click

from lib.main import pdf_into_images


@click.command()
@click.option(
    "--pdf-realpath",
    help="Fully qualified path to the source PDF.",
    required=True,
)
@click.option(
    "--output-directory",
    help="The directory to which files will be written.",
    required=True,
)
@click.option(
    "--zoom",
    default=2,
    help="""
        Zoom factor for rendering. A higher number means better quality
        but a larger file.
    """,
    type=click.INT,
)
def main(
    pdf_realpath: str,
    output_directory: str,
    zoom: int = 2,
):
    """
    Convert a PDF to JPEG images using PyMuPDF.
    """
    image_paths = list(pdf_into_images(pdf_realpath, output_directory, zoom))

    print(
        f"Converted '{pdf_realpath}' to {len(image_paths):,} images into path: {output_directory}"
    )

    print("Files created:")

    print("\n".join(image_paths))


if __name__ == "__main__":
    main(auto_envvar_prefix="PDF_TO_IMAGES")
