# battlefield.py
import time, random
from entity import Entity
from priest import Priest
from mechanist import Mechanist
from gods import get_all_gods
from gods import Brahma, Vishnu, Shiva
from cosmic_event import CosmicEvent

def print_status(e1, e2, turn):
    print("\n" + "="*70)
    print(f"Turn {turn} Summary:")
    print("="*70)
    print(f"{'Name':<10} | {'Health':>8} | {'Mana':>8} | {'Karma':>6} | {'Stamina':>8}")
    print("-"*70)
    print(f"{e1.name:<10} | {e1.health:8.1f} | {e1.mana:8.1f} | {e1.karma:6} | {e1.stamina:8.1f}")
    print(f"{e2.name:<10} | {e2.health:8.1f} | {e2.mana:8.1f} | {e2.karma:6} | {e2.stamina:8.1f}")
    print("="*70 + "\n")

def print_deity_stats(brahma, vishnu, shiva):
    print("\n" + "="*70)
    print("Divine Intervention Summary:")
    print("="*70)
    print(f"Brahma: Interventions = {brahma.interventions}, Total Health Restored = {brahma.total_health_restored:.1f}, Remaining Energy = {brahma.divine_energy:.1f}")
    print(f"Vishnu: Interventions = {vishnu.interventions}, Total Mana Granted = {vishnu.total_mana_granted:.1f}, Total Health Healed = {vishnu.total_health_healed:.1f}, Remaining Energy = {vishnu.divine_energy:.1f}")
    print(f"Shiva: Interventions = {shiva.interventions}, Total Decay Inflicted = {shiva.total_decay_inflicted:.1f}, Remaining Energy = {shiva.divine_energy:.1f}")
    print("="*70 + "\n")

def main():
    config1 = {
        "max_health": 120, "attack": 25, "defense": 8, "healing_ability": 20,
        "max_mana": 100, "mana_cost": 25, "special_attack_damage": 45,
        "karma": 50, "max_stamina": 100, "accuracy": 0.8, "evasion": 0.1, "critical_chance": 0.15
    }
    config2 = {
        "max_health": 110, "attack": 23, "defense": 10, "healing_ability": 18,
        "max_mana": 110, "mana_cost": 30, "special_attack_damage": 40,
        "karma": 50, "max_stamina": 100, "accuracy": 0.82, "evasion": 0.12, "critical_chance": 0.12
    }
    gods = get_all_gods()
    entity1 = Priest("High Priest Tenzin", gods=gods, config=config1)
    entity2 = Entity("Entity2", config2)
    entity3 = Mechanist("Entity3") # A godless machine enters the battlefield.

    brahma = gods["brahma"]
    vishnu = gods["vishnu"]
    shiva = gods["shiva"]
    shiva = Shiva()
    cosmic = CosmicEvent()
    turn = 0
    max_turns = 50

    while all(e.is_alive() for e in [entity1, entity2, entity3]) and turn < max_turns:
        turn += 1
        print(f"\n{'-'*20} Turn {turn} {'-'*20}\n")
        cosmic.apply_event(entity1, entity2, brahma, vishnu, shiva)
        
        # Priest tries divine intervention every 4 turns, otherwise fights
        # Entity1 (Priest) logic
        if isinstance(entity1, Priest) and turn % 4 == 0:
            target = min([entity2, entity3], key=lambda e: e.health)
            entity1.ability(target)
        else:
            entity1.take_turn(random.choice([entity2, entity3]))

        # Entity2 logic — same ol' punch machine
        entity2.take_turn(random.choice([entity1, entity3]))

        # Entity3 enters the arena — probably ready to tase somebody
        entity3.take_turn(random.choice([entity1, entity2]))
        
        entities = [entity1, entity2]
        weights = [0.6, 0.4]  # 60% chance to favor entity1

        target1 = random.choices(entities, weights=weights)[0]
        target2 = entity2 if target1 is entity1 else entity1

        brahma.influence_battle(target1, target2)
        vishnu.influence_battle(target1, target2)
        shiva.influence_battle(target1, target2)
        
        # Trade Phase every 5 turns:
        if turn % 5 == 0:
            if entity1.health < 50 and entity1.inventory.get("health_potion", 0) < 1 and entity2.inventory.get("health_potion", 0) > 0:
                offer = {"mana_potion": 1}
                request = {"health_potion": 1}
                if entity1.propose_trade(entity2, offer, request):
                    entity2.accept_trade(entity1, offer, request)
        
        print_status(entity1, entity2, turn)
        time.sleep(1)
    
    if entity1.is_alive() and entity2.is_alive():
        print("After 50 intense turns, the war ends in a stalemate!")
    elif entity1.is_alive():
        print(f"{entity1.name} wins after {turn} turns!")
    else:
        print(f"{entity2.name} wins after {turn} turns!")
    
    print_deity_stats(brahma, vishnu, shiva)

if __name__ == "__main__":
    main()
