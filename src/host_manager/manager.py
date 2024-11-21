import json
from threading import Lock
from typing import Optional

from src.host_manager.domain import Host

file_lock = Lock()


class HostManager:
    def __init__(self, file_path: str = "current_host.json"):
        self.file_path = file_path

    def read_host_from_file(self) -> Optional[Host]:
        try:
            with file_lock:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    if data is not None:
                        return Host.model_validate(data)
        except FileNotFoundError:
            return None

        return None

    def write_host_to_file(self, host: Host) -> None:
        with file_lock:
            with open(self.file_path, "w") as f:
                f.write(json.dumps(host.model_dump(mode="json")))


def get_host_manager() -> HostManager:
    return HostManager()
