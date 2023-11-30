#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

sys.path.append(os.getcwd())

import yaml
from kubejobs.jobs import KubernetesJob


def argument_parser():
    parser = argparse.ArgumentParser(description="Backend Runner")
    parser.add_argument("config", type=str)
    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    configs = yaml.safe_load(open(args.config, "r"))

    base_args = "apt -y update && " \
            "apt-get install git-lfs && " \
            "git lfs install && " \
            "git clone https://huggingface.co/spaces/hallucinations-leaderboard/leaderboard && " \
            "cd leaderboard && pip -U -r requirements.txt && HF_TOKEN=$HF_TOKEN H4_TOKEN=$HF_TOKEN "
    command = "python backend-cli.py"

    secret_env_vars = configs["env_vars"]

    # Create a Kubernetes Job with a name, container image, and command
    print(f"Creating job for: {command}")
    job = KubernetesJob(name="hl-backend",
                        image=configs["image"],
                        gpu_type="nvidia.com/gpu",
                        gpu_limit=configs["gpu_limit"],
                        gpu_product=configs["gpu_product"],
                        backoff_limit=4,
                        command=["/bin/bash", "-c", "--"],
                        args=[base_args + command],
                        secret_env_vars=secret_env_vars,
                        user_email="p.minervini@ed.ac.uk")

    # Run the Job on the Kubernetes cluster
    job.run()


if __name__ == "__main__":
    main()
