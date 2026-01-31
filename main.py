from engine import GameEngine
from entities import Player, NPC, Bounds
from text_backend import TextGraphicsEngine, TextInputSystem
from pygame_backend import PygameGraphicsEngine, PygameInputSystem


def main():
    USE_PYGAME = True

    bounds = Bounds(0, 0, 100, 100)

    player = Player(50, 50, speed=2, radius=8)

    npcs = [
        NPC(20, 20, vx=2, vy=1, radius=8),
        NPC(80, 70, vx=-2, vy=2, radius=8),
        NPC(40, 80, vx=1, vy=-2, radius=8),
        NPC(60, 30, vx=-1, vy=1, radius=8),
    ]
    if USE_PYGAME:
        graphics = PygameGraphicsEngine(bounds=bounds, width=900, height=600, title="Collision Game")
        input_system = PygameInputSystem()
        fps = 60
    else:
        graphics = TextGraphicsEngine()
        input_system = TextInputSystem()
        fps = 5

    engine = GameEngine(
        player=player,
        npcs=npcs,
        graphics=graphics,
        input_system=input_system,
        bounds=bounds,
        fps=fps
    )

    try:
        engine.run()
    finally:
        if USE_PYGAME:
            graphics.close()


if __name__ == "__main__":
    main()
