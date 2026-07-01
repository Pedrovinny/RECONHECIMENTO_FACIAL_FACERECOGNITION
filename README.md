# Reconhecimento Facial

Projeto de TCC de alunos do Ensino Médio: um sistema de identificação de rostos em tempo real via webcam, feito em Python com OpenCV e DeepFace.

## Como funciona

O reconhecimento roda em uma thread separada da captura/exibição de vídeo, para a imagem não travar enquanto o DeepFace processa:

1. **Loop principal (`webcam.py`)** — captura o vídeo continuamente e detecta rostos a cada frame com um classificador Haar Cascade (OpenCV), que é rápido. Os retângulos são desenhados na hora, então a imagem fica sempre fluida, independente da velocidade do reconhecimento.
2. **Thread de reconhecimento** — em paralelo, a cada `INTERVALO_RECONHECIMENTO` segundos (padrão: 1s), pega o frame e os rostos detectados mais recentes, recorta cada rosto e chama `reconhece_frame()` (`engine.py`), que usa o DeepFace para comparar contra o banco de imagens em [img/](img/).
3. **Casamento por posição** — como a thread de reconhecimento é mais lenta que o loop de exibição, o nome de cada rosto detectado agora é casado com o resultado reconhecido mais próximo (por distância entre centros), dentro de uma janela de memória (`TEMPO_MEMORIA`, padrão: 2s). Isso evita que o rótulo suma ou pisque enquanto a pessoa se move.
4. O nome (ou "Desconhecido") e um retângulo verde são desenhados sobre cada rosto. Pressione `q` para encerrar.

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| [webcam.py](webcam.py) | Script principal — captura da câmera, detecção de rostos (Haar Cascade), thread de reconhecimento em background e exibição em tempo real. |
| [engine.py](engine.py) | Motor de reconhecimento — `reconhece_frame()` usa o DeepFace para comparar um rosto contra o banco em `img/`. |
| [fotos.py](fotos.py) | Teste offline — reconhece o rosto de `img/desconhecido.png` contra o mesmo banco, sem usar a webcam. |
| [img/](img/) | Banco de rostos conhecidos. Cada imagem representa uma pessoa (o nome do arquivo vira o nome exibido no reconhecimento). |

## Tecnologias

- **[OpenCV](https://opencv.org/)** — captura de vídeo e detecção rápida de rostos (Haar Cascade).
- **[DeepFace](https://github.com/serengil/deepface)** — geração de embeddings faciais (modelo VGG-Face) e comparação com o banco de imagens.
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

Basta colocar uma foto do rosto da pessoa dentro de [img/](img/), nomeando o arquivo com o nome que deve aparecer no reconhecimento (ex: `joao.png`). Na primeira execução seguinte, o DeepFace reprocessa o banco automaticamente (o cache de embeddings, um arquivo `.pkl` dentro de `img/`, é gerado localmente e não é versionado no git).

## Ajustes finos

Esses parâmetros podem ser alterados diretamente no código conforme a necessidade:

| Parâmetro | Arquivo | Efeito |
|---|---|---|
| `LIMIAR_SIMILARIDADE` | `engine.py` | Quão parecido um rosto precisa ser para ser reconhecido. Valor padrão do DeepFace (VGG-Face + cosine) é `0.68`; está em `0.80` para tolerar melhor variações como óculos, ângulo e iluminação. Subir esse valor aumenta a tolerância (mais reconhecimentos, porém mais risco de confundir pessoas parecidas); descer deixa mais rígido. |
| `INTERVALO_RECONHECIMENTO` | `webcam.py` | Frequência (em segundos) com que a thread de reconhecimento roda. Valores menores identificam mais rápido, porém consomem mais CPU. |
| `TEMPO_MEMORIA` | `webcam.py` | Por quantos segundos um nome reconhecido continua sendo exibido depois da última confirmação, evitando que o rótulo pisque. |
