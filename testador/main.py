#!/usr/bin/python
# encoding: utf-8

import sys
import os
import subprocess
import codecs
from progunit import *
from graphcheck import *

VALIDADORS = { 
    "bfs"   : bfs_main,
    "ts"    : ts_main,
    "scc"   : scc_main,
    "bf"    : sp_main,
    "bfall" : sp_main,
    "dk"    : sp_main,
    "dkall" : sp_main,
    "fw"    : sp_main,
    "mst"   : mst_main,
}

GRAPH_EXT=".g"
EXPECTED_EXT = ".out"
PROG_RUN="/run"
PROG_BUILD="/build"
LOG_FILE="testes.log"

def available_validadors():
    return [validador for validador in VALIDADORS]

def get_validador(alg):
    return VALIDADORS[alg]

def main():
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) != 4:
        print u"Número inválido de parâmetros"
        show_usage()
        sys.exit(1)
    algs, progs_path, cases_path = sys.argv[1:]
    algs = algs.split("|")
    validade_algs(algs)    
    progs = find_programs(progs_path.decode('utf-8'))
    validade_progs(progs)
    progs = build_programs(progs)
    test_cases = create_test_cases(progs, algs, cases_path.decode('utf-8'))
    run_test_cases(test_cases)

def show_usage():
    print "Modo de usar: %s %s nome-do-programa caminho-testes" % (sys.argv[0], "|".join(available_validadors()))

def validade_algs(algs):
    avaliable = set(available_validadors())
    algs = set(algs)
    if not algs.issubset(avaliable):
        print u"Validador(es) não encontrado:", " ".join(algs - avaliable)
        show_usage()
        sys.exit(1)

def validade_progs(progs):
    if not progs:
        print u"Nenhum arquivo run executável encontrado."
        print u"Lembre-se de executar o comando 'chmod -f +x src/lang/{run,build}'"
        print u"onde lang é a linguagem escolhida para implementar o trabalho."
        sys.exit(1)

def build_programs(progs):
    r = []
    for run, build in progs:
        if build:
            print u"Executando", build
        if build and subprocess.call(build) < 0:
            print u"Compilação", build, "falhou. IGNORANDO", run
        else:
            r.append(run)
    return r

def create_test_cases(progs, algs, cases_path):
    m = max(len(algs) for alg in algs) - 1
    def desc(prog, alg, case):
        return u" ".join([prog, alg.ljust(m), case])
    tests = []
    for alg in algs:
        validador = get_validador(alg)
        cases = find_cases(os.path.join(cases_path, alg))
        for prog in progs:
            for case in cases:
                case_abs = os.path.abspath(case)
                description = desc(prog, alg, case)
                program = create_program([prog, alg, case_abs])
                checker = create_checker(case_abs, validador)
                tests.append(TestCase(description, program, checker))
    return tests

def run_test_cases(test_cases):
    reporter = SimpleReporter(LOG_FILE)
    runner = Runner(test_cases, reporter)
    runner.run()

def create_checker(case, check_func):
    expected = replace_ext(case, EXPECTED_EXT)
    def check(test_result, program_result):
        return check_func(test_result, case, expected, program_result)
    return check

# utilities
def find_cases(path):
    return sorted(find_files(path, is_graph_file))

def is_graph_file(path):
    return os.path.isfile(path) and path.endswith(GRAPH_EXT)

def find_programs(path):
    progs = sorted(find_files(path, is_program_run))
    return [(run, get_program_build(run)) for run in progs]

def is_program_run(path):
    return path.endswith(PROG_RUN) and is_executable(path)

def get_program_build(run):
    build = run[:-len(PROG_RUN)] + PROG_BUILD
    return build if is_executable(build) else None

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_files(path, filter):
    files = []
    for dirpath, _, _files in os.walk(path):
        for f in _files:
            f = os.path.join(dirpath, f)
            if filter(f):
                files.append(f)
    return files

def replace_ext(path, new_ext):
    base, _ = os.path.splitext(path)
    return base + new_ext

# main body
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
        print u'Interrompido'
