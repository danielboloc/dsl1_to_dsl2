#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import inspect
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

#mainfile = open('/Users/dboloc/Workspace/SOFTPROJECTS/gwas-nf/main_dsl1.nf').readlines()
mainfile = open('test.nf').readlines()
processes = dict()

# find the string and capture process name
# example: 'process foo {', will capture 'foo'
#find_process_regex = r"(\s+)?process\s+(?P<process_name>\w+)(\s+)?\{"
find_process_regex = r"process\s+(\w+)\s+\{(\s+)?\n(.*?)\n(\s+)?\}"
# not used ATM, but this is to retrieve the sections from the process
#find_input_regex = r"\s+input:(.*?)\n\n"
#find_output_regex = r"\s+output:(.*?)\n\n"

def find_all_processes(mainfile):
    """Go over a main.nf file and get all processes names and closure contents
    It also replaces 'set' to 'tuple' and 'file' to 'path' inside the process'
    'input' and 'output' scopes
    """
    matches = re.finditer(find_process_regex, "".join(mainfile), re.MULTILINE | re.DOTALL)
    for matchNum, match in enumerate(matches):
        # append to dict name of the process as key and when process as values
        # make sure the replace unused keywords in DSL2
        #print(match.group(0).replace("set","tuple").replace("file","path"))
        #print(match.span())
        process_name = match.group(1)
        # leave only one indent
        process_code = match.group(0)
        # works
        find_input_regex = r"(.*?)\s+from\s+(\w+)(.*?)\n"
        find_output_regex = r"(.*?)\s+into\s+(\w+)(.*?)\n"
        #find_input_regex = r"\s+input:(.*?)\n\n"
        # m = re.findall(find_input_regex, match.group(0))
        match_in = re.finditer(find_input_regex, process_code, re.MULTILINE | re.DOTALL)
        in_channels = []
        for matchNum, match in enumerate(match_in):
            in_channels.append(match.group(2))
        match_out = re.finditer(find_output_regex, process_code, re.MULTILINE | re.DOTALL)
        out_channels = []
        for matchNum, match in enumerate(match_out):
            out_channels.append(match.group(2))

        # replace 'from' and 'into'
        process_wo_from = re.sub(r"\s+from\s+\w+", "", process_code)
        process_wo_into = re.sub(r"\s+into\s+\w+", "", process_wo_from)
        processes[process_name] = { 'code': inspect.cleandoc(process_wo_into.replace("set","tuple").replace("file","path")),
                                    'input_channels': in_channels,
                                    'output_channels': out_channels }


find_all_processes(mainfile)
print("CODE: ", processes["foo"]['code'])
print("IN: ", processes["foo"]['input_channels'])
print("OUT: ", processes["foo"]['output_channels'])
print(processes.keys())

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
t = env.get_template("main_template.nf")

help_message = "HELP"
proces_def = processes["foo"]['code']
subworkflows = "subworkflows placeholder"
param_checks = "param checks placeholder"
inputs = "input channels"
run = '\n'.join(processes.keys())
render = t.render(
    help_message=help_message,
    proces_def=proces_def,
    subworkflows=subworkflows,
    param_checks=param_checks,
    inputs=inputs,
    run=run
)
with open(f"main.nf","w") as f:
    f.write(render)