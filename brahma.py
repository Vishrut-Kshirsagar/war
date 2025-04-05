# brahma.py
import random

class Brahma:
    def __init__(self):
        self.name = "Brahma"
        self.cooldown = 0
        self.divine_energy = 100.0  # Brahma's own well-being.
        self.interventions = 0
        self.total_health_restored = 0.0
        self.cost_multiplier = 1.0  # Dynamic multiplier (set by cosmic events).

    def influence_battle(self, combatant1, combatant2):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        bonus1 = 0.1 * combatant1.max_health * (1 + (combatant1.karma - 50) / 100.0 + random.uniform(-0.1, 0.1))
        bonus2 = 0.1 * combatant2.max_health * (1 + (combatant2.karma - 50) / 100.0 + random.uniform(-0.1, 0.1))
        before1 = combatant1.health
        before2 = combatant2.health
        combatant1.health = min(combatant1.health + bonus1, combatant1.max_health)
        combatant2.health = min(combatant2.health + bonus2, combatant2.max_health)
        restored1 = combatant1.health - before1
        restored2 = combatant2.health - before2
        total_restored = restored1 + restored2
        self.total_health_restored += total_restored
        self.interventions += 1
        cost = total_restored * 0.1 * self.cost_multiplier
        self.divine_energy -= cost
        print(f"{self.name} blesses {combatant1.name} for {restored1:.1f} health and {combatant2.name} for {restored2:.1f} health. (Cost: {cost:.1f} energy)")
        self.cooldown = random.randint(1, 3)
