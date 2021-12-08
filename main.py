# Created by BaiJiFeiLong@gmail.com at 2021/12/7 16:48
import os
import urllib.request
from pathlib import Path

import jpype
from PySide2 import QtWidgets, QtGui


def swaggerToHtml(swagger: str) -> str:
    jar = list(Path().glob("**/swagger-converter-*-SNAPSHOT.jar"))[-1]
    jvm = str(sorted(Path("jre").glob("**/jvm.*"), key=lambda x: x.stat().st_size)[-1])
    jpype.startJVM(jvm, f"-Djava.class.path={jar}")
    clazz = jpype.JClass("io.github.baijifeilong.swaggerconverter.SwaggerConverterApplication")
    html = clazz.swaggerToHtml(swagger)[:]
    jpype.shutdownJVM()
    return html


def doConvert():
    mainWindow.statusBar().showMessage("Converting...")
    mainWindow.repaint()
    url = swaggerEdit.text()
    swaggerJson = urllib.request.urlopen(url).read().decode("utf8")
    html = swaggerToHtml(swaggerJson).replace('<html lang="en">', '<html lang="zh">')
    htmlEdit.setPlainText(html)
    Path("outputs/doc.html").write_text(html, encoding="utf8")
    mainWindow.statusBar().showMessage("Converted.")


app = QtWidgets.QApplication()
app.setWindowIcon(QtGui.QIcon("resources/crown.ico"))
app.setApplicationName("Ice Spring Swagger Converter")
app.setApplicationDisplayName(app.applicationName())
font = app.font()
font.setPointSize(12)
app.setFont(font)

mainWindow = QtWidgets.QMainWindow()
mainWindow.resize(1280, 720)
mainWidget = QtWidgets.QWidget(mainWindow)
mainWindow.setCentralWidget(mainWidget)
mainLayout = QtWidgets.QVBoxLayout(mainWidget)
mainWidget.setLayout(mainLayout)

buttonsLayout = QtWidgets.QHBoxLayout(mainWidget)
swaggerLayout = QtWidgets.QHBoxLayout(mainWidget)
htmlEdit = QtWidgets.QPlainTextEdit(mainWidget)
mainLayout.addLayout(swaggerLayout)
mainLayout.addWidget(htmlEdit)
mainLayout.addLayout(buttonsLayout)

swaggerLabel = QtWidgets.QLabel("Swagger JSON URL:", mainWidget)
swaggerEdit = QtWidgets.QLineEdit("http://localhost:8080/v2/api-docs", mainWidget)
swaggerLayout.addWidget(swaggerLabel)
swaggerLayout.addWidget(swaggerEdit)

convertButton = QtWidgets.QPushButton("Convert")
convertButton.clicked.connect(lambda: swaggerEdit.text() and doConvert())
openFolderButton = QtWidgets.QPushButton("Open Output Folder")
openFolderButton.clicked.connect(lambda: os.system("explorer outputs"))
buttonsLayout.addWidget(convertButton)
buttonsLayout.addWidget(openFolderButton)

Path("outputs").mkdir(exist_ok=True)
mainWindow.statusBar().showMessage("Ready.")
mainWindow.show()
app.exec_()
