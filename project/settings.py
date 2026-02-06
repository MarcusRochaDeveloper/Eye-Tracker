"""
Configurações centralizadas do Eye Tracker.
Valores podem ser sobrescritos por variáveis de ambiente.
"""
import os
from dataclasses import dataclass
from os import environ
from pathlib import Path

_obter_env = environ.get


def _dir_base():
    return Path(os.path.split(os.path.abspath(__file__))[0])


@dataclass
class Configuracoes:
    """Configurações do projeto."""

    BASE_DIR: Path = None
    ASSETS: Path = None
    GUI_FILE_PATH: Path = None
    STYLE_FILE_PATH: Path = None
    REFRESH_PERIOD: int = 2
    DEBUG_DUMP: bool = False
    DEBUG_DUMP_LOCATION: Path = None
    STATIC_FILE_PATH: Path = None
    STATIC_VIDEO_PATH: str = None

    def __post_init__(self):
        if self.BASE_DIR is None:
            self.BASE_DIR = _dir_base()
        if self.ASSETS is None:
            self.ASSETS = self.BASE_DIR / "gui" / "assets"
        if self.GUI_FILE_PATH is None:
            self.GUI_FILE_PATH = Path(_obter_env("GUI_FILE_PATH") or str(self.ASSETS / "GUImain.ui"))
        if self.STYLE_FILE_PATH is None:
            self.STYLE_FILE_PATH = Path(_obter_env("STYLE_FILE_PATH") or str(self.ASSETS / "style.css"))
        self.REFRESH_PERIOD = int(_obter_env("CAMERA_REFRESH_PERIOD") or 2)
        self.DEBUG_DUMP = _obter_env("DEBUG_DUMP", "false").lower() in ("1", "true", "yes")
        if self.DEBUG_DUMP_LOCATION is None:
            self.DEBUG_DUMP_LOCATION = Path(_obter_env("DEBUG_DUMP_LOCATION") or str(self.BASE_DIR / "capturers" / "dump"))
        if self.STATIC_FILE_PATH is None:
            self.STATIC_FILE_PATH = Path(_obter_env("STATIC_FILE_PATH") or str(self.BASE_DIR / "capturers" / "dump" / "man.png"))
        if self.STATIC_VIDEO_PATH is None:
            self.STATIC_VIDEO_PATH = _obter_env("STATIC_VIDEO_PATH")
# Instância global (compatível com código que usa settings.XXX)
settings = Configuracoes()
