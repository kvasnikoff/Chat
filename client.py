from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive(): #получаем сообщения
    while True: #нон-стоп
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") #докодируем байты
            msg_list.insert(tkinter.END, msg) #отправляем сообщение в массив, чтобы отображать на экране
        except OSError:  # на случай, если клиент покинул чат
            break


def send(event=None): #отправка сообщений
    msg = my_msg.get() #когда нажимает "send", получаем информацию с mymsg (поле с сообщением)
    my_msg.set("")  # очищаем mymsg
    client_socket.send(bytes(msg, "utf8")) #отправляем сообщение на сервер (а он посылает всем)
    if msg == "{quit}": #выход
        client_socket.close()
        top.quit()


def on_closing(event=None):
    #вызывается, когда закрываем окно
    my_msg.set("{quit}")
    send()

top = tkinter.Tk() #создаем окно
top.title("Чат")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  #переменная типа string для отправки сообщений
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  #скроллбар для навигации к прошлым сообщениям
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set) #содержит сообщения
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH) #упаковываем все для tkinter
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg) #entry для ввода сообщений
entry_field.bind("<Return>", send) #привязываем отправку на кнопку "enter"
entry_field.pack()
send_button = tkinter.Button(top, text="Отправить", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing) #очищает все при выходе

HOST = input('Укажите host: ')
PORT = input('Укажите port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024 #передаем сообщения по размеру
ADDR = (HOST, PORT) #картеж

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR) #подключение к серверу

receive_thread = Thread(target=receive) #поток для получения сообщений
receive_thread.start()
tkinter.mainloop()  #интерфейс работает до закрытия