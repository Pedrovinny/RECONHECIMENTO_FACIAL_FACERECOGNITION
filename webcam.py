import cv2
import time
import threading
from engine import reconhece_frame

video_capture = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

TEMPO_MEMORIA = 2               # segundos que um nome fica "lembrado" apos sumir
INTERVALO_RECONHECIMENTO = 1.0  # segundos entre rodadas de reconhecimento

lock = threading.Lock()
frame_compartilhado = None
faces_compartilhadas = []
rostos_reconhecidos = []  # lista de (x, y, w, h, nome, timestamp)


def centro(caixa):
    x, y, w, h = caixa
    return (x + w / 2, y + h / 2)


def distancia(c1, c2):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5


def worker_reconhecimento():
    global rostos_reconhecidos
    while True:
        with lock:
            frame = frame_compartilhado.copy() if frame_compartilhado is not None else None
            faces = list(faces_compartilhadas)

        if frame is not None:
            novos = []
            for (x, y, w, h) in faces:
                rosto = frame[y:y+h, x:x+w]
                if rosto.size == 0:
                    continue
                _, nome = reconhece_frame(rosto)
                novos.append((x, y, w, h, nome, time.time()))

            with lock:
                rostos_reconhecidos = novos

        time.sleep(INTERVALO_RECONHECIMENTO)


threading.Thread(target=worker_reconhecimento, daemon=True).start()

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    with lock:
        frame_compartilhado = frame.copy()
        faces_compartilhadas = faces
        reconhecidos = list(rostos_reconhecidos)

    tempo_atual = time.time()

    for (x, y, w, h) in faces:
        nome = "Desconhecido"
        c_atual = centro((x, y, w, h))

        melhor_nome = None
        melhor_dist = None

        for (rx, ry, rw, rh, rnome, rtempo) in reconhecidos:
            if tempo_atual - rtempo > TEMPO_MEMORIA:
                continue

            d = distancia(c_atual, centro((rx, ry, rw, rh)))
            if d < max(w, h) and (melhor_dist is None or d < melhor_dist):
                melhor_nome = rnome
                melhor_dist = d

        if melhor_nome:
            nome = melhor_nome

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
