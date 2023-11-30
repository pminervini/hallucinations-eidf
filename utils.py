# -*- coding: utf-8 -*-

from kubernetes import client, config

def check_if_completed(job_name: str, namespace: str = 'informatics') -> bool:
    # Load the kube config
    config.load_kube_config()

    # Create an instance of the API class
    api = client.BatchV1Api()

    job_exists = False
    is_completed = True

    # Check if the job exists in the specified namespace
    jobs = api.list_namespaced_job(namespace)
    if job_name in {job.metadata.name for job in jobs.items}:
        job_exists = True

    if job_exists is True:
        job = api.read_namespaced_job(job_name, namespace)
        is_completed = False

        # Check the status conditions
        if job.status.conditions:
            for condition in job.status.conditions:
                if condition.type == 'Complete' and condition.status == 'True':
                    is_completed = True
                elif condition.type == 'Failed' and condition.status == 'True':
                    print(f"Job {job_name} has failed.")
        else:
            print(f"Job {job_name} still running or status is unknown.")
        
        if is_completed:
            api_res = api.delete_namespaced_job(name=job_name, namespace=namespace,
                                                body=client.V1DeleteOptions(propagation_policy='Foreground'))
            print(f"Job '{job_name}' deleted. Status: {api_res.status}")
    return is_completed
