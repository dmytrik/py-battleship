class VisibilityError(Exception):
    def __init__(self) -> None:
        self.message = "The ship isn't field's area"
        super().__init__(self.message)

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
        self.ships = {coords: Ship(coords[0], coords[1]) for coords in ships}
        self.field = [
            (i, j)
            for i in range(10)
            for j in range(10)
        ]
        self._validate_field()
    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        current_ship = None

        for ship in self.ships.values():
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

    def print_field(self) -> None:
        decks = []
        for ship in self.ships.values():
            if ship.is_drowned:
                for deck in ship.decks:
                    deck.symbol = "x"
                    decks.append(deck)
            else:
                for deck in ship.decks:
                    if deck.is_alive:
                        deck.symbol = "\u25A1"
                    if not deck.is_alive:
                        deck.symbol = "*"
                    decks.append(deck)
        symbols_list = []
        is_found = False
        for row, column in self.field:
            for index, deck in enumerate(decks):
                if deck.row == row and deck.column == column:
                    symbols_list.append(deck.symbol)
                    is_found = True
                    break
                if index == len(decks) - 1:
                    is_found = False

            if not is_found:
                symbols_list.append("~")

        symbols = ""
        for index, symbol in enumerate(symbols_list):
            if index % 10 == 0 and index != 0:
                symbols += "\n"
            symbols += f"{symbol}   "

        print(symbols)

    def _validate_field(self) -> None:
        coords = self.ships.keys()

        for x, y in coords:
            condition = (0 <= x[0] < 10 and
                         0 <= x[1] < 10 and
                         0 <= y[0] < 10 and
                         0 <= y[1] < 10)
            if not condition:
                raise VisibilityError

        assert len(coords) == 10, "The total number of the ships should be 10"
        one_decks = 0
        two_decks = 0
        three_decks = 0
        four_decks = 0
        ships = [ship.decks for ship in self.ships.values()]
        for ship in ships:
            if len(ship) == 2:
                if (ship[0].row == ship[1].row and
                        ship[0].column == ship[1].column):
                    one_decks += 1
                    continue
                two_decks += 1
            if len(ship) == 3:
                three_decks += 1
            if len(ship) == 4:
                four_decks += 1
        assert one_decks == 4, "There should be 4 single-deck ships"
        assert two_decks == 3, "There should be 3 double-deck ships"
        assert three_decks == 2, "There should be 2 three-deck ships"
        assert four_decks == 1, "There should be 1 four-deck ship"
        invalid_cells = []
        for coord in coords:
            cells = self.get_invalid_cells_for_one_ship(coord)
            invalid_cells += cells



    def get_invalid_cells_for_one_ship(
            self,
            coord: tuple
    ) -> list[tuple]:
        row_range = (coord[0][0] - 1, coord[1][0] + 2)
        column_range = (coord[0][1] - 1, coord[1][1] + 2)

        start_row, end_row = row_range
        start_column, end_column = column_range

        current_ship = self.ships[coord]
        print(current_ship)

        result = []

        for i in range(start_row, end_row):
            for j in range(start_column, end_column):
                result.append((i, j),)

        return result

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


print(battle_ship.fire((0, 2)))
print(battle_ship.fire((0, 1)))
print(battle_ship.fire((0, 0)))

battle_ship.print_field()