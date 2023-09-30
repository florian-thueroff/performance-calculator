import os
from subprocess import CalledProcessError
from subprocess import PIPE
from subprocess import run
import tempfile

def _store_pdf(
    source: str,
    directory: str,
    filename: str = "test",
    command: str = "pdflatex",
) -> str:

    with open(
        os.path.join(directory, f"{filename}.tex"), "x", encoding="utf-8"
    ) as f_source:
        f_source.write(source)

    args = (
        f'cd "{directory}" && '
        # f"cp {_get_latex_style_folder(theme_name=theme)}/* ./ && "
        f"{command} -interaction=batchmode {filename}.tex && "
        f"{command} -interaction=batchmode {filename}.tex && "
        # f"rm *.png *.log *.aux *.tex *.cls"
        "find . -type f ! -name '*.pdf' -delete"
    )

    try:
        run(args, shell=True, stdout=PIPE, stderr=PIPE, check=True)
    except CalledProcessError as e:
        print(f"stderr: {e.stderr}")

    return os.path.join(directory, f"{filename}.pdf")

def _make_pdf(
    source: str,
    directory: str,
    filename: str = "aufgaben_blatt",
    command: str = "pdflatex",
) -> bytes:

    pdf_file = _store_pdf(
        source=source,
        directory=directory,
        filename=filename,
        command=command,
    )

    with open(pdf_file) as f_out:  # type: BinaryIO
        pdf = f_out.read()

    return pdf

def generate_pdf(source: str, dir: str) -> str:

    # with tempfile.TemporaryDirectory() as tempdir:
    #     pdf = _make_pdf(
    #         source=source,
    #         directory=tempdir,
    #     )
    
    return _store_pdf(
        source=source,
        directory=dir,
        filename="performance",
    )

    # return pdf