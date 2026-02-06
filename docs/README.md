# 👁️ Eye Tracker - Monitoramento de Atenção

> **Status:** Ativo | **Python:** 3.10+ | **Interface:** PyQt6

Sistema de visão computacional para rastreamento ocular com **alerta de atenção em tempo real**. O software monitora o rosto do usuário e emite avisos visuais e sonoros caso o olhar seja desviado da tela. Ideal para aplicações em provas remotas, treinamentos e monitoramento de segurança.

---

## 🚀 Funcionalidades

* **Rastreamento Híbrido:** Utiliza *Haar Cascade* para detecção facial e algoritmos de *Blob* para precisão na detecção das pupilas.
* **Alerta de Atenção:** Feedback imediato (borda vermelha na tela + aviso sonoro) quando o usuário não olha para a câmera.
* **Multi-Input:** Suporte nativo para:
    * Webcams Integradas e USB.
    * Câmeras Virtuais (DroidCam, Iriun, OBS).
    * Arquivos de vídeo e imagens estáticas (para testes).
* **Interface Moderna:** GUI portada para **PyQt6**, com sliders para calibração de sensibilidade (threshold) em tempo real.
* **Código Localizado:** Todo o código-fonte e comentários foram traduzidos e adaptados para Português (BR).

---

## 📜 Histórico e Créditos

Este projeto é uma **modernização e refatoração completa** de uma iniciativa open-source desenvolvida originalmente há cerca de 5 anos.

Embora a lógica base de detecção tenha sido preservada, esta versão traz evoluções significativas desenvolvidas:
1.  **Atualização de Stack:** Migração do Python legado para **3.10+** e substituição do PyQt5 pelo **PyQt6**.
2.  **Novas Features:** Implementação do sistema de **Alerta de Atenção** (visual e sonoro), inexistente na versão original.
3.  **Otimização:** Correção de bugs de performance, vazamento de memória e melhoria na estabilidade de leitura da câmera.

---

## 💻 Requisitos

* **Python:** 3.10 ou superior.
* **Gerenciador:** Poetry (Recomendado) ou Pip.
* **S.O.:** Windows, Linux ou macOS.

---

## ⚡ Instalação Rápida

Na raiz do projeto:

```bash
# 1. Instalar dependências
poetry install

# 2. Entrar na pasta do código-fonte
cd project

# 3. Executar
poetry run python main.py
```

> **Modo Teste (Sem Câmera):**
> Para rodar usando uma imagem estática de teste:
> ```bash
> poetry run python main.py -fs arquivo
> ```

---

## 📖 Documentação Complementar

Para detalhes técnicos específicos, consulte os manuais na pasta `docs/`:

* 📄 **[docs/INSTALACAO.md](docs/INSTALACAO.md)** – Guia passo a passo para configurar o ambiente em Windows, Linux e macOS.
* 📷 **[docs/CAMERAS.md](docs/CAMERAS.md)** – Como configurar câmeras USB, DroidCam e resolver conflitos de dispositivo.

---

## 🛠️ Guia de Uso (CLI)

O sistema aceita argumentos via linha de comando para facilitar automação e testes:

| Argumento | Função | Padrão |
| :--- | :--- | :--- |
| `-fs`, `--fonte` | Define a entrada de vídeo: `camera`, `pasta`, `arquivo`, `video`. | `camera` |
| `-cam`, `--camera-id` | Define o ID da câmera (0, 1, 2...). Use junto com `-fs camera`. | `0` |

### Exemplos Práticos

```bash
# Usar a câmera padrão (Webcam integrada)
python main.py

# Usar uma segunda câmera (ex: DroidCam ou USB externa)
python main.py -fs camera -cam 1

# Testar com uma imagem estática (sem precisar de webcam)
# Usa a imagem padrão em project/capturers/dump/man.png
python main.py -fs arquivo

# Processar um vídeo gravado
# (Defina o caminho na variável de ambiente ou no settings.py)
STATIC_VIDEO_PATH='./video_teste.mp4' python main.py -fs video
```

---

## ⚙️ Variáveis de Ambiente e Configuração

O arquivo `settings.py` centraliza as configurações, mas você pode sobrescrever algumas via variáveis de ambiente:

| Variável | Descrição | Padrão |
| :--- | :--- | :--- |
| `GUI_FILE_PATH` | Caminho do layout `.ui`. | `gui/ui/main_window.ui` |
| `STYLE_FILE_PATH` | Caminho do arquivo de estilos CSS. | `assets/style.qss` |
| `CAMERA_REFRESH_PERIOD` | Taxa de atualização (ms). | `2` |
| `DEBUG_DUMP` | Salvar frames com erro (`true`/`false`). | `false` |

---

## 📂 Estrutura do Projeto


project/
├── main.py              # Ponto de entrada (Entry Point)
├── settings.py          # Configurações globais
├── capturers/           # Núcleo de Visão Computacional
│   ├── face_detector    # Detecção facial (Haar)
│   ├── eye_tracker      # Algoritmo de blobs para pupilas
│   └── attention        # Lógica de alerta de atenção
├── frame_sources/       # Drivers de entrada (Camera, Video, File)
└── gui/                 # Interface Gráfica (PyQt6 + Assets)
```