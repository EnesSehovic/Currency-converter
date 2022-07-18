import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

c = os.getcwd()
os.chdir(c)

class CurrencyConvert(QDialog):
    def __init__(self):
        super(CurrencyConvert, self).__init__()
        loadUi("currencyConverter.ui", self)

        self.fromComboBox.addItem(self.onLoad())
        self.fromComboBox.setCurrentIndex(0)
        self.toComboBox.addItem(self.onLoad())
        self.toComboBox.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.pressed)
        self.buttonBox.rejected.connect(self.reject)

    def onLoad(self):
        import requests
        url = 'https://api.exchangerate.host/latest'
        res = requests.get(url)
        data = res.json()
        excRates = data['rates']
        keys = []
        for key in excRates.keys():
            keys.append(key)
        for k in range(len(keys)):
            self.fromComboBox.addItem(keys[k])
            self.toComboBox.addItem(keys[k])

    def pressed(self):
        self.errorLabel.setText('')
        self.convAmountLabel.setText('')
        import requests
        url = 'https://api.exchangerate.host/latest'
        res = requests.get(url)
        data = res.json()
        excRates = data['rates']
        currFrom = self.fromComboBox.currentText()
        currTo = self.toComboBox.currentText()
        amount = self.amountLineEdit.text()
        try:
            toEur = float(amount) / float(excRates[currFrom])
            toWanted = float(toEur) * float(excRates[currTo])
            self.convAmountLabel.setText(str(toWanted))
        except ValueError:
            self.errorLabel.setText('Enter only numbers')


app = QApplication(sys.argv)
mainScreen = CurrencyConvert()

window = CurrencyConvert()
window.setFixedHeight(540)
window.setFixedWidth(300)
window.show()


try:
    sys.exit(app.exec())
except:
    print('Exiting')
