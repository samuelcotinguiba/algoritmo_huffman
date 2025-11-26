class Node:
    def __init__(self, char, freq):
        self.char = char       # caractere ou None
        self.freq = freq       # frequência
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"Node(char={self.char!r}, freq={self.freq})"
