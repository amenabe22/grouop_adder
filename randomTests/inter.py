from subprocess import Popen, PIPE

process1 = Popen(['python3','test1.py'], stdin=PIPE, stdout=PIPE)
process1.communicate(input='something')
