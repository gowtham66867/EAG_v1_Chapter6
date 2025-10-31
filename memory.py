class Memory:
    def __init__(self):
        self.history = []

    def add_entry(self, entry: str):
        """Adds a new entry to the memory log."""
        self.history.append(entry)

    def get_history_str(self) -> str:
        """Returns the entire memory log as a formatted string."""
        return "\n".join(self.history)
