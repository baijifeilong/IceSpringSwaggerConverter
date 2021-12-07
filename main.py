# Created by BaiJiFeiLong@gmail.com at 2021/12/7 16:48
import os
from pathlib import Path

import delegator
from PySide2 import QtWidgets, QtGui


def doConvert():
    mainWindow.statusBar().showMessage("Converting...")
    mainWindow.repaint()
    url = swaggerEdit.text()
    java = Path("jre") / "bin" / "java"
    jar = list(Path(".").glob("**/swagger-converter*.jar"))[0]
    command = f"{java} -jar {jar} {url}"
    response = delegator.run(command)
    assert response.return_code == 0
    html = "\n".join([x for x in response.out.strip().splitlines() if "[main]" not in x])
    html = html.replace('<html lang="en">', '<html lang="zh">')
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
