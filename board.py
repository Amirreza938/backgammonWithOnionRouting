class BackgammonBoard:
    def __init__(self):
        # Initialize the board with starting positions
        # Positive numbers represent white pieces, negative represent black
        self.board = [
            2, 0, 0, 0, 0, -5,  # 1-6
            0, -3, 0, 0, 0, 5,  # 7-12
            -5, 0, 0, 0, 3, 0,  # 13-18
            5, 0, 0, 0, 0, -2   # 19-24
        ]
        self.bar = [0, 0]  # [white, black]
        self.off = [0, 0]  # [white, black]
        
    def draw(self):
        """Draw the beautiful ASCII board"""
        print("\n" + "=" * 57)
        # Top numbers
        print("║", end=" ")
        for i in range(13, 19):
            print(f"{i:2}", end=" ")
        print("║BAR║", end=" ")
        for i in range(19, 25):
            print(f"{i:2}", end=" ")
        print("║")
        
        # Upper board
        for row in range(5):
            print("║", end=" ")
            # Print pieces for positions 13-18
            for pos in range(12, 18):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print("   ", end="")
            print("║", end="")
            # Bar area
            if abs(self.bar[0]) > row:
                print(" ○ ", end="")
            else:
                print("   ", end="")
            print("║", end=" ")
            # Print pieces for positions 19-24
            for pos in range(18, 24):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print("   ", end="")
            print("║")
        
        # Middle section
        print("║" + "═" * 17 + "║" + "═" * 3 + "║" + "═" * 17 + "║")
        print("║     WHITE (○) DIRECTION →    ║   ║                      ║")
        print("║" + "─" * 17 + "║" + "─" * 3 + "║" + "─" * 17 + "║")
        print("║     BLACK (●) DIRECTION →    ║   ║                      ║")
        print("║" + "═" * 17 + "║" + "═" * 3 + "║" + "═" * 17 + "║")
        
        # Lower board
        for row in range(5):
            print("║", end=" ")
            # Print pieces for positions 1-6
            for pos in range(0, 6):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print("   ", end="")
            print("║", end="")
            # Bar area
            if abs(self.bar[1]) > row:
                print(" ● ", end="")
            else:
                print("   ", end="")
            print("║", end=" ")
            # Print pieces for positions 7-12
            for pos in range(6, 12):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print("   ", end="")
            print("║")
        
        # Bottom numbers
        print("║", end=" ")
        for i in range(1, 7):
            print(f"{i:2}", end=" ")
        print("║BAR║", end=" ")
        for i in range(7, 13):
            print(f"{i:2}", end=" ")
        print("║")
        print("=" * 57)
        
        # Show pieces on bar and off the board
        print(f"Bar - White: {self.bar[0]} Black: {abs(self.bar[1])}")
        print(f"Off - White: {self.off[0]} Black: {self.off[1]}\n")