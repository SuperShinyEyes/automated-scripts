import socket
import subprocess, os, sys


def check(p):
    rv = p.poll()
#     if rv:
#         raise Fatal('%r returned %d' % (self.argv, rv))

python_path = os.path.dirname(os.path.dirname(__file__))
argvbase = ([sys.executable, "hello.py"])

argv_tries = [
            ['ssh', 'kosh', 'python < ./hello.py' #'sudo', '-p', '[local sudo] Password: '
        ] + ['ls']
]

(s1, s2) = socket.socketpair()

def setup():
    # run in the child process
    s2.close()
e = None
if os.getuid() == 0:
	print("os.getuid() == 0")
	argv_tries = argv_tries[-1:]  # last entry only
for argv in argv_tries:
    try:
        if argv[0] == 'su':
            print(argv)
            sys.stderr.write('[local su] ')
        else:
            print("No write to stderr")
        print("Create Popen")    
        p = subprocess.Popen(argv, stdout=s1, preexec_fn=setup)
        e = None
        break
    except OSError as e:
        print("OSERROR")
        pass

s1.close()
if sys.version_info < (3, 0):
    # python 2.7
    pfile = s2.makefile('wb+')
else:
    # python 3.5
    pfile = s2.makefile('rwb')
line = pfile.readline()
#check(p)

# if line[0:5] != b'READY':
#     raise Fatal('%r expected READY, got %r' % (argv, line))
# method_name = line[6:-1]
# method = get_method(method_name.decode(ASCII))

# method.set_firewall()
print("close")
pfile.close()
p.wait()