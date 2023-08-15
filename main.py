import socket
import random
import flask
import threading
app=flask.Flask(__name__)
@app.route("/")
def index():
    return "Hello World!"
def app_run():
    app.run("0.0.0.0",80)
app_thread=threading.Thread(target=app_run)
app_thread.start()
with open("log.txt","w") as f:
    f.write("")
sock=[None for i in range(1000000)]
s=socket.socket()
host="0.0.0.0"
port=4514
s.bind((host,port))
s.listen(5)
def b(c):
    uid=random.randint(0,1000000)
    while sock[uid]:
        uid=random.randint(0,1000000)
    sock[uid]=c
    try:
        while 1:
            a=c.recv(20).decode()
            with open("log.txt","a") as f:
                f.write("{} {}\n".format(uid,a))
            print("{} {}".format(uid,a))
            a=a.split()
            if a[0]=="new":
                c.send(bytes(str(uid),encoding="utf-8"))
            elif a[0]=="send":
                uid=int(a[1])
                sock[uid].send(bytes(a[2],encoding="utf-8"))
            elif a[0]=="exit":
                break
    except:
        pass
    sock[uid]=None
    c.close()
while 1:
    c,addr=s.accept()
    a=threading.Thread(target=b,args=(c,))
    a.start()
f.close()
