class Deck:
    def __init__(
            self,
            row: int,
            column,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return str(self.__dict__)


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row, column) -> Deck | None:
        # Find the corresponding deck in the list
        decks = self.decks
        for deck in decks:
            if deck.row == row and deck.column == column:
                self.fire(row, column)
                return deck
    def fire(self, row, column) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        decks = self.decks
        for deck in decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False
        decks_values = [deck.is_alive for deck in self.decks]
        if not any(decks_values):
            self.is_drowned = True

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list[Deck]:
        result = []
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                result.append(Deck(start[0], i))
        if start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                result.append(Deck(i, start[1]))
        return result

    def __repr__(self) -> str:
        return str(self.__dict__)

class Battleship:
    def __init__(self, ships):
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {coords: Ship(coords[0], coords[1]) for coords in ships}

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        current_ship = None

        for ship in self.field.values():
            if ship.is_drowned:
                continue
            deck = ship.get_deck(location[0], location[1])
            if deck:
                current_ship = ship

        if current_ship and not current_ship.is_drowned:
            return "Hit!"
        if current_ship and current_ship.is_drowned:
            return "Sunk!"
        return "Miss!"

    def __repr__(self) -> str:
        return str(self.__dict__)

battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)

print(battle_ship.fire((0, 3)))
print(battle_ship.fire((0, 2)))
print(battle_ship.fire((0, 1)))
print(battle_ship.fire((0, 0)))