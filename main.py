from src.scheduler import queue_priority_round_robin
from sys import argv

reserved = {
    "-v": "verbose",
    "-w": "write",
}

options = {
    "verbose": False,
    "write": True,
}

for arg in argv:
    if arg in reserved.keys():
        options[reserved[arg]] = True

queue_priority_round_robin(options)
