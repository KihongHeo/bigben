#!/usr/bin/python3
import logging
import os
import random
import re
import shutil
import string
import subprocess
import util

afl = "AFL"

def setup():
    if os.path.exists('afl_input'):
        shutil.rmtree('afl_input')
    if os.path.exists('afl_output'):
        shutil.rmtree('afl_output')
    os.mkdir('afl_input')
    with open('afl_input/input.txt', 'w') as f:
        s = string.printable
        f.write(''.join(random.sample(s, 100)))
    os.mkdir('afl_output')

def get_afl_bug_type(msg):
    m = re.search(r'SUMMARY: AddressSanitizer: ([a-z\-]+)', msg)
    try:
        bug_type = m.group(1)
    except AttributeError:
        bug_type = "Unknown"
    return bug_type


def get_afl_bug_location(msg):
    cwd = os.getcwd()
    cwd = cwd.replace("cb-multios/build", "cb-multios")
    rexp = re.compile(cwd + '/([a-zA-Z0-9_/]+.c):([0-9]+)')
    m = re.search(rexp, msg)
    try:
        return (m.group(1), int(m.group(2)))
    except AttributeError:
        return ("Unknown", -1)

def label(args, logger, project, exe):
    inputs = [ f for f in os.listdir('afl_output/crashes') if f != 'README.txt' ]
    logger.info(str(len(inputs)) + " crashes found")
    for f in inputs:
        try:
            crash_cmd = exe + " < afl_output/crashes/" + f
            output = subprocess.Popen(crash_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = output.communicate()[1].decode(encoding="utf-8", errors="ignore")
            bug_type = get_afl_bug_type(output)
            (bug_file, bug_line) = get_afl_bug_location(output)
            util.dump(args, project, bug_file, bug_line, bug_type, afl)
        except:
            pass

def run_test(args, logger):
    project = 'test/afl'
    os.chdir(project)
    setup()
    afl_cmd = "AFL_USE_ASAN=1 afl-clang  -m32 -fno-omit-frame-pointer -fsanitize=address -g -o test src/test.c"
    output = subprocess.getoutput(afl_cmd)
    afl_cmd = "timeout " + str(args.timeout) + " afl-fuzz -m 700 -i afl_input -o afl_output ./test"
    output = subprocess.getoutput(afl_cmd)
    label(args, logger, project, './test')

def run_cgc(args, logger):
    project_root = 'cb-multios/build/challenges'
    os.chdir(project_root)
    for d in [ d for d in os.listdir('.') if os.path.isdir(d) ]:
        project = project_root + '/' + d
        logger.info("fuzzing " + project)
        logging.info("fuzzing")
        os.chdir(d)
        setup()
        afl_cmd = "timeout " + str(args.timeout) + " afl-fuzz -m 700 -i afl_input -o afl_output ./" + d
        output = subprocess.getoutput(afl_cmd)
        label(args, logger, project, "./" + d)
        os.chdir("..")

def run_cgc_label_only(args, logger):
    project_root = 'cb-multios/build/challenges'
    os.chdir(project_root)
    for d in [ d for d in os.listdir('.') if os.path.isdir(d) ]:
        project = project_root + '/' + d
        logger.info("fuzzing " + project)
        logging.info("fuzzing")
        os.chdir(d)
        try:
            label(args, logger, project, "./" + d)
        except FileNotFoundError:
            pass
        os.chdir("..")


def run(args, logger):
    if args.test:
        run_test(args, logger)
    elif args.label_only:
        run_cgc_label_only(args, logger)
    else:
        run_cgc(args, logger)
