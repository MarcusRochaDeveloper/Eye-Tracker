# 👁️ Eye Tracker - Guia Completo de Instalação e Configuração

> **Status:** Ativo | **Versão:** 1.0.0 | **Python:** 3.10+

Este documento fornece as diretrizes técnicas para a implantação do sistema **Eye Tracker - Controle de Atenção**. O guia foi estruturado para padronização e performance, atendendo de desenvolvedores iniciantes a seniores.

---

## 📑 Índice
1. [Arquitetura e Dependências](#-arquitetura-e-dependências)
2. [Preparação do Ambiente](#-1-preparação-do-ambiente-universal)
3. [Instalação por Sistema Operacional](#-2-instalação-por-sistema-operacional)
4. [Método Alternativo (Pip)](#-3-método-alternativo-sem-poetry)
5. [Interface de Linha de Comando (CLI)](#-4-interface-de-linha-de-comando-cli)
6. [Resolução de Problemas](#-5-resolução-de-problemas-troubleshooting)
7. [Estrutura do Projeto](#-6-estrutura-de-diretórios)

---

## 🛠️ Arquitetura e Dependências

O sistema utiliza processamento de imagem em tempo real e uma interface reativa de alta fidelidade.

* 🐍 **Python 3.10+**: Runtime mandatório.
* 👁️ **OpenCV (`opencv-python`)**: Motor de visão computacional para detecção facial e análise de frames.
* 🖥️ **PyQt6**: Framework de interface gráfica (GUI) moderna.
* 🧮 **NumPy**: Processamento vetorial de matrizes para cálculos oculares.
* 📦 **Poetry**: Gerenciador de dependências e ambientes virtuais (**Recomendado**).

---

## 🚀 1. Preparação do Ambiente (Universal)

A recomendação profissional é o uso do **Poetry** para isolamento de dependências.

### Instalando o Poetry
Se ainda não possui o Poetry instalado:

* **Windows (PowerShell):**
    ```powershell
    (Invoke-WebRequest -Uri [https://install.python-poetry.org](https://install.python-poetry.org) -UseBasicParsing).Content | python -
    ```
* **Linux / macOS (Terminal):**
    ```bash
    curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
    ```

---

## 💻 2. Instalação por Sistema Operacional

Selecione seu sistema operacional para instruções específicas de drivers e permissões.

### 🪟 Windows

1.  **Python:** Baixe em [python.org](https://www.python.org/downloads/).
    * ⚠️ **Importante:** Marque a opção **"Add Python to PATH"** durante a instalação.
2.  **Execução do Projeto:**
    ```powershell
    cd eye-tracker-project
    poetry install
    poetry run python main.py
    ```
    *Nota: O áudio utiliza o módulo nativo `winsound`.*

### 🐧 Linux (Debian, Fedora, Arch)

Essencial configurar permissões de vídeo e bibliotecas de áudio.

1.  **Dependências de Sistema:**
    ```bash
    # Ubuntu / Debian
    sudo apt update && sudo apt install python3-pip python3-venv alsa-utils pulseaudio-utils -y

    # Fedora
    sudo dnf install alsa-utils pulseaudio-utils

    # Arch Linux
    sudo pacman -S alsa-utils pulseaudio-utils
    ```
2.  **Permissões de Hardware:**
    Adicione seu usuário ao grupo de vídeo para acesso ao `/dev/video*`.
    ```bash
    sudo usermod -aG video $USER
    ```
    > 🔄 **Atenção:** É necessário fazer logout/login para aplicar as permissões.

3.  **Execução:**
    ```bash
    cd eye-tracker-project
    poetry install
    poetry run python main.py
    ```

### 🍎 macOS

1.  **Setup via Homebrew:**
    ```bash
    brew install python@3.11
    cd eye-tracker-project
    poetry install
    poetry run python main.py
    ```
2.  **Permissões:** Aceite a solicitação de acesso à câmera na primeira execução.

---

## 📦 3. Método Alternativo (Sem Poetry)

Caso prefira utilizar o `pip` e `venv` padrão:

```bash
# 1. Criação do ambiente virtual
python -m venv venv

# 2. Ativação
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalação e Execução
pip install numpy opencv-python PyQt6
python main.py
```

---

## ⚙️ 4. Interface de Linha de Comando (CLI)

O sistema suporta flags para testes automatizados e debugging:

| Flag | Descrição | Exemplo |
| :--- | :--- | :--- |
| `-cam <ID>` | Define o ID da câmera (padrão: 0). | `python main.py -cam 1` |
| `-fs <arquivo>` | Simula entrada usando imagem estática. | `python main.py -fs face_test.jpg` |
| `-fs <pasta>` | Processa sequência de imagens (dataset). | `python main.py -fs ./dataset/` |

---

## 🩺 5. Resolução de Problemas (Troubleshooting)

| Erro / Sintoma | Causa Provável | Solução |
| :--- | :--- | :--- |
| **`ModuleNotFoundError`** | Ambiente virtual inativo. | Execute `poetry shell` ou ative o venv antes de rodar. |
| **`No camera found`** | Câmera em uso ou ID incorreto. | Feche outros apps (Zoom/Teams) ou tente `-cam 1`. |
| **`X11 connection error`** | Linux sem interface gráfica. | Certifique-se de rodar em ambiente desktop ou use `Xvfb`. |
| **Sem Áudio (Linux)** | Falta de pacotes de som. | Instale `alsa-utils` e verifique o volume do sistema. |

---

## 📂 6. Estrutura de Diretórios

A organização do código segue o padrão MVC (Model-View-Controller) simplificado:

```text
eye-tracker-project/
├── project/
│   ├── assets/           # Ícones, sons e modelos XML
│   ├── modules/          # Core: Detector, VideoThread, AudioService
│   └── main.py           # Entry point da aplicação
├── docs/                 # Documentação técnica complementar
├── pyproject.toml        # Configuração do Poetry
└── README.md             
```