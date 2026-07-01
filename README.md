# Reconhecimento Facial

Projeto de TCC de alunos do Ensino Médio: um sistema de identificação de rostos em tempo real via webcam, feito em Python com OpenCV e DeepFace.

## Como funciona

1. A webcam captura o vídeo continuamente.
2. Cada frame é convertido para escala de cinza e passado por um classificador Haar Cascade (OpenCV), que localiza os rostos presentes na imagem — essa etapa é rápida e roda a cada frame.
3. Para cada rosto detectado, o recorte é enviado ao DeepFace, que compara o rosto contra o banco de imagens em [img/](img/) e retorna o nome da pessoa mais parecida (ou "Desconhecido" se não houver correspondência). Essa comparação é mais pesada, então só é feita a cada 2 frames.
4. Um cache temporal (2 segundos) guarda o último nome identificado por posição, evitando que o rótulo pisque quando o rosto sai momentaneamente do quadro.
5. O nome e um retângulo são desenhados sobre o rosto na janela de vídeo. Pressione `q` para encerrar.

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| [webcam.py](webcam.py) | Script principal — captura da câmera, detecção de rostos (Haar Cascade) e exibição em tempo real. |
| [engine.py](engine.py) | Motor de reconhecimento — `reconhece_frame()` usa o DeepFace para comparar um rosto contra o banco em `img/`. |
| [fotos.py](fotos.py) | Teste offline — reconhece o rosto de `img/desconhecido.png` contra o mesmo banco, sem usar a webcam. |
| [img/](img/) | Banco de rostos conhecidos. Cada imagem representa uma pessoa (o nome do arquivo vira o nome exibido no reconhecimento). |

## Tecnologias

- **[OpenCV](https://opencv.org/)** — captura de vídeo e detecção rápida de rostos (Haar Cascade).
- **[DeepFace](https://github.com/serengil/deepface)** — geração de embeddings faciais e comparação com o banco de imagens.
- **NumPy** — suporte a operações com os frames de vídeo.

## Instalação

1. Crie e ative um ambiente virtual (recomendado Python 3.10–3.12, para compatibilidade com o TensorFlow):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   Ou, se preferir Anaconda:
   ```
   conda create -n nome_projeto python=3.11
   conda activate nome_projeto
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

- `python webcam.py` — reconhecimento facial em tempo real pela webcam.
- `python fotos.py` — teste de reconhecimento comparando uma foto (`img/desconhecido.png`) contra o banco de rostos.

## Adicionando novas pessoas

Basta colocar uma foto do rosto da pessoa dentro de [img/](img/), nomeando o arquivo com o nome que deve aparecer no reconhecimento (ex: `joao.png`). Na primeira execução seguinte, o DeepFace reprocessa o banco automaticamente.
