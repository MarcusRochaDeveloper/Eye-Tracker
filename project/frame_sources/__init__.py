"""
Fontes de quadro: câmera, arquivo, pasta de imagens ou vídeo.
Protocolo que toda fonte deve implementar: start(), next_frame(), stop().
"""
from typing import Protocol

from .camera import FrameSource as CameraFrameSource
from .file import FrameSource as FileFrameSource
from .folder import FrameSource as FolderFrameSource
from .video import FrameSource as VideoFrameSource


class FrameSource(Protocol):
    """
    Protocolo de fonte de quadros.
    A taxa de atualização é controlada por REFRESH_PERIOD em settings (em ms).
    """

    def next_frame(self):
        ...

    def start(self):
        ...

    def stop(self):
        ...
