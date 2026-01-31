import pygame
import math


class PygameInputSystem:
    def __init__(self):
        self.last_click = None

    def scan_keys(self):
        quit_requested = False
        self.last_click = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_requested = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.last_click = event.pos

        keys = pygame.key.get_pressed()
        pressed = set()

        if keys[pygame.K_w]: pressed.add("w")
        if keys[pygame.K_a]: pressed.add("a")
        if keys[pygame.K_s]: pressed.add("s")
        if keys[pygame.K_d]: pressed.add("d")

        if keys[pygame.K_UP]: pressed.add("w")
        if keys[pygame.K_LEFT]: pressed.add("a")
        if keys[pygame.K_DOWN]: pressed.add("s")
        if keys[pygame.K_RIGHT]: pressed.add("d")

        if keys[pygame.K_q]: pressed.add("q")
        if keys[pygame.K_e]: pressed.add("e")

        if keys[pygame.K_SPACE]: pressed.add("space")

        if keys[pygame.K_ESCAPE]:
            pressed.add("qquit")

        return pressed, quit_requested


class PygameGraphicsEngine:
    def __init__(self, bounds, width=900, height=600, title="Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.bounds = bounds
        self.width = width
        self.height = height

    def _map(self, x, y):
        sx = int(x / self.bounds.x_max * self.width)
        sy = int(y / self.bounds.y_max * self.height)
        return sx, sy

    def unmap(self, sx, sy):
        x = sx / self.width * self.bounds.x_max
        y = sy / self.height * self.bounds.y_max
        return x, y

    def render(self, player, npcs, bullets):
        self.screen.fill((20, 20, 20))

        px, py = self._map(player.x, player.y)
        pygame.draw.circle(self.screen, (255, 0, 0), (px, py), int(player.radius))

        length = 18
        ox = px + int(math.cos(player.angle) * length)
        oy = py + int(math.sin(player.angle) * length)
        pygame.draw.line(self.screen, (255, 220, 120), (px, py), (ox, oy), 3)

        for b in bullets:
            pygame.draw.circle(self.screen, (255, 255, 255),
                               self._map(b.x, b.y), int(b.radius))

        for npc in npcs:
            pygame.draw.circle(self.screen, (0, 120, 255),
                               self._map(npc.x, npc.y), int(npc.radius))

        pygame.display.flip()

    def close(self):
        pygame.quit()
