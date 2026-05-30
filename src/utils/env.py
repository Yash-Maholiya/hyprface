import os
import warnings
import onnxruntime

os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

onnxruntime.set_default_logger_severity(3)

warnings.filterwarnings(
    "ignore",
    message=".*estimate.*deprecated.*",
    category=FutureWarning,
    module="insightface",
)


class suppress_stdout:
    def __enter__(self):
        self._orig_fd = os.dup(1)
        self._devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(self._devnull, 1)
        return self

    def __exit__(self, *_):
        os.dup2(self._orig_fd, 1)
        os.close(self._orig_fd)
        os.close(self._devnull)