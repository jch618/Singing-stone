import random

class Quiz:
    def __init__(self):
        self.noteList = ['C', 'D', 'E', 'F', 'G', 'A', 'B', '_C', 'C#', 'D#', 'F#', 'G#', 'A#']
        self.uniqueSongList = ['F', 'C#', 'D#', 'F#', 'G#', 'A#']
        self.answerList = []
        self.checkList = []
        self.number = 3
        self.level = 0
        self.uniqueSong = 0
        self.maxLevel = 2
        self.speed = 1

        ###
        self.makeQuiz()

        #13개


    def makeQuiz(self):
        self.answerList = []
        levelRange = [2, 7, 12]

        if self.uniqueSong == 1:
            self.uniqueSong = 0
            for _ in range(self.number):
                self.answerList.append(self.uniqueSongList[random.randint(0, 5)])

        else:
            for _ in range(self.number):
                self.answerList.append(self.noteList[random.randint(0, levelRange[self.level])])


    def checkAnswer(self, inputList):
        self.checkList = []
        for i in range(len(inputList)):
            if inputList[i] == self.answerList[i]:
                self.checkList.append('O')
            else:
                self.checkList.append('X')
        resultText = ' '.join(self.checkList)

        if self.checkList.count('O') >= len(inputList) - 1:
            self.levelUpgrade()

        self.ArgumentSettings()



        return resultText

    def getLevel(self):
        return self.level

    def getNumber(self):
        return self.number

    def getAnswerList(self):
        return self.answerList

    def getSpeed(self):
        return self.speed

    def levelUpgrade(self):
        self.speed = 1
        if self.level < self.maxLevel:
            self.level += 1


    def ArgumentSettings(self):
        if self.level >= 1:
            if random.randint(1, 3) == 3:
                self.speed = random.randint(2, 3)
            if random.randint(1, 4) == 4:
                self.uniqueSong = 1
                self.number = 7
            else:
                self.number = random.randint(3, 5)
                self.speed = random.randint(1, 3)

