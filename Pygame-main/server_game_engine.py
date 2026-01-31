import time

class ServerGameEngine:
    def __init__(self, bounds, npcs, fps=60):
        self.bounds = bounds
        self.npcs = npcs
        self.fps = fps
        self.players = {}
        self.inputs = {}
        self.running = True

    def add_player(self, pid, x=50, y=50, speed=2, radius=8):
        self.players[pid] = {"x": float(x), "y": float(y), "speed": speed, "radius": radius}
        self.inputs[pid] = set()

    def remove_player(self, pid):
        self.players.pop(pid, None)
        self.inputs.pop(pid, None)

    def set_input(self, pid, pressed):
        if pid in self.inputs:
            self.inputs[pid] = pressed

    def tick(self):
        for npc in self.npcs:
            npc.update(self.bounds)

        for pid, p in self.players.items():
            k = self.inputs.get(pid, set())
            s = p["speed"]
            if "w" in k: p["y"] -= s
            if "s" in k: p["y"] += s
            if "a" in k: p["x"] -= s
            if "d" in k: p["x"] += s
            p["x"], p["y"], _, _ = self.bounds.clamp(p["x"], p["y"])

    def state(self):
        return {
            "players": self.players,
            "npcs": [{"x": n.x, "y": n.y, "r": n.radius} for n in self.npcs],
            "bounds": {
                "x_min": self.bounds.x_min,
                "y_min": self.bounds.y_min,
                "x_max": self.bounds.x_max,
                "y_max": self.bounds.y_max,
            },
        }

    def run(self, on_tick):
        dt = 1 / self.fps
        while self.running:
            start = time.time()
            self.tick()
            on_tick(self.state())
            time.sleep(max(0, dt - (time.time() - start)))
