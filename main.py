import sys, time, _thread, os, subprocess, shutil
from PyQt5.QtWidgets import *
from windows import Ui_Form

# ===== 默认参数 =======
ffmpeg_dir = ''
files_out_dir = ''

input_files_dict = {}
input_sub_dict = {}


class MainWindow(QWidget, Ui_Form):

    def __init__(self, parent=None):
        global control_data, status_flag, time1
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('简易ffmpeg批量执行工具 V0.1')
        # ==/ Icon设置 /===
        # self.setWindowIcon(QIcon('icon/256x256.ico'))
        # ==/ 按键信号设置 /================
        # self.bt_start.clicked.connect(lambda: self.start())
        self.pushButton_ffmpeg_dir.clicked.connect(lambda: self.set_FFmpeg_dir())
        self.pushButton_files_add.clicked.connect(lambda: self.input_files_add())
        self.pushButton_files_del_one.clicked.connect(lambda: self.input_files_del_one())
        self.pushButton_files_del_all.clicked.connect(lambda: self.input_files_del_all())
        self.pushButton_files_sub_add.clicked.connect(lambda: self.input_sub_add())
        self.pushButton_files_sub_del_one.clicked.connect(lambda: self.input_sub_del_one())
        self.pushButton_files_sub_del_all.clicked.connect(lambda: self.input_sub_del_all())
        self.pushButton_files_sub_pass.clicked.connect(lambda: self.input_sub_pass())
        self.pushButton_out_dir.clicked.connect(lambda: self.set_files_out_dir())
        self.pushButton_start.clicked.connect(lambda: self.start())
        self.pushButton_stop.clicked.connect(lambda: self.stop())

        # ==/ 界面初始化 /==========
        # self.show_potdir.setText(pot_dir)
        # 界面更新
        _thread.start_new_thread(lambda: self.flash(), ())

    def flash(self):  # ==/ 页面刷新函数 /====
        # ===/ 更新控件 /=================================
        self.lineEdit_ffmpeg_dir.setText(ffmpeg_dir)
        self.lineEdit__out_dir.setText(files_out_dir)
        # self.show_potdir.setText(pot_dir)
        # self.show_workdir.setText(work_dir)
        # time.sleep(0.02)
        # self.show_video_dir.append(now_dir)
        # time.sleep(0.02)
        # self.show_video_dir.moveCursor(self.show_video_dir.textCursor().End)
        # self.show_now_number.setText(str(now_number))
        # self.show_files_number.setText(str(file_list_number))

    def set_FFmpeg_dir(self):
        global ffmpeg_dir, updata_flag
        file = QFileDialog.getOpenFileName(self)
        ffmpeg_dir = file[0]
        self.flash()

    def set_files_out_dir(self):
        global files_out_dir, updata_flag
        dir = QFileDialog.getExistingDirectory(self)
        files_out_dir = dir
        self.flash()

    def input_files_add(self):
        files = QFileDialog.getOpenFileNames(self, '选择输入的视频文件')
        if files[0] != []:
            files = files[0]
            for file in files:
                filename = file[file.rfind('/') + 1:]
                input_files_dict[filename] = file
                self.listWidget_files_input.addItem(filename)
            self.flash()

    def input_files_del_one(self):
        try:
            file = self.listWidget_files_input.currentItem().text()
            self.listWidget_files_input.takeItem(self.listWidget_files_input.currentRow())
            del input_files_dict[file]
        except:
            print('error')
        self.flash()

    def input_files_del_all(self):
        try:
            self.listWidget_files_input.clear()
            input_files_dict.clear()
        except:
            print('error')
        self.flash()

    def input_sub_add(self):
        subs = QFileDialog.getOpenFileNames(self, '选择需要内嵌得字幕文件')
        if subs[0] != []:
            subs = subs[0]
            for sub in subs:
                subname = sub[sub.rfind('/') + 1:]
                input_sub_dict[subname] = sub
                self.listWidget_sub.addItem(subname)
            self.flash()

    def input_sub_del_one(self):
        try:
            sub = self.listWidget_sub.currentItem().text()
            self.listWidget_sub.takeItem(self.listWidget_sub.currentRow())
            del input_sub_dict[sub]
        except:
            print('error')
        self.flash()

    def input_sub_del_all(self):
        try:
            self.listWidget_sub.clear()
            input_sub_dict.clear()
        except:
            print('error')
        self.flash()

    def input_sub_pass(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = MainWindow()
    ma.show()
    sys.exit(app.exec_())
