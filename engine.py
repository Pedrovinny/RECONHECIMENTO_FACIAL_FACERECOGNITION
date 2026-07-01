from deepface import DeepFace

def reconhece_frame(frame):
    try:
        resultado = DeepFace.find(
            img_path=frame,  # agora usamos o frame direto
            db_path="./img",
            enforce_detection=False
        )

        if len(resultado) > 0 and not resultado[0].empty:
            identidade = resultado[0].iloc[0]['identity']
            nome = identidade.split("\\")[-1].split(".")[0]
            return True, nome

        return False, "Desconhecido"

    except Exception as e:
        return False, "Erro"