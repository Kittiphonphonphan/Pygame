class TextInputSystem:
    def scan_keys(self):
        s = input("keys (wasd, q): ").lower()
        return set(s), False


class TextGraphicsEngine:
    def render(self, player, npcs):
        print(f"Player: ({player.x}, {player.y})")
        for i, npc in enumerate(npcs, 1):
            print(f"NPC {i}: ({npc.x}, {npc.y})")
        print("-" * 20)
