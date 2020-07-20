#bin/python
#client


import sys
import socket
import select
import signal

def sigint_handler(signum, frame):
    print '\n user interrupt ! shutting down'
    print "[info] shutting down Chat server \n\n"
    sys.exit()  
    

signal.signal(signal.SIGINT, sigint_handler)
 
def chat_client():
    if(len(sys.argv) < 4) :
        print 'Usage : python client.py hostname port Name'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    uname=sys.argv[3]
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Sorry , Unable to connect Check Ip or Port'
        sys.exit()
     
    print 'Connected to Chat server . You can start sending messages'
    sys.stdout.write('[Me :] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                msg = '['+ uname + ':]' +msg
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
