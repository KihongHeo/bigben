#!/usr/bin/python3
import os
import logging
import subprocess

petablox = "Petablox"

def run_test(args, logger):
    project = 'test/petablox'
    os.chdir(project)
    cmd = "java -Dpetablox.work.dir=" + project + "/elevator -Dpetablox.scope.kind=rta -Dpetablox.run.analyses=queryE,datarace-java -Dpetablox.reflect.kind=dynamic -jar ./petablox.jar"
    print(cmd)
    output = subprocess.getoutput(cmd)
    print(output)

def run(args, logger):
    if args.test:
        run_test(args, logger)
    else:
        run_benchmark(args, logger)
