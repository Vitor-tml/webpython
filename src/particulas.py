from ursina import *
from random import uniform

class ParticleSystem:
    def __init__(self, num_particles=1000, bounds=40):
        self.particles = []
        self.bounds = bounds
        self.create_particles(num_particles)
        self.velocidade = 0.2

    def create_particles(self, num_particles):
        for i in range(num_particles):
            p = Entity(
                model='sphere',
                color=color.azure,
                scale=0.2,
                position=(uniform(-3, 3), uniform(-3, 3), uniform(-3, 3))
            )
            p.velocity = Vec3(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
            self.particles.append(p)
    
    def update(self):
        for p in self.particles:
            # posicao = velocidade * tempo
            p.position += p.velocity *  time.dt  * self.velocidade * 3
            for i in range(3): 
                # Inverte a velocidade se a partícula sair dos limites
                if abs(p.position[i]) > self.bounds:
                    p.velocity[i] *= -1

    def reset_particles(self):
        for p in self.particles:
            p.position = Vec3(uniform(-3, 3), uniform(-3, 3), uniform(-3, 3))
            p.velocity = Vec3(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))

    def increase_speed(self, amount=0.2):
        self.velocidade += amount
        print(f"Velocidade: {self.velocidade:.2f}")

    def decrease_speed(self, amount=0.2):
        self.velocidade = max(0, self.velocidade - amount)
        print(f"Velocidade: {self.velocidade:.2f}")

