import os
import sys
from typing import Literal, TypeAlias, cast

import pymupdf
import typer

app = typer.Typer()

ExtensionType: TypeAlias = Literal["jpeg", "png"]


def pdf_into_images(
    pdf_realpath: str,
    output_directory: str,
    zoom: int = 2,
    extension: ExtensionType = "jpeg",
) -> list[str]:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_document = pymupdf.open(pdf_realpath)

    image_paths = []

    pdf_basename = os.path.basename(pdf_realpath)

    for i, page in enumerate(pdf_document.pages(), 1):
        matrix = pymupdf.Matrix(zoom, zoom)

        pixmap = page.get_pixmap(matrix=matrix)

        image_path = os.path.join(output_directory, f"{pdf_basename}.{i}.{extension}")

        pixmap.save(image_path)

        image_paths.append(image_path)

    return image_paths


@app.command()
def main(
    pdf_realpath: str,
    output_directory: str,
    zoom: int = 2,
    extension: str = "jpeg",
):
    """
    Convert a PDF to JPEG images using PyMuPDF

    Args:
        pdf_path (str): Path to the PDF file
        output_folder (str): Folder to save the JPEG or PNG images. If it doesn't
        exist, it will be created
        zoom (int): Zoom factor for rendering (higher = better quality but larger file)
        extension (str): Either `jpeg` or `png`

    Returns:
        list: List of paths to the created JPEG images
    """
    if extension.lower() not in ("jpeg", "png"):
        raise RuntimeError("Extension must be either `jpeg` or `png`!")

    image_paths = pdf_into_images(
        pdf_realpath, output_directory, zoom, cast(ExtensionType, extension)
    )

    sys.stdout.write(
        f"Converted '{pdf_realpath}' to {len(image_paths):,} images into path: {output_directory}\n"
    )

    sys.stdout.write("Files created:\n")

    sys.stdout.writelines("\n".join(image_paths))


if __name__ == "__main__":
    app()
