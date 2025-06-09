from camera import Camera
from detector import HandDetector                
from audio import AudioPlayer
import threading
from ursina import *
from random import uniform
from particulas import ParticleSystem


palm_position = [0.5, 0.5]  # Começa centralizado (valores normalizados)
palm_angle = [0.0]  # Use lista para mutabilidade entre threads


# INICIANDO CAMERA
# URL do stream do Yawcam
# url = 'http://192.168.15.30:8081/video.mjpg'
# Camera direto do windows
url = 0
webcam = Camera()
hand_detector = HandDetector()
hand_detector.initHandsModule()
webcam.openStream(url) 

# INICIANDO AUDIO
# Configurações do audio
player = AudioPlayer("./assets/audio.wav")

# Thread para tocar o áudio
threadVolume = threading.Thread(target=player.playAudio, daemon=True)
threadVolume.start()
print("Tocando... digite valores para volume durante a execução.")

# Thread para receber o input do usuário
threadInput = threading.Thread(target=player.input_thread, daemon=True)
threadInput.start()

# INICIANDO PARTICULAS
# Inicialização Ursina
app = Ursina()
particle_system = ParticleSystem()

def update():
    # Mapeia o ângulo (0° a 90°) para velocidade (0 a 3)
    # Limita o ângulo para evitar valores fora do esperado
    angle = max(0, min(90, palm_angle[0]))
    particle_system.velocidade = (angle / 90) * 3
    for p in particle_system.particles:
        p.rotation_y = palm_angle[0]
    particle_system.update()
    velocidade_text.text = f"Velocidade: {particle_system.velocidade:.2f}"

def input(key):
    if key == 'space':
        particle_system.reset_particles()
    if key == '+':
        particle_system.increase_speed()
    if key == '-':
        particle_system.decrease_speed()

camera.position = (0, 0, -10)
camera.look_at(Vec3(0, 0, 0))
EditorCamera()

def aplicacao():
    global palm_position, palm_angle
    while not webcam.checkExit() and not player.stop_event.is_set():   
        webcam.readFrame()
        bounding_box = hand_detector.generateBoundingBox(webcam.getFrame()) 
        webcam.drawBoundingBox(bounding_box)
        results = hand_detector.processFrame(webcam.frame)
        webcam.frame = hand_detector.drawLandmarks(webcam.frame)

        # Atualiza a posição da palma
        # pos = hand_detector.getPalmPosition(webcam.frame)
        # if pos:
        #     palm_position[0], palm_position[1] = pos

        # # Atualiza o ângulo do indicador
        # angle = hand_detector.getPalmAndIndexAngle(webcam.frame)
        # if angle is not None:
        #     palm_angle[0] = angle

        # Atualiza o ângulo entre indicador e médio
        angle = hand_detector.getFingersAngle(webcam.frame)
        if angle is not None:
            palm_angle[0] = angle

        webcam.showFrame()

threadAplicacao = threading.Thread(target=aplicacao, daemon=True)
threadAplicacao.start()


velocidade_text = Text(
    text=f"Velocidade: {particle_system.velocidade:.2f}",
    position=(-0.85, 0.45),  # canto superior esquerdo
    scale=2,
    color=color.white,
    background=True
)

app.run()