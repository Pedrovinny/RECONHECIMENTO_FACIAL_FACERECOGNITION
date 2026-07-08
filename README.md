# Reconhecimento Facial

Projeto de TCC de alunos do Ensino Médio: um sistema de identificação de rostos em tempo real via webcam, feito em Python com [OpenCV](https://opencv.org/) e [DeepFace](https://github.com/serengil/deepface).

O sistema liga a webcam, detecta rostos no vídeo e, para cada rosto detectado, tenta identificar a pessoa comparando-o com um banco de fotos conhecidas ([img/](img/)). Se encontrar uma correspondência, exibe o nome da pessoa sobre o rosto; caso contrário, exibe "Desconhecido".

## Como funciona

O reconhecimento roda em uma thread separada da captura/exibição de vídeo, para a imagem não travar enquanto o DeepFace processa (a comparação de rostos é bem mais lenta que a captura de vídeo):

1. **Loop principal (`webcam.py`)** — captura o vídeo continuamente e detecta rostos a cada frame com um classificador Haar Cascade (OpenCV), que é rápido. Os retângulos são desenhados na hora, então a imagem fica sempre fluida, independente da velocidade do reconhecimento. Detecções duplicadas/sobrepostas do mesmo rosto são filtradas (`remover_sobrepostas`).
2. **Thread de reconhecimento** — em paralelo, a cada `INTERVALO_RECONHECIMENTO` segundos (padrão: 1s), pega o frame e os rostos detectados mais recentes, recorta cada rosto e chama `reconhece_frame()` (`engine.py`), que usa o DeepFace para comparar contra o banco de imagens em [img/](img/).
3. **Casamento por posição** — como a thread de reconhecimento é mais lenta que o loop de exibição, o nome de cada rosto detectado agora é casado com o resultado reconhecido mais próximo (por distância entre centros), dentro de uma janela de memória (`TEMPO_MEMORIA`, padrão: 2s). Isso evita que o rótulo suma ou pisque enquanto a pessoa se move.
4. O nome (ou "Desconhecido") e um retângulo verde são desenhados sobre cada rosto. Pressione `q` para encerrar.

Por baixo dos panos, o DeepFace gera um *embedding* (vetor numérico que representa o rosto) usando o modelo **VGG-Face**, e compara esse vetor com os embeddings do banco em `img/` usando distância de cosseno. Quanto menor a distância, mais parecidos os rostos são considerados.

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| [webcam.py](webcam.py) | Script principal — captura da câmera, detecção de rostos (Haar Cascade), thread de reconhecimento em background e exibição em tempo real. |
| [engine.py](engine.py) | Motor de reconhecimento — `reconhece_frame()` usa o DeepFace para comparar um rosto contra o banco em `img/`. |
| [fotos.py](fotos.py) | Teste offline — reconhece o rosto de `img/desconhecido.png` contra o mesmo banco, sem usar a webcam. |
| [img/](img/) | Banco de rostos conhecidos. Cada imagem representa uma pessoa (o nome do arquivo vira o nome exibido no reconhecimento). |
| [requirements.txt](requirements.txt) | Dependências Python do projeto. |

## Tecnologias

- **[OpenCV](https://opencv.org/)** (`opencv-python`) — captura de vídeo e detecção rápida de rostos (Haar Cascade).
- **[DeepFace](https://github.com/serengil/deepface)** — geração de embeddings faciais (modelo VGG-Face) e comparação com o banco de imagens.
- **TensorFlow / tf-keras** — backend usado internamente pelo DeepFace para rodar o modelo VGG-Face.
- **NumPy** — suporte a operações com os frames de vídeo.

## Pré-requisitos

- Python 3.10–3.12 (recomendado, para compatibilidade com o TensorFlow).
- Uma webcam funcional (para `webcam.py`).
- Espaço em disco para o TensorFlow e os pesos do modelo VGG-Face (baixados automaticamente pelo DeepFace no primeiro uso, e armazenados em `~/.deepface`).

## Instalação

1. Clone o repositório e entre na pasta do projeto:
   ```
   git clone <url-do-repositorio>
   cd RECONHECIMENTO_FACIAL_FACERECOGNITION
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   Ou, se preferir Anaconda:
   ```
   conda create -n reconhecimento_facial python=3.11
   conda activate reconhecimento_facial
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Como executar

- **Reconhecimento em tempo real pela webcam:**
  ```
  python webcam.py
  ```
  Uma janela abrirá mostrando o vídeo da webcam com os rostos detectados e identificados. Pressione `q` com a janela em foco para encerrar.

- **Teste offline (sem webcam):**
  ```
  python fotos.py
  ```
  Compara `img/desconhecido.png` contra o banco de rostos e imprime no terminal se a pessoa foi reconhecida.

> Na primeira execução, o DeepFace baixa os pesos do modelo VGG-Face (alguns MB) e gera um cache de embeddings do banco de fotos — pode demorar um pouco mais que as execuções seguintes.

## Adicionando novas pessoas

Basta colocar uma foto do rosto da pessoa dentro de [img/](img/), nomeando o arquivo com o nome que deve aparecer no reconhecimento (ex: `joao.png`). Na primeira execução seguinte, o DeepFace reprocessa o banco automaticamente (o cache de embeddings, um arquivo `.pkl` dentro de `img/`, é gerado localmente e não é versionado no git — veja [.gitignore](.gitignore)).

Dicas para a foto de referência:
- Um rosto bem iluminado, de frente para a câmera, ocupando boa parte da imagem.
- Se trocar ou remover uma foto já usada, apague o `.pkl` de `img/` (ou deixe o DeepFace detectar a mudança) para forçar a regeneração do cache.

## Ajustes finos

Esses parâmetros podem ser alterados diretamente no código conforme a necessidade:

| Parâmetro | Arquivo | Efeito |
|---|---|---|
| `LIMIAR_SIMILARIDADE` | `engine.py` | Quão parecido um rosto precisa ser para ser reconhecido. Valor padrão do DeepFace (VGG-Face + cosine) é `0.68`; está em `0.70` para tolerar melhor variações como óculos, ângulo e iluminação. Subir esse valor aumenta a tolerância (mais reconhecimentos, porém mais risco de confundir pessoas parecidas); descer deixa mais rígido. |
| `INTERVALO_RECONHECIMENTO` | `webcam.py` | Frequência (em segundos) com que a thread de reconhecimento roda. Valores menores identificam mais rápido, porém consomem mais CPU. |
| `TEMPO_MEMORIA` | `webcam.py` | Por quantos segundos um nome reconhecido continua sendo exibido depois da última confirmação, evitando que o rótulo pisque. |

## Solução de problemas

- **A webcam não abre / janela preta:** verifique se nenhum outro programa está usando a câmera e se o índice `0` em `cv2.VideoCapture(0)` corresponde à câmera correta (troque para `1`, `2`, etc. se houver mais de uma câmera).
- **Erro ao instalar TensorFlow:** confirme que está usando Python 3.10–3.12; versões mais novas do Python podem não ter build do TensorFlow disponível ainda.
- **Reconhecimento lento:** aumente `INTERVALO_RECONHECIMENTO` em `webcam.py`, ou reduza a resolução da webcam.
- **Muitos "Desconhecido" para pessoas cadastradas:** aumente `LIMIAR_SIMILARIDADE` em `engine.py` (com cautela, pois isso também aumenta falsos positivos).

## Documentação adicional

Veja [Explicacao_Projeto.pdf](Explicacao_Projeto.pdf) para uma explicação mais aprofundada do projeto.
