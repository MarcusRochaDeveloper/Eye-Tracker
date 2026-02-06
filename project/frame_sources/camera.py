"""
Fonte de quadros a partir de câmera (USB, integrada, DroidCam, etc.).
"""
import cv2


class FrameSource:
    """Captura quadros de uma câmera (dispositivo de vídeo)."""

    def __init__(self, cam_id=None):
        self.camera_rodando = False
        self.id_camera = cam_id  # índice do dispositivo (0, 1, 2...)
        self.capture = None

    def _camera_ok(self):
        return self.capture is not None and self.capture.read()[0]

    def start(self):
        if not self.camera_rodando:
            if self.id_camera is not None:
                self.capture = cv2.VideoCapture(self.id_camera)
                if not self._camera_ok():
                    self.capture.release()
                    self.capture = None
                    raise SystemError(f"Câmera id={self.id_camera} não disponível.")
                self.camera_rodando = True
                return
            for indice in range(0, 5000, 100):
                self.capture = cv2.VideoCapture(indice)
                if self._camera_ok():
                    self.camera_rodando = True
                    return
                self.capture.release()
                self.capture = None
            raise SystemError(
                "Nenhuma câmera encontrada. Use -fs arquivo ou -fs pasta para testar com imagem ou pasta."
            )

    def stop(self):
        if self.camera_rodando:
            self.capture.release()
            self.camera_rodando = False

    def next_frame(self):
        assert self.camera_rodando, "Inicie a câmera com start() antes de next_frame()"
        sucesso, quadro = self.capture.read()
        if not sucesso:
            raise SystemError("Falha ao capturar quadro")
        return quadro
