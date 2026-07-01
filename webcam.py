import cv2
import time
from engine import reconhece_frame

video_capture = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

processar = True
resultados = []

# memória de rostos
memoria = {}

TEMPO_MEMORIA = 2  # segundos

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    tempo_atual = time.time()

    if processar:
        resultados = []

        for (x, y, w, h) in faces:
            rosto = frame[y:y+h, x:x+w]

            encontrado, nome = reconhece_frame(rosto)

            # salva na memória
            if encontrado:
                memoria[(x, y, w, h)] = (nome, tempo_atual)

            # tenta recuperar da memória
            else:
                for key in memoria:
                    nome_mem, tempo_mem = memoria[key]
                    if tempo_atual - tempo_mem < TEMPO_MEMORIA:
                        nome = nome_mem
                        break

            resultados.append(((x, y, w, h), nome))

    processar = not processar

    # desenhar
    for (x, y, w, h), nome in resultados:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), (0, 255, 0), cv2.FILLED)

        cv2.putText(frame, nome, (x+6, y+h-6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()