# Copyright (C) 2011-2012, Valentin Lorentz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from PyQt4 import QtGui

from wididit import People
from wididit.utils import userid2tuple

from wididitclient import conf
from wididitclient.i18n import _
from wididitclient.utils import get_qicon, log

username = None
hostname = None
password = None
_login_window = None

def get_people():
    global username, hostname, password
    if None in (username, hostname, password):
        return None
    else:
        return People(username, hostname, password, connect=True)

def authenticate(callback):
    global _login_window

    def new_callback(new_userid, new_password):
        global username, hostname, password
        try:
            username, hostname = userid2tuple(new_userid)
        except:
            return False
        password = new_password
        if People(username, hostname, password, connect=True).authenticated:
            return callback(new_userid, new_password)
        else:
            return False

    _login_window = LoginWindow(new_callback)

class LoginWindow(QtGui.QMainWindow):
    def __init__(self, callback):
        super(LoginWindow, self).__init__()
        self._callback = callback

        log.debug('Spawning login window.')

        # Title of login window.
        self.setWindowTitle(_('Connect to Wididit'))
        self.setWindowIcon(get_qicon())

        self.setCentralWidget(QtGui.QWidget())

        self._init_geometry()
        self._init_widgets()

        self.show()

        log.debug('Login window displayed.')

    def _init_widgets(self):
        layout = QtGui.QVBoxLayout()
        self.centralWidget().setLayout(layout)

        self._userid = QtGui.QLineEdit()
        # Value of the login prompt when it is empty and not focused.
        self._userid.setPlaceholderText(_('login@hostname'))
        # Help text for the login prompt.
        self._userid.setToolTip(_('Enter your unique userid.'))
        self._userid.returnPressed.connect(self.on_connect)
        self._userid.setText(conf.get(['accounts', 'default', 'userid']))
        layout.addWidget(self._userid)

        self._password = QtGui.QLineEdit()
        # Value of the password prompt when it is empty and not focused
        self._password.setPlaceholderText(_('password'))
        # Help text for the password prompt.
        self._password.setToolTip(_('The password for your Wididit account.'))
        self._password.setEchoMode(QtGui.QLineEdit.Password)
        self._password.returnPressed.connect(self.on_connect)
        self._password.setText(conf.get(['accounts', 'default', 'pass']))
        layout.addWidget(self._password)

        self._validate = QtGui.QPushButton(
                # Text of the button used to connect.
                _('Connect'),
                )
        layout.addWidget(self._validate)
        self._validate.clicked.connect(self.on_connect)

    def on_connect(self, event=None):
        log.debug('User clicked the authentication button. Validating '
                'creditentials...')
        userid = self._userid.text()
        password = self._password.text()
        valid = self._callback(userid, password)
        conf.set(['accounts', 'default', 'userid'], str(userid))
        conf.set(['accounts', 'default', 'pass'], str(password))
        if valid:
            log.info('Valid userid and password. Connected.')
            self._save_geometry()
            self.hide()
        else:
            log.info('Invalid userid or password. Asking authentication again.')

            dialog = QtGui.QDialog(self)
            # Message displayed when authentication failed.
            label = QtGui.QLabel(_('Invalid userid or password. Try again.'))
            # Close the "authentication failed" dialog.
            close = QtGui.QPushButton(_('Close'))
            close.clicked.connect(dialog.accept)
            dialog.setLayout(QtGui.QVBoxLayout())
            dialog.layout().addWidget(label)
            dialog.layout().addWidget(close)
            dialog.show()

    def closeEvent(self, event):
        self._save_geometry()

    def _init_geometry(self):
        posx = conf.get(['look', 'loginwindow', 'geometry', 'posx'], 0)
        posy = conf.get(['look', 'loginwindow', 'geometry', 'posy'], 0)
        self.move(posx, posy)

    def _save_geometry(self):
        conf.set(['look', 'loginwindow', 'geometry', 'posx'], self.x())
        conf.set(['look', 'loginwindow', 'geometry', 'posy'], self.y())
