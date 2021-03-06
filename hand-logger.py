import re


class Hand:
    def __init__(self, log: list[str]):
        self.log = log
        self.ID()
        self.blinds()
        self.dateTime()
        self.buttonPlace()
        self.players = []

    def ID(self):
        self.id = self.log[0][self.log[0].find('#'): self.log[0].find(':')]

    def blinds(self):
        blinds, self.country = self.log[0][self.log[0].find(
            '(') + 1: self.log[0].find(")")].split()
        self.small, self.big = blinds.split('/')

    def dateTime(self):
        self.date = self.log[0][self.log[0].find('-') + 2:]

    def buttonPlace(self):
        self.button = int(re.search(r'[#][\d]+', self.log[1]).group()[1:])

    def findPlayersOnHand(self):
        i = 2
        while self.log[i][:4] == "Seat":
            self.players.append(Player(self.log[i]))
            i += 1

    def __str__(self):
        return f'Hand ID: {self.id}\n' \
               f'The Blinds: {self.small}/{self.big}\n' \
               f'Date and Time: {self.date}\n'


class Player():
    def __init__(self, info: str) -> None:
        self.info = info
        self.playerName()
        self.playerSeat()
        self.playerStack()

    def playerSeat(self):
        self.seat = int(self.info[5: self.info.find(':')])

    def playerName(self):
        self.name = self.info[self.info.find(':') + 2: self.info.find('(') - 1]

    def playerStack(self):
        self.stack = float(re.search(r'[$][\d.]+', self.info).group()[1:])

    def __str__(self):
        return f'\t- {self.name}, {self.stack}, {self.seat}\n'


def openAndSplitFile(filePath: str) -> list:
    with open(filePath) as file:
        return file.read().strip().split("\n\n")


def splitIntoLines(text: str) -> list:
    return [line.strip() for line in text.strip().splitlines()]


filePath = "hand-samples\\Aaltje II-0.50-1-USD-NoLimitHoldem" \
           "-PokerStars-8-6-2017.txt"
table = []
handsData = openAndSplitFile(filePath)
for handLog in handsData:
    logByLine = splitIntoLines(handLog)
    hand = Hand(logByLine)
    hand.findPlayersOnHand()
    table.append(hand)

f = open('hand-logs\\sampleLog.txt', 'w')
for ihand in table:
    f.write(f'{ihand}')
    f.write('Players names, stacks, seats\n')
    for player in ihand.players:
        f.write(f'{player}')
    f.write('\n')
f.close()
