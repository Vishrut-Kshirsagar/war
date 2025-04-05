# shiva.py
import random

class Shiva:
    def __init__(self):
        self.name = "Shiva"
        self.cooldown = 0
        self.divine_energy = 90.0
        self.interventions = 0
        self.total_decay_inflicted = 0.0
        self.cost_multiplier = 1.0

    def influence_battle(self, combatant1, combatant2):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        base_decay = 5
        mult1 = max(0.5, 1 + (50 - combatant1.karma) / 100.0 + random.uniform(-0.1, 0.1))
        mult2 = max(0.5, 1 + (50 - combatant2.karma) / 100.0 + random.uniform(-0.1, 0.1))
        decay1 = base_decay * mult1
        decay2 = base_decay * mult2
        combatant1.take_damage(decay1)
        combatant2.take_damage(decay2)
        total_decay = decay1 + decay2
        self.total_decay_inflicted += total_decay
        self.interventions += 1
        cost = total_decay * 0.05 * self.cost_multiplier
        self.divine_energy -= cost
        print(f"{self.name} inflicts decay: {combatant1.name} loses {decay1:.1f} health, {combatant2.name} loses {decay2:.1f} health. (Cost: {cost:.1f} energy)")
        self.cooldown = random.randint(1, 3)
