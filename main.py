
import sys, os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog, QLabel, QCheckBox, QToolBar, QStyle,
                             QListWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QMenu, QMenuBar, QStatusBar)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from pdf_watermark_remover import PDFWatermarkRemover
from version import __version__

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lastPath = PDFWatermarkRemover.load_last_path()  # 加载上次路径
        self.initUI()
        self.language = 'CN'

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.filesList = QListWidget()
        self.layout.addWidget(self.filesList)

        hbox = QHBoxLayout()
        self.overwriteCheckBox = QCheckBox('覆盖原始文件')
        self.overwriteCheckBox.setChecked(True)
        hbox.addWidget(self.overwriteCheckBox)
        self.layout.addLayout(hbox)

        self.createMenuBar()
        self.createToolBar()
        self.createStatusBar()
        # self.statusBar = QStatusBar()
        # self.setStatusBar(self.statusBar)

        self.setWindowTitle('PDF水印移除工具')
        self.setWindowIcon(QIcon('favicon.ico'))
        self.resize(800, 600)

    def createMenuBar(self):
        menuBar = self.menuBar()

        # 文件菜单
        fileMenu = menuBar.addMenu('文件')
        openAction = QAction('添加PDF文件', self)
        openAction.triggered.connect(self.openFileNamesDialog)
        fileMenu.addAction(openAction)

        removeAction = QAction('移除水印', self)
        removeAction.triggered.connect(self.startProcessing)
        fileMenu.addAction(removeAction)

        exitAction = QAction('退出', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # 编辑菜单
        editMenu = menuBar.addMenu('编辑')
        toggleLanguageAction = QAction('切换语言', self)
        toggleLanguageAction.triggered.connect(self.toggleLanguage)
        editMenu.addAction(toggleLanguageAction)

        overwriteAction = QAction('覆盖原文件', self, checkable=True)
        overwriteAction.setChecked(True)
        overwriteAction.triggered.connect(lambda: self.overwriteCheckBox.setChecked(overwriteAction.isChecked()))
        editMenu.addAction(overwriteAction)

        # 帮助菜单
        helpMenu = menuBar.addMenu('帮助')
        aboutAction = QAction('关于', self)
        aboutAction.triggered.connect(self.showAboutDialog)
        helpMenu.addAction(aboutAction)

    def createToolBar(self):
        self.toolBar = QToolBar("主工具栏")
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.openIcon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        self.openAct = QAction(self.openIcon, '添加pdf文件', self)
        self.openAct.triggered.connect(self.openFileNamesDialog)
        self.toolBar.addAction(self.openAct)

        self.removeIcon = self.style().standardIcon(QStyle.SP_CommandLink)
        self.removeAct = QAction(self.removeIcon, '移除水印', self)
        self.removeAct.triggered.connect(self.startProcessing)
        self.toolBar.addAction(self.removeAct)

        self.toggleLanguageIcon = self.style().standardIcon(QStyle.SP_BrowserReload)
        self.toggleLanguageAct = QAction(self.toggleLanguageIcon, '切换语言', self)
        self.toggleLanguageAct.triggered.connect(self.toggleLanguage)
        self.toolBar.addAction(self.toggleLanguageAct)
        
        self.aboutIcon = self.style().standardIcon(QStyle.SP_FileDialogInfoView)
        self.aboutAct = QAction(self.aboutIcon, '关于', self)
        self.aboutAct.triggered.connect(self.showAboutDialog)
        self.toolBar.addAction(self.aboutAct)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def startProcessing(self):
        self.statusBar.showMessage("正在移除水印...")
        try:
            for index in range(self.filesList.count()):
                input_pdf = self.filesList.item(index).text()
                output_pdf = input_pdf if self.overwriteCheckBox.isChecked() else PDFWatermarkRemover.rename_file(input_pdf)
                result = PDFWatermarkRemover.remove_watermark(input_pdf, output_pdf)
                if result == "Success":
                    self.statusBar.showMessage(f"水印移除成功: {os.path.basename(input_pdf)}")
                else:
                    self.statusBar.showMessage(f"水印移除失败: {os.path.basename(input_pdf)}")
        except Exception as e:
            self.statusBar.showMessage(f"发生错误: {e}")

    def showAboutDialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon('favicon.ico'))
        msgBox.setTextFormat(Qt.RichText)  # 设置文本格式为富文本
        if self.language == 'CN':
            msgBox.setWindowTitle("关于")
            msgBox.setText("<div align='center'>PDF水印移除工具<br>"
                        "<p style='font-family:黑体; font-size:24px'>此程序可能会移除PDF中的所有图像，<br>"
                        "包括非水印图像。请谨慎使用!<br>"
                        "移除水印文件可能导致侵犯他人合法权益的风险，请确认您对文件的所有权。<br>"
                        "请备份你的PDF文件后再进行操作。<br>"
                        "选择PDF文件并点击开始移除水印。<br>"
                        "作者：<a href='https://github.com/weizy0219'>weizy0219@github</a><br>"
                        "公司网站：<a href='http://www.wesinx.com'>www.wesinx.com</a></p></div>")
        else:
            msgBox.setWindowTitle("About")
            msgBox.setText("<div align='center'><h4>PDF Watermark Remover Tool</h4><br>"
                       "<p style='font-family: Arial; font-size:24px'>This program may remove all images in the PDF,<br>"
                       "including non-watermark images. Please use with caution!<br>"
                       "Removing watermarks may risk infringing on others' legal rights. Please ensure you have the rights to the file.<br>"
                       "Back up your PDF files before proceeding.<br>"
                       "Select a PDF file and click to start removing watermarks.<br>"
                       "Author: <a href='https://github.com/weizy0219'>weizy0219@github</a><br>"
                       "Company Website: <a href='http://www.wesinx.com'>www.wesinx.com</a></p></div>")
            
        msgBox.exec_()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        initialPath = self.lastPath if os.path.exists(self.lastPath) else ''
        files, _ = QFileDialog.getOpenFileNames(self, "选择一个或多个文件", initialPath, "PDF 文件 (*.pdf)", options=options)
        # files, _ = QFileDialog.getOpenFileNames(self, "选择一个或多个文件", "", "PDF 文件 (*.pdf)", options=options)
        if files:
            self.filesList.clear()
            self.filesList.addItems(files)
            self.lastPath = os.path.dirname(files[0])  # 更新最后的路径
            PDFWatermarkRemover.save_last_path(self.lastPath)  # 保存当前路径

    def toggleLanguage(self):
        if self.language == 'EN':
            self.language = 'CN'
            self.updateUI('CN')
        else:
            self.language = 'EN'
            self.updateUI('EN')

    def updateUI(self, lang):
        if lang == 'CN':
            self.overwriteCheckBox.setText('覆盖原始文件')
            self.setWindowTitle('PDF水印移除工具')
        else:
            self.overwriteCheckBox.setText('Overwrite original files')
            self.setWindowTitle('PDF Watermark Remover')

        # 更新菜单栏和工具栏文本
        self.menuBar().actions()[0].setText('文件' if lang == 'CN' else 'File')
        self.menuBar().actions()[0].menu().actions()[0].setText('添加PDF文件' if lang == 'CN' else 'Add PDF(s)')
        self.menuBar().actions()[0].menu().actions()[1].setText('移除水印' if lang == 'CN' else 'Remove Watermark')
        self.menuBar().actions()[0].menu().actions()[2].setText('退出' if lang == 'CN' else 'Exit')
        self.menuBar().actions()[1].setText('编辑' if lang == 'CN' else 'Edit')
        self.menuBar().actions()[1].menu().actions()[0].setText('切换语言' if lang == 'CN' else 'Toggle Language')
        self.menuBar().actions()[1].menu().actions()[1].setText('覆盖原文件' if lang == 'CN' else 'Overwrite original files')
        self.menuBar().actions()[2].setText('帮助' if lang == 'CN' else 'Help')
        self.menuBar().actions()[2].menu().actions()[0].setText('关于' if lang == 'CN' else 'About')
        self.openAct.setText('添加PDF文件' if lang == 'CN' else 'Add PDF(s)')
        self.removeAct.setText('移除水印' if lang == 'CN' else 'Remove Watermark')
        self.toggleLanguageAct.setText('切换语言' if lang == 'CN' else 'Toggle Language')
        self.aboutAct.setText('关于' if lang == 'CN' else 'About')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
