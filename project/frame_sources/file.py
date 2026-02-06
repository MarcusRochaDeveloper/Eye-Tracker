"""
Fonte de quadros a partir de uma única imagem estática.
"""
from pathlib import Path

import cv2
from settings import settings


class FrameSource:
    """Reproduz uma imagem estática como se fosse um vídeo (mesmo quadro sempre)."""

    def __init__(self, local: Path = settings.STATIC_FILE_PATH):
        self.local = local
        self.imagem = None

    def start(self):
        self.imagem = cv2.imread(str(self.local))
        if self.imagem is None:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.local}")

    def next_frame(self):
        return self.imagem

    def stop(self):
        ...
