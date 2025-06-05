from camera import Camera
from detector import HandDetector                
from audio import AudioPlayer
import threading

# URL do stream do Yawcam
# url = 'http://192.168.15.30:8081/video.mjpg'
# Camera direto do windows
url = 0
camera = Camera()
hand_detector = HandDetector()
hand_detector.initHandsModule()
camera.openStream(url) 


# Configurações do audio
player = AudioPlayer("./assets/audio.wav")

# Thread para tocar o áudio
threadVolume = threading.Thread(target=player.playAudio, daemon=True)
threadVolume.start()
print("Tocando... digite valores para volume durante a execução.")

# Thread para receber o input do usuário
threadInput = threading.Thread(target=player.input_thread, daemon=True)
threadInput.start()
while not camera.checkExit() and not player.stop_event.is_set():   
    # Camera              
    camera.readFrame()

    # # Bounding Box
    bounding_box = hand_detector.generateBoundingBox(camera.getFrame()) 
    camera.drawBoundingBox(bounding_box)

    # Desenha os pontos e conexões no frame original (BGR)
    results = hand_detector.processFrame(camera.frame)
    camera.frame = hand_detector.drawLandmarks(camera.frame)

    camera.showFrame()
