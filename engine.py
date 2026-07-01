from deepface import DeepFace

# Limite padrao do VGG-Face+cosine e 0.68 (quanto menor, mais parecido precisa ser).
# Afrouxado para tolerar oculos/objetos no rosto, ao custo de mais falsos positivos.
LIMIAR_SIMILARIDADE = 0.70

def reconhece_frame(frame):
    try:
        resultado = DeepFace.find(
            img_path=frame,  # agora usamos o frame direto
            db_path="./img",
            enforce_detection=False,
            silent=True,
            threshold=LIMIAR_SIMILARIDADE,
        )

        if len(resultado) > 0 and not resultado[0].empty:
            identidade = resultado[0].iloc[0]['identity']
            nome = identidade.split("\\")[-1].split(".")[0]
            return True, nome

        return False, "Desconhecido"

    except Exception as e:
        return False, "Erro"