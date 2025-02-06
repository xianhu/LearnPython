import socket
import threading

"""服务器"""
def main():
    #建立字节流套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #设置端口复用
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = ('127.0.0.1', 9999)
    #套接字绑定地址，端口号
    s.bind(addr)
    print("----------快乐聊天室已开启----------")
    #地址：用户名
    user = {}
    while True:
        try:
            data, addr = s.recvfrom(1024)

            #新用户
            if not addr in user:
                #判断是否重名
                if data.decode('utf-8') in user.values():
                    s.sendto('用户名已存在!'.encode(), addr)
                    continue
                else:
                    s.sendto('OK'.encode(), addr)
                #给其他用户发送欢迎信息
                for address in user:
                    s.sendto(data + ' 进入聊天室...'.encode(), address)
                user[addr] = data.decode('utf-8')
                print('聊天室当前人数：%s' % len(user))
                continue

            #退出聊天室
            if 'EXIT' in data.decode('utf-8'):
                name = user[addr]
                user.pop(addr)
                for address in user:
                    s.sendto((name + ' 离开了聊天室...').encode(), address)
                print('聊天室当前人数：%s' % len(user))
            else:
                print('"%s" from %s:%s' %
                      (data.decode('utf-8'), addr[0], addr[1]))
                for address in user:
                    if address != addr:
                        s.sendto(data, address)

        except ConnectionResetError:
            raise Exception('Someone left unexcept')

if __name__ == '__main__':
    main()


"""客户端"""
def recv(sock, addr):
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


def send(sock, name, addr):
    while True:
        string = input()
        message = name + ' : ' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string == 'EXIT':
            break

def main():
    #创建udp套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ('127.0.0.1', 9999)
    print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----")
    name = input('请输入你的名称:')
    #判断名字是否重复
    while True:
        s.sendto(name.encode('utf-8'), server)
        data = s.recv(1024)
        if data.decode('utf-8') == '用户名已存在!':
            print('用户名已存在，请重新输入!')
            name = input('请输入你的名称:')
            continue
        elif data.decode('utf-8') == 'OK':
            break
    print('-----------------%s------------------' % name)
    #建立两个子进程，分别用于接收数据和发送数据，其中接受线程是守护线程
    pr = threading.Thread(target=recv, args=(s, server), daemon=True)
    ps = threading.Thread(target=send, args=(s, name, server))
    #子进程运行
    pr.start()
    ps.start()
    #阻塞主进程，等待发送线程完成
    ps.join()
    s.close()

if __name__ == '__main__':
    main()
