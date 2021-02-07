# @Author: michael
# @Date:   01-Jan-1970
# @Filename: blueberry_sendTask.py
# @Last modified by:   michael
# @Last modified time: 31-Jan-2021
# @License: GNU GPL v3

import argparse

import zmq

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.connect("tcp://127.0.0.1:5555")

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--task", help="specify task", type=str,
                    choices=["hids", "nids"], required=True)
parser.add_argument("-m", "--message", help="specify message", type=str)


args = parser.parse_args()

message = args.message.replace("+", "-")
mq_message = bytes('{}+{}'.format(args.task, message), 'utf-8')
sender.send(mq_message)
