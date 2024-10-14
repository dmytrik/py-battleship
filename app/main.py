class VisibilityError(Exception):
    def __init__(self) -> None:
        self.message = "The ship isn't field's area"
        super().__init__(self.message)


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
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

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        decks = self.decks
        for deck in decks:
            if deck.row == row and deck.column == column:
                self.fire(row, column)
                return deck

    def fire(self, row: int, column: int) -> None:
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
        if start == end:
            result.append(Deck(start[0], start[1]))
            return result
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
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = {coords: Ship(coords[0], coords[1]) for coords in ships}
        self.field = [
            (row, column)
            for row in range(10)
            for column in range(10)
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

        for x_, y_ in coords:
            condition = (0 <= x_[0] < 10
                         and 0 <= x_[1] < 10
                         and 0 <= y_[0] < 10
                         and 0 <= y_[1] < 10)
            if not condition:
                raise VisibilityError

        assert len(coords) == 10, "The total number of the ships should be 10"
        one_decks = 0
        two_decks = 0
        three_decks = 0
        four_decks = 0
        ships = [ship.decks for ship in self.ships.values()]

        for ship in ships:
            if len(ship) == 1:
                one_decks += 1
            if len(ship) == 2:
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
            cells = self._get_invalid_cells_for_one_ship(coord)
            invalid_cells += cells

        invalid_cells = set(invalid_cells)
        decks = sum([ship.decks for ship in self.ships.values()], [])
        for cell in invalid_cells:
            for deck in decks:
                if cell[0] == deck.row and cell[1] == deck.column:
                    raise Exception("ships shouldn't be located in"
                                    " the neighboring cells"
                                    " (even if cells are neighbors"
                                    " by diagonal)")

    def _get_invalid_cells_for_one_ship(
            self,
            coord: tuple
    ) -> list[tuple]:
        row_range = (coord[0][0] - 1, coord[1][0] + 2)
        column_range = (coord[0][1] - 1, coord[1][1] + 2)

        start_row, end_row = row_range
        start_column, end_column = column_range

        current_ship = self.ships[coord].decks

        area_cells = []

        for row in range(start_row, end_row):
            for column in range(start_column, end_column):
                area_cells.append((row, column))

        for deck in current_ship:
            for cell in area_cells:
                if cell[0] == deck.row and cell[1] == deck.column:
                    area_cells.remove(cell)

        return area_cells

    def __repr__(self) -> str:
        return str(self.__dict__)
