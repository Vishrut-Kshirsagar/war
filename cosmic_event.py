# cosmic_event.py
import random

class CosmicEvent:
    def __init__(self):
        self.events = [
            {
                "name": "Celestial Alignment",
                "description": "A rare alignment boosts combat effectiveness.",
                "attack_multiplier": 1.1,
                "mana_regen_bonus": 5,
                "duration": 1
            },
            {
                "name": "Cosmic Drought",
                "description": "Cosmic energies are low; mana recovery suffers.",
                "attack_multiplier": 0.95,
                "mana_regen_bonus": -5,
                "duration": 1
            },
            {
                "name": "Mystic Winds",
                "description": "Evasive winds aid dodging—accuracy and evasion are slightly improved.",
                "accuracy_bonus": 0.05,
                "evasion_bonus": 0.05,
                "duration": 1
            },
            {
                "name": "Astral Surge",
                "description": "A surge of astral energy empowers divine intervention, reducing their cost by 50% this turn.",
                "divine_cost_multiplier": 0.5,
                "duration": 1
            },
            {
                "name": "Temporal Flux",
                "description": "Time seems to slow, allowing better recovery of stamina.",
                "stamina_recovery_bonus": 10,
                "duration": 1
            }
        ]
    
    def apply_event(self, e1, e2, brahma, vishnu, shiva):
        event = random.choice(self.events)
        print(f"\n*** Cosmic Event: {event['name']} - {event['description']} ***")
        if "attack_multiplier" in event:
            e1.attack *= event["attack_multiplier"]
            e2.attack *= event["attack_multiplier"]
        if "accuracy_bonus" in event:
            e1.accuracy += event["accuracy_bonus"]
            e2.accuracy += event["accuracy_bonus"]
            e1.evasion += event.get("evasion_bonus", 0)
            e2.evasion += event.get("evasion_bonus", 0)
        if "stamina_recovery_bonus" in event:
            e1.recover_stamina(event["stamina_recovery_bonus"])
            e2.recover_stamina(event["stamina_recovery_bonus"])
        if "mana_regen_bonus" in event:
            e1.mana = min(e1.mana + event["mana_regen_bonus"], e1.max_mana)
            e2.mana = min(e2.mana + event["mana_regen_bonus"], e2.max_mana)
        if "divine_cost_multiplier" in event:
            brahma.cost_multiplier = event["divine_cost_multiplier"]
            vishnu.cost_multiplier = event["divine_cost_multiplier"]
            shiva.cost_multiplier = event["divine_cost_multiplier"]
        else:
            brahma.cost_multiplier = 1.0
            vishnu.cost_multiplier = 1.0
            shiva.cost_multiplier = 1.0
        return event
