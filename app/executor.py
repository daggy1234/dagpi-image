from concurrent.futures import ProcessPoolExecutor

executor: ProcessPoolExecutor = ProcessPoolExecutor(max_workers=4)


def get_executor() -> ProcessPoolExecutor:
    global executor
    return executor
