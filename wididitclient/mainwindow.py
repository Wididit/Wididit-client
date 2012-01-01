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

from wididitclient import conf
from wididitclient.i18n import _
from wididitclient.login import get_people
from wididitclient.utils import get_qicon, log
from wididitclient.entrylistwidget import EntryListWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self, application):
        super(MainWindow, self).__init__()
        self._application = application

        log.debug('Spawning main window.')

        # Title of main window.
        self.setWindowTitle(_('Wididit'))
        self.setWindowIcon(get_qicon())

        self.setCentralWidget(QtGui.QTabWidget(self))
        self.centralWidget().setTabsClosable(True)
        self.centralWidget().setMovable(True)

        self._init_geometry()
        self._init_tabs()
        self._init_toolbar()

        self.show()

        log.debug('Main window displayed.')

    def _init_tabs(self):
        self._tabs = {}

        tabs = conf.get(['look', 'mainwindow', 'tabs', 'opened'],
                ['timeline', 'all', 'own'])

        for tab in tabs:
            self.opentab(tab)

    def _init_toolbar(self):
        self._menus = {
                # File menu title.
                'file': self.menuBar().addMenu(_('&File')),
                # Tabs menu title.
                'tabs': self.menuBar().addMenu(_('&Tabs')),
                }
        self._menus.update({
                # Tabs>Open/Close menu title.
                'openclosetab': self._menus['tabs'].addMenu(_('Open/Close')),
                })
        self._actions = {
                # Quit Wididit from the 'File' menu.
                'quit': QtGui.QAction(_('Quit'), self),
                'openclosetab': {
                    # Open timeline tab.
                    'timeline': QtGui.QAction(_('Timeline'), self),
                    # Open 'All entries' tab.
                    'all': QtGui.QAction(_('All'), self),
                    # Open timeline tab.
                    'own': QtGui.QAction(_('Your entries'), self),
                    }
                }
        self._actions['quit'].triggered.connect(self.quit)
        self._menus['file'].addSeparator()
        self._menus['file'].addAction(self._actions['quit'])

        for name in ('timeline', 'all', 'own'):
            self._actions['openclosetab'][name].setCheckable(True)
            if name in self._tabs:
                self._actions['openclosetab'][name].setChecked(True)
            self._actions['openclosetab'][name].toggled \
                    .connect(self.openclosetab_slot(name))
            self._menus['openclosetab'].addAction(
                    self._actions['openclosetab'][name])
        self.centralWidget().tabCloseRequested.connect(self.closetab_slot)

    def openclosetab_slot(self, id_):
        def new_openclosetab_slot(checked):
            log.debug('Called new_openclosetab_slot for %s with %r.' %
                    (id_, checked))
            if checked:
                self.opentab(id_)
            else:
                self.closetab(id_)
        return new_openclosetab_slot

    def closetab_slot(self, index):
        widget = self.centralWidget().widget(index)
        for key, value in self._tabs.items():
            if value[0] == widget:
                self.closetab(key)
                self._actions['openclosetab'][key].setChecked(False)
                break

    def opentab(self, id_):
        if id_ == 'timeline':
            # Title of tab containing the timeline.
            title = _('Timeline')
            entries = Entry.Query(get_people().server).shared(True).fetch()
            value = (EntryListWidget(self, entries), title)
        elif id_ == 'all':
            # Title of tab containing all entries.
            title = _('All')
            entries = Entry.Query(get_people().server,
                    Entry.Query.MODE_ALL).fetch()
            value = (EntryListWidget(self, entries), title)
        elif id_ == 'own':
            # Title of tab containing user's entries.
            title = _('Your entries')
            entries = Entry.Query(get_people().server,
                    Entry.Query.MODE_ALL).filterAuthor(get_people()) \
                    .fetch()
            value = (EntryListWidget(self, entries), title)
            self.centralWidget().addTab(*value)
        self._tabs[id_] = value
        self.centralWidget().addTab(*value)

    def closetab(self, id_):
        log.debug('Closing tab %s.' % id_)
        if id_ not in self._tabs: # Already removed:
            return
        index = self.centralWidget().indexOf(self._tabs[id_][0])
        self.centralWidget().removeTab(index)
        del self._tabs[id_]

    def closeEvent(self, event):
        self._save_geometry()

    def quit(self, *args, **kwargs):
        self._save_geometry()
        return self._application.quit()
        conf.set(['look', 'mainwindow', 'geometry', 'height'], self.height)


    def _init_geometry(self):
        width = conf.get(['look', 'mainwindow', 'geometry', 'width'], 800)
        height = conf.get(['look', 'mainwindow', 'geometry', 'height'], 600)
        posx = conf.get(['look', 'mainwindow', 'geometry', 'posx'], 0)
        posy = conf.get(['look', 'mainwindow', 'geometry', 'posy'], 0)
        self.resize(width, height)
        self.move(posx, posy)

    def _save_geometry(self):
        conf.set(['look', 'mainwindow', 'geometry', 'width'], self.width())
        conf.set(['look', 'mainwindow', 'geometry', 'height'], self.height())
        conf.set(['look', 'mainwindow', 'geometry', 'posx'], self.x())
        conf.set(['look', 'mainwindow', 'geometry', 'posy'], self.y())
