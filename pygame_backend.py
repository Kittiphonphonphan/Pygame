import pygame

class PygameInputSystem:
    def scan_keys(self):
        quit_requested = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_requested = True

        keys = pygame.key.get_pressed()
        pressed = set()

        # WASD
        if keys[pygame.K_w]: pressed.add("w")
        if keys[pygame.K_a]: pressed.add("a")
        if keys[pygame.K_s]: pressed.add("s")
        if keys[pygame.K_d]: pressed.add("d")

        # Arrow keys (สำรอง)
        if keys[pygame.K_UP]: pressed.add("w")
        if keys[pygame.K_LEFT]: pressed.add("a")
        if keys[pygame.K_DOWN]: pressed.add("s")
        if keys[pygame.K_RIGHT]: pressed.add("d")

        # Quit
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            pressed.add("q")

        return pressed, quit_requested


class PygameGraphicsEngine:
    def __init__(self, bounds, width=800, height=600, title="Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)   # 👈 ตรงนี้
        self.clock = pygame.time.Clock()

        self.bounds = bounds
        self.width = width
        self.height = height

    def _map(self, x, y):
        sx = int(x / self.bounds.x_max * self.width)
        sy = int(y / self.bounds.y_max * self.height)
        return sx, sy

    def render(self, player, npcs):
        self.screen.fill((20, 20, 20))
        pygame.draw.circle(self.screen, (255, 0, 0),
                           self._map(player.x, player.y),
                           int(player.radius))
        for npc in npcs:
            pygame.draw.circle(self.screen, (0, 120, 255),
                               self._map(npc.x, npc.y),
                               int(npc.radius))
        pygame.display.flip()

    def close(self):
        pygame.quit()
