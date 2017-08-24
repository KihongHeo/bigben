#!/usr/bin/python3
import logging
import os
import re
import shutil
import subprocess
import util

rr = "RoadRunner"

def setup():
    if os.path.exists('classes'):
        shutil.rmtree('classes')
    os.mkdir('classes')

def get_rr_bug_location(msg):
    cwd = os.getcwd()
    line = '=' * 69
    rexp = re.compile(line + '\n(## FastTrack Error.+)' + line, re.DOTALL)
    alarms = rexp.findall(msg)
    
    locations = set()
    for alarm in alarms:
        try:
            rexp = re.compile('Class: ([a-zA-Z0-9_/$]+)\n')
            m = re.search(rexp, msg)
            bug_file = m.group(1) + '.java'
            rexp = re.compile('Previous Op: [a-zA-Z]+ at [a-zA-Z_$]+.java:([0-9]+):')
            m = re.search(rexp, msg)
            bug_line1 = m.group(1)
            rexp = re.compile('Currrent Op: [a-zA-Z]+ at [a-zA-Z_$]+.java:([0-9]+):')
            m = re.search(rexp, msg)
            bug_line2 = m.group(1)
            locations.add((bug_file, int(bug_line1)))
            locations.add((bug_file, int(bug_line2)))
        except Exception:
            continue
    return locations

def label(args, logger, project, output, main):
    locations = get_rr_bug_location(output)
    logger.info(str(len(locations)) + " data races found from " + main)
    for (bug_file, bug_line) in locations:
#        try:
            bug_type = "race condition"
            print(args.output)
            util.dump(args, project, bug_file, bug_line, bug_type, rr, main=main)
#        except Exception:
#            print("error")
#            pass

def run_test(args, logger):
    project = 'test/rr'
    os.chdir(project)
    setup()
    cmd = "javac -d classes src/Test.java"
    output = subprocess.getoutput(cmd)
    cmd = "rrrun -classpath=classes -tool=FT_LOC test.Test"
    output = subprocess.getoutput(cmd)
    label(args, logger, project, output, "test.Test")

def run_benchmark(args, logger):
    project = 'java-benchmarks'
    os.chdir(project)
    dlist = [ d for d in os.listdir('.') if os.path.isdir(d) ]
    i = 1
    for d in dlist:
        logger.info("RR on " + project + "/" + d + " (" + str(i) + "/" + str(len(dlist)) + ")")
        os.chdir(d)
        with open('info/mainclasses') as f:
            mainclasses = f.read().splitlines()
        for main in mainclasses:
            rr_cmd = "rrrun -classpath=classes:lib -tool=FT_LOC -maxTime=" + str(args.timeout) + " " + main
            output = subprocess.getoutput(rr_cmd)
            with open('../../temp/' + d + '_' + main, 'w') as f:
                f.write(output)
            label(args, logger, project, output, main)
        os.chdir("..")
        i += 1

  
def run(args, logger):
    if args.test:
        run_test(args, logger)
    else:
        run_benchmark(args, logger)
