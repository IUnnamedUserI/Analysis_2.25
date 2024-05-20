#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Для своего индивидуального задания лабораторной работы 2.23 необходимо
организовать конвейер, в котором сначала в отдельном потоке вычисляется
значение первой функции, после чего результаты вычисления должны передаваться
второй функции, вычисляемой в отдельном потоке. Потоки для вычисления значений
двух функций должны запускаться одновременно.
"""


import math
import threading


e = 10e-7
stepArray = [1]


def calculateY(x):
    return 0.5 * math.log((x + 1) / (x - 1))


def first_function(x, n, results, barrier):
    result = (2 * n - 1) * x**(2 * n - 1)
    results[n] = result
    barrier.wait()


def second_function(step, index, results, barrier):
    barrier.wait()
    result = 1 / results[index]
    step[index] = result


def main():
    x = 3
    index = 0
    results = {}
    barrier = threading.Barrier(2)

    while abs(stepArray[index]) > e:
        stepArray.append(0)

        firstThread = threading.Thread(
            target=first_function,
            args=(x, index + 1, results, barrier)
        )
        secondThread = threading.Thread(
            target=second_function,
            args=(stepArray, index + 1, results, barrier)
        )

        firstThread.start()
        secondThread.start()

        firstThread.join()
        secondThread.join()

        index += 1

    S = sum(stepArray) - 1
    y = calculateY(x)

    print(f"\nРезультат при x = {x}")
    print(f"Сумма = {round(S, 4)}")
    print(f"Y = {round(y, 4)}")
    print(f"Разница между S и Y: {abs(round(S - y, 4))}\n")


if __name__ == "__main__":
    main()
