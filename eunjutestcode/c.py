B
i# -*- coding: utf-8 -*- 

import socket
import sys
import time
import base64
import subprocess

if __name__ == '__main__':
    HOST = '' #all available interfaces
    PORT = 2222
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
        sys.exit()
    print ('Socket bind complete')

    s.listen(10)
    print ('Socket now listening')

    while(1):   # loop 
        while 1:
            #4. Accept connection
            conn, addr = s.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))

            for i in range(1, 4):
                #5. Read/Send
                img = ""
                len_data = conn.recv(1024).decode()
                len_data = int(len_data)
                size = 0

                print("Data Reading") 

                while 1:
                    data = conn.recv(65536)
                    str_data = data.decode()
                    img += data.decode()
                    size += len(str_data)
                    if size == len_data:
                        print("Finished Data Reading")
                        break

                with open('/root/openface/temp/test_'+str(i)+'.jpeg', 'wb') as f:
                    f.write(base64.b64decode(img))
                time.sleep(0.1)

            break

        res_list = {}

        for j in range(1,4):
            # start face recognigionc
            res=subprocess.check_output(['/root/openface/demos/classifier_test.py infer /root/openface/embedding/us/classifier.pkl /root/openface/temp/test_'+str(j)+'.jpeg'], universal_newlines=True,shell=True)
            print("res: {}".format(res))
    
            # store recognition result
            name, accuracy = res.split(':')
            accuracy = float(accuracy)

            if accuracy > 0.5:
                if name in res_list.keys():
                    res_list[name][1] += 1
                    if res_list[name][0] < accuracy:
                        res_list[name][0] = accuracy
                else:
                    res_list[name] = [accuracy, 1]

            print("res_list: {}".format(res_list))

        if not res_list:
            print("stranger")
        else:
            res_list = sorted(res_list.items(), key = lambda x: (x[1][1], x[1][0]), reverse = True)
            print("final res: {}".format(res_list[0][0]))
    
        print("--------------end----------------")

    conn.close()
    s.close()

