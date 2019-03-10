from socket import *
import sys,time

#具体功能
class FtpClient(object):
    def __init__(self,s):
        self.s = s

    def do_list(self):
        self.s.send(b'L')#发送请求
        #等待回复
        data = self.s.recv(128).decode()
        if data == 'OK':
            data = self.s.recv(4096).decode()
            files = data.split(',')
            for file in files:
                print(file)
        else:
            #无法完成操作
            print(data)

    def do_get(self,filename):
        self.s.send(("G "+filename).encode())
        data = self.s.recv(128).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            while True:
                data = self.s.recv(1024)
                if data == b"##":
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)
        # return

    def do_put(self,filename):
        try:
            fd = open(filename,'rb')
        except IOError:
            print("文件不存在")
            return
        #获取真是文件名，对路径解析
        filename = filename.split('/')[-1]
        self.s.send(("P "+filename).encode())
        data = self.s.recv(128).decode()
        if data == 'OK':
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.s.send(b'##')
                    break
                self.s.send(data)
            fd.close()
        else:
            print(data)
        return


    def do_quit(self):
        self.s.send(b'Q')
        self.s.close()
        sys.exit("谢谢使用")

#网络连接
def main():
    server_addr = ('176.13.10.241',8888)
    s = socket()
    try:
        s.connect(server_addr)
    except Exception as e:
        print("连接服务器失败",e)
        return

    #创建文件处理类对象
    ftp = FtpClient(s)

    while True:
        print("\n******************命令选项******************")
        print("***                list                  ***")
        print("***               get file               ***")
        print("***               put file               ***")
        print("***                 quit                 ***")

        cmd = input("输入命令>>")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        else:
            print("请输入正确命令")

if __name__ == "__main__":
    main()




