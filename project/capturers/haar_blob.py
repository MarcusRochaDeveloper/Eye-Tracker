"""
Detecção de rosto e olhos com Haar Cascade e pupilas com blob.
Usado para estimar se a pessoa está olhando para a câmera (atenção).
"""
import logging
from collections import deque
from typing import Optional, Tuple

import numpy
import cv2
from cv2.data import haarcascades
from settings import settings

logger = logging.getLogger(__name__)

# Margem em torno do centro do olho para considerar “olhando para a câmera”
MARGEM_CENTRO = 0.45
# Quantos quadros usar para suavizar o estado de atenção
TAMANHO_HISTORICO_ATENCAO = 5
# Mínimo de quadros “com atenção” no histórico para considerar atenção OK
LIMIAR_ATENCAO = 4


class ErroCV2(Exception):
    pass


class HaarCascadeBlobCapture:
    """Detecta rosto e olhos com Haar Cascade e pupilas com blob."""

    face_detector = cv2.CascadeClassifier(haarcascades + "haarcascade_frontalface_default.xml")
    eye_detector = cv2.CascadeClassifier(haarcascades + "haarcascade_eye.xml")
    blob_detector = None

    def __init__(self):
        self.area_blob_esquerdo_anterior = 1
        self.area_blob_direito_anterior = 1
        self.keypoints_esquerdo_anterior = None
        self.keypoints_direito_anterior = None
        self._historico_atencao: deque[bool] = deque(maxlen=TAMANHO_HISTORICO_ATENCAO)

    def _inicializar_blob(self):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 30
        params.maxArea = 1200
        params.filterByCircularity = True
        params.minCircularity = 0.5
        params.filterByConvexity = False
        params.filterByInertia = True
        params.minInertiaRatio = 0.4
        self.blob_detector = cv2.SimpleBlobDetector_create(params)

    def detectar_rosto(self, img: numpy.ndarray) -> Optional[numpy.ndarray]:
        """Retorna o maior rosto encontrado no quadro (recorte da imagem)."""
        coords = self.face_detector.detectMultiScale(img, 1.2, 6)
        if len(coords) > 1:
            maior = (0, 0, 0, 0)
            for i in coords:
                if i[3] > maior[3]:
                    maior = i
            maior = numpy.array([maior], numpy.int32)
        elif len(coords) == 1:
            maior = coords
        else:
            return None
        for (x, y, w, h) in maior:
            return img[y : y + h, x : x + w]

    @staticmethod
    def _cortar_sobrancelhas(img):
        """Remove a parte superior do recorte do olho (sobrancelhas)."""
        if img is None:
            return img
        altura, largura = img.shape[:2]
        return img[15:altura, 0:largura]

    def detectar_olhos(
        self, face_img: numpy.ndarray, cortar_sobrancelhas: bool = True
    ) -> Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray]]:
        """Detecta olho esquerdo e direito no rosto; opcionalmente corta sobrancelhas."""
        coords = self.eye_detector.detectMultiScale(face_img, 1.2, 6)
        olho_esquerdo = olho_direito = None
        largura_img = face_img.shape[1]
        if coords is None or len(coords) == 0:
            return olho_esquerdo, olho_direito
        for (x, y, w, h) in coords:
            centro_x = int(float(x) + (float(w) / 2.0))
            if centro_x < largura_img * 0.4:
                olho_esquerdo = face_img[y : y + h, x : x + w]
            elif centro_x > largura_img * 0.5:
                olho_direito = face_img[y : y + h, x : x + w]
        if cortar_sobrancelhas and (olho_esquerdo is not None or olho_direito is not None):
            return self._cortar_sobrancelhas(olho_esquerdo), self._cortar_sobrancelhas(olho_direito)
        return olho_esquerdo, olho_direito

    def _pupila_centralizada(self, roi_olho: numpy.ndarray, keypoints) -> bool:
        """True se pelo menos um keypoint (pupila) está na região central do ROI do olho."""
        if not keypoints or len(keypoints) == 0:
            return False
        h, w = roi_olho.shape[:2]
        cx, cy = w / 2.0, h / 2.0
        margem = min(w, h) * MARGEM_CENTRO
        for kp in keypoints:
            x, y = kp.pt
            if abs(x - cx) <= margem and abs(y - cy) <= margem:
                return True
        return False

    def rastrear_blob(self, img, threshold, area_anterior):
        """Detecta blob (pupila) na imagem do olho com threshold dado."""
        img = cv2.GaussianBlur(img, (3, 3), 0)
        _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=2)
        img = cv2.dilate(img, None, iterations=4)
        img = cv2.medianBlur(img, 5)
        keypoints = self.blob_detector.detect(img)
        if keypoints and len(keypoints) > 1:
            melhor = 1000
            escolhido = keypoints[0]
            for kp in keypoints:
                if abs(kp.size - area_anterior) < melhor:
                    escolhido = kp
                    melhor = abs(kp.size - area_anterior)
            keypoints = (escolhido,)
        return keypoints

    def desenhar(self, origem, keypoints, dest=None):
        """Desenha os keypoints (pupilas) na imagem."""
        try:
            if dest is None:
                dest = origem
            return cv2.drawKeypoints(
                origem, keypoints, dest, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
        except cv2.error as e:
            raise ErroCV2(str(e))

    def debug_salvar(self, quadro):
        """Salva o quadro em pasta de debug (quando DEBUG_DUMP ativo)."""
        cv2.imwrite(str(settings.DEBUG_DUMP_LOCATION / f"{id(quadro)}.png"), quadro)

    def process(self, frame: numpy.ndarray, threshold_esq, threshold_dir):
        """
        Processa um quadro: detecta rosto, olhos, pupilas e se a pessoa está olhando para a câmera.
        Retorna (quadro, olho_esq, olho_dir, atencao_ok).
        """
        if not self.blob_detector:
            self._inicializar_blob()

        try:
            rosto = self.detectar_rosto(frame)
            if rosto is None:
                self._historico_atencao.append(False)
                return (
                    frame,
                    None,
                    None,
                    sum(self._historico_atencao) >= LIMIAR_ATENCAO,
                )
            rosto_cinza = cv2.cvtColor(rosto, cv2.COLOR_RGB2GRAY)
            olho_esquerdo, olho_direito = self.detectar_olhos(rosto_cinza)

            kp_esq = kp_dir = None
            if olho_esquerdo is not None:
                kp_esq = self.rastrear_blob(
                    olho_esquerdo, threshold_esq, self.area_blob_esquerdo_anterior
                ) or self.keypoints_esquerdo_anterior
                self.keypoints_esquerdo_anterior = kp_esq
            if olho_direito is not None:
                kp_dir = self.rastrear_blob(
                    olho_direito, threshold_dir, self.area_blob_direito_anterior
                ) or self.keypoints_direito_anterior
                self.keypoints_direito_anterior = kp_dir

            esq_ok = olho_esquerdo is not None and self._pupila_centralizada(olho_esquerdo, kp_esq)
            dir_ok = olho_direito is not None and self._pupila_centralizada(olho_direito, kp_dir)

            if olho_esquerdo is not None:
                olho_esquerdo = self.desenhar(olho_esquerdo, kp_esq, frame)
            if olho_direito is not None:
                olho_direito = self.desenhar(olho_direito, kp_dir, frame)

            atencao_quadro = esq_ok and dir_ok
            self._historico_atencao.append(atencao_quadro)
            atencao_ok = sum(self._historico_atencao) >= LIMIAR_ATENCAO

            return frame, olho_esquerdo, olho_direito, atencao_ok
        except (cv2.error, ErroCV2) as e:
            logger.error("Erro ao processar: %s", str(e))
            logger.error("Thresholds: esquerdo=%s, direito=%s", threshold_esq, threshold_dir)
            if settings.DEBUG_DUMP:
                self.debug_salvar(frame)
            self._historico_atencao.append(False)
            raise
