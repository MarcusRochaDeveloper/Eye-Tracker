"""
Ponto de entrada do Eye Tracker.
Rastreamento de olhar com alerta de atenção (sistema de segurança).
"""
import argparse
import sys

from capturers.haar_blob import HaarCascadeBlobCapture
from frame_sources import (
    CameraFrameSource,
    FileFrameSource,
    FolderFrameSource,
    VideoFrameSource,
)
from gui.application_window import Window
from PyQt6.QtWidgets import QApplication

# Fonte de quadros: camera, pasta de imagens, arquivo único ou vídeo (chaves em PT-BR e EN)
FONTES_QUADRO = {
    "camera": CameraFrameSource,
    "pasta": FolderFrameSource,
    "folder": FolderFrameSource,
    "arquivo": FileFrameSource,
    "file": FileFrameSource,
    "video": VideoFrameSource,
}


def obter_argumentos():
    """Interpreta argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Eye Tracker com alerta de atenção. Use -fs para escolher a fonte de imagem."
    )
    parser.add_argument(
        "-fs",
        "--fonte",
        action="store",
        dest="fonte",
        choices=["camera", "pasta", "arquivo", "video"],
        default="camera",
        help="Fonte dos quadros: camera, pasta, arquivo ou video",
    )
    parser.add_argument(
        "-cam",
        "--camera-id",
        action="store",
        dest="id_camera",
        type=int,
        default=None,
        help="Índice do dispositivo de câmera (0, 1, 2...). Use apenas com -fs camera.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = obter_argumentos()
    ClasseFonte = FONTES_QUADRO[args.fonte]

    kwargs_fonte = {}
    if args.id_camera is not None and args.fonte == "camera":
        kwargs_fonte["cam_id"] = args.id_camera

    captura = HaarCascadeBlobCapture()
    app = QApplication(sys.argv)
    janela = Window(ClasseFonte(**kwargs_fonte), captura)
    janela.setWindowTitle("Eye Tracker - Controle de Atenção")
    janela.show()
    sys.exit(app.exec())
