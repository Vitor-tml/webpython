import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.hands = None
        self.results = None
        self.mp_drawing = None
    def initHandsModule(self):
        # Inicializa o detector de mãos do MediaPipe
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,     # Detecta mão em vídeo
            max_num_hands=2,             # Detecta até 2 mãos    
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