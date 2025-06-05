import cv2
import mediapipe as mp

# URL do stream do Yawcam
url = 'http://192.168.15.30:8081/video.mjpg'

class Camera:
    def __init__(self):
        self.video = None
        self.frame = None
        self.rectangle_color = (0, 255, 0)
        self.retangle_thickness = 2
    
    def __dell__(self):
        self.video.release() # Libera o vídeo ao sair do contexto
        cv2.destroyAllWindows()

    def openStream(self, url):
        # Inicializa o objeto de captura de vídeo com a URL do stream
        self.video = cv2.VideoCapture(url)        
        if not self.video.isOpened():
            print("Não foi possível abrir o stream")
            exit()
    
    def readFrame(self):
        # Lê um frame do vídeo
        ret, self.frame = self.video.read()
        if not ret:
            print("Falha na captura")
            exit()
        # self.convertToRGB()

    # def convertToRGB(self):
    #     # Converte o frame de BGR para RGB
    #     self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    
    def drawBoundingBox(self, bounding_box):
        # Desenha uma caixa delimitadora no frame
        if bounding_box:
            cv2.rectangle(self.frame,
                          (bounding_box['x_min'], bounding_box['y_min']),
                          (bounding_box['x_max'], bounding_box['y_max']),
                          self.rectangle_color,
                          self.retangle_thickness)
    
    def getFrame(self):
        # Retorna o frame atual
        return cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    
    def showFrame(self, title='Capicamera'):
        # Verifica se o frame existe e mostra informações básicas
        if self.frame is not None:
            print("Frame shape:", self.frame.shape)
        else:
            print("Frame está vazio!")
        cv2.imshow(title, self.frame)

class HandDetector:
    def __init__(self):
        self.hands = None
        self.results = None

    def initHandsModule(self):
        # Inicializa o detector de mãos do MediaPipe
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,     # Detecta mão em vídeo
            max_num_hands=2,             # Detecta até 2 mãos    
            min_detection_confidence=0.7 # Confiança mínima para detectar
        )
    
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
                

camera = Camera()
hand_detector = HandDetector()
hand_detector.initHandsModule()
camera.openStream(url) 

while True:                 
    camera.readFrame()
    bounding_box = hand_detector.generateBoundingBox(camera.getFrame()) 
    camera.drawBoundingBox(bounding_box)
    camera.showFrame()    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Sai se apertar 'q'
        break
