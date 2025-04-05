# attack_types.py
import random
import math

def variable_damage(base_damage, variance=0.1):
    """
    Returns damage with random variation.
    'variance' is the percentage of the base damage that can vary.
    """
    variation = random.gauss(0, base_damage * variance)
    return max(0, base_damage + variation)


def normal_attack(attacker, defender):
    if attacker.stamina < 10:
        print(f"{attacker.name} is too exhausted for a normal attack!")
        return False
    attacker.stamina -= 10
    hit_chance = attacker.accuracy - defender.evasion
    if random.random() > hit_chance:
        print(f"{attacker.name}'s normal attack missed {defender.name}!")
        attacker.karma -= 2
        return False
    # Compute damage with variance.
    damage = variable_damage(attacker.attack, variance=0.2)
    defender.take_damage(damage)
    print(f"{attacker.name} performs a normal attack on {defender.name} for {damage:.1f} damage.")
    attacker.karma -= 5
    return True


def fatigue_multiplier(entity):
    """
    Returns a multiplier based on current stamina.
    When stamina is low, multiplier falls below 1, reducing effectiveness.
    """
    ratio = entity.stamina / entity.max_stamina  # value between 0 and 1.
    return 0.5 + 0.5 * ratio  # multiplier between 0.5 and 1.

# Example in an attack function:
def heavy_attack(attacker, defender):
    if attacker.stamina < 20:
        print(f"{attacker.name} is too exhausted for a heavy attack!")
        return False
    attacker.stamina -= 20
    effective_accuracy = (attacker.accuracy * fatigue_multiplier(attacker)) - defender.evasion
    if random.random() > effective_accuracy:
        print(f"{attacker.name}'s heavy attack missed {defender.name}!")
        attacker.karma -= 3
        return False
    damage = variable_damage(attacker.attack * 1.5, variance=0.25) * fatigue_multiplier(attacker)
    defender.take_damage(damage)
    print(f"{attacker.name} performs a heavy attack on {defender.name} for {damage:.1f} damage.")
    attacker.karma -= 7
    return True


def quick_attack(attacker, defender):
    if attacker.stamina < 5:
        print(f"{attacker.name} is too exhausted for a quick attack!")
        return False
    attacker.stamina -= 5
    hit_chance = (attacker.accuracy - defender.evasion) * 1.1  # Better accuracy
    if random.random() > hit_chance:
        print(f"{attacker.name}'s quick attack missed {defender.name}!")
        attacker.karma -= 1
        return False
    damage = attacker.attack * 0.75  # Lower damage
    defender.take_damage(damage)
    print(f"{attacker.name} performs a quick attack on {defender.name} for {damage:.1f} damage.")
    attacker.karma -= 3
    return True

def magic_attack(attacker, defender):
    if attacker.mana < attacker.mana_cost:
        print(f"{attacker.name} lacks mana for a magic attack!")
        return False
    attacker.mana -= attacker.mana_cost
    hit_chance = attacker.accuracy - defender.evasion
    if random.random() > hit_chance:
        print(f"{attacker.name}'s magic attack missed {defender.name}!")
        attacker.karma -= 4
        return False
    damage = attacker.special_attack_damage
    defender.take_damage(damage)
    print(f"{attacker.name} casts a magic attack on {defender.name} for {damage:.1f} damage.")
    attacker.karma -= 5
    return True
