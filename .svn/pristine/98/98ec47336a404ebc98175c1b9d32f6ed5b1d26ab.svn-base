import subprocess
import shlex
import os
from flask import Flask
from subprocess import call

app = Flask(__name__)

@app.route('/',methods=['GET',])
def home():
    # subprocess.call(["sh", "/var/www/html/svn_scopiq/some.sh"])
    # subprocess.call(shlex.split('./some.sh Zoho_Corporation 5002'))
    # os.system('./some.sh')
    # print('Welcome')
    
    # arg1 = '5003'
    # bashCommand = "/bin/bash some.sh " + arglist 
    # bashCommand = "./some.sh" + arglist
    # bashCommand = 'sh', '/var/www/html/svn_scopiq/some.sh'
    # os.system("./some.sh")
    # os.system('sh /var/www/html/svn_scopiq/some.sh')
    # subprocess.Popen(["/bin/sh", "/var/www/html/sample.sh"])
    # file = 'var\\www\\html\\filename.exe'
    # os.system('"' + file + '"')
    # os.system("/var/www/html/sample.sh")
    subprocess.Popen(
    ['/usr/bin/python /var/www/html/svn_scopiq/runserver.py'],             
    shell=True,
    stdout=subprocess.PIPE
    )
    val = 'Success'
    return val
    
host = "127.0.0.1"
port = "5004"
app.run(debug=True,host=host,port=port)
