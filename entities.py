from __future__ import annotations

class Bounds:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def clamp(self, x, y):
        x_edge = x < self.x_min or x > self.x_max
        y_edge = y < self.y_min or y > self.y_max
        x = max(self.x_min, min(self.x_max, x))
        y = max(self.y_min, min(self.y_max, y))
        return x, y, x_edge, y_edge


class NPC:
    def __init__(self, x, y, vx=1, vy=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self, bounds):
        self.x += self.vx
        self.y += self.vy
        self.x, self.y, x_edge, y_edge = bounds.clamp(self.x, self.y)
        if x_edge:
            self.vx *= -1
        if y_edge:
            self.vy *= -1


class Player:
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, pressed, bounds):
        if "w" in pressed:
            self.y -= self.speed
        if "s" in pressed:
            self.y += self.speed
        if "a" in pressed:
            self.x -= self.speed
        if "d" in pressed:
            self.x += self.speed

        self.x, self.y, _, _ = bounds.clamp(self.x, self.y)
