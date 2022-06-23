import multiprocessing
import os
from random import randint, random
import time
import matplotlib.pyplot as plt


def find_prime_numbers(start, end, step):
    for i in range(start, end, step):
        if i > 1:
            for j in range(2, int(i**0.5) + 1):
                if i % j == 0:
                    break


def main():
    cpus = os.cpu_count()
    lenght = [cpus * n for n in [1, 10, 100, 1000, 10000, 100000, 1000000, 2000000]]
    results = {key: {} for key in lenght}

    for l in lenght:
        for cpu in range(1, cpus + 1):
            start_time = time.perf_counter()

            starts_steps = [[x, cpu] for x in range(cpu)]
            p = [
                multiprocessing.Process(
                    target=find_prime_numbers,
                    args=(x[0], l, x[1]),
                )
                for x in starts_steps
            ]

            for i in p:
                i.start()
            for i in p:
                i.join()

            end = time.perf_counter()
            time_res = end - start_time
            print(
                f"Program wykonywal sie w {time_res}s na",
                cpu,
                "wątkach dla",
                l,
                "liczb",
            )

            results[l].update({cpu: time_res})
    figure, axis = plt.subplots(len(lenght), 1, figsize=(15, len(lenght) * 5))
    x = 0

    cpus_list = [z for z in range(1, cpus + 1)]
    for l in lenght:
        time_results = [round(results[l][z], 4) for z in cpus_list]

        axis[x].bar(
            cpus_list,
            time_results,
            color=[
                "red" if x is not min(time_results) else "green" for x in time_results
            ],
        )
        axis[x].set_title(f"Dla {l} liczb")
        axis[x].set_xlabel("Procesy")
        axis[x].set_ylabel("Czas[s]")
        for cpu in range(len(cpus_list)):
            axis[x].text(
                cpu + 1,
                time_results[cpu],
                str(time_results[cpu]),
                ha="center",
                va="bottom",
            )
        x += 1

    figure.tight_layout()
    [os.remove(file) for file in os.listdir() if file.endswith(".png")]
    plt.savefig("wynik.png")
    plt.close()


if __name__ == "__main__":
    main()
