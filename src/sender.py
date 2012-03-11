from PyQt4 import QtCore
import smtplib  


class Sender(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        
        self.fromaddr = 'sms@root'
        self.toaddr = ''
        self.msg = ''
        
    def __del__(self):
        try:
            self.conn.quit()
        except:
            pass
        self.exiting = True
        self.wait()

    def connect(self, server, username='', password='', tls=False):
        print('connecting')
        try:
            self.conn = smtplib.SMTP(server)
        except:
            print('conection failed')
            return False;
        
        if  tls != False:
            print('using tls')
            self.conn.starttls()
        
        if username != '':
            print('logging in')
            try:
                self.conn.login(username,password)
            except:
                print('login failed')
                return False
        
        self.start() #start the thread! [calls run()]
        
        return True

        
    def run(self):
        print('running the thread')
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        
        while not self.exiting:
            try:
                self.conn.sendmail(self.fromaddr, self.toaddr, self.msg)
                self.emit(QtCore.SIGNAL('plusOne()'))
            except:
                print('Error in the sending thread')
                self.emit(QtCore.SIGNAL('sendingError(res)'))
                
                

        