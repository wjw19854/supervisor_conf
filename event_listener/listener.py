import sys
from util.email_util import send_email_smtp
import conf
import logging


def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while True:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line and print it to stderr
        line = sys.stdin.readline()
        write_stderr(line)
        # read event payload and print it to stderr
        headers = dict([x.split(':') for x in line.split()])
        data = sys.stdin.read(int(headers['len']))
        data_l1 = data.split('\n')
        data_sp = dict([x.split(':') for x in data_l1[0].split()])
        write_stderr(data)
        if headers['eventname'] in ('PROCESS_STATE_FATAL', 'PROCESS_LOG_STDERR'):
            send_email_smtp(
                conf.email_to,
                'program:{program} {event}'.format(
                    program=data_sp['processname'],
                    event=headers['eventname']),
                data.replace('\n','<br>'))

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
