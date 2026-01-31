from __future__ import annotations
import math


class Bounds:
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def clamp(self, x: float, y: float) -> tuple[float, float, bool, bool]:
        x_edge = x < self.x_min or x > self.x_max
        y_edge = y < self.y_min or y > self.y_max
        x = max(self.x_min, min(self.x_max, x))
        y = max(self.y_min, min(self.y_max, y))
        return x, y, x_edge, y_edge


def circles_collide(ax: float, ay: float, ar: float, bx: float, by: float, br: float) -> bool:
    dx = ax - bx
    dy = ay - by
    return (dx * dx + dy * dy) <= (ar + br) * (ar + br)


def separate_circles(ax: float, ay: float, ar: float, bx: float, by: float, br: float) -> tuple[float, float, float, float]:
    dx = ax - bx
    dy = ay - by
    dist = math.hypot(dx, dy)

    if dist == 0:
        dx, dy = 1.0, 0.0
        dist = 1.0

    overlap = (ar + br) - dist
    if overlap <= 0:
        return ax, ay, bx, by

    nx = dx / dist
    ny = dy / dist

    ax += nx * (overlap / 2)
    ay += ny * (overlap / 2)
    bx -= nx * (overlap / 2)
    by -= ny * (overlap / 2)
    return ax, ay, bx, by


class NPC:
    def __init__(self, x: float, y: float, vx: float = 1, vy: float = 1, radius: float = 6):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def update(self, bounds):
        self.x += self.vx
        self.y += self.vy

        self.x, self.y, x_ed_
