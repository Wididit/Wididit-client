# Copyright (C) 2012, Valentin Lorentz
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

__all__ = ['PeopleWidget', 'ProfileWidget', 'AuthorWidget']

from PyQt4 import QtGui

from wididit import Entry, People

from wididitclient import login
from wididitclient.utils import log
from wididitclient.entrylistwidget import EntryListWidget

class PeopleWidget(QtGui.QScrollArea):
    def __init__(self, parent, people, with_entries=False):
        super(PeopleWidget, self).__init__(parent)

        log.debug('Showing user %s.' % people.userid)

        self.setWidgetResizable(True)

        self._widget = QtGui.QWidget()
        self.setWidget(self._widget)
        self._widget.setLayout(PeopleLayout(people, self._widget,
            with_entries))

class PeopleLayout(QtGui.QVBoxLayout):
    def __init__(self, people, parent=None, with_entries=False):
        super(PeopleLayout, self).__init__(parent)

        self._profile = ProfileWidget(parent, people)
        self.addWidget(self._profile)

        if with_entries:
            log.debug('Showing entries for user %s' % people.userid)
            entries = Entry.Query(login.get_server(),
                    mode=Entry.Query.MODE_ALL).filterAuthor(people).fetch()
            self._entries = EntryListWidget(parent, entries)
            self.addWidget(self._entries)

class ProfileWidget(QtGui.QFrame):
    def __init__(self, parent, people):
        super(ProfileWidget, self).__init__(parent)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored)
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)

        self.setStyleSheet('background-color: white;');
        self._layout = ProfileLayout(people)
        self.setLayout(self._layout)

class ProfileLayout(QtGui.QGridLayout):
    def __init__(self, people):
        super(ProfileLayout, self).__init__()

        self._userid = QtGui.QLabel(people.userid)
        self.addWidget(self._userid, 0, 0)
        self._biography = QtGui.QLabel(people.biography)
        self.addWidget(self._biography, 1, 0)

class AuthorWidget(QtGui.QCommandLinkButton):
    def __init__(self, author):
        super(AuthorWidget, self).__init__()
        self._author = author

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored))

        self.setText(author.username)
        self.setToolTip(author.userid)

        self.clicked.connect(self.on_click)

    def on_click(self, event=None):
        import wididitclient

        wididitclient.app.mainwindow.showuser(self._author)
