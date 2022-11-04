from src.classes import SchedulerArgs
from src.scheduler import queue_priority_round_robin
from sys import argv

reserved = {
    "-v": "verbose",
    "-n": "number_of_list",
    "-q": "quantum",

}

options = {
    "verbose": False,
    "write": True,
}


def check_args_quantum(quantum: list) -> bool:
    for i in range(len(quantum)):
        if quantum[i] <= 0:
            return False
    return True


args_already = []
args_quantum = []

for arg in argv:
    args_already.append(arg)
    if arg in reserved.keys():
        options[reserved[arg]] = True

    if '-q' in args_already or '-n' in args_already:
        if arg != "-q" and arg != "-n":
            args_quantum.append(int(arg))
        else:
            args_quantum.append(arg)

print(args_quantum)
print(args_quantum[3::])

if '-n' in args_quantum:
    n = args_quantum.index("-n")
    number_of_lists = args_quantum[n + 1]
    print(number_of_lists)
    print(len(args_quantum[3::]))
    if number_of_lists == len(args_quantum[3::]) and check_args_quantum(args_quantum[3::]):
        SchedulerArgs.getInstance(int(number_of_lists), tuple(args_quantum[3::]))
    else:
        SchedulerArgs.getInstance()
else:
    SchedulerArgs.getInstance()

queue_priority_round_robin(options)
