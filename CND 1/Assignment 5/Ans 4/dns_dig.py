import subprocess
import shlex

for i in range(0,100):
    cmd='dig @127.0.0.1 z.tiwaz.net'
    proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
    out,err=proc.communicate()
    print(out)
