import time
from entities import Player, NPC, Bounds

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
            if quit_requested:
                break

            if "q" in pressed:
                break

            for npc in self.npcs:
                npc.update(self.bounds)

            self.player.update(pressed, self.bounds)
            self.graphics.render(self.player, self.npcs)

            if self.clock:
                self.clock.tick(self.fps)
            else:
                time.sleep(1 / self.fps)
