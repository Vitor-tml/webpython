import mediapipe as mp
import math

class HandDetector:
    def __init__(self):
        self.hands = None
        self.results = None
        self.mp_drawing = None
    def initHandsModule(self):
        # Inicializa o detector de mãos do MediaPipe
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,     # Detecta mão em vídeo
            max_num_hands=8,             # Detecta até 2 mãos    
            min_detection_confidence=0.7 # Confiança mínima para detectar
        )
        # Inicializa o módulo de desenho do MediaPipe
        self.mp_drawing = mp.solutions.drawing_utils
    
    def processFrame(self, image):
        self.results =  self.hands.process(image)
        return self.results.multi_hand_landmarks
    
    def generateBoundingBox(self, image):
        height, width, _ = image.shape

        if self.processFrame(image):
            # Se encontrou mãos, gera uma caixa delimitadora
            for hands in self.results.multi_hand_landmarks:
                x_list = [int(coordinate.x * width) for coordinate in hands.landmark]   # Lista de X dos pontos
                y_list = [int(coordinate.y * height) for coordinate in hands.landmark]  # Lista de Y dos pontos
            return {
                'x_min': min(x_list),
                'x_max': max(x_list),
                'y_min': min(y_list),
                'y_max': max(y_list)
            }
        else:
            return None
    
    def drawLandmarks(self, image):
        results = self.processFrame(image)
        if results:
            for hand_landmarks in results:
                # Desenha os pontos e conexões no frame original (BGR)
                self.mp_drawing.draw_landmarks(
                    image,  # frame BGR
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
        return image
    

    def getPalmPosition(self, image):
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            # Posição normalizada (0~1)
            print(f"Palm position: {hand.landmark[0].x}, {hand.landmark[0].y}")
            return hand.landmark[0].x, hand.landmark[0].y
        return None
    
    def getPalmAndIndexAngle(self, image):
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            # Landmark 0: centro da palma
            # Landmark 8: ponta do dedo indicador
            x0, y0 = hand.landmark[0].x, hand.landmark[0].y
            x8, y8 = hand.landmark[8].x, hand.landmark[8].y
            # Calcula o ângulo em relação ao eixo horizontal (em radianos)
            angle_rad = math.atan2(y8 - y0, x8 - x0)
            # Converte para graus
            angle_deg = math.degrees(angle_rad)
            print(f"Angle (palm-index): {angle_deg:.2f}°")
            return angle_deg
        return None
    
    def getFingersAngle(self, image):
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            # Vetor palma→polegar
            v1 = (
                hand.landmark[4].x - hand.landmark[0].x,
                hand.landmark[4].y - hand.landmark[0].y
            )
            # Vetor palma→indicador
            v2 = (
                hand.landmark[8].x - hand.landmark[0].x,
                hand.landmark[8].y - hand.landmark[0].y
            )
            # Produto escalar e módulo dos vetores
            dot = v1[0]*v2[0] + v1[1]*v2[1]
            mod1 = math.sqrt(v1[0]**2 + v1[1]**2)
            mod2 = math.sqrt(v2[0]**2 + v2[1]**2)
            if mod1 == 0 or mod2 == 0:
                return None
            # Ângulo em radianos e depois em graus
            angle_rad = math.acos(dot / (mod1 * mod2))
            angle_deg = math.degrees(angle_rad)
            print(f"Angle (polegar-indicador): {angle_deg:.2f}°")
            return angle_deg
        return None