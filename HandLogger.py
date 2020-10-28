import re


class TextHandle:
    @staticmethod
    def findTable(text) -> str:
        compiler = re.compile(r'^Table \'[\w\s]+\'', flags=re.MULTILINE)
        return re.search(compiler, text).group()

    @staticmethod
    def findHandId(text) -> str:
        compiler = re.compile(r'#[\d]+', flags=re.MULTILINE)
        return re.search(compiler, text).group()

    @staticmethod
    def findDateTime(text) -> str:
        compiler = re.compile(r'\d{4}/\d{2}/\d{2}.+$', flags=re.MULTILINE)
        return re.search(compiler, text).group()

    @staticmethod
    def findBlinds(text) -> str:
        compiler = re.compile(r'[$£]\d+\.\d+/[$£]\d+\.\d+', flags=re.MULTILINE)
        return re.search(compiler, text).group()

    @staticmethod
    def findButton(text) -> str:
        compiler = re.compile(r'(?=#4).+button$', flags=re.MULTILINE)
        return re.search(compiler, text).group()[1:2]

    @staticmethod
    def findPlayers(text) -> list:
        compiler = re.compile(r'(^Seat \d.+chips\)$)', flags=re.MULTILINE)
        players = re.finditer(compiler, text)
        return [player.group() for player in players]

    @staticmethod
    def foldedBeforeFlop(text, name: str) -> bool:
        compiler = re.compile(rf'{name}.+(?=folded before Flop)')
        if re.search(compiler, text):
            return True
        return False


class Table:
    def __init__(self) -> None:
        self.hands = []


class Hand:
    def __init__(self) -> None:
        self.players = []
        self.flop = False
        self.turn = False
        self.river = False
        self.showdown = False

    def hasRound(self, n_rounds):
        if n_rounds == 5:
            self.flop = True
            self.turn = True
            self.river = True
            self.showdown = True
        elif n_rounds == 4:
            self.flop = True
            self.turn = True
            self.river = True
        elif n_rounds == 3:
            self.flop = True
            self.turn = True
        elif n_rounds == 2:
            self.flop = True


class Player:
    def __init__(self, info: str) -> None:
        self.name = self.Name(info)
        self.stack = self.Stack(info)
        self.seat = self.Seat(info)
        self.flop = False
        self.turn = False
        self.river = False
        self.showdown = False

    def stayedInGame(self, rounds: list, n_rounds):
        count = 0
        token = " ".join(rounds[1::2]).splitlines()
        if n_rounds == 1:
            return
        else:
            for i in token:
                if i.find(self.name+':') > -1:
                    count += 1
        if count == 5:
            self.flop = True
            self.turn = True
            self.river = True
            self.showdown = True
        elif count == 4:
            self.flop = True
            self.turn = True
            self.river = True
        elif count == 3:
            self.flop = True
            self.turn = True
        elif count == 2:
            self.flop = True

    @staticmethod
    def Name(info: str) -> str:
        compiler = re.compile(r'(?<=: ).+(?= \()')
        return re.search(compiler, info).group()

    @staticmethod
    def Stack(info: str) -> float:
        compiler = re.compile(r'(?<=[$£])[\d.]+')
        return float(re.search(compiler, info).group())

    @staticmethod
    def Seat(info: str) -> int:
        compiler = re.compile(r'(?<=Seat )\d+')
        return int(re.search(compiler, info).group())

    def __str__(self):
        return f"{self.name}, {self.stack}, {self.seat}"


with open("hand-samples\\Aaltje II-0.50-1-USD-NoLimitHoldem"
          "-PokerStars-8-6-2017.txt") as file:
    tableLog = file.read().strip().split("\n\n")

table = Table()
table.name = TextHandle.findTable(tableLog[0])

for info in tableLog:
    rodadas = info.split('***')[1: -2]
    numRodadas = int(len(rodadas) / 2)
    players = TextHandle.findPlayers(info)
    hand = Hand()
    hand.id = TextHandle.findHandId(info)
    hand.blind = TextHandle.findBlinds(info)
    hand.date = TextHandle.findDateTime(info)
    hand.hasRound(numRodadas)
    for pl in players:
        player = Player(pl)
        player.stayedInGame(rodadas, numRodadas)
        player.foldBeforeFlop = TextHandle.foldedBeforeFlop(info, player.name)
        hand.players.append(player)
    table.hands.append(hand)

f = open(f"{table.name}.txt", 'a')
for hand in table.hands:
    f.write(f"Hand ID: {hand.id[1:]}\n")
    f.write(f"The Blinds: {hand.blind}\n")
    f.write(f"Date and Time: {hand.date}\n")
    f.write("Players names, stacks and seats:\n")
    for player in hand.players:
        f.write(f"\t- {player}\n")
    f.write("Players that folded preflop (if any)\n")
    for player in hand.players:
        if player.foldBeforeFlop:
            f.write(f"\t- {player.name}\n")
    if (hand.flop):
        f.write("Players that played the flop (if any)\n")
        for player in hand.players:
            if player.flop:
                f.write(f"\t- {player.name}\n")
    if (hand.turn):
        f.write("Players that played the turn (if any)\n")
        for player in hand.players:
            if player.turn:
                f.write(f"\t- {player.name}\n")
    if (hand.river):
        f.write("Players that played the river (if any)\n")
        for player in hand.players:
            if player.river:
                f.write(f"\t- {player.name}\n")
    if (hand.showdown):
        f.write("Players that played the showdown (if any)\n")
        for player in hand.players:
            if player.showdown:
                f.write(f"\t- {player.name}\n")
    f.write("\n")
f.close()
