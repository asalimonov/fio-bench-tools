import datetime
import os
from pathlib import Path
import sys
import subprocess

JOBS_DIR = "jobs"
REPORTS_DIR = "reports"
OUTPUT_FORMAT = "normal,terse,json,json+"
DEBUG = False
DRY_RUN = False


def get_current_dir():
    return Path().absolute()


def new_experiment():
    dt = datetime.datetime.now()
    id_date = dt.strftime("%Y-%m-%d")
    id_exp_number = 0
    while True:
        exp_id = "{0}-{1}".format(id_date, "{:02d}".format(id_exp_number))
        path = Path.joinpath(get_current_dir(), REPORTS_DIR, exp_id)
        if not Path.exists(path):
            break
        id_exp_number += 1
    return exp_id, path


def get_jobs(jobs_dir):
    jobs = []
    for file in os.listdir(jobs_dir):
        if file.endswith(".fio"):
            jobs.append((file, str(Path.joinpath(get_current_dir(), JOBS_DIR, file))))
    return jobs


# noinspection PyListCreation
def get_cmd(job, exp):
    cmd = ["fio"]
    cmd.append("--output-format={0}".format(OUTPUT_FORMAT))
    cmd.append("--output={0}.report".format(Path.joinpath(exp[1], job[0])))
    if DEBUG:
        cmd.append("--debug")

    # the last should be:
    cmd.append(job[1])
    return cmd


def run_experiment(exp):
    exp[1].mkdir()
    jobs_dir = Path.joinpath(get_current_dir(), JOBS_DIR)
    print("Jobs dir: {0}".format(jobs_dir))
    jobs = get_jobs(jobs_dir)
    print("Jobs found: {0}".format(len(jobs)))
    i = 0
    for job in jobs:
        i += 1
        cmd = get_cmd(job, exp)
        cmd_str = " ".join(cmd)
        print("Job {0} ({1}/{2}) is running".format(job[0], i, len(jobs)))
        print("Command: {0}".format(cmd_str))
        if not DRY_RUN:
            subprocess.call(cmd)
        else:
            print("DRY RUN!")
        print("Job {0} was done".format(job[0]))


def set_params(args):
    if "--debug" in args:
        global DEBUG
        DEBUG = True
        print("DEBUG is ON")
    if "--dry-run" in args:
        global DRY_RUN
        print("DRY_RUN is ON")
        DRY_RUN = True


def main(args):
    print("Started fio launcher")
    print("Current dir: {0}".format(get_current_dir()))
    set_params(args)
    exp = new_experiment()
    print("Experiment {0} is running".format(exp[0]))
    run_experiment(exp)
    print("Finished")
    sys.exit(0)


def pre_init():
    jd = Path.joinpath(get_current_dir(), JOBS_DIR)
    if not jd.exists():
        Path.mkdir(jd)
    rd = Path.joinpath(get_current_dir(), REPORTS_DIR)
    if not rd.exists():
        Path.mkdir(rd)


if __name__ == '__main__':
    pre_init()
    main(sys.argv)
