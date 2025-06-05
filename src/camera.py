import cv2

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
        cv2.imshow(title, self.frame)

    def checkExit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')