# Created by BaiJiFeiLong@gmail.com at 2021/12/7 16:48
import subprocess
import urllib.request

import jpype
from IceSpringPathLib import Path
from PySide2 import QtWidgets, QtGui


def startJvm():
    if jpype.isJVMStarted():
        return
    jarPath = Path("target/tmp") if Path("target/tmp").exists() else Path()
    jar = next(jarPath.glob("swagger-converter-*-SNAPSHOT.jar"), None)
    jvm = str(sorted(Path("jre").glob("**/jvm.*"), key=lambda x: x.stat().st_size)[-1])
    jpype.startJVM(jvm, f"-Djava.class.path={jar}")


def swaggerToHtml(swagger: str) -> str:
    startJvm()
    clazz = jpype.JClass("io.github.baijifeilong.swaggerconverter.SwaggerConverterApplication")
    html = clazz.swaggerToHtml(swagger)[:]
    return html


def doConvert():
    mainWindow.statusBar().showMessage("Converting...")
    mainWindow.repaint()
    swaggerJson = swaggerEdit.toPlainText()
    language = languageCombo.currentText()
    html = swaggerToHtml(swaggerJson).replace('<html lang="en">', f'<html lang="{language}">')
    htmlEdit.setPlainText(html)
    Path(outputEdit.text()).write_text(html)
    mainWindow.statusBar().showMessage("Converted.")


def doRead():
    filename = inputEdit.text()
    try:
        if filename.startswith("http:") or filename.startswith("https:"):
            jsonText = urllib.request.urlopen(filename).read().decode("utf8")
        else:
            jsonText = Path(filename).read_text()
    except Exception as e:
        QtWidgets.QMessageBox.warning(mainWindow, "Error", str(e))
        return
    swaggerEdit.setPlainText(jsonText)


def onOpenInput():
    filename, _ = QtWidgets.QFileDialog.getOpenFileName()
    if filename != "":
        inputEdit.setText(filename)


def onOpenOutput():
    filename, _ = QtWidgets.QFileDialog.getSaveFileName(mainWindow, "Save As", ".",
        "HTML Files (*.html);; All Files (*)")
    if filename != "":
        outputEdit.setText(filename)


def openOutputFolder():
    subprocess.Popen(("explorer", str(Path(outputEdit.text()).parent)))


app = QtWidgets.QApplication()
app.setWindowIcon(QtGui.QIcon("resources/crown.ico"))
app.setApplicationName("Ice Spring Swagger Converter")
app.setApplicationDisplayName(app.applicationName())
font = app.font()
font.setPointSize(12)
app.setFont(font)

mainWindow = QtWidgets.QMainWindow()
mainWindow.resize(1280, 720)
mainWidget = QtWidgets.QWidget()
mainWindow.setCentralWidget(mainWidget)

inputLabel = QtWidgets.QLabel("Input File/URL:")
inputEdit = QtWidgets.QLineEdit("https://petstore.swagger.io/v2/swagger.json")
inputButton = QtWidgets.QPushButton("Open")
inputButton.clicked.connect(onOpenInput)
outputLabel = QtWidgets.QLabel("Output File:")
outputEdit = QtWidgets.QLineEdit()
outputEdit.setText(str(Path("swagger.html").absolute()))
outputButton = QtWidgets.QPushButton("Open")
outputButton.clicked.connect(onOpenOutput)
languageLabel = QtWidgets.QLabel("HTML Language:")
languageCombo = QtWidgets.QComboBox()
languageCombo.addItems(("en", "zh",))
gridLayout = QtWidgets.QGridLayout()
gridLayout.setColumnStretch(2, 0)
gridLayout.addWidget(inputLabel)
gridLayout.addWidget(inputEdit)
gridLayout.addWidget(inputButton)
gridLayout.addWidget(outputLabel)
gridLayout.addWidget(outputEdit)
gridLayout.addWidget(outputButton)
gridLayout.addWidget(languageLabel)
gridLayout.addWidget(languageCombo, gridLayout.rowCount() - 1, 1, 1, 2)

swaggerEdit = QtWidgets.QPlainTextEdit()
swaggerEdit.textChanged.connect(lambda: convertButton.setDisabled(swaggerEdit.toPlainText() == ""))
swaggerGroup = QtWidgets.QGroupBox("Swagger Edit")
swaggerGroup.setLayout(QtWidgets.QGridLayout())
swaggerGroup.layout().addWidget(swaggerEdit)
htmlEdit = QtWidgets.QPlainTextEdit()
htmlGroup = QtWidgets.QGroupBox("HTML Preview")
htmlGroup.setLayout(QtWidgets.QGridLayout())
htmlGroup.layout().addWidget(htmlEdit)
previewLayout = QtWidgets.QHBoxLayout()
previewLayout.addWidget(swaggerGroup)
previewLayout.addWidget(htmlGroup)

readButton = QtWidgets.QPushButton("Read")
readButton.clicked.connect(doRead)
convertButton = QtWidgets.QPushButton("Convert")
convertButton.clicked.connect(lambda: inputEdit.text() and doConvert())
convertButton.setDisabled(True)
openFolderButton = QtWidgets.QPushButton("Open Output Folder")
openFolderButton.clicked.connect(openOutputFolder)
buttonsLayout = QtWidgets.QHBoxLayout()
buttonsLayout.addWidget(readButton)
buttonsLayout.addWidget(convertButton)
buttonsLayout.addWidget(openFolderButton)

mainLayout = QtWidgets.QVBoxLayout()
mainLayout.addLayout(gridLayout)
mainLayout.addLayout(previewLayout)
mainLayout.addLayout(buttonsLayout)
mainWidget.setLayout(mainLayout)

mainWindow.statusBar().showMessage("Ready.")
mainWindow.show()
app.exec_()
