"""
Protocolo de captura: qualquer implementação deve fornecer process(quadro, threshold_esq, threshold_dir).
"""
from typing import Protocol

import numpy


class Capture(Protocol):
    """Protocolo para módulos de captura de olhar."""

    def process(
        self, frame: numpy.ndarray, l_threshold: int, r_threshold: int
    ) -> tuple:
        """Processa quadro e retorna (quadro, olho_esq, olho_dir) ou (+ atencao_ok)."""
        ...
