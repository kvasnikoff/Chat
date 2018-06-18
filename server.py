from socket import AF_INET, socket, SOCK_STREAM #AF_INET для сетевого протокола IPv4 #
from threading import Thread #SOCK_STREAM (надёжная потокоориентированная служба (сервис) или потоковый сокет)


def accept_incoming_connections():
    #ожидаем в бесконеном цикле подключение клиента
    while True:
        client, client_address = SERVER.accept() #ждет появление входящего соед. и возвращает новый сокет и адресс клиента
        print("%s:%s присоединился." % client_address)
        client.send(bytes("Успешно подключено! Введите свое имя и нажмите «enter»!", "utf8")) #закодировав, отправл. данные
        addresses[client] = client_address #сохраняет адрес клиента в словаре
        Thread(target=handle_client, args=(client,)).start() #передаем: имя функции, которая будет исполняться в потоке, параметры, которые передаем в функцию + запускаем поток


def handle_client(client):  # принимает сокет клиента как аргумент"

    name = client.recv(BUFSIZ).decode("utf8") #декодируем принятые байты с именем
    welcome = 'Добро пожаловать, %s! Для выхода отправьте {quit}.' % name #отправляем клиенту приветственное сообщение
    client.send(bytes(welcome, "utf8"))
    msg = "%s присоединился к чату!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name #сохраняем сокет клиента в словаре

    while True: #принимаем данные в бесконечном цикле
        msg = client.recv(BUFSIZ) #recv принимает байты для чтения.
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s вышел из чата." % name, "utf8"))
            break


def broadcast(msg, prefix=""): #prefix принимает имя клиента для отображения в чате
    #отправляем сообщение всем клиентам

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = '127.0.0.1' #localhost
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT) #кортеж с хостом и портом, который привяжем к сокету

SERVER = socket(AF_INET, SOCK_STREAM) #создаем сокет
SERVER.bind(ADDR) #привязываем сокет. принимает хост и порт

if __name__ == "__main__": #код будет исполняться только при условии, что данный модуль запущен как программа, и запретить исполнять его, если его хотят импортировать и использовать функции модуля отдельно.
    SERVER.listen(5) #максимальное количество подключений в очереди
    print("Ожидается подключение...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join() #не позволяем выполнять следующее, пока не выполнится thread, чтобы сервер не закрылся
    SERVER.close() #закрываем соединение