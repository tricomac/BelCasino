from PyQt5 import QtWidgets, QtCore, QtGui
from random import randint
import pandas as pd
from numpy import savetxt
import sys
import os


class CasinoWindow(QtWidgets.QMainWindow):
    def __init__(self, other, user, i):
        super().__init__()
        self.other = other
        self.user = user
        self.i = i
        self.money = user[3]
        if self.money <= 0:
            self.loser()
        self.setFixedSize(595, 500)
        self.fields = ["1 to 18", "RED", "BLACK", "19 to 36"]
        self.field_nums = {"1 to 18": set(), "RED": set(), "BLACK": set(), "19 to 36": set()}
        self.selected_numbers = dict()
        self.selected_regions = dict()
        self.rows = [set(), set(), set()]
        self.columns = [set(), set(), set()]

        self.setWindowTitle("БелКазино")
        self.setStyleSheet(
            "background-color: rgb(0,120,0);"
        )

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.move(0, 240)
        self.label_1.setText("Делайте ставки!")
        self.label_1.setStyleSheet(
            "color: rgb(0,0,0);font:18pt \"Arial\";color:rgb(255,255,255);"
        )
        self.label_1.adjustSize()

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.move(0, 280)
        self.label_2.setText("")
        self.label_2.setStyleSheet(
            "color: rgb(0,0,0);font:18pt \"Arial\";color:rgb(255,255,255);"
        )

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.move(0, 320)
        self.label_3.setText("Ставка:")
        self.label_3.setStyleSheet(
            "color: rgb(0,0,0);font:16pt \"Arial\";color:rgb(255,255,255);"
        )

        self.label_result = QtWidgets.QLabel(self)
        self.label_result.setText("")
        self.label_result.move(0, 400)
        self.label_result.setStyleSheet(
            "color: rgb(0,0,0);font:18pt \"Arial\";color:rgb(255,255,255);"
        )

        self.bet = QtWidgets.QSpinBox(self)
        self.bet.setGeometry(90, 320, 75, 35)
        self.bet.setStyleSheet(
            "font:18pt \"Arial\";background-color:rgb(255,255,255);color:rgb(0,0,0);"
        )
        self.bet.setRange(0, self.money)

        for i in range(4):
            crisp = QtWidgets.QPushButton(self)
            crisp.setGeometry(2 + 43 * i, 365, 35, 35)
            crisp.setText(str(5 ** i))
            crisp.setStyleSheet(
                "font:16pt \"Arial\";background-color:"
                + "rgb("+str(i * 255 % 256)+','+str(i * 100 // 4)+','+str((i ** 4 + 100) % 256)+");" +
                ";color:rgb(255,255,255);"
            )
            crisp.clicked.connect(lambda f, crisp=5**i: self.clickCrisp(crisp))
        #######

        for i in range(36):
            button = QtWidgets.QPushButton(self)
            button.setGeometry(80 + 40 * (i % 12), 40 * (i // 12) + 2, 40, 40)
            self.columns[(i % 12) // 4].add(i + 1)
            self.rows[i // 12].add(i + 1)
            button.setText(str(i + 1))
            back_color = "background-color:"
            if i < 18:
                self.field_nums["1 to 18"].add(i + 1)
            elif i >= 18:
                self.field_nums["19 to 36"].add(i + 1)
            if i % 2 == 0:
                back_color += "rgb(200,0,0);"
                self.field_nums["RED"].add(i + 1)
            else:
                back_color += "rgb(0,0,0);"
                self.field_nums["BLACK"].add(i + 1)
            button.setStyleSheet(
                back_color + "color: rgb(255,255,255);font:18pt \"Arial\";"
            )
            button.clicked.connect(lambda f, num=int(button.text()): self.clickNumber(num))

            if i // 12 == i / 12:
                row_button = QtWidgets.QPushButton(self)
                row_button.setGeometry(0, 40 * (i // 12) + 2, 80, 40)
                row_button.setStyleSheet(
                    "color: rgb(255,255,255);font:18pt \"Arial\";"
                )
                row_button.setText("2 to 1")

                row_button.clicked.connect(lambda f, region=str((i // 12) + 1) + "st 2 to 1": self.clickRegion(region))

            if (i % 12) // 4 == (i % 12) // 4:
                column_button = QtWidgets.QPushButton(self)
                column_button.setGeometry(80 + ((i % 12) // 4) * 40 * 4, 40 * 3 + 1, 4 * 40, 40)
                column_button.setStyleSheet(
                    "color: rgb(255,255,255);font:18pt \"Arial\";"
                )
                column_button.setText(f"{(i % 12) // 4 + 1}st 12")
                column_button.clicked.connect(
                    lambda f, region=str((i % 12) // 4 + 1) + "st 12": self.clickRegion(region)
                )

        # 0
        button = QtWidgets.QPushButton(self)
        button.setGeometry(12 * 40 + 80, 2, 35, 40 * 3)
        button.setText(str(0))
        button.setStyleSheet(
            "color: rgb(255,255,255);font:18pt \"Arial\";"
        )
        button.clicked.connect(lambda f, num=int(button.text()): self.clickNumber(num))

        # X
        button = QtWidgets.QPushButton(self)
        button.setGeometry(180, 320, 35, 35)
        button.setStyleSheet(
            "color: rgb(200,0,0);font:18pt \"Arial\";"
        )
        button.setText('X')
        button.clicked.connect(lambda f, num=-1: self.clickNumber(num))

        self.label_money = QtWidgets.QLabel(self)
        self.label_money.setText(str(self.money))
        self.label_money.setStyleSheet(
            "color: rgb(255,255,255); font:18pt \"Arial\";"
        )
        self.label_money.setGeometry(220, 320, 35, 35)
        self.label_money.adjustSize()

        # red ...
        buttons = self.fields
        for i in range(len(buttons)):
            button = QtWidgets.QPushButton(self)
            button.setGeometry(80 + 120 * i, 40 * 4 + 1, 120, 40)
            if buttons[i] == "RED" or buttons[i] == "BLACK":
                button.setStyleSheet(
                    f"color: rgb(255, 255, 255);background-color: {buttons[i].lower()};font:14pt \"Arial\";"
                )
            else:
                button.setStyleSheet(
                    "color: rgb(255, 255, 255);font:14pt \"Arial\";"
                )
            button.setText(buttons[i])
            button.clicked.connect(lambda f, field=buttons[i]: self.clickRegion(field))
        #######
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10000, self)
        self.fps = QtCore.QBasicTimer()
        self.fps.start(1000, self)
        self.secs = 10
        self.show()

    def clickNumber(self, number: int):
        if number == -1:
            self.selected_numbers = dict()
            self.clickRegion("None")
            self.label_1.setText("Делайте ставки!")
        elif number >= 0 and self.bet.value() > 0:
            self.money -= self.bet.value()
            self.label_1.setText("Выбранные числа: ")
            self.selected_numbers[number] = self.bet.value()
            for i in self.selected_numbers.keys():
                self.label_1.setText(self.label_1.text() + str(i) + ": " + str(self.selected_numbers[i]) + ";   ")
        self.clickCrisp(-5000)
        self.label_1.adjustSize()
        return True

    def clickRegion(self, region: str):
        self.label_2.setText("")
        if region == "None":
            self.selected_regions = dict()
        elif self.bet.value() > 0:
            self.money -= self.bet.value()
            self.selected_regions[region] = self.bet.value()
            for i in self.selected_regions.keys():
                self.label_2.setText(self.label_2.text() + str(i) + ": " + str(self.selected_regions[i]) + ";   ")
        self.label_2.adjustSize()
        self.clickCrisp(-5000)
        return True

    def clickCrisp(self, crisp: int):
        self.bet.setValue(self.bet.value() + crisp)

    def loser(self):
        w = QtWidgets.QMessageBox()
        w.setText("Вы проигрались!")
        w.setStyleSheet("font:18pt \"Arial\";background-color:rgb(255,0,0);color:rgb(255,255,255);")
        del self.timer
        del self.fps
        sys.exit(w.exec_())

    def timerEvent(self, a0) -> None:
        if self.fps.timerId() == a0.timerId():
            if self.secs <= 10:
                self.label_result.setText("У Вас "+str(self.secs - 1)+" секунд до прокрута рулетки!")
                self.label_result.adjustSize()
            self.secs -= 1
        else:
            self.secs = 10
            self.play()

    def play(self):
        win = int()
        num = randint(0, 36)
        for i in self.selected_numbers.keys():
            if i == num:
                win += int(self.selected_numbers[num] * 37)
        else:
            for region in self.selected_regions.keys():
                if region in self.fields:
                    if num in self.field_nums[region]:
                        win += (self.selected_regions[region] * 2)
                elif region[1:] == "st 2 to 1":
                    if num in self.rows[int(region[0]) - 1]:
                        win += (self.selected_regions[region] * 3)
                elif region[1:] == "st 12":
                    if num in self.columns[int(region[0]) - 1]:
                        win += (self.selected_regions[region] * 3)

        self.label_result.setText(
            "Выиграло число " + str(num) + ". Ваш выигрыш: " + str(win)
        )
        self.clickNumber(-1)
        self.label_result.adjustSize()
        self.money += win

        self.user.iloc[3] = self.money
        self.other.users.iloc[self.i, :] = self.user
        self.other.users.to_csv(os.path.join(os.getcwd(), "users.csv"), index=False)

        self.label_money.setText(str(self.money))
        self.label_money.adjustSize()
        if not self.money > 0:
            self.loser()
        self.bet.setRange(0, self.money)
        self.secs = 15
        self.fps.start(1000, self)
        self.timer.start(self.secs * 1000, self)
        self.update()

    def closeEvent(self, a0) -> None:
        sys.exit()


class AuthorisationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setStyleSheet("background-color:rgb(0,180,180);")
        self.setFixedSize(700, 500)

        self.button_login = QtWidgets.QPushButton(self)
        my_style = "background-color:rgb(255,255,255);font:18pt \"Arial\";color:rgb(0,0,0);"
        self.button_login.setStyleSheet(my_style)
        self.button_login.setGeometry(300, 400, 100, 50)
        self.button_login.setText("Вход")
        self.button_login.clicked.connect(lambda f: self.button_login_click())

        self.line_login = QtWidgets.QLineEdit(self)
        self.line_login.setStyleSheet(my_style)
        self.line_login.setGeometry(325, 125, 250, 50)

        self.line_password = QtWidgets.QLineEdit(self)
        self.line_password.setStyleSheet(my_style)
        self.line_password.setGeometry(325, 205, 250, 50)
        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)

        label = QtWidgets.QLabel(self)
        label.setStyleSheet("font:24pt \"Arial\";")
        label.setGeometry(155, 125, 250, 50)
        label.setText("Логин:")
        label.adjustSize()

        label = QtWidgets.QLabel(self)
        label.setStyleSheet("font:24pt \"Arial\";")
        label.setGeometry(155, 205, 250, 50)
        label.setText("Пароль:")
        label.adjustSize()

        self.users = pd.read_csv(os.path.join(os.getcwd(), "users.csv"), sep=r',|;')
        self.users.reset_index(drop=True, inplace=True)
        self.show()

    def error(self, description):
        error_window = QtWidgets.QMessageBox(self)
        error_window.setText(description)
        error_window.setStyleSheet("font:18pt \"Arial\";background-color:rgb(255,0,0);color:rgb(255,255,255);")
        error_window.show()

    def button_login_click(self):
        login = self.line_login.text()
        password = self.line_password.text()
        try:
            j = self.users.columns.get_loc("Пароль")
            i = self.users.index[self.users["Логин"] == login].tolist()[0]
            assert self.users.iloc[i, j] == password
            user = self.users.iloc[i, :]
            self.destroy()
            self = CasinoWindow(self, user, i)
        except IndexError:
            self.error("Ошибка логина")
        except AssertionError:
            self.error("Ошибка пароля")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AuthorisationWindow()
    sys.exit(app.exec_())
