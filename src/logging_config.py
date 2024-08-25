import logging


class ContextFilter(logging.Filter):
    def __init__(self, dataset=None, scenario=None, model=None):
        super().__init__()
        self.dataset = dataset
        self.scenario = scenario
        self.model = model

    def filter(self, record):
        record.dataset = self.dataset
        record.scenario = self.scenario
        record.model = self.model
        return True


def setup_logging(log_file_path: str):
    """
    Set up logging configuration to log to a file and disable console logging.

    Args:
        log_file_path (str): The path to the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path)],
    )
