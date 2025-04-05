# battlefield.py
import time, random
from entity_one import Entity as EntityOne
from entity_two import Entity as EntityTwo
from brahma import Brahma
from vishnu import Vishnu
from shiva import Shiva
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
    entity1 = EntityOne("Entity1", config1)
    entity2 = EntityTwo("Entity2", config2)
    brahma = Brahma()
    vishnu = Vishnu()
    shiva = Shiva()
    cosmic = CosmicEvent()
    turn = 0
    max_turns = 50

    while entity1.is_alive() and entity2.is_alive() and turn < max_turns:
        turn += 1
        print(f"\n{'-'*20} Turn {turn} {'-'*20}\n")
        cosmic.apply_event(entity1, entity2, brahma, vishnu, shiva)
        
        entity1.take_turn(entity2)
        entity2.take_turn(entity1)
        
        brahma.influence_battle(entity1, entity2)
        vishnu.influence_battle(entity1, entity2)
        shiva.influence_battle(entity1, entity2)
        
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
