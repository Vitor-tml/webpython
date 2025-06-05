import cv2
import mediapipe as mp

# URL do stream do Yawcam
url = 'http://192.168.15.30:8081/video.mjpg'

cap = cv2.VideoCapture(url)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

if not cap.isOpened():
    print("Não foi possível abrir o stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha na captura")
        break

    # Converte para RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtém as coordenadas dos pontos da mão
            h, w, _ = frame.shape
            x_list = [int(lm.x * w) for lm in hand_landmarks.landmark]
            y_list = [int(lm.y * h) for lm in hand_landmarks.landmark]
            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)
            # Desenha o retângulo verde
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow('Webcam via Yawcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()