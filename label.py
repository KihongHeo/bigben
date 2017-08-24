#!/usr/bin/python3
import argparse
import logging
import logging.handlers
import os

import afl
import petablox
import rr

def add_afl_command(subparsers):
    parser = subparsers.add_parser("afl", help="lable bugs with the AFL fuzzer")
    parser.add_argument("--timeout", type = int, default = 86400)
    parser.add_argument("--test", action='store_true')
    parser.add_argument("--label-only", action='store_true')
    parser.add_argument("--output", default = os.getcwd() + '/bigben.json')

def add_petablox_command(subparsers):
    parser = subparsers.add_parser("petablox", help="lable bugs with Petablox")
    parser.add_argument("--test", action='store_true')
    parser.add_argument("--output", default = os.getcwd() + '/bigben.json')

def add_rr_command(subparsers):
    parser = subparsers.add_parser("rr", help="lable bugs with Road Runner")
    parser.add_argument("--timeout", type = int, default = 86400)
    parser.add_argument("--test", action='store_true')
    parser.add_argument("--output", default = os.getcwd() + '/bigben.json')

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    add_afl_command(subparsers)
    add_petablox_command(subparsers)
    add_rr_command(subparsers)
    return parser.parse_args()

def main():
    args = parse_args()
    logger = logging.getLogger('logger')
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler('./bigben.log')
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    if args.cmd == "afl":
        afl.run(args, logger)
    elif args.cmd == "petablox":
        petablox.run(args, logger)
    elif args.cmd == "rr":
        rr.run(args, logger)
    else:
        print("no")

if __name__ == "__main__":
    main()
