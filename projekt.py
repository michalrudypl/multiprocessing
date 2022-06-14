import itertools
import time
import os
import random
import multiprocessing
from turtle import color
import matplotlib.pyplot as plt


class SortingClass:
    @staticmethod
    def merge_sort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            SortingClass.merge_sort(L)
            SortingClass.merge_sort(R)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
        return arr

    @staticmethod
    def bubble_sort(array):
        n = len(array)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    already_sorted = False
            if already_sorted:
                break

        return array

    @staticmethod
    def insertion_sort(array):
        for i in range(1, len(array)):
            key_item = array[i]
            j = i - 1
            while j >= 0 and array[j] > key_item:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key_item

        return array


def divide_numbers(numbers, cpus):
    all_numbers_divided = []
    for i in range(cpus - 1):
        all_numbers_divided.append(
            numbers[i * len(numbers) // cpus : (i + 1) * len(numbers) // cpus]
        )
    all_numbers_divided.append(numbers[(cpus - 1) * len(numbers) // cpus :])
    return all_numbers_divided


def sort(numbers, sorted_numbers, method):
    numbers = getattr(SortingClass, method)(numbers)
    sorted_numbers.append(numbers)


def main():
    # cpu_count = 2
    cpu_count = os.cpu_count()

    sorting_methods = [x for x in dir(SortingClass) if x[0:2] != "__"]
    res = {key: {x: {} for x in sorting_methods} for key in range(1, cpu_count + 1)}

    numbers = [
        10,
        100,
        1000,
        5000,
        10000,
        25000,
        50000,
        100000,
    ]
    sorting_methods = [x for x in dir(SortingClass) if x[0:2] != "__"]

    for number in numbers:
        random_numbers = [random.randint(-100, 100) for x in range(number)]
        for cpu in range(1, cpu_count + 1):
            for method in sorting_methods:
                start_time = time.perf_counter()
                manager = multiprocessing.Manager()
                sorted_numbers = manager.list()
                divided_numbers = divide_numbers(random_numbers, cpu)

                p = [
                    multiprocessing.Process(
                        target=sort,
                        args=(numbers, sorted_numbers, method),
                    )
                    for numbers in divided_numbers
                ]

                for i in p:
                    i.start()
                for i in p:
                    i.join()

                sorted_numbers = list(
                    itertools.chain.from_iterable(sorted_numbers)
                ).sort()

                end = time.perf_counter()
                time_res = end - start_time
                print(
                    f"Program wykonywal sie w {time_res}s na",
                    cpu,
                    "wątkach dla",
                    number,
                    "liczb, dla algorytmu",
                    method,
                )

                res[cpu][method].update({number: time_res})

    figure, axis = plt.subplots(
        len(numbers),
        len(sorting_methods),
        figsize=(len(sorting_methods) * 6, len(numbers) * 5),
    )
    x, y = 0, 0
    labels = [str(c) for c in range(1, cpu_count + 1)]
    for number in numbers:
        y = 0
        for method in sorting_methods:
            values = [res[c][method][number] for c in range(1, cpu_count + 1)]
            axis[x, y].bar(
                labels,
                values,
                color=["red" if x is not min(values) else "green" for x in values],
            )

            for cpu in range(cpu_count):
                axis[x, y].text(
                    cpu, values[cpu], round(values[cpu], 2), ha="center", va="bottom"
                )

            axis[x, y].set_title(f"{method} dla {number} liczb")
            axis[x, y].set_xlabel("Processes", fontsize=10)
            axis[x, y].set_ylabel("Time", fontsize=10)

            y += 1
        x += 1

    # plt.ylim()
    plt.tight_layout()
    plt.savefig("analiza.png")
    plt.show()


if __name__ == "__main__":
    main()
