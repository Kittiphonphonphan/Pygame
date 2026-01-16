import time
from entities import circles_collide, separate_circles


class GameEngine:
    def __init__(self, player, npcs, graphics, input_system, bounds, fps=60):
        self.player = player
        self.npcs = npcs
        self.graphics = graphics
        self.input = input_system
        self.bounds = bounds
        self.fps = fps
        self.running = True
        self.clock = getattr(graphics, "clock", None)

    def run(self):
        while self.running:
            pressed, quit_requested = self.input.scan_keys()

            if quit_requested or "q" in pressed:
                break

            self.update(pressed)
            self.graphics.render(self.player, self.npcs)

            if self.clock:
                self.clock.tick(self.fps)
            else:
                time.sleep(1 / self.fps)

    def update(self, pressed: set[str]):
        for npc in self.npcs:
            npc.update(self.bounds)

        self.player.update(pressed, self.bounds)

        self._handle_player_npc_collisions()
        self._handle_npc_npc_collisions()

        self.player.x, self.player.y, _, _ = self.bounds.clamp(self.player.x, self.player.y)
        for npc in self.npcs:
            npc.x, npc.y, _, _ = self.bounds.clamp(npc.x, npc.y)

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

                if circles_collide(
                    a.x, a.y, a.radius,
                    b.x, b.y, b.radius
                ):
                    ax, ay, bx, by = separate_circles(
                        a.x, a.y, a.radius,
                        b.x, b.y, b.radius
                    )
                    a.x, a.y = ax, ay
                    b.x, b.y = bx, by

                    a.vx, b.vx = b.vx, a.vx
                    a.vy, b.vy = b.vy, a.vy
