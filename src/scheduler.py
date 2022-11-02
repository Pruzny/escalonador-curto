from src.classes import *
from src.file_manager import read_txt

NUMBER_OF_LISTS = 4

process_list = read_txt()
priority_lists = list(Queue(i, (i + 1) * 5) for i in range(NUMBER_OF_LISTS))
io_list = list()

time = 0


def is_empty_queue_list(priority_lists: list[Queue]) -> bool:
    for queue in priority_lists:
        if not queue.isEmpty():
            return False
    return True


def is_empty_process_list(process_list: list[Process]):
    return len(process_list) == 0


def is_empty_io_list(io_list: list[Process]):
    return len(io_list) == 0


def add_processes(processes: list[Process], queue_list: list[Queue], io_processes: list[Process], cpu_time: int) -> None:
    while len(processes) > 0 and processes[0].admission_time == cpu_time:
        if processes[0].state == Process.IO:
            io_processes.append(processes.pop(0))
        else:
            queue_list[0].add(processes.pop(0))


def get_higher_queue(queue_list: list[Queue]) -> Queue:
    for queue in queue_list:
        if not queue.isEmpty():
            return queue
    return queue_list[0]


def border() -> str:
    return "—"*30


def generate_ready_text(first: Process) -> str:
    text = ""
    for queue in priority_lists:
        text += f"Ready Queue {queue.priority} (q{queue.max_quantum}):\n"
        for process in queue.processes:
            if process != first:
                text += f"\t{process}\n"
    return text


def generate_waiting_text(highest_queue: Queue, is_running: bool) -> tuple[bool, str]:
    text = f"Waiting Queue:\n"
    for process in io_list:
        text += f"\t{process}, Remaining: {process.io_bursts[0]}\n"
        process.waitIO()
        process.update()
        if process.state == Process.EX:
            io_list.remove(process)
            if is_running:
                highest_queue.add(highest_queue.remove())
                highest_queue.resetQuantum()
                is_running = False
            priority_lists[0].add(process)

    return is_running, text


def queue_priority_round_robin(options: dict[str, bool]):

    timer = 0
    process_running = False
    highest_priority_list = priority_lists[0]
    file = None
    if options["write"]:
        file = open("process.out", "w")
    while not (is_empty_process_list(process_list) and is_empty_queue_list(priority_lists) and is_empty_io_list(io_list)):
        try:
            text = f"Timer: {timer}\n"
            add_processes(process_list, priority_lists, io_list, timer)
            process_running, waiting_text = generate_waiting_text(highest_priority_list, process_running)

            highest_priority_list = highest_priority_list if process_running else get_higher_queue(priority_lists)  # Pode ser uma fila vazia (e ainda ter processo que ainda não entrou)
            if not highest_priority_list.isEmpty():
                first_process = highest_priority_list.processes[0]
                ready_text = generate_ready_text(first_process)

                text += f"Executing Queue {highest_priority_list.priority} (q{highest_priority_list.quantum}) - " \
                        f"{first_process}, Remaining: {first_process.cpu_bursts[0]}\n"
                text += ready_text
                text += waiting_text

                first_process.execute()
                first_process.update()
                highest_priority_list.quantum -= 1
                process_running = True

                # Verifica se o processo que executou acabou ou espera IO
                if first_process.state == Process.IO:
                    process_running = False
                    highest_priority_list.remove()
                    highest_priority_list.resetQuantum()
                    if not first_process.hasEnded():
                        io_list.append(first_process)

                # Verifica se o quantum zerou
                if highest_priority_list.quantum == 0:
                    process_running = False
                    priority_lists[min(highest_priority_list.priority + 1, NUMBER_OF_LISTS - 1)].add(highest_priority_list.remove())
                    highest_priority_list.resetQuantum()

                text += f"{border()}"

            if options["verbose"]:
                print(text)
            if options["write"]:
                file.write(text + "\n")

        except Exception as error:
            raise error
        finally:
            timer += 1

    if options["verbose"]:
        print("End of execution")
    if options["write"]:
        file.close()
