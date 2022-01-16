import sys, time, _thread, os, subprocess, shutil
from PyQt5.QtWidgets import *
from windows import Ui_Form

# ===== 默认参数 =======
ffmpeg_dir = ''
files_out_dir = ''

input_files_dict = {}
input_sub_dict = {}
out_dict = {}

mission_all = 0
mission_now = 0

command = ''

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
        self.pushButton_files_up.clicked.connect(lambda: self.input_files_up())
        self.pushButton_files_down.clicked.connect(lambda: self.input_files_down())
        self.pushButton_files_sub_add.clicked.connect(lambda: self.input_sub_add())
        self.pushButton_files_sub_del_one.clicked.connect(lambda: self.input_sub_del_one())
        self.pushButton_files_sub_del_all.clicked.connect(lambda: self.input_sub_del_all())
        self.pushButton_files_sub_pass.clicked.connect(lambda: self.input_sub_pass())
        self.pushButton_files_sub_up.clicked.connect(lambda: self.input_sub_up())
        self.pushButton_files_sub_down.clicked.connect(lambda: self.input_sub_down())
        self.pushButton_out_dir.clicked.connect(lambda: self.set_files_out_dir())
        self.pushButton_start.clicked.connect(lambda: self.start())
        self.pushButton_stop.clicked.connect(lambda: self.stop())

        # ==/ 界面初始化 /==========
        # self.show_potdir.setText(pot_dir)
        self.label_num_all.setText(str(mission_all))
        self.label_num_now.setText(str(mission_now))
        self.progressBar.setRange(0, 10)
        # 界面更新
        _thread.start_new_thread(lambda: self.flash(), ())

    def flash(self):  # ==/ 页面刷新函数 /====
        pass
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

    def input_files_del_one(self):
        try:
            file = self.listWidget_files_input.currentItem().text()
            self.listWidget_files_input.takeItem(self.listWidget_files_input.currentRow())
            del input_files_dict[file]
        except:
            print('error')

    def input_files_del_all(self):
        try:
            self.listWidget_files_input.clear()
            input_files_dict.clear()
        except:
            print('error')

    def input_files_up(self):
        try:
            count = self.listWidget_files_input.currentRow()
            uptext = self.listWidget_files_input.currentItem().text()
            self.listWidget_files_input.takeItem(count)
            self.listWidget_files_input.insertItem(count - 1, uptext)
            if self.listWidget_files_input.currentRow() > 0:
                self.listWidget_files_input.setCurrentRow(count - 1)
        except:
            print('error')

    def input_files_down(self):
        try:
            count = self.listWidget_files_input.currentRow()
            downtext = self.listWidget_files_input.currentItem().text()
            self.listWidget_files_input.takeItem(count)
            self.listWidget_files_input.insertItem(count + 1, downtext)
            if self.listWidget_files_input.currentRow() < self.listWidget_files_input.count():
                self.listWidget_files_input.setCurrentRow(count + 1)
        except:
            print('error')

    def input_sub_add(self):
        subs = QFileDialog.getOpenFileNames(self, '选择需要内嵌得字幕文件')
        if subs[0] != []:
            subs = subs[0]
            for sub in subs:
                subname = sub[sub.rfind('/') + 1:]
                input_sub_dict[subname] = sub
                self.listWidget_sub.addItem(subname)

    def input_sub_del_one(self):
        try:
            sub = self.listWidget_sub.currentItem().text()
            self.listWidget_sub.takeItem(self.listWidget_sub.currentRow())
            del input_sub_dict[sub]
        except:
            print('error')

    def input_sub_del_all(self):
        try:
            self.listWidget_sub.clear()
            input_sub_dict.clear()
        except:
            print('error')

    def input_sub_pass(self):
        count = self.listWidget_sub.currentRow()
        self.listWidget_sub.insertItem(count, '此视频不添加内嵌字幕')

    def input_sub_up(self):
        try:
            count = self.listWidget_sub.currentRow()
            uptext = self.listWidget_sub.currentItem().text()
            self.listWidget_sub.takeItem(count)
            self.listWidget_sub.insertItem(count - 1, uptext)
            if self.listWidget_sub.currentRow() > 0:
                self.listWidget_sub.setCurrentRow(count - 1)
        except:
            print('error')

    def input_sub_down(self):
        try:
            count = self.listWidget_sub.currentRow()
            downtext = self.listWidget_sub.currentItem().text()
            self.listWidget_sub.takeItem(count)
            self.listWidget_sub.insertItem(count + 1, downtext)
            if self.listWidget_sub.currentRow() < self.listWidget_sub.count():
                self.listWidget_sub.setCurrentRow(count + 1)
        except:
            print('error')

    def start(self):
        self.pushButton_start.setEnabled(False)
        if self.listWidget_files_input.count() == 0 :
            self.pushButton_start.setEnabled(True)
        else:
            file_count = self.listWidget_files_input.count()
            if self.groupBox_encode.clicked:
                if self.radioButton_encode_libx264.isChecked():
                    radio = ' -c:v libx264'
                elif self.radioButton_encode_libx265.isChecked():
                    radio = ' -c:v libx265'
                elif self.radioButton_encode_h264_nvenc.isChecked():
                    radio = ' -c:v h264_nvenc'
                elif self.radioButton_encode_hevc_nvenc.isChecked():
                    radio = ' -c:v hevc_nvenc'
                elif self.radioButton_encode_cust.isChecked():
                    radio = self.lineEdit_encode_cust.text()
                encode = radio
            else:
                encode = ''
            if self.groupBox_rate.clicked:
                if self.radioButton_rate_rate.isChecked():
                    bv = ' -b:v %s' % self.lineEdit_rate_rate.text()
                else:
                    bv = ''
                if self.radioButton_rate_bufsize.isChecked():
                    buf = ' -bufsize %s' % self.lineEdit_rate_bufsize.text()
                else:
                    buf = ''
                if self.radioButton_rate_max.isChecked():
                    max = ' -maxrate %s' % self.lineEdit_rate_max.text()
                else:
                    max = ''
                if self.radioButton_rate_cust.isChecked():
                    cust = ' %s' % self.lineEdit_rate_cust.text()
                else:
                    cust = ''
                rate = bv + buf + max + cust
            else:
                rate = ''
            #for number in range(file_count):
            #    filename = self.listWidget_files_input.item().text()


    def stop(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = MainWindow()
    ma.show()
    sys.exit(app.exec_())
