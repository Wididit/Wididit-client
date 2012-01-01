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

__all__ = ['EntryListWidget']

from PyQt4 import QtGui

from wididit import Entry

class EntryListWidget(QtGui.QScrollArea):
    def __init__(self, parent, entries):
        super(EntryListWidget, self).__init__(parent)
        self.setWidgetResizable(True)

        self._widget = QtGui.QWidget()
        self.setWidget(self._widget)
        self._widget.setLayout(EntryListLayout(entries, self._widget))

class EntryListLayout(QtGui.QVBoxLayout):
    def __init__(self, entries, parent=None):
        super(EntryListLayout, self).__init__(parent)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored)
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)

        for entry in entries:
            item = QtGui.QFrame()
            item.setStyleSheet('background-color: white;');
            item.setSizePolicy(size_policy)
            item.setLayout(EntryListWidgetItem(entry))
            self.addWidget(item)

        # Take all the trailing space at the end of the scrollarea.
        widget = QtGui.QWidget()
        self.addWidget(widget)

class EntryListWidgetItem(QtGui.QGridLayout):
    def __init__(self, entry):
        super(EntryListWidgetItem, self).__init__()

        self._title = QtGui.QLabel(entry.title)
        self.addWidget(self._title, 0, 0)
        self._content = QtGui.QLabel(entry.content)
        self.addWidget(self._content, 1, 0)
