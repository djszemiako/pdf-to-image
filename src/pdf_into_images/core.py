import os
from typing import Generator

import pymupdf


def pdf_into_images(
    pdf_realpath: str,
    output_directory: str,
    zoom: int = 2,
) -> Generator[str, None, None]:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_document = pymupdf.open(pdf_realpath)

    pdf_basename, *_ = os.path.splitext(os.path.basename(pdf_realpath))

    for i, page in enumerate(pdf_document.pages(), 1):
        matrix = pymupdf.Matrix(zoom, zoom)

        pixmap = page.get_pixmap(matrix=matrix)

        image_path = os.path.join(output_directory, f"{pdf_basename}.{i}.jpeg")

        pixmap.save(image_path)

        yield image_path
