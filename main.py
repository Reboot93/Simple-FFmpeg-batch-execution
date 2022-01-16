import sys, time, _thread, os, subprocess, shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from windows import Ui_Form
from dialog import Ui_Dialog_start_confirm

# ===== 默认参数 =======
ffmpeg_dir = ''
files_out_dir = ''

input_files_dict = {}
input_sub_dict = {}
command_list = []

mission_all = 0
mission_now = 0
run_flag = 0
flash_flag = 0


class cmd(QThread):
    progressbar_set_signal = pyqtSignal(int)
    progressbar_setvalue_signal = pyqtSignal(int)
    textedit_claer_signal = pyqtSignal()
    textedit_edit_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.finished.connect(self.finish)

    def run(self):
        global mission_all, mission_now, command_list
        # self.progressBar.setRange(0, len(command_list))
        self.progressbar_set_signal.emit(len(command_list))
        mission_all = len(command_list)
        i = 1
        for command in command_list:
            mission_now = i
            self.textedit_claer_signal.emit()
            # self.textEdit_now.setText(command)
            self.textedit_edit_signal.emit(command)
            subprocess.call(command, shell=False)
            # self.progressBar.setValue(i)
            self.progressbar_setvalue_signal.emit(i)
            i = i + 1
        command_list.clear()

    def finish(self):
        self.finish_signal.emit()


class dialogWindow(QDialog, Ui_Dialog_start_confirm):

    def __init__(self, parent=None):
        super(dialogWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('请确认')
        self.listWidget_out_confirm.addItems(command_list)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())


class MainWindow(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('简易ffmpeg批量执行工具 V0.1')
        self.CMD = cmd()
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

        # ==/ 耗时线程信号定义 / ===========
        self.CMD.progressbar_set_signal.connect(self.progressbar_set)
        self.CMD.progressbar_setvalue_signal.connect(self.progressbar_setvalue)
        self.CMD.textedit_claer_signal.connect(self.textedit_claer)
        self.CMD.textedit_edit_signal.connect(self.textedit_edit)
        self.CMD.finish_signal.connect(self.thread_finish)

        # ==/ 界面初始化 /==========
        # self.show_potdir.setText(pot_dir)
        self.label_num_all.setText(str(mission_all))
        self.label_num_now.setText(str(mission_now))
        self.progressBar.setRange(0, 10)

    def flash(self):
        self.label_num_now.setText(str(mission_now))
        self.label_num_all.setText(str(mission_all))
        self.lineEdit_ffmpeg_dir.setText(ffmpeg_dir)
        self.lineEdit__out_dir.setText(files_out_dir)

    def progressbar_set(self, i):
        self.progressBar.setRange(0, i)
        self.progressBar.setValue(0)

    def progressbar_setvalue(self, i):
        self.progressBar.setValue(i)

    def textedit_claer(self):
        self.textEdit_now.clear()
        self.flash()  # 更新界面中的label

    def textedit_edit(self, command):
        self.textEdit_now.setText(command)

    def thread_finish(self):
        self.pushButton_start.setEnabled(True)

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
        global command_list, input_files_dict, input_sub_dict, run_flag, mission_now, mission_all
        self.pushButton_start.setEnabled(False)
        if self.listWidget_files_input.count() == 0:
            self.pushButton_start.setEnabled(True)
        else:
            file_count = self.listWidget_files_input.count()
            if self.groupBox_encode.isChecked():
                if self.radioButton_encode_libx264.isChecked():
                    radio = ' -c:v libx264'
                elif self.radioButton_encode_libx265.isChecked():
                    radio = ' -c:v libx265'
                elif self.radioButton_encode_h264_nvenc.isChecked():
                    radio = ' -c:v h264_nvenc'
                elif self.radioButton_encode_hevc_nvenc.isChecked():
                    radio = ' -c:v hevc_nvenc'
                elif self.radioButton_encode_hevc_qsv.isChecked():
                    radio = ' -c:v hevc_qsv'
                elif self.radioButton_encode_cust.isChecked():
                    radio = self.lineEdit_encode_cust.text()
                encode = radio
            else:
                encode = ''
            if self.groupBox_rate.isChecked():
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
            if self.groupBox_extra.isChecked():
                extra = ' %s' % self.textEdit_extra.toPlainText()
            else:
                extra = ''
            # if self.groupBox_file_outname.isChecked():
            #    out_name = self.lineEdit_file_outname.text()
            # else:
            #    out_name = ''
            if self.groupBox_out_dir.isChecked():
                out_dir = self.lineEdit__out_dir.text()
            else:
                out_dir = ''
            for number in range(file_count):
                filename = self.listWidget_files_input.item(number).text()
                if self.groupBox_files_sub.isChecked() and self.listWidget_sub.count() != 0:
                    if self.listWidget_sub.item(number).text() != '此视频不添加内嵌字幕':
                        sub = ' -i %s' % input_sub_dict[self.listWidget_sub.item(number).text()]
                    else:
                        sub = ''
                else:
                    sub = ''
                if self.groupBox_out_dir.isChecked():
                    file_out = out_dir \
                               + input_files_dict[filename][input_files_dict[filename].rfind('/'):]
                    print(file_out)
                else:
                    file_out = input_files_dict[filename]
                if self.radioButton_out_mkv.isChecked():
                    file_out = file_out[:file_out.rfind('.')] + '.mkv'
                if self.radioButton_out_cust.isChecked():
                    file_out = file_out[:file_out.rfind('.')] + self.lineEdit__out_dir.text()
                if self.groupBox_file_outname.isChecked():
                    file_out = file_out[:file_out.rfind('.')] + self.lineEdit_file_outname.text() + file_out[
                                                                                                    file_out.rfind(
                                                                                                        '.'):]
                if self.groupBox_ffmpeg_dir.isChecked():
                    command = './%s -i %s%s%s%s%s %s' % (ffmpeg_dir,
                                                         input_files_dict[filename],
                                                         sub,
                                                         encode,
                                                         rate,
                                                         extra,
                                                         file_out
                                                         )
                else:
                    command = 'ffmpeg -i %s%s%s%s%s %s' % (input_files_dict[filename],
                                                           sub,
                                                           encode,
                                                           rate,
                                                           extra,
                                                           file_out
                                                           )
                command_list.append(command)
            dialog_confirm = dialogWindow()
            dialog_confirm.show()
            reply = dialog_confirm.exec_()
            del dialog_confirm
            if reply == 1:
                self.CMD.start()
            else:
                QMessageBox.information(self, '操作信息', '已取消操作，未执行命令。')
                command_list.clear()
                self.pushButton_start.setEnabled(True)

    def stop(self):
        global run_flag
        #if self.CMD.isRunning():
        #    subprocess.call('taskkill.exe /f /im ffmpeg.exe', shell=False)
        #    self.CMD.quit()
        #else:
        #    print(self.CMD.isRunning())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = MainWindow()
    ma.show()
    sys.exit(app.exec_())
