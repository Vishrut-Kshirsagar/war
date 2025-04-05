# entity2.py
import random
from attack_types import normal_attack, heavy_attack, quick_attack, magic_attack

def weighted_choice(choices):
    total = sum(weight for action, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for action, weight in choices:
        if upto + weight >= r:
            return action
        upto += weight
    return choices[-1][0]

class Entity:
    def __init__(self, name, config=None):
        if config is None:
            config = {}
        self.name = name
        self.max_health = config.get("max_health", 110)
        self.health = self.max_health
        self.attack = config.get("attack", 23)
        self.defense = config.get("defense", 10)
        self.healing_ability = config.get("healing_ability", 18)
        self.max_mana = config.get("max_mana", 110)
        self.mana = self.max_mana
        self.mana_cost = config.get("mana_cost", 30)
        self.special_attack_damage = config.get("special_attack_damage", 40)
        self.karma = config.get("karma", 50)
        self.max_stamina = config.get("max_stamina", 100)
        self.stamina = self.max_stamina
        self.accuracy = config.get("accuracy", 0.82)
        self.evasion = config.get("evasion", 0.12)
        self.critical_chance = config.get("critical_chance", 0.12)
        self.heal_turns = 0
        self.inventory = {
            "health_potion": 2,
            "mana_potion": 2,
            "stamina_boost": 1,
            "karma_scroll": 1,
        }

    def recover_stamina(self, amount=10):
        self.stamina = min(self.stamina + amount, self.max_stamina)
        
    def rest(self):
        recovered_stamina = random.uniform(15, 25)
        self.stamina = min(self.stamina + recovered_stamina, self.max_stamina)
        recovered_mana = random.uniform(5, 10)
        self.mana = min(self.mana + recovered_mana, self.max_mana)
        print(f"{self.name} rests and recovers {recovered_stamina:.1f} stamina and {recovered_mana:.1f} mana.")
        
    def take_damage(self, damage):
        actual_damage = max(damage - self.defense, 0)
        self.health -= actual_damage
        print(f"{self.name} takes {actual_damage:.1f} damage (Health: {self.health:.1f}).")
        
    def heal(self):
        self.health += self.healing_ability
        if self.health > self.max_health:
            self.health = self.max_health
        self.heal_turns += 1
        self.karma += 5
        self.recover_stamina(15)
        print(f"{self.name} heals for {self.healing_ability} (Health: {self.health:.1f}), karma now {self.karma}.")
        
    def defend(self):
        print(f"{self.name} takes a defensive stance, boosting defense temporarily.")
        self.defense += 5
        self.stamina -= 5
        
    def choose_attack(self, opponent):
        attack_options = []
        if self.stamina >= 20:
            attack_options.append(("heavy_attack", 0.3))
        if self.mana >= self.mana_cost:
            attack_options.append(("magic_attack", 0.3))
        if self.stamina >= 5:
            attack_options.append(("quick_attack", 0.3))
        if self.stamina >= 10:
            attack_options.append(("normal_attack", 0.4))
        if not attack_options:
            return "rest"
        return weighted_choice(attack_options)
        
    def choose_action(self, opponent):
        actions = []
        health_ratio = self.health / self.max_health
        if health_ratio < 0.4:
            actions.append(("heal", 0.6))
        if self.stamina < 10:
            actions.append(("rest", 0.8))
        if self.stamina >= 20:
            actions.append(("heavy_attack", 0.3))
        if self.mana >= self.mana_cost:
            actions.append(("magic_attack", 0.3))
        if self.stamina >= 5:
            actions.append(("quick_attack", 0.3))
        if self.stamina >= 10:
            actions.append(("normal_attack", 0.4))
        if not actions:
            actions.append(("defend", 0.5))
        return weighted_choice(actions)
        
    def take_turn(self, opponent):
        if self.health < 40 and self.inventory.get("health_potion", 0) > 0:
            self.use_health_potion()
        elif self.mana < 30 and self.inventory.get("mana_potion", 0) > 0:
            self.use_mana_potion()
        elif self.stamina < 20 and self.inventory.get("stamina_boost", 0) > 0:
            self.use_stamina_boost()
        else:
            action = self.choose_action(opponent)
            if action == "heal":
                self.heal()
            elif action == "rest":
                self.rest()
            elif action == "defend":
                self.defend()
            elif action in ["normal_attack", "heavy_attack", "quick_attack", "magic_attack"]:
                if action == "normal_attack":
                    normal_attack(self, opponent)
                elif action == "heavy_attack":
                    heavy_attack(self, opponent)
                elif action == "quick_attack":
                    quick_attack(self, opponent)
                elif action == "magic_attack":
                    magic_attack(self, opponent)
        self.recover_stamina(random.uniform(5, 10))
        
    def is_alive(self):
        return self.health > 0
    
    def propose_trade(self, other, offer, request):
        if all(self.inventory.get(item, 0) >= qty for item, qty in offer.items()) and \
           all(other.inventory.get(item, 0) >= qty for item, qty in request.items()):
            print(f"{self.name} proposes trade to {other.name}: {offer} for {request}")
            return True
        print(f"{self.name}'s trade proposal failed due to insufficient items.")
        return False
    
    def accept_trade(self, other, offer, request):
        for item, qty in offer.items():
            self.inventory[item] = self.inventory.get(item, 0) + qty
            other.inventory[item] = other.inventory.get(item, 0) - qty
        for item, qty in request.items():
            self.inventory[item] = self.inventory.get(item, 0) - qty
            other.inventory[item] = other.inventory.get(item, 0) + qty
        print(f"{self.name} accepted trade with {other.name}: {offer} for {request}")
    
    def use_health_potion(self):
        if self.inventory.get("health_potion", 0) > 0:
            healed_amount = min(30, self.max_health - self.health)
            self.health += healed_amount
            self.inventory["health_potion"] -= 1
            print(f"{self.name} uses a health potion and heals {healed_amount} HP.")
        else:
            print(f"{self.name} has no health potions!")
    
    def use_mana_potion(self):
        if self.inventory.get("mana_potion", 0) > 0:
            recovered_mana = min(25, self.max_mana - self.mana)
            self.mana += recovered_mana
            self.inventory["mana_potion"] -= 1
            print(f"{self.name} uses a mana potion and recovers {recovered_mana} mana.")
        else:
            print(f"{self.name} has no mana potions!")
    
    def use_stamina_boost(self):
        if self.inventory.get("stamina_boost", 0) > 0:
            recovered_stamina = min(20, self.max_stamina - self.stamina)
            self.stamina += recovered_stamina
            self.inventory["stamina_boost"] -= 1
            print(f"{self.name} uses a stamina boost and recovers {recovered_stamina} stamina.")
        else:
            print(f"{self.name} has no stamina boosts!")
