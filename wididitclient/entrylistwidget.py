# Copyright (C) 2011, Valentin Lorentz
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

class EntryListWidget(QtGui.QVBoxLayout):
    def __init__(self, entries, parent=None):
        super(EntryListWidget, self).__init__(parent)

        for entry in entries:
            item = QtGui.QFrame()
            item.setStyleSheet('background-color: white;');
            item.setLayout(EntryListWidgetItem(entry))
            self.addWidget(item)

class EntryListWidgetItem(QtGui.QGridLayout):
    def __init__(self, entry):
        super(EntryListWidgetItem, self).__init__()

        self._title = QtGui.QLabel(entry.title)
        self.addWidget(self._title, 0, 0)
        self._content = QtGui.QLabel(entry.content)
        self.addWidget(self._content, 1, 0)
