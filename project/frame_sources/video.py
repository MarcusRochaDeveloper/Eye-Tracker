"""
Fonte de quadros a partir de um arquivo de vídeo.
"""
from pathlib import Path

import cv2
from settings import settings


class FrameSource:
    """Lê um vídeo quadro a quadro. Caminho padrão ou variável STATIC_VIDEO_PATH."""

    def __init__(self, local: Path = settings.STATIC_FILE_PATH):
        self.local = local
        self.capture = None

    def start(self):
        self.capture = cv2.VideoCapture(str(self.local))
        if self.capture is None or not self.capture.read()[0]:
            raise FileNotFoundError(f"Não foi possível abrir o vídeo: {self.local}")

    def next_frame(self):
        sucesso, quadro = self.capture.read()
        if not sucesso:
            raise SystemError("Falha ao ler quadro do vídeo")
        return quadro

    def stop(self):
        self.capture.release()
