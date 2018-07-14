
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import configs
import data
import views
import qdarkstyle
import estimator

class MainWindow(QMainWindow, views.MainWindowUi):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.actionOpenFile.triggered.connect(self.openImageFile)

        self.mainScene = data.Scene()
        self.depthPred = estimator.DepthPred()

        self.panoView.setMainWindow(self)
        self.monoView.setMainWindow(self)
        self.resultView.setMainWindow(self)
        self.labelListView.setMainWindow(self)

        self.selectObjects = []

        #self.depthPred = None

    def openImageFile(self):
        filePath, ok = QFileDialog.getOpenFileName(self, "open", configs.Params.fileDefaultOpenPath,
                                                  "Images (*.png *.jpg)")

        if ok:
            self.mainScene = self.createNewScene(filePath)
        else:
            print('open file error')

        return ok
    
    def createNewScene(self, filePath):
        scene = data.Scene()
        scene.initScene(filePath, self.depthPred)

        if scene.isAvailable():
            self.panoView.initByScene(scene)
            self.monoView.initByScene(scene)
            self.resultView.initByScene(scene)
            self.labelListView.initByScene(scene)
        else :
            print("Fail to create Scene")

        return scene

    def updateViews(self):
        self.panoView.update()
        self.monoView.update()
        self.resultView.update()

    def updateListView(self):
        self.labelListView.refreshList()
    
    def closeEvent(self, event):
        if self.depthPred:
            self.depthPred.sess.close()
        event.accept()

    def keyPressEvent(self, event):
        print("main")
        key = event.key()
        print(key)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
