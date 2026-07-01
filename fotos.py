from engine import reconhece_frame

encontrado, nome = reconhece_frame("./img/desconhecido.png")

if encontrado:
    print("Rosto de", nome, "foi reconhecido")
else:
    print("Nao foi encontrado nenhum rosto")
