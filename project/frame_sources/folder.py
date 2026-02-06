"""
Fonte de quadros a partir de uma pasta de imagens (.png).
"""
from pathlib import Path

import cv2
from settings import settings


class FrameSource:
    """Percorre arquivos .png de uma pasta, quadro a quadro, como um vídeo."""

    def __init__(self, local: Path = settings.DEBUG_DUMP_LOCATION):
        self.local = local
        self.lista_arquivos = None
        self.indice = 0

    def start(self):
        self.lista_arquivos = list(self.local.glob("*.png"))
        if not self.lista_arquivos:
            raise FileNotFoundError(f"Pasta vazia ou sem .png: {self.local}")

    def next_frame(self):
        if self.indice >= len(self.lista_arquivos):
            self.indice = 0
        img = cv2.imread(str(self.lista_arquivos[self.indice]))
        self.indice += 1
        return img

    def stop(self):
        ...
