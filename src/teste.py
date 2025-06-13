import sys
from vispy import app, scene
from vispy.visuals.transforms import STTransform
import numpy as np

# Criação do canvas e view
canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(800, 600), show=True)
view = canvas.central_widget.add_view()
view.camera = 'arcball'

# Esferas fixas (como no código base)
# sphere1 = scene.visuals.Sphere(radius=1, method='latitude', parent=view.scene,
#                                 edge_color='black', color=(0.8, 0.2, 0.2, 1))
# sphere1.transform = STTransform(translate=[-2.5, 0, 0])

# sphere2 = scene.visuals.Sphere(radius=1, method='ico', parent=view.scene,
#                                 edge_color='black', color=(0.2, 0.8, 0.2, 1))

# sphere3 = scene.visuals.Sphere(radius=1, rows=10, cols=10, depth=10, method='cube', parent=view.scene,
#                                 edge_color='black', color=(0.2, 0.2, 0.8, 1))
# sphere3.transform = STTransform(translate=[2.5, 0, 0])

# Nuvem de partículas - inicial
num_particles = 5000
particle_positions = np.random.uniform(low=-3, high=3, size=(num_particles, 3))
particle_colors = np.random.rand(num_particles, 4)

particles = scene.visuals.Markers(parent=view.scene,
                                   pos=particle_positions,
                                   face_color=particle_colors,
                                   size=7)

view.camera.set_range(x=[-3, 3], y=[-3, 3], z=[-3, 3])

axis = scene.visuals.XYZAxis(parent=view.scene)

# Função para animar/alterar posições das partículas
def update(event):
    global particle_positions
    # Movimento _aleatório_ simples: pequenas variações na posição
    delta = 0.1 * (np.random.rand(num_particles, 3) - 0.5)
    particle_positions += delta
    
    # Manter partículas dentro do limite -3 a 3 em cada eixo
    np.clip(particle_positions, -3, 3, out=particle_positions)
    
    # Atualizar posições para o visual
    particles.set_data(particle_positions, face_color=particle_colors, size=7)

# Timer para atualizações periódicas (60 FPS aprox)
timer = app.Timer(interval=1/600, connect=update, start=True)

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()

