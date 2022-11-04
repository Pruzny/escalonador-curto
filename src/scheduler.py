from src.classes import *
from src.file_manager import read_txt

process_list = read_txt()


def is_empty_queue_list(priority_lists: list[Queue]) -> bool:
    for queue in priority_lists:
        if not queue.isEmpty():
            return False
    return True


def is_empty_process_list(process_list: list[Process]):
    return len(process_list) == 0


def is_empty_io_list(io_list: list[Process]):
    return len(io_list) == 0


def add_processes(processes: list[Process], queue_list: list[Queue], io_processes: list[Process],
                  cpu_time: int) -> None:
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
    return "—" * 30


def generate_ready_text(first: Process) -> str:
    text = ""
    for queue in SchedulerArgs.getInstance().priority_lists:
        text += f"Ready Queue {queue.priority} (q{queue.max_quantum}):\n"
        for process in queue.processes:
            if process != first:
                text += f"\t{process}\n"
    return text


def generate_waiting_text(highest_queue: Queue) -> tuple[list[Process], str]:
    reset_list = []
    text = f"Waiting Queue:\n"
    sc_args = SchedulerArgs.getInstance()
    for process in sc_args.io_list:
        text += f"\t{process}, Remaining: {process.io_bursts[0]}\n"
        process.waitIO()
        process.update()
        if process.state == Process.EX:
            sc_args.io_list.remove(process)
            reset_list.append(process)

    return reset_list, text


def queue_priority_round_robin(options: dict[str, bool]):
    timer = 0
    process_running = False
    sc_args = SchedulerArgs.getInstance()
    highest_priority_list = sc_args.priority_lists[0]
    file = None

    if options["write"]:
        file = open("process.out", "w")
    while not (is_empty_process_list(process_list) and is_empty_queue_list(sc_args.priority_lists) and is_empty_io_list(
            sc_args.io_list)):
        try:
            text = f"Timer: {timer}\n"
            add_processes(process_list, sc_args.priority_lists, sc_args.io_list, timer)

            highest_priority_list = highest_priority_list if process_running else get_higher_queue(
                sc_args.priority_lists)  # Pode ser uma fila vazia (e ainda ter processo que ainda não entrou)
            if not highest_priority_list.isEmpty():
                first_process = highest_priority_list.processes[0]
                ready_text = generate_ready_text(first_process)

                # Fila de espera
                reset_list, waiting_text = generate_waiting_text(highest_priority_list)

                text += f"Executing Queue {highest_priority_list.priority} (q{highest_priority_list.quantum}) - " \
                        f"{first_process}, Remaining: {first_process.cpu_bursts[0]}\n"
                text += ready_text
                text += waiting_text

                first_process.execute()
                first_process.update()
                highest_priority_list.quantum -= 1
                process_running = True

                # Verifica se o processo que executou acabou ou espera IO
                pop_first = False
                if first_process.state == Process.IO:
                    process_running = False
                    highest_priority_list.remove()
                    pop_first = True
                    highest_priority_list.resetQuantum()
                    if not first_process.hasEnded():
                        sc_args.io_list.append(first_process)

                # Verifica se o quantum zerou
                if highest_priority_list.quantum == 0:
                    process_running = False
                    sc_args.priority_lists[min(highest_priority_list.priority + 1, sc_args.number_of_lists - 1)].add(
                        highest_priority_list.remove())
                    pop_first = True
                    highest_priority_list.resetQuantum()

                # Verifica se saiu processo da fila de espera
                if len(reset_list) > 0:
                    process_running = False
                    if not pop_first:
                        highest_priority_list.add(highest_priority_list.remove())
                    highest_priority_list.resetQuantum()
                    for process in reset_list:
                        sc_args.priority_lists[0].add(process)

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
