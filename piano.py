from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QLabel, QHBoxLayout
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractButton

import time, random


from pianoButton import *
from pianoQuiz import Quiz




class NoteButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, color = 0, parent = None):
        super(NoteButton, self).__init__(parent)

        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)
        self.color = color

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed


        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(40, 80) if self.color == 0 else QSize(20, 50)



class Piano(QWidget):

    def __init__(self):
        super().__init__()

        main = QGridLayout()
        pianoLayout = QGridLayout()
        pianoLayout.setSpacing(0)

        self.dol = QLabel()
        self.dol.setPixmap(QPixmap('./image/dol.png'))
        self.dol.show()

        self.statusLb = QLabel()
        self.dolExplainLb = QLabel()
        self.oxcheckLine = QLineEdit()
        self.oxcheckLine.setReadOnly(True)
        self.inputNote = QLineEdit()
        self.inputNote.setReadOnly(True)

        i = 0
        for note in white:
            button = NoteButton(QPixmap("./image/pianoWhite.png"), QPixmap("./image/pianoWhite.png"),
                                QPixmap("./image/pianoWhiteClicked.png"))
            button.setText(note)
            button.clicked.connect(self.noteClicked)

            pianoLayout.addWidget(button, 2, i, 1, 2, alignment=Qt.AlignLeft)
            i += 2

        i = 1
        for note in black:
            button = NoteButton(QPixmap("./image/pianoBlack.png"), QPixmap("./image/pianoBlack.png"),
                                QPixmap("./image/pianoBlack.png"), 1)
            button.setText(note)
            button.clicked.connect(self.noteClicked)
            if i == 5: i += 2
            pianoLayout.addWidget(button, 2, i, 1, 2,
                                  alignment=Qt.AlignCenter | Qt.AlignTop)
            i += 2

        self.startbt = QToolButton()
        self.startbt.setText('start')
        self.startbt.clicked.connect(self.startClicked)

        self.submitbt = QToolButton()
        self.submitbt.setText('제출')
        self.submitbt.clicked.connect(self.submitClicked)

        self.removebt = QToolButton()
        self.removebt.setText('지우기')
        self.removebt.clicked.connect(self.removeClicked)

        self.relistenbt = QToolButton()
        self.relistenbt.setText('다시 듣기')
        self.relistenbt.clicked.connect(self.relistenClicked)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.startbt)
        buttonLayout.addWidget(self.submitbt)
        buttonLayout.addWidget(self.removebt)
        buttonLayout.addWidget(self.relistenbt)
        buttonLayout.setAlignment(Qt.AlignLeft)


        main.addWidget(self.dol, 0, 0)
        main.addWidget(self.dolExplainLb, 1, 0, 1, 2)
        main.addWidget(self.oxcheckLine, 2, 0, 1, 2)
        main.addLayout(pianoLayout, 3, 0, 1, 8)
        main.addWidget(self.inputNote, 4, 0, 1, 1)
        main.addLayout(buttonLayout, 5, 0)
        main.addWidget(self.statusLb, 7, 0, 1, 2)



        self.setWindowTitle('노래하는 돌멩이')
        self.setMaximumSize(400, 400)
        # self.setFixedSize(340, 320)

        self.setLayout(main)

        print(self.width())
        print(self.height())

        self.startGame()

    def startGame(self):
        self.dolStatus = 0
        self.quiz = Quiz()
        self.inputList = []
        self.isGameStart = False
        self.removebt.setEnabled(False)
        self.statusLb.setText(f"{self.quiz.getLevel()}단계, {self.quiz.getNumber()}개의 노트")
        self.relistenbt.setEnabled(False)



    def noteClicked(self):
        button = self.sender()
        key = button.text()

        self.playNote(key)
        self.inputNoteEvent(key)

        # if self.isGameStart and len(self.inputList) < self.quiz.getNumber():
        #     self.inputList.append(key.upper())
        #     self.inputNote.setText(' '.join(self.inputList))
        # if len(self.inputList) == len(self.quiz.getAnswerList()):
        #     self.submitbt.setEnabled(True)


    def startClicked(self):
        self.drawDol(1)
        self.dol.show()
        self.inputNote.setText('')
        self.inputList = []
        self.oxcheckLine.setText('')
        self.dolExplainLb.setText("돌멩이가 노래를 부르기 시작합니다.")
        self.quiz.makeQuiz()
        self.startbt.setEnabled(False)
        QtTest.QTest.qWait(1000)
        self.isGameStart = True
        self.dol.show()
        self.playMusic(self.quiz.getAnswerList())



    def submitClicked(self):
        self.inputList = self.inputNote.text().split()
        # if len(self.inputList) == 0:
        #     self.dolExplainLb.setText('하나라도 입력해주세요')
        resultText = self.quiz.checkAnswer(self.inputList)
        if self.quiz.getNumber() == 7:
            self.statusLb.setText(f"돌멩이가 특별한 음악을 준비하고 있습니다.")
        else:
            self.statusLb.setText(f"{self.quiz.getLevel()}단계, {self.quiz.getNumber()}개의 노트")
        self.oxcheckLine.setText(resultText)
        self.startbt.setEnabled(True)
        self.submitbt.setEnabled(False)
        self.removebt.setEnabled(False)



    def removeClicked(self):
        self.inputList = []
        self.inputNote.setText('')
        self.removebt.setEnabled(False)




    def keyPressEvent(self, e):
        if e.key() in pianoNote:
            self.playNote(pianoNote[e.key()])

            key = (pianoNote[e.key()])
            self.inputNoteEvent(key)


    def inputNoteEvent(self, key):
        if self.isGameStart and len(self.inputList) < self.quiz.getNumber():
            self.inputList.append(key.upper())
            self.inputNote.setText(' '.join(self.inputList))
        if len(self.inputList) == len(self.quiz.getAnswerList()):
            self.submitbt.setEnabled(True)
        if len(self.inputList) >= 1:
            self.removebt.setEnabled(True)



    def playMusic(self, keyList):

        for k in keyList:
            key = k.lower()
            if key in white:
                white[key].play()
            else:
                black[key].play()
            # time.sleep(1)
            if self.quiz.getSpeed == 3:
                QtTest.QTest.qWait(250)
            elif self.quiz.getSpeed() == 2:
                QtTest.QTest.qWait(500)
            else:
                QtTest.QTest.qWait(1000)
        self.drawDol(0)

        if random.randint(0, 2) == 2:
            QtTest.QTest.qWait(1000)
            self.drawDol(3)
            self.dolExplainLb.setText("노래를 마친 돌멩이가 감격의 눈물을 흘립니다.")
        else:
            QtTest.QTest.qWait(1000)
            self.dolExplainLb.setText("돌멩이가 아름다운 노래를 마칩니다.")


    def playNote(self, key):
        if key in white:
            white[key].play()
        else:
            black[key].play()


    def relistenClicked(self):

        self.dolExplainLb.setText("돌멩이가 당신을 위해 노래를 다시 들려줍니다.")
        self.drawDol(1)
        self.playMusic(self.quiz.getAnswerList())

    def drawDol(self, dolStatus):
        fileName =''
        if dolStatus == 1:
            movie = QMovie('./image/dol_singing.gif')
            self.dol.setMovie(movie)
            movie.start()
            return
        if dolStatus == 0:
            fileName = 'dol.png'
        # elif dolStatus == 1: #singing
        #     fileName = 'dol_1.png'
        # elif dolStatus == 2:
        #     fileName = 'dol_2.png'
        elif dolStatus == 3: #tear
            fileName = 'dol_3.png'
        fileName = "./image/" + fileName
        self.dol.setPixmap(QPixmap(fileName))




















if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    piano = Piano()
    piano.show()
    sys.exit(app.exec_())
