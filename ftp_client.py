# ftp_client.py
#　ftp文件服务　客户端
from socket import *
import sys

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

class FTPClient:
    """docstring for FTPClient"""
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")
        data = self.sockfd.recv(128).decode()
        if data == "ok":
            data = self.sockfd.recv(4096).decode()
            print(data)
        else:
            print(data)
    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self,filename):
        name ="G "+filename
        self.sockfd.send(name.encode())
        data = self.sockfd.recv(128).decode()
        print(data)
        if data == "ok":
            f = open(filename,"wb")
            while True:
                data = self.sockfd.recv(1024)
                if not data or data == b"##":
                    f.close()
                    return
                f.write(data)
        else:
            print(data)

    def do_upload(self,filename):
        name ="P "+filename
        self.sockfd.send(name.encode())
        data = self.sockfd.recv(128)
        if data == b"ok":
            f = open(filename,"rb")
            while True:
                data = f.read(1024)
                if not data:
                    self.sockfd.send(b"##")
                    f.close()
                    return
                self.sockfd.send(data)

        else:
            print(data.decode())

def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return

    ftp = FTPClient(sockfd)

    while True:
        print("\n========命令选项=========")
        print("*****      list      *****")
        print("*****    get file    *****")
        print("*****    put file    *****")
        print("*****      quit      *****")
        print("===========================")
        cmd = input("请输入命令：")
        if cmd == "list":
            ftp.do_list()
        elif cmd == "quit":
            ftp.do_quit()
        elif cmd[:3] == "get":
            filename = cmd.split(" ")[-1]
            ftp.do_get(filename)
        elif cmd[:3] == "put":
            filename = cmd.split(" ")[-1]
            ftp.do_upload(filename)
        else:
            print("请输入正确的命令")


if __name__ == "__main__":
    main()