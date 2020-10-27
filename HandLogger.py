import re


class Table():
    def __init__(self) -> None:
        pass
    pass


class Hand():
    def __init__(self) -> None:
        pass
    pass


class Player():
    def __init__(self, info: str) -> None:
        self.name = self.Name(info)
        self.stack = self.Stack(info)
        self.seat = self.Seat(info)

    def Name(self, info: str) -> str:
        return info.split()[2]

    def Stack(self, info: str) -> float:
        return float(info.split()[3][2:])

    def Seat(self, info: str) -> str:
        return info.split()[1][:-1]


class TextHandle():
    def __init__(self, text: str) -> None:
        self.text = text

    def findTable(self):
        compiler = re.compile(r'^Table \'[\w\s]+\'', flags=re.MULTILINE)
        return re.search(compiler, self.text).group()

    def findHandId(self):
        compiler = re.compile(r'#[\d]+', flags=re.MULTILINE)
        return re.search(compiler, self.text).group()

    def findDateTime(self):
        compiler = re.compile(r'\d{4}/\d{2}/\d{2}.+$', flags=re.MULTILINE)
        return re.search(compiler, self.text).group()

    def finBlinds(self):
        compiler = re.compile(r'[$£]\d+\.\d+/[$£]\d+\.\d+', flags=re.MULTILINE)
        return re.search(compiler, self.text).group()

    def findButton(self):
        compiler = re.compile(r'(?=#4).+button$', flags=re.MULTILINE)
        return re.search(compiler, self.text).group()[1:2]

    def findPlayers(self):
        compiler = re.compile(r'(^Seat \d.+chips\)$)', flags=re.MULTILINE)
        players = re.finditer(compiler, self.text)
        return [player.group() for player in players]


with open("hand-samples\\Aaltje II-0.50-1-USD-NoLimitHoldem"
          "-PokerStars-8-6-2017.txt") as file:
    tableLog = file.read().strip().split("\n\n")
