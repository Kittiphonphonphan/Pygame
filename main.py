from engine import GameEngine
from entities import Player, NPC, Bounds
from text_backend import TextGraphicsEngine, TextInputSystem
from pygame_backend import PygameGraphicsEngine, PygameInputSystem

USE_PYGAME = True

bounds = Bounds(0, 0, 100, 100)
player = Player(50, 50, speed=2)
npcs = [NPC(20,20,2,1), NPC(80,70,-2,2)]

if USE_PYGAME:
    graphics = PygameGraphicsEngine(bounds)
    input_system = PygameInputSystem()
else:
    graphics = TextGraphicsEngine()
    input_system = TextInputSystem()

engine = GameEngine(player, npcs, graphics, input_system, bounds, fps=60)
engine.run()

if USE_PYGAME:
    graphics.close()
