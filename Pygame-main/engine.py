import time
import random
import math
from entities import circles_collide, separate_circles, NPC, Bullet


class GameEngine:
    def __init__(self, player, npcs, graphics, input_system, bounds, fps=60):
        self.player = player
        self.npcs = npcs
        self.bullets = []
        self.graphics = graphics
        self.input = input_system
        self.bounds = bounds
        self.fps = fps
        self.running = True
        self.clock = getattr(graphics, "clock", None)

        self.fire_cooldown = 0
        self.spawn_timer = 0

    def run(self):
        while self.running:
            pressed, quit_requested = self.input.scan_keys()

            if quit_requested or "qquit" in pressed:
                break

            self.update(pressed)
            self.graphics.render(self.player, self.npcs, self.bullets)

            if self.clock:
                self.clock.tick(self.fps)
            else:
                time.sleep(1 / self.fps)

    def update(self, pressed: set[str]):
        click = getattr(self.input, "last_click", None)
        if click is not None:
            wx, wy = self.graphics.unmap(*click)
            self._spawn_npc(wx, wy)
            self.input.last_click = None

        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            self.spawn_timer = 0
            self._spawn_npc()

        for npc in self.npcs:
            npc.update(self.bounds)

        self.player.update(pressed, self.bounds)

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        if "space" in pressed and self.fire_cooldown == 0:
            self.fire_cooldown = 10
            self._fire_bullet()

        alive_bullets = []
        for b in self.bullets:
            if b.update(self.bounds):
                alive_bullets.append(b)
        self.bullets = alive_bullets

        self._handle_player_npc_collisions()
        self._handle_npc_npc_collisions()
        self._handle_bullet_hits()

        self.player.x, self.player.y, _, _ = self.bounds.clamp(self.player.x, self.player.y)
        for npc in self.npcs:
            npc.x, npc.y, _, _ = self.bounds.clamp(npc.x, npc.y)

    def _spawn_npc(self, x=None, y=None):
        if x is None:
            x = random.uniform(self.bounds.x_min + 5, self.bounds.x_max - 5)
        if y is None:
            y = random.uniform(self.bounds.y_min + 5, self.bounds.y_max - 5)
        vx = random.choice([-2, -1, 1, 2])
        vy = random.choice([-2, -1, 1, 2])
        self.npcs.append(NPC(x, y, vx=vx, vy=vy, radius=8))

    def _fire_bullet(self):
        speed = 6.0
        vx = math.cos(self.player.angle) * speed
        vy = math.sin(self.player.angle) * speed
        self.bullets.append(Bullet(self.player.x, self.player.y, vx, vy, radius=3))

    def _handle_player_npc_collisions(self):
        for npc in self.npcs:
            if circles_collide(
                self.player.x, self.player.y, self.player.radius,
                npc.x, npc.y, npc.radius
            ):
                px, py, _, _ = separate_circles(
                    self.player.x, self.player.y, self.player.radius,
                    npc.x, npc.y, npc.radius
                )
                self.player.x, self.player.y = px, py
                npc.vx *= -1
                npc.vy *= -1

    def _handle_npc_npc_collisions(self):
        n = len(self.npcs)
        for i in range(n):
            for j in range(i + 1, n):
                a = self.npcs[i]
                b = self.npcs[j]
                if circles_collide(a.x, a.y, a.radius, b.x, b.y, b.radius):
                    ax, ay, bx, by = separate_circles(a.x, a.y, a.radius, b.x, b.y, b.radius)
                    a.x, a.y = ax, ay
                    b.x, b.y = bx, by
                    a.vx, b.vx = b.vx, a.vx
                    a.vy, b.vy = b.vy, a.vy

    def _handle_bullet_hits(self):
        remove_b = set()
        remove_n = set()

        for bi, b in enumerate(self.bullets):
            for ni, npc in enumerate(self.npcs):
                if circles_collide(b.x, b.y, b.radius, npc.x, npc.y, npc.radius):
                    remove_b.add(bi)
                    remove_n.add(ni)

        if remove_b:
            self.bullets = [b for i, b in enumerate(self.bullets) if i not in remove_b]
        if remove_n:
            self.npcs = [n for i, n in enumerate(self.npcs) if i not in remove_n]
