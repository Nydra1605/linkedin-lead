"""Finite‑State‑Machine to track lead progress."""
from transitions import Machine

states = ["NEW", "TOUCHED", "REPLIED", "QUALIFIED", "DISQUALIFIED"]

class LeadFSM(Machine):
    def __init__(self, initial="NEW"):
        super().__init__(states=states, initial=initial)
        self.add_transition("touch", "NEW", "TOUCHED")
        self.add_transition("reply", "TOUCHED", "REPLIED")
        self.add_transition("qualify", ["TOUCHED", "REPLIED"], "QUALIFIED")
        self.add_transition("disqualify", "*", "DISQUALIFIED")