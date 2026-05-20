import os
import sys


def caminho_recurso(caminho_relativo):

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        caminho_relativo
    )