#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Display the kanji for the current weekday in the system tray.
"""

import sys
import datetime

from PySide import QtCore, QtGui

# How frequently to update the icon
update_interval = 60 * 1000  # 1 minute

# Font, color and size of the icon
icon_font = QtGui.QFont(u"小塚明朝 Pro R", 12)
icon_color = QtCore.Qt.white
icon_size = QtCore.QSize(16, 16)

weekday_kanji = [
    u"月",
    u"火",
    u"水",
    u"木",
    u"金",
    u"土",
    u"日",
]

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QtGui.QApplication.quit)
        self.setContextMenu(menu)

    def update(self):
        """
        Repaint the icon to show the current day.
        """
        now = datetime.datetime.now()
        weekday = now.weekday()
        kanji = weekday_kanji[weekday]
        pixmap = draw_pixmap(kanji)
        icon = QtGui.QIcon(pixmap)
        self.setIcon(icon)

def draw_pixmap(character):
    """
    Draw and return a pixmap with the given character.
    """
    pixmap = QtGui.QPixmap(icon_size)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    try:
        painter.setFont(icon_font)
        painter.setPen(icon_color)
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, character)
    finally:
        painter.end()
    return pixmap

def main():
    app = QtGui.QApplication(sys.argv)
    trayIcon = SystemTrayIcon(QtGui.QIcon())
    trayIcon.update()
    trayIcon.show()

    timer = QtCore.QTimer(trayIcon)
    timer.timeout.connect(trayIcon.update)
    timer.start(update_interval)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
