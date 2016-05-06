from PySide.QtSvg import *
from PySide.QtCore import *
from PySide.QtGui import *
import hou, os, zipfile

iconSize = 50

class iconsWidgetClass(QWidget):
    def __init__(self):
        super(iconsWidgetClass, self).__init__()
        self.vLy = QVBoxLayout(self)

        self.fLy = QHBoxLayout()
        self.vLy.addLayout(self.fLy)
        label = QLabel('Filter: ')
        self.fLy.addWidget(label)

        self.clear_btn = QPushButton('')
        self.clear_btn.setIcon(hou.ui.createQtIcon('BUTTONS_remove'))
        self.clear_btn.clicked.connect(self.fill)
        self.clear_btn.setFixedSize(QSize(20,20))
        self.fLy.addWidget(self.clear_btn)
        @self.clear_btn.clicked.connect
        def clearFilter():
            if self.filter.text():
                self.filter.setText('')
                self.fill()

        self.filter = QLineEdit()
        self.filter.returnPressed.connect(self.fill)
        self.fLy.addWidget(self.filter)
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.fill)
        self.fLy.addWidget(self.search_btn)

        # self.btn = QPushButton('Clear')
        # self.btn.clicked.connect(self.clearList)
        # self.vLy.addWidget(self.btn)

        self.scrollArea = QScrollArea(self)
        self.vLy.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.sawc = QFrame()
        self.ly = QVBoxLayout(self.sawc)
        self.scrollArea.setWidget(self.sawc)

        hfs = hou.getenv('HFS')
        if hou.applicationVersion()[0] < 15:
            path = os.path.join(hfs,'houdini/help/icons/large')
        else:
            path = os.path.join(hfs,'houdini/help/icons.zip')
        self.icons = {}
        self.content = None

        if os.path.exists(path):
            self.path = path
            self.findIcons()
            self.fill()
        else:
            err = QLabel('Icons not found!')
            err.setStyleSheet('font-size:25px;')
            err.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
            self.ly.addWidget(err)

    def findIcons(self):
        if hou.applicationVersion()[0] < 15:
            for category in os.listdir(self.path):
                for ico in os.listdir(os.path.join(self.path, category)):
                    iconPath = os.path.join(os.path.join(self.path, category, ico))
                    iconName = '_'.join([category, os.path.splitext(ico)[0]])
                    self.icons[iconName] = QPixmap(iconPath)
        else:
            zf = zipfile.ZipFile(self.path, 'r')
            for f in zf.namelist():
                if f.startswith('old'):continue
                if os.path.splitext(f)[-1] == '.svg':
                    svg = QSvgRenderer(QByteArray(zf.read(f)))
                    if not svg.isValid():
                        continue
                    pixmap = QPixmap(iconSize, iconSize)
                    painter = QPainter()
                    painter.begin(pixmap)
                    pixmap.fill(QColor(Qt.black))
                    svg.render(painter)
                    painter.end()
                    category, ico = f.split('/')
                    iconName = '_'.join([category, os.path.splitext(ico)[0]])
                    self.icons[iconName] = pixmap
            zf.close()

    def fill(self):
        text = self.filter.text()
        if self.content:
            self.content.setParent(None)
            del self.content
        self.content = QWidget(self)
        self.grid = QGridLayout(self.content)
        self.ly.addWidget(self.content)
        i = 0
        for ico in sorted(self.icons):
            if text:
                if not text.lower() in ico.lower():
                    continue
            w = QWidget(self)
            w.setObjectName(ico)
            l = QHBoxLayout(w)
            label = QLabel()
            label.setMinimumSize(QSize(iconSize,iconSize))
            label.setPixmap(self.icons[ico])
            l.addWidget(label)
            name = QLineEdit()
            name.setReadOnly(1)
            name.setText(ico)
            l.addWidget(name)
            r = i%3
            c= i/3
            i += 1
            self.grid.addWidget(w, c, r)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(spacerItem, i+1, 0, 1, 1)


