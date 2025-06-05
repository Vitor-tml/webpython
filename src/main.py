from camera import Camera
from detector import HandDetector                

# URL do stream do Yawcam
url = 'http://192.168.15.30:8081/video.mjpg'

camera = Camera()
hand_detector = HandDetector()
hand_detector.initHandsModule()
camera.openStream(url) 

while not camera.checkExit():                 
    camera.readFrame()
    bounding_box = hand_detector.generateBoundingBox(camera.getFrame()) 
    camera.drawBoundingBox(bounding_box)
    camera.showFrame()