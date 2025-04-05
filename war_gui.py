import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import time
from entity import Entity
from priest import Priest
from mechanist import Mechanist
from gods import get_all_gods
from cosmic_event import CosmicEvent

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WarGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cosmic War Simulator")
        self.geometry("1000x800")
        self.resizable(False, False)

        self.gods = get_all_gods()
        self.cosmic = CosmicEvent()

        self.turn = 0
        self.max_turns = 50
        self.running = False

        self.entity1 = Priest("High Priest Tenzin", gods=self.gods, logger=self.log)
        self.entity2 = Entity("Entity2", logger=self.log)
        self.entity3 = Mechanist("Entity3", logger=self.log)

        self.entities = [self.entity1, self.entity2, self.entity3]

        self.build_ui()
        self.update_stats()
        self.log("Welcome to the Cosmic War Simulator!")

    def build_ui(self):
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure(2, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Cosmic War Simulator", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.cosmic_label = ctk.CTkLabel(self, text="Cosmic Event: None", font=("Arial", 14))
        self.cosmic_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.status_frames = []
        for i, entity in enumerate(self.entities):
            frame = self.create_status_frame(entity)
            frame.grid(row=2, column=i, sticky="nsew", padx=10, pady=10)
            self.status_frames.append(frame)

        self.log_box = ctk.CTkTextbox(self, width=950, height=300)
        self.log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.controls = ctk.CTkFrame(self)
        self.controls.grid(row=4, column=0, columnspan=3, pady=10)

        self.next_btn = ctk.CTkButton(self.controls, text="Next Turn", command=self.next_turn)
        self.next_btn.pack(side="left", padx=10)

        self.auto_btn = ctk.CTkButton(self.controls, text="Auto Run", command=self.toggle_auto)
        self.auto_btn.pack(side="left", padx=10)

        self.reset_btn = ctk.CTkButton(self.controls, text="Reset", command=self.reset)
        self.reset_btn.pack(side="left", padx=10)

    def create_status_frame(self, entity):
        frame = ctk.CTkFrame(self)
        entity.name_label = ctk.CTkLabel(frame, text=entity.name, font=("Arial", 16, "bold"))
        entity.name_label.pack(pady=5)
        entity.health_bar = ctk.CTkProgressBar(frame)
        entity.health_bar.set(entity.health / entity.max_health)
        entity.health_bar.pack(fill="x", padx=10)
        entity.health_text = ctk.CTkLabel(frame, text=f"Health: {entity.health:.1f}/{entity.max_health}")
        entity.health_text.pack()
        return frame

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def update_stats(self):
        for entity in self.entities:
            entity.health_bar.set(entity.health / entity.max_health)
            entity.health_text.configure(text=f"Health: {entity.health:.1f}/{entity.max_health}")

    def next_turn(self):
        alive_entities = [e for e in self.entities if e.is_alive()]
        if self.turn >= self.max_turns or len(alive_entities) <= 1:
            self.end_battle()
            return

        self.turn += 1
        self.log(f"\n-- Turn {self.turn} --")
        event = self.cosmic.apply_event(*self.entities[:2], *self.gods.values())
        if event:
            self.cosmic_label.configure(text=f"Cosmic Event: {event.name}")
            self.log(f"*** Cosmic Event: {event.name} - {event.description} ***")

        # Each entity takes a turn against a random opponent
        for entity in self.entities:
            if not entity.is_alive():
                continue  # dead men tell no tales, nor do they punch
            opponents = [e for e in self.entities if e != entity and e.is_alive()]
            if opponents:
                target = random.choice(opponents)
                entity.take_turn(target)

        # Divine influence: gods favor entity1, smite someone else (if someone else is alive)
        favored_target = self.entity1
        possible_targets = [e for e in self.entities if e != favored_target and e.is_alive()]
        for god in self.gods.values():
            if possible_targets:
                god_opponent = random.choice(possible_targets)
                god.influence_battle(favored_target, god_opponent)

        self.update_stats()

        if len([e for e in self.entities if e.is_alive()]) <= 1:
            self.end_battle()


    def toggle_auto(self):
        self.running = not self.running
        self.auto_btn.configure(text="Pause" if self.running else "Auto Run")
        if self.running:
            self.run_auto()

    def run_auto(self):
        if self.running and len([e for e in self.entities if e.is_alive()]) > 1:
            self.next_turn()
            self.after(1000, self.run_auto)

    def reset(self):
        self.entity1 = Priest("High Priest Tenzin", gods=self.gods, logger=self.log)
        self.entity2 = Entity("Entity2", logger=self.log)
        self.entity3 = Mechanist("Entity3", logger=self.log)
        self.entities = [self.entity1, self.entity2, self.entity3]

        self.turn = 0
        self.running = False
        self.log_box.delete("1.0", "end")

        for frame in self.status_frames:
            frame.destroy()
        self.status_frames = []

        for i, entity in enumerate(self.entities):
            frame = self.create_status_frame(entity)
            frame.grid(row=2, column=i, sticky="nsew", padx=10, pady=10)
            self.status_frames.append(frame)

        self.update_stats()
        self.cosmic_label.configure(text="Cosmic Event: None")
    def end_battle(self):
        alive = [e for e in self.entities if e.is_alive()]
        
        if len(alive) == 1:
            winner = alive[0].name
        elif len(alive) == 0:
            winner = "No one"
        else:
            # In case multiple are still alive after max turns
            winner = "No one (stalemate)"

        self.log(f"\n*** {winner} wins after {self.turn} turns! ***")
        messagebox.showinfo("Battle Over", f"{winner} is victorious!")

if __name__ == "__main__":
    app = WarGUI()
    app.mainloop()
