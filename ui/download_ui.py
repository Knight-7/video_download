import sys
import requests
import time

from PyQt5 import QtWidgets as qw, QtCore as qc


class Download_thread(qc.QThread):

    values = qc.pyqtSignal(list)
    isFinish = qc.pyqtSignal(str)

    def __init__(self, url=None, parent=None):
        super().__init__(parent=parent)
        self.url = url

    def run(self):
        start = time.time()
        try:
            size = 0
            response = requests.get(self.url, stream=True)
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            print(f'文件大小{round(float(content_size / chunk_size ** 2), 2)}MB')
            with open('v1.mp3', 'wb') as f:
                s_time = time.time()
                p_size = 0
                for data in response.iter_content(chunk_size):
                    f.write(data)
                    size += len(data)
                    if (time.time() - s_time >= 1):
                        s_time = time.time()
                        count = int(size * 100 / content_size)
                        speed = round(float((size - p_size) / chunk_size ** 2), 2)
                        self.values.emit([count, f'速度:{speed}MB/s'])
                        p_size = size
            speed = round(float((size - p_size) / chunk_size ** 2), 2)
            self.values.emit([100, f'速度:{speed}MB/s'])
            download_time = round(time.time() - start, 2)
            self.isFinish.emit(f'下载完成，耗时{download_time}秒, 平均速度为:{round(float(content_size / download_time / chunk_size ** 2), 2)}MB/s')
            print(f'下载完成，耗时{download_time}秒, 平均速度为:{round(float(content_size / download_time / chunk_size ** 2), 2)}MB/s')
        except Exception as e:
            print(e.args)




class Download_ui(qw.QWidget):
    def __init__(self, parent=None):
        super(Download_ui, self).__init__(parent=parent)
        self.url = None
        self.download_thread = None

        self.init_ui()
        self.pushButton.clicked.connect(self.download)

    def init_ui(self):
        self.setGeometry(0, 0, 600, 400)
        self.label = qw.QLabel('请输入网址:', self)
        self.label.setGeometry(50, 30, 100, 30)
        self.inputEdit = qw.QTextEdit(self)
        self.inputEdit.setGeometry(50, 70, 400, 100)
        self.progressBar = qw.QProgressBar(self)
        self.progressBar.setGeometry(50, 200, 430, 20)
        self.speed_label = qw.QLabel('', self)
        self.speed_label.setGeometry(50, 250, 400, 30)
        self.pushButton = qw.QPushButton('下载', self)
        self.pushButton.setGeometry(200, 300, 130, 50)

    def download(self):
        self.url = self.inputEdit.toPlainText()
        if self.url != '':
            self.download_thread = Download_thread(self.url)
            self.download_thread.values.connect(self.changeValues)
            self.download_thread.isFinish.connect(self.finish)
            self.download_thread.start()
        else:
            qw.QMessageBox.information(self, 'tips', '请输入链接',qw.QMessageBox.Yes)

    def changeValues(self, values):
        self.progressBar.setValue(values[0])
        self.speed_label.setText(values[1])

    def finish(self, str):
        self.speed_label.setText(str)


class Application:
    def __init__(self):
        self.app = qw.QApplication(sys.argv)
        self.win = Download_ui()

    def run(self):
        self.win.show()

        exit(self.app.exec_())


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    main_win = Download_ui()
    main_win.show()

    exit(app.exec_())