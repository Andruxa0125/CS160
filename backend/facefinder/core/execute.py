from subprocess import Popen, PIPE
import subprocess

class command():
    def init(__self__):
        self.command = command

    def execute(self, command):

        proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        try:
            outs, errs = proc.communicate(timeout=100)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        return outs.strip()

if __name__ == '__main__':
    print("lol")