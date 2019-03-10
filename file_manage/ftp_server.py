'''
ftp文件服务器
fork server训练
'''
from socket import *
import os,sys
import signal
import time

#全局变量
HOST = '176.13.10.88'
PORT = 2018
ADDR = (HOST,PORT)
FILE_PATH = '/home/tarena/test/'

class FtpServer(object):
    def __init__(self,c):
        self.c = c

    def do_list(self):
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self .c.send("文件库为空".encode())
            return
        else:
            self.c.send(b'OK')#防止粘包做个延迟
            time.sleep(1)

        files = ""
        for file in file_list:
            if file[0] != '.' and os.path.isfile(FILE_PATH+file):
                files = files + file + ','
        #将拼接好的字符串传给客户端
        self.c.send(files.encode())
        
    def do_get(self,filename):
        try:
            fd = open(FILE_PATH+filename,'rb')
        except IOError:
            self.c.send('文件不存在'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)
            #发送文件内容
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.c.send(b'##')
                    break
                self.c.send(data)

    def do_put(self,filename):
        if os.path.exists(FILE_PATH+filename):
            self.c.send('文件已存在'.encode())
            return
        fd = open (FILE_PATH+filename,'wb')
        self.c.send(b'OK')
        time.sleep(0.1)
        while True:
            data = self.c.recv(1024)
            if data == b"##":
                break
            fd.write(data)
        fd.close()


def do_request(c):
    ftp = FtpServer(c)
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'Q':
            c.close()
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == 'G':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0] == 'P':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)

#网络搭建
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Watting for connect...")

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("Error:",e)
            continue
        print("连接客户端：",addr)
        
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_request(c)
            os._exit(0)
        else:
            c.close()
        
if __name__ == "__main__":
    main()




