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

__all__ = ['EntryListWidget', 'ScrollableEntryListWidget',
        'EntryListItemWidget']

from PyQt4 import QtGui
from PyQt4 import QtCore

from wididit import Entry

class EntryListWidget(QtGui.QWidget):
    def __init__(self, parent, entries):
        super(EntryListWidget, self).__init__(parent)

        self.setLayout(EntryListLayout(entries, self))

class ScrollableEntryListWidget(QtGui.QScrollArea):
    def __init__(self, parent, entries):
        super(ScrollableEntryListWidget, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self._widget = EntryListWidget(parent, entries)
        self.setWidget(self._widget)

    def resizeEvent(self, event):
        self._widget.resize(self.size().width(),
                self._widget.size().height())

class EntryListLayout(QtGui.QVBoxLayout):
    def __init__(self, entries, parent):
        super(EntryListLayout, self).__init__(parent)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored)
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)

        for entry in entries:
            widget = EntryListItemWidget(entry, parent)
            widget.setSizePolicy(size_policy)
            self.addWidget(widget)

        # Take all the trailing space at the end of the scrollarea.
        widget = QtGui.QWidget()
        self.addWidget(widget)

class EntryListItemWidget(QtGui.QFrame):
    def __init__(self, entry, parent):
        super(EntryListItemWidget, self).__init__(parent)

        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setLayout(EntryListItemLayout(entry))

class EntryListItemLayout(QtGui.QGridLayout):
    def __init__(self, entry):
        super(EntryListItemLayout, self).__init__()

        from wididitclient.peoplewidget import AuthorWidget

        title_font = QtGui.QFont()
        title_font.setBold(True)
        title_font.setCapitalization(QtGui.QFont.SmallCaps)
        title_font.setUnderline(True)
        self._title = QtGui.QLabel(entry.title)
        self._title.setFont(title_font)
        self.addWidget(self._title, 0, 0)

        self._author = AuthorWidget(entry.author)
        self.addWidget(self._author, 0, 1)

        self._summary = QtGui.QLabel(entry.summary)
        self._summary.setWordWrap(True)
        self._summary.setAlignment(QtCore.Qt.AlignJustify)
        self.addWidget(self._summary, 1, 0, 1, 2)
