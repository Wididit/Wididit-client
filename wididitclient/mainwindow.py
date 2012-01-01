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

from wididit import Entry

from wididitclient.i18n import _
from wididitclient.login import get_people
from wididitclient.utils import get_qicon, log
from wididitclient.entrylistwidget import EntryListWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        log.debug('Spawning main window.')

        # Title of main window.
        self.setWindowTitle(_('Wididit'))
        self.setWindowIcon(get_qicon())

        self.setCentralWidget(QtGui.QTabWidget(self))

        # Title of tab containing the timeline.
        title = _('Timeline')
        entries = Entry.Query(get_people().server).shared(True).fetch()
        self._timeline = EntryListWidget(self, entries)
        self.centralWidget().addTab(self._timeline, title)

        # Title of tab containing all entries.
        title = _('All')
        entries = Entry.Query(get_people().server, Entry.Query.MODE_ALL).fetch()
        self._all = EntryListWidget(self, entries)
        self.centralWidget().addTab(self._all, title)

        # Title of tab containing user's entries.
        title = _('Your entries')
        entries = Entry.Query(get_people().server, Entry.Query.MODE_ALL) \
                .filterAuthor(get_people()).fetch()
        self._ownentries = EntryListWidget(self, entries)
        self.centralWidget().addTab(self._ownentries, title)

        self.show()

        log.debug('Main window displayed.')
