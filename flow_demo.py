from prefect import flow, task, get_run_logger

@task
def log_message(name:str):
    logger = get_run_logger()
    logger.info(f"Hello {name}!")
    return

@flow(name="flow_demo")
def flow_demo(name: str):
    log_message(name)
    return
