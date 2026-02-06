"""
Janela principal do Eye Tracker: exibe câmera, olhos e alerta de atenção (som + texto vermelho).
"""
import array
import subprocess
import sys
import tempfile
import wave
import numpy
from capturers import Capture
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QSlider
from PyQt6.uic import loadUi

from frame_sources import FrameSource
from settings import settings

# Intervalo em ms para repetir o som de alerta enquanto a atenção estiver ausente
INTERVALO_ALERTA_SOM_MS = 2000


def _tocar_som_alerta():
    try:
        sample_rate = 8000
        duration_s = 0.2
        freq = 440
        n = int(sample_rate * duration_s)
        samples = array.array("h")
        for i in range(n):
            t = i / sample_rate
            samples.append(int(32000 * 0.3 * (1 if (int(t * freq * 2) % 2 == 0) else -1)))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sample_rate)
                w.writeframes(samples.tobytes())
            path = f.name
        if sys.platform == "win32":
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_NOSTOP)
        else:
            r = subprocess.run(["aplay", "-q", path], timeout=1, capture_output=True)
            if r.returncode != 0:
                subprocess.run(["paplay", path], timeout=1, capture_output=True)
        try:
            import os
            os.unlink(path)
        except OSError:
            pass
    except Exception:
        pass


class Window(QMainWindow):

    startButton: QPushButton
    stopButton: QPushButton
    leftEyeThreshold: QSlider
    rightEyeThreshold: QSlider

    def __init__(self, video_source: FrameSource, capture: Capture):
        super(Window, self).__init__()
        loadUi(settings.GUI_FILE_PATH, self)
        with open(settings.STYLE_FILE_PATH, "r") as css:
            self.setStyleSheet(css.read())

        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.timer = None
        self.fonte_video = video_source
        self.capture = capture
        self._alerta_visivel = False
        self._timer_som_alerta = None

        self.rotulo_alerta = QLabel(self.centralwidget)
        self.rotulo_alerta.setGeometry(40, 60, 640, 56)
        self.rotulo_alerta.setStyleSheet(
            "background-color: rgba(180, 0, 0, 0.9); color: white; "
            "font-weight: bold; font-size: 24px; border: 3px solid red;"
        )
        self.rotulo_alerta.setFont(QFont("Sans", 24, QFont.Weight.Bold))
        self.rotulo_alerta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotulo_alerta.setText("PRESTE ATENÇÃO! Olhe para a câmera.")
        self.rotulo_alerta.hide()

    def start(self):
        self.fonte_video.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(settings.REFRESH_PERIOD)

    def stop(self):
        self.timer.stop()
        if self._timer_som_alerta is not None:
            self._timer_som_alerta.stop()
            self._timer_som_alerta = None
        self.fonte_video.stop()

    def _disparar_som_alerta(self):
        _tocar_som_alerta()
        if self._timer_som_alerta is None:
            self._timer_som_alerta = QTimer(self)
            self._timer_som_alerta.timeout.connect(_tocar_som_alerta)
        self._timer_som_alerta.start(INTERVALO_ALERTA_SOM_MS)

    def _parar_som_alerta(self):
        if self._timer_som_alerta is not None:
            self._timer_som_alerta.stop()
            self._timer_som_alerta = None

    def update_frame(self):
        frame = self.fonte_video.next_frame()
        result = self.capture.process(
            frame, self.leftEyeThreshold.value(), self.rightEyeThreshold.value()
        )
        if len(result) == 4:
            face, l_eye, r_eye, attention_ok = result
        else:
            face, l_eye, r_eye = result
            attention_ok = True

        if face is not None:
            self.display_image(self.opencv_to_qt(frame))

        if l_eye is not None:
            self.display_image(self.opencv_to_qt(l_eye), window="leftEyeBox")

        if r_eye is not None:
            self.display_image(self.opencv_to_qt(r_eye), window="rightEyeBox")

        if not attention_ok:
            if not self._alerta_visivel:
                self._alerta_visivel = True
                self.rotulo_alerta.show()
                self.rotulo_alerta.raise_()
                self._disparar_som_alerta()
        else:
            if self._alerta_visivel:
                self._alerta_visivel = False
                self.rotulo_alerta.hide()
                self._parar_som_alerta()

    @staticmethod
    def opencv_to_qt(img) -> QImage:
        """Converte imagem OpenCV (BGR) para QImage (RGB/RGBA)."""
        qformat = QImage.Format.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:  # RGBA
                qformat = QImage.Format.Format_RGBA8888
            else:  # RGB
                qformat = QImage.Format.Format_RGB888

        img = numpy.require(img, numpy.uint8, "C")
        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)  # BGR to RGB
        out_image = out_image.rgbSwapped()

        return out_image

    def display_image(self, img: QImage, window="baseImage"):
        """Exibe a imagem no widget indicado pelo nome no .ui (baseImage, leftEyeBox, rightEyeBox)."""

        display_label: QLabel = getattr(self, window, None)
        if display_label is None:
            raise ValueError(f"No such display window in GUI: {window}")

        display_label.setPixmap(QPixmap.fromImage(img))
        display_label.setScaledContents(True)
