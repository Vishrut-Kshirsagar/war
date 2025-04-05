# vishnu.py
import random

class Vishnu:
    def __init__(self):
        self.name = "Vishnu"
        self.cooldown = 0
        self.divine_energy = 120.0
        self.interventions = 0
        self.total_mana_granted = 0.0
        self.total_health_healed = 0.0
        self.cost_multiplier = 1.0

    def influence_battle(self, combatant1, combatant2):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if combatant1.health < 0.5 * combatant1.max_health:
            mult = 1 + (combatant1.karma - 50) / 100.0 + random.uniform(-0.1, 0.1)
            heal_amt = 15 * mult
            before = combatant1.health
            combatant1.health = min(combatant1.health + heal_amt, combatant1.max_health)
            actual_heal = combatant1.health - before
            self.total_health_healed += actual_heal
            self.interventions += 1
            cost = actual_heal * 0.1 * self.cost_multiplier
            self.divine_energy -= cost
            print(f"{self.name} heals {combatant1.name} for {actual_heal:.1f} health. (Cost: {cost:.1f} energy)")
        elif combatant2.health < 0.5 * combatant2.max_health:
            mult = 1 + (combatant2.karma - 50) / 100.0 + random.uniform(-0.1, 0.1)
            heal_amt = 15 * mult
            before = combatant2.health
            combatant2.health = min(combatant2.health + heal_amt, combatant2.max_health)
            actual_heal = combatant2.health - before
            self.total_health_healed += actual_heal
            self.interventions += 1
            cost = actual_heal * 0.1 * self.cost_multiplier
            self.divine_energy -= cost
            print(f"{self.name} heals {combatant2.name} for {actual_heal:.1f} health. (Cost: {cost:.1f} energy)")
        else:
            mult1 = 1 + (combatant1.karma - 50) / 100.0 + random.uniform(-0.1, 0.1)
            mult2 = 1 + (combatant2.karma - 50) / 100.0 + random.uniform(-0.1, 0.1)
            mana1 = 10 * mult1
            mana2 = 10 * mult2
            before1 = combatant1.mana
            before2 = combatant2.mana
            combatant1.mana = min(combatant1.mana + mana1, combatant1.max_mana)
            combatant2.mana = min(combatant2.mana + mana2, combatant2.max_mana)
            granted1 = combatant1.mana - before1
            granted2 = combatant2.mana - before2
            total_granted = granted1 + granted2
            self.total_mana_granted += total_granted
            self.interventions += 1
            cost = total_granted * 0.1 * self.cost_multiplier
            self.divine_energy -= cost
            print(f"{self.name} grants mana: {combatant1.name} gets {granted1:.1f}, {combatant2.name} gets {granted2:.1f}. (Cost: {cost:.1f} energy)")
        self.cooldown = random.randint(1, 3)
