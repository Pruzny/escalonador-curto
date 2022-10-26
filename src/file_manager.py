from src.classes import Process

PATH = "process.in"


def check_positive(ad_time: int, priority: int) -> None:
    """checks if admission time and priority time is positive, if not throws a ValueError"""
    if ad_time < 0:
        raise ValueError("Admission time must be  positive ")
    if priority < 0:
        raise ValueError("Priority must be positive.")


def read_txt() -> list[Process]:
    """open a .in with process and manipulate input for create a process object"""
    processes = list()
    for line in open(PATH, "r").readlines():
        try:
            admission_time, name, priority, *bursts = line.split()

            admission_time = int(admission_time)
            priority = int(priority)
            check_positive(admission_time, priority)
            processes.append(Process(
                0,
                admission_time,
                name,
                priority,
                bursts,
            ))
        except Exception as error:
            print(repr(error))
            # print("Admission time and Priority must be a number")

    processes.sort(key=lambda x: x.admission_time)
    count = 0
    for process in processes:
        process.pid = count
        count += 1

    return processes
