# war_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import sys, random

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from entity_one import Entity as EntityOne
from entity_two import Entity as EntityTwo
from brahma import Brahma
from vishnu import Vishnu
from shiva import Shiva
from cosmic_event import CosmicEvent

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
    def flush(self):
        pass

class WarSimulation:
    def __init__(self, gui):
        self.gui = gui
        self.turn = 0
        self.max_turns = 50
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
        self.entity1 = EntityOne("Entity1", config1)
        self.entity2 = EntityTwo("Entity2", config2)
        self.brahma = Brahma()
        self.vishnu = Vishnu()
        self.shiva = Shiva()
        self.cosmic = CosmicEvent()
        self.simulation_over = False
        self.turn_history = []
        self.e1_health_history = []
        self.e2_health_history = []

    def update_history(self):
        self.turn_history.append(self.turn)
        self.e1_health_history.append(max(self.entity1.health, 0))
        self.e2_health_history.append(max(self.entity2.health, 0))

    def update_gui(self):
        self.gui.update_stats(self.entity1, self.entity2, self.turn)
        self.gui.update_chart(self.turn_history, self.e1_health_history, self.e2_health_history)

    def next_turn(self):
        if self.simulation_over:
            return
        if not (self.entity1.is_alive() and self.entity2.is_alive() and self.turn < self.max_turns):
            self.end_simulation()
            return
        self.turn += 1
        print(f"\n{'-'*20} Turn {self.turn} {'-'*20}\n")
        event = self.cosmic.apply_event(self.entity1, self.entity2, self.brahma, self.vishnu, self.shiva)
        self.gui.update_cosmic_event(event)
        self.entity1.take_turn(self.entity2)
        self.entity2.take_turn(self.entity1)
        self.brahma.influence_battle(self.entity1, self.entity2)
        self.vishnu.influence_battle(self.entity1, self.entity2)
        self.shiva.influence_battle(self.entity1, self.entity2)
        self.update_history()
        self.update_gui()
        if not (self.entity1.is_alive() and self.entity2.is_alive()) or self.turn >= self.max_turns:
            self.end_simulation()

    def end_simulation(self):
        self.simulation_over = True
        if self.entity1.is_alive() and self.entity2.is_alive():
            result = "After 50 intense turns, the war ends in a stalemate!"
        elif self.entity1.is_alive():
            result = f"{self.entity1.name} wins after {self.turn} turns!"
        else:
            result = f"{self.entity2.name} wins after {self.turn} turns!"
        print("\n" + "="*70)
        print(result)
        print("="*70)
        deity_stats = (
            f"Brahma: Interventions = {self.brahma.interventions}, Total Health Restored = {self.brahma.total_health_restored:.1f}, Remaining Energy = {self.brahma.divine_energy:.1f}\n"
            f"Vishnu: Interventions = {self.vishnu.interventions}, Total Mana Granted = {self.vishnu.total_mana_granted:.1f}, Total Health Healed = {self.vishnu.total_health_healed:.1f}, Remaining Energy = {self.vishnu.divine_energy:.1f}\n"
            f"Shiva: Interventions = {self.shiva.interventions}, Total Decay Inflicted = {self.shiva.total_decay_inflicted:.1f}, Remaining Energy = {self.shiva.divine_energy:.1f}\n"
        )
        print(deity_stats)
        messagebox.showinfo("Simulation Ended", result)

class WarGUI:
    def __init__(self, root):
        self.root = root
        root.title("Cosmic War Simulation - Ultimate Interface")
        root.geometry("1200x800")
        
        self.top_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.cosmic_label = tk.Label(self.top_frame, text="Cosmic Event: None", font=("Helvetica", 14, "bold"), fg="blue")
        self.cosmic_label.pack(pady=5)
        
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.btn_next = tk.Button(self.control_frame, text="Next Turn", font=("Helvetica", 12), command=self.next_turn)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        self.btn_run = tk.Button(self.control_frame, text="Run Simulation", font=("Helvetica", 12), command=self.run_simulation)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        self.btn_pause = tk.Button(self.control_frame, text="Pause", font=("Helvetica", 12), command=self.pause_simulation)
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        self.btn_reset = tk.Button(self.control_frame, text="Reset Simulation", font=("Helvetica", 12), command=self.reset_simulation)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.DoubleVar(value=1000)
        self.speed_slider = tk.Scale(self.control_frame, variable=self.speed_var, from_=200, to=2000, resolution=100,
                                     orient=tk.HORIZONTAL, label="Turn Delay (ms)")
        self.speed_slider.pack(side=tk.LEFT, padx=5)
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SUNKEN)
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_area = ScrolledText(self.log_frame, width=80, height=30, font=("Courier", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        self.status_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.status_label = tk.Label(self.status_frame, text="Entity Status", font=("Helvetica", 12, "bold"))
        self.status_label.pack(pady=5)
        self.entity1_status = tk.Label(self.status_frame, text="", font=("Courier", 10))
        self.entity1_status.pack(pady=2)
        self.health_bar1 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.health_bar1.pack(pady=2)
        self.mana_bar1 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.mana_bar1.pack(pady=2)
        self.stamina_bar1 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.stamina_bar1.pack(pady=2)
        self.entity2_status = tk.Label(self.status_frame, text="", font=("Courier", 10))
        self.entity2_status.pack(pady=10)
        self.health_bar2 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.health_bar2.pack(pady=2)
        self.mana_bar2 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.mana_bar2.pack(pady=2)
        self.stamina_bar2 = ttk.Progressbar(self.status_frame, orient="horizontal", length=150, mode="determinate")
        self.stamina_bar2.pack(pady=2)
        
        self.chart_frame = tk.Frame(self.main_frame, bd=2, relief=tk.RIDGE)
        self.chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Health Trends")
        self.ax.set_xlabel("Turn")
        self.ax.set_ylabel("Health")
        self.line1, = self.ax.plot([], [], label="Entity1", color="red")
        self.line2, = self.ax.plot([], [], label="Entity2", color="green")
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.simulation = WarSimulation(self)
        self.update_stats(self.simulation.entity1, self.simulation.entity2, self.simulation.turn)
        sys.stdout = TextRedirector(self.log_area)
        self.running = False

    def update_cosmic_event(self, event):
        if event and "name" in event:
            self.cosmic_label.config(text=f"Cosmic Event: {event['name']}", fg="blue")
        else:
            self.cosmic_label.config(text="Cosmic Event: None", fg="black")
    
    def update_stats(self, e1, e2, turn):
        status_text1 = f"{e1.name} | Health: {e1.health:.1f}/{e1.max_health} | Mana: {e1.mana:.1f}/{e1.max_mana} | Karma: {e1.karma} | Stamina: {e1.stamina:.1f}/{e1.max_stamina}"
        status_text2 = f"{e2.name} | Health: {e2.health:.1f}/{e2.max_health} | Mana: {e2.mana:.1f}/{e2.max_mana} | Karma: {e2.karma} | Stamina: {e2.stamina:.1f}/{e2.max_stamina}"
        self.entity1_status.config(text=status_text1)
        self.entity2_status.config(text=status_text2)
        self.health_bar1.config(maximum=e1.max_health, value=max(e1.health, 0))
        self.mana_bar1.config(maximum=e1.max_mana, value=e1.mana)
        self.stamina_bar1.config(maximum=e1.max_stamina, value=max(e1.stamina, 0))
        self.health_bar2.config(maximum=e2.max_health, value=max(e2.health, 0))
        self.mana_bar2.config(maximum=e2.max_mana, value=e2.mana)
        self.stamina_bar2.config(maximum=e2.max_stamina, value=max(e2.stamina, 0))
    
    def update_chart(self, turns, health1, health2):
        self.line1.set_data(turns, health1)
        self.line2.set_data(turns, health2)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
    
    def next_turn(self):
        self.simulation.next_turn()
        if self.simulation.simulation_over:
            self.btn_next.config(state=tk.DISABLED)
            self.btn_run.config(state=tk.DISABLED)
    
    def run_simulation(self):
        self.running = True
        self.auto_run()
    
    def auto_run(self):
        if self.running and not self.simulation.simulation_over:
            self.next_turn()
            delay = int(self.speed_var.get())
            self.root.after(delay, self.auto_run)
    
    def pause_simulation(self):
        self.running = False
    
    def reset_simulation(self):
        self.log_area.delete("1.0", tk.END)
        self.simulation = WarSimulation(self)
        self.update_stats(self.simulation.entity1, self.simulation.entity2, 0)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_run.config(state=tk.NORMAL)
        self.cosmic_label.config(text="Cosmic Event: None", fg="black")
        self.running = False
        self.ax.clear()
        self.ax.set_title("Health Trends")
        self.ax.set_xlabel("Turn")
        self.ax.set_ylabel("Health")
        self.line1, = self.ax.plot([], [], label="Entity1", color="red")
        self.line2, = self.ax.plot([], [], label="Entity2", color="green")
        self.ax.legend()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = WarGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
