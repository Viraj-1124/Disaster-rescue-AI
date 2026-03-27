# logic/knowledge_base.py

class KnowledgeBase:
    def __init__(self):
        self.victims = []
        self.ambulances = []

    def add_victims(self, victims):
        self.victims = victims

    def add_ambulances(self, ambulances):
        self.ambulances = ambulances

    def get_state(self):
        return {
            "victims": self.victims,
            "ambulances": self.ambulances
        }