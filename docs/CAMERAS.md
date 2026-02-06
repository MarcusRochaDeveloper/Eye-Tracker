# 📷 Suporte a Câmeras (USB, Integrada e DroidCam)

> **Documentação Técnica** | **Módulo:** Captura de Vídeo

Este documento descreve detalhadamente como o **Eye Tracker** gerencia a captura de vídeo, a lógica de seleção de dispositivos e os procedimentos de configuração para diferentes tipos de hardware (Webcams integradas, USB e Câmeras Virtuais).

---

## 📑 Índice
1. [Visão Geral Técnica](#-visão-geral-técnica)
2. [Lógica de Seleção de Câmera](#-lógica-de-seleção-de-câmera)
3. [Guia por Tipo de Dispositivo](#-guia-por-tipo-de-dispositivo)
    - [Webcam Integrada](#webcam-integrada-notebook)
    - [Câmera USB](#câmera-usb)
    - [DroidCam / Iriun (Virtual)](#droidcam-celular-como-webcam)
4. [Diagnóstico de Problemas](#-diagnóstico-de-problemas-troubleshooting)
5. [Resumo de Comandos](#-resumo-rápido-cheat-sheet)

---

## ⚙️ Visão Geral Técnica

O Eye Tracker utiliza a fonte de quadros `camera` (flag `-fs camera`), operando sobre a API nativa do OpenCV:

```python
# O sistema tenta abrir o índice numérico do dispositivo
cv2.VideoCapture(index)
```

Qualquer dispositivo reconhecido pelo Kernel do Sistema Operacional será acessível, incluindo:
* ✅ Webcams integradas (Notebooks).
* ✅ Câmeras USB externas (Logitech, Redragon, etc).
* ✅ Câmeras virtuais (DroidCam, OBS Virtual Camera, Iriun).

---

## 🎯 Lógica de Seleção de Câmera

O sistema opera em dois modos de seleção de hardware:

### 1. Seleção Explícita (`-cam N`)
Quando o usuário define manualmente o ID do dispositivo. O sistema ignora a busca automática e tenta forçar a conexão com o índice informado.

**Exemplo:** Usar a segunda câmera conectada.
```bash
python main.py -fs camera -cam 1
```

### 2. Seleção Automática (Padrão)
Se `-cam` não for informado, o algoritmo de busca percorre os índices (`0, 100, 200...`) até encontrar um dispositivo que:
1.  Abra a conexão com sucesso (`isOpened()`).
2.  Retorne um quadro (frame) válido e não vazio.

---

## 📘 Guia por Tipo de Dispositivo

### Webcam Integrada (Notebook)
Geralmente é o dispositivo padrão do sistema.

* **Índice Típico:** `0`
* **Comando:**
    ```bash
    python main.py
    # Ou explicitamente:
    python main.py -fs camera -cam 0
    ```

### Câmera USB
Requer que o sistema operacional inicialize o driver antes da execução do script.

#### 🪟 Windows
O Windows gerencia os índices automaticamente.
* **Notebooks:** Integrada = `0`, USB = `1`.
* **Desktops:** USB Principal = `0`.

#### 🐧 Linux
As câmeras são mapeadas como arquivos de dispositivo `/dev/video*`.

1.  **Verificar dispositivos:**
    ```bash
    ls /dev/video*
    # ou
    v4l2-ctl --list-devices
    ```
2.  **Permissões:** O usuário deve pertencer ao grupo `video`.
    ```bash
    sudo usermod -aG video $USER
    # Necessário logout/login após o comando.
    ```
3.  **Execução:** Se a câmera for `/dev/video1`:
    ```bash
    python main.py -fs camera -cam 1
    ```

#### 🍎 macOS
* **FaceTime HD:** Geralmente índice `0`.
* **USB Externa:** Geralmente índice `1`.
    ```bash
    python main.py -fs camera -cam 1
    ```

### DroidCam (Celular como Webcam)
O DroidCam cria um "driver virtual". Para o Eye Tracker, ele funciona exatamente como uma webcam física.

#### Passo a Passo
1.  **Smartphone:** Instale o app (Android/iOS) e abra-o.
2.  **Computador:** Instale o [Cliente PC DroidCam](https://www.dev47apps.com/droidcam/).
3.  **Conexão:** Conecte via Wi-Fi (mesma rede) ou Cabo USB e inicie o vídeo no cliente PC.
4.  **Execução:**
    Descubra o índice (geralmente é o próximo número disponível após as câmeras físicas).
    ```bash
    python main.py -fs camera -cam 1
    ```

> **Nota:** O mesmo procedimento se aplica ao **Iriun Webcam** e **OBS Virtual Camera**.

---

## 🩺 Diagnóstico de Problemas (Troubleshooting)

| Sintoma | Causa Provável | Solução |
| :--- | :--- | :--- |
| **`Câmera id=X não disponível`** | Índice errado ou câmera em uso. | 1. Tente outro índice (`-cam 0`, `-cam 1`).<br>2. Feche outros apps (Zoom, Teams, Discord). |
| **Tela Preta (Sem Imagem)** | Driver virtual travado ou permissão. | No Linux, verifique as permissões de `video`. No DroidCam, reinicie o app no celular. |
| **Latência Alta (Atraso)** | Conexão Wi-Fi instável (DroidCam). | Use conexão via cabo USB ou reduza a resolução no cliente DroidCam. |

---

## ⚡ Resumo Rápido (Cheat Sheet)

Tabela de referência para execução imediata:

| Cenário | Comando Recomendado |
| :--- | :--- |
| **Padrão (Notebook)** | `python main.py` |
| **Forçar Câmera Principal** | `python main.py -fs camera -cam 0` |
| **Câmera Secundária (USB/Virtual)** | `python main.py -fs camera -cam 1` |
| **Terceira Câmera** | `python main.py -fs camera -cam 2` |
| **Modo Teste (Sem Câmera)** | `python main.py -fs arquivo` |

---

> **Dúvidas sobre instalação?**
> Consulte o arquivo principal `INSTALACAO.md` para instruções sobre dependências (Python, OpenCV, Poetry) e configuração inicial do ambiente.