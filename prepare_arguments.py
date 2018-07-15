from typing import Optional
from sys import argv

def get_argument(name: str) -> Optional[str]:
    if name in argv:
        id: int = argv.index(name)
        return argv[id + 1]
    else:
        return None


def get_bool_argument(name: str) -> bool:
    if name in argv:
        return True
    else:
        return False
