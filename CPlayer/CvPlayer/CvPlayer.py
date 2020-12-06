import os,sys,platform
os.environ['PYTHON_VLC_MODULE_PATH']='vlc'
import vlc
from threading import Thread
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu,QAction,QMessageBox,QApplication,QMainWindow,QFileDialog,QDesktopWidget
from Ui_CPlayer import Ui_MainWindow
class Window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Listadd()
        self.step=0
        self.loop=1
        self.flag=self.listtag=self.fulltag=True
        self.player=vlc.MediaPlayer()
        screen=QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move(int((screen.width()-size.width())/2),int((screen.height()-size.height())/2))
    def resizeEvent(self,event):
        self.ratio()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_P:
            self.Listhide()
        if event.key()==Qt.Key_T:
            self.Fastback()
        if event.key()==Qt.Key_L:
            self.Loop()
        if event.key()==Qt.Key_Space:
            self.Play()
        if event.key()==Qt.Key_S:
            self.Stop()
        if event.key()==Qt.Key_F:
            self.Full()
        if event.key()==Qt.Key_J:
            self.Fastforward()
        if event.key()==Qt.Key_M:
            self.Mute()
        if event.key()==Qt.Key_A:
            self.svolume.setValue(self.svolume.value()+1)
        if event.key()==Qt.Key_R:
            self.svolume.setValue(self.svolume.value()-1)
    def eventFilter(self,sender,event):
        if (event.type()==event.ChildRemoved):
            self.Moved()
        return False
    def Listmenu(self,position):
        lm=QMenu()
        addact=QAction("添加到播放列表",self,triggered=self.Add)
        removeact=QAction("从播放列表移除",self,triggered=self.Remove)
        renameact=QAction('重命名',self,triggered=self.Rename)
        clearact=QAction('清空播放列表',self,triggered=self.Clear)
        saveact=QAction('保存当前播放列表',self,triggered=self.Saved)
        lm.addAction(addact)
        if self.list.itemAt(position):
            lm.addAction(removeact)
            lm.addAction(renameact)
        lm.addAction(clearact)
        lm.addAction(saveact)
        lm.exec_(self.list.mapToGlobal(position))
    def Listadd(self):
        self.l=[]
        self.list.installEventFilter(self)
        if os.path.isfile('CPlayerlist.txt'):
            with open('CPlayerlist.txt') as f:
                for i in f:
                    i=i.strip()
                    name=i[0:i.find(',')]
                    filelist=i[i.find(',')+1:len(i)]
                    self.list.addItem(name)
                    self.l.append(filelist)
    def Add(self):
        filelists,_=QFileDialog.getOpenFileNames(self,'添加到播放列表','.','媒体文件(*)')
        for filelist in filelists:
            name=filelist[filelist.rfind('/')+1:filelist.rfind('.')]
            self.list.addItem(name)
            self.l.append(filelist)
    def Remove(self):
        ltmp=[]
        for i in self.list.selectedIndexes():
            ltmp.append(i.row())
        ltmp.sort(reverse=True)
        for j in ltmp:
            self.list.takeItem(j)
            self.l.pop(j)
    def Rename(self):
        item=self.list.item(self.list.currentRow())
        item.setFlags(item.flags()|Qt.ItemIsEditable)
        self.list.editItem(item)
    def Clear(self):
        self.l=[]
        self.list.clear()
        if os.path.isfile('CPlayerlist.txt'):
            os.remove('CPlayerlist.txt')
    def Drag(self):
        self.tmp1=[]
        self.tmp2=self.l[:]
        for i in range(self.list.count()):
            self.tmp1.append(self.list.item(i).text())
    def Moved(self):
        for i in range(self.list.count()):
            if self.list.item(i).text()==self.tmp1[i]:
                continue
            else:
                self.l[i]=self.tmp2[self.tmp1.index(self.list.item(i).text())]
    def Saved(self):
        with open('CPlayerlist.txt','w') as f:
            for i in range(self.list.count()):
                f.write('%s,%s\n'%(self.list.item(i).text(),self.l[i]))
        QMessageBox.information(self,'保存','播放列表保存成功！')
    def Listhide(self):
        if self.listtag:
            self.frame.hide()
            self.listtag=False
        else:
            self.frame.show()
            self.listtag=True
        self.ratio()
    def ratio(self):
        QApplication.processEvents()
        self.player.video_set_aspect_ratio('%s:%s'%(self.lmedia.width(),self.lmedia.height()))
    def Loop(self):
        if self.loop==0:
            self.loop=1
            self.bloop.setIcon(QIcon(r'img\withloop.png'))
            self.bloop.setToolTip('循环播放，快捷键“l”')
        else:
            self.loop=0
            self.bloop.setIcon(QIcon(r'img\withoutloop.png'))
            self.bloop.setToolTip('取消循环，快捷键“l”')
    def set_window(self,winid):
        if platform.system()=='Windows':
            self.player.set_hwnd(winid)
        elif platform.system()=='Linux':
            self.player.set_xwindow(winid)
        else:
            self.player.set_nsobject(winid)
    def Play(self):
        if self.flag:
            try:
                self.playitem=self.l[self.list.currentRow()]
                self.player.set_mrl("%s"%self.playitem)
                self.set_window(int(self.lmedia.winId()))
                self.ratio()
                self.player.play()
                self.timer=QTimer()
                self.timer.start(100)
                self.timer.timeout.connect(self.Show)
                self.steptimer=QTimer()
                self.steptimer.start(1000)
                self.steptimer.timeout.connect(self.Step)
                self.flag=False
                self.bplay.setIcon(QIcon(r'img\pause.png'))
                self.bplay.setToolTip('暂停，快捷键“Space”')
            except:
                QMessageBox.warning(self,'错误','找不到要播放的文件！')
        else:
            if self.l[self.list.currentRow()]==self.playitem:
                if self.player.is_playing():
                    self.player.pause()
                    self.steptimer.stop()
                    self.bplay.setIcon(QIcon(r'img\play.png'))
                    self.bplay.setToolTip('播放，快捷键“Space”')
                else:
                    self.player.play()
                    self.steptimer.start()
                    self.bplay.setIcon(QIcon(r'img\pause.png'))
                    self.bplay.setToolTip('暂停，快捷键“Space”')
            else:
                self.playitem=self.l[self.list.currentRow()]
                self.step=0
                self.stime.setValue(0)
                self.player.set_mrl("%s"%self.playitem)
                self.player.play()
                self.timer.start()
                self.steptimer.start()
                self.bplay.setIcon(QIcon(r'img\pause.png'))
                self.bplay.setToolTip('暂停，快捷键“Space”')
    def Show(self):
        self.mediatime=self.player.get_length()/1000
        self.stime.setMaximum(int(self.mediatime))
        mediamin,mediasec=divmod(self.mediatime,60)
        mediahour,mediamin=divmod(mediamin,60)
        playmin,playsec=divmod(self.step,60)
        playhour,playmin=divmod(playmin,60)
        self.ltime.setText('%02d:%02d:%02d/%02d:%02d:%02d'%(playhour,playmin,playsec,mediahour,mediamin,mediasec))
    def Stop(self):
        if self.flag==False:
            Thread(target=self.Threadstop,daemon=True).start()
            self.timer.stop()
            self.steptimer.stop()
            self.step=0
            self.loop=1
            self.flag=True
            self.stime.setValue(0)
            self.ltime.setText('')
            self.bplay.setIcon(QIcon(r'img\play.png'))
            self.bplay.setToolTip('播放，快捷键“Space”')
    def Threadstop(self):
        self.player.stop()
    def Full(self):
        if self.fulltag:
            self.frame.hide()
            self.frame_2.hide()
            self.showFullScreen()
            self.bfull.setIcon(QIcon(r'img\exitfullscreen.png'))
            self.bfull.setToolTip('退出全屏，快捷键“f”')
            self.fulltag=False
        else:
            self.frame.show()
            self.frame_2.show()
            self.showNormal()
            self.bfull.setIcon(QIcon(r'img\expandfullscreen.png'))
            self.bfull.setToolTip('全屏，快捷键“f”')
            self.fulltag=True
    def Curvol(self):
        self.curvol=self.svolume.value()
    def Mute(self):
        if self.flag==False:
            if self.player.audio_get_volume()!=0:
                self.player.audio_set_volume(0)
                self.bmute.setIcon(QIcon(r'img\withoutvolume.png'))
                self.bmute.setToolTip('取消静音，快捷键“m”')
                self.tag=False
            else:
                if self.svolume.value()!=0:
                    self.player.audio_set_volume(self.svolume.value())
                else:
                    self.player.audio_set_volume(self.curvol)
                    self.svolume.setValue(self.curvol)
                self.bmute.setIcon(QIcon(r'img\withvolume.png'))
                self.bmute.setToolTip('静音，快捷键“m”')
                self.tag=True
    def Volume(self):
        if self.flag==False:
            if self.svolume.value()==0:
                self.bmute.setIcon(QIcon(r'img\withoutvolume.png'))
                self.bmute.setToolTip('取消静音，快捷键“m”')
            else:
                self.bmute.setIcon(QIcon(r'img\withvolume.png'))
                self.bmute.setToolTip('静音，快捷键“m”')
            self.player.audio_set_volume(self.svolume.value())
    def Step(self):
        if self.step>=int(self.mediatime):
            self.step=int(self.mediatime)
            if self.loop==0:
                self.step=0
                self.stime.setValue(0)
                self.flag=True
                self.Play()
            else:
                if not self.player.is_playing() and self.player.get_state!=vlc.State.Paused:
                    self.Stop()
        else:
            self.step+=1
            self.stime.setValue(self.step)
    def Slidechanged(self):
        self.step=self.stime.value()
    def Slidemoved(self):
        if self.flag==False:
            self.player.set_position(self.step/int(self.mediatime))
    def Fastforward(self):
        if self.flag==False:
            self.step+=10
            if self.step>=int(self.mediatime):
                self.stime.setValue(int(self.mediatime))
            self.stime.setValue(self.step)
            self.player.set_position(self.step/int(self.mediatime))
    def Fastback(self):
        if self.flag==False:
            self.step-=10
            if self.step<=0:
                self.step=0
                self.stime.setValue(0)
            self.stime.setValue(self.step)
            self.player.set_position(self.step/int(self.mediatime))
if __name__=='__main__':
    app=QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())