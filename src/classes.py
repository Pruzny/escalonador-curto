import random


class Process:
    IO = 0
    EX = 1

    pid: int
    admission_time: int
    name: str  # nome do programa
    priority: int  # prioridade
    cpu_bursts: list  # listas de tempo de burst cpu
    io_bursts: list  # listas de tempo de burst io
    state: int

    def __init__(self, pid, admission_time, name, priority, bursts: list) -> None:
        self.pid = pid
        self.admission_time = admission_time
        self.name = name
        self.priority = priority
        self.cpu_bursts = list(reversed(list(int(burst) for burst in bursts[::-2])))
        self.io_bursts = list(reversed(list(int(burst) for burst in bursts[-2::-2])))
        self.state = Process.EX if len(bursts) % 2 == 1 else Process.IO

    def __str__(self) -> str:
        return f"PID: {self.pid}, Name: {self.name}, Ad. time: {self.admission_time}, Priority: {self.priority}"

    def hasEnded(self):
        return len(self.cpu_bursts) == len(self.io_bursts) == 0

    def canExecute(self):
        return len(self.cpu_bursts) > 0 and self.state == Process.EX

    def execute(self) -> None:
        if not self.canExecute():
            print(f"Erro: {self}")
            raise IndexError("There is no CPU execution")
        self.cpu_bursts[0] -= 1

    def waitIO(self):
        if self.state == Process.IO and len(self.io_bursts) > 0:
            self.io_bursts[0] -= 1

    def update(self):
        if self.state == Process.IO:
            if self.io_bursts[0] == 0:
                self.io_bursts.pop(0)
                self.state = Process.EX
        elif self.state == Process.EX:
            if self.cpu_bursts[0] == 0:
                self.cpu_bursts.pop(0)
                self.state = Process.IO


class Queue:
    priority: int
    processes: list[Process]
    max_quantum: int
    quantum: int

    def __init__(self, priority: int, quantum: int) -> None:
        self.processes = list()
        self.priority = priority
        self.max_quantum = quantum
        self.quantum = quantum

    def remove(self) -> Process:
        return self.processes.pop(0)

    def add(self, process) -> None:
        self.processes.append(process)

    def isEmpty(self) -> bool:
        return len(self.processes) == 0

    def execute(self) -> None:
        if self.isEmpty():
            raise IndexError("Attempt to execute empty queue")
        self.processes[0].execute()
        self.quantum -= 1

    def resetQuantum(self) -> None:
        self.quantum = self.max_quantum


class SchedulerArgs:
    instance = None
    number_of_lists: int
    priority_lists: list
    io_list: list
    quantum: list

    def __init__(self, nl: int, quantum_list: list):
        self.number_of_lists = nl
        self.quantum = quantum_list
        self.priority_lists = list(Queue(i, k) for i, k in zip(range(nl), quantum_list))
        self.io_list = list()

    @staticmethod
    def getInstance(number_of_list: int = 4, quantum_list: tuple = (5, 10, 15, 20)):
        if SchedulerArgs.instance is None:
            SchedulerArgs.instance = SchedulerArgs(number_of_list, list(quantum_list))
        return SchedulerArgs.instance
