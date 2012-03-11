#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore
from mainUI import Ui_MainWindow
from aboutUI import Ui_About
from sender import Sender

version = 0.7

class GUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.addCarriers()
        
        self.thread = Sender()
        
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.showAbout)
        self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), exit)
        self.connect(self.ui.button, QtCore.SIGNAL('clicked()'), self.toggle)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.done)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.done)
        self.connect(self.thread, QtCore.SIGNAL("plusOne()"), self.plusOne)
        self.connect(self.thread, QtCore.SIGNAL("sendingError()"), self.stop)

        self.ui.server.setText('127.0.0.1:25') #set default
        self.ui.message.setPlainText('SPAM!')
        self.ui.statusBar().showMessage('Ready') #broken
        
    
    def toggle(self):
        self.state = self.ui.button.text()
        if self.state == 'Start':
            self.start()
        if self.state == 'Stop':
            self.stop()
            
    def stop(self):
        self.thread.terminate()
        print('stoping')
        self.done()
        
    def done(self):
        self.ui.button.setText('Start')
        self.ui.phone.setEnabled(True)
        self.ui.provider.setEnabled(True)
        self.ui.server.setEnabled(True)
        self.ui.tls.setEnabled(True)
        self.ui.user.setEnabled(True)
        self.ui.password.setEnabled(True)
        self.ui.message.setEnabled(True)
        
    def start(self):
        if self.ui.phone.text() != '' and self.thread.connect(
                            self.ui.server.text(),
                            self.ui.user.text(), 
                            self.ui.password.text(),
                            self.ui.tls.isChecked()
                              ):
            self.ui.button.setText('Stop')
            self.ui.phone.setEnabled(False)
            self.ui.provider.setEnabled(False)
            self.ui.server.setEnabled(False)
            self.ui.tls.setEnabled(False)
            self.ui.user.setEnabled(False)
            self.ui.password.setEnabled(False)
            self.ui.message.setEnabled(False)
            self.ui.lcd.display('0')
            
            print('starting')
            
            
            self.thread.toaddr = self.ui.phone.text() + self.providers[self.ui.provider.currentText()]
            self.thread.msg = self.ui.message.toPlainText()
            
            print('sending to:', self.thread.toaddr)
            
        
        
    def plusOne(self):
        self.ui.lcd.display(str(self.ui.lcd.intValue() + 1))

    def showAbout(self):
        self.about = QtGui.QWidget()
        ui = Ui_About()
        ui.setupUi(self.about)
        ui.Version.setText(str(version))
        self.connect(ui.pushButton, QtCore.SIGNAL('clicked()'),self.about.close)
        self.about.show()
    
    def addCarriers(self):
        '''can get more from
        http://www.emailtextmessages.com/
        '''
        self.providers = {
                          'Alltel':'@message.alltel.com',
                          'AT&T':'@txt.att.net',
                          'Boost Mobile':'@myboostmobile.com',
                          'Metro PCS':'@mymetropcs.com',
                          'Sprint':'@messaging.sprintpcs.com',
                          'T-Mobile':'@tmomail.net',
                          'US Cellular':'@email.uscc.net',
                          'Verizon':'@vtext.com',
                          'Virgin Mobile':'@vmobl.com',
                          'Gmail':'@gmail.com',
                          'Other':''
                          }
        self.ui.provider.addItems(sorted(list(self.providers.keys())))


        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    smsdos = GUI()
    smsdos.show()
    sys.exit(app.exec_())