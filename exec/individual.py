#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import multiprocessing

"""
Задача:
Для своего индивидуального задания лабораторной работы 2.23 необходимо
реализовать вычисление значений в двух функций в отдельных процессах.
"""

e = 10e-7
stepArray = multiprocessing.Array('d', [1])


def calculateY(x):
    return 0.5 * math.log((x + 1) / (x - 1))


def calculate_step(step, index, x, n):
    step[index] = 1

    def firstStep():
        step[index] *= (2 * n - 1)

    def secondStep():
        step[index] *= x**(2 * n - 1)

    def thirdStep():
        step[index] **= -1

    with multiprocessing.Pool(processes=3) as pool:
        pool.map(lambda f: f(), [firstStep, secondStep, thirdStep])


def main():
    x = 3
    index = 0

    while abs(stepArray[index]) > e:
        stepArray.append(0)
        calculate_step(stepArray, index + 1, x, index + 1)
        index += 1

    S = sum(stepArray) - 1
    y = calculateY(x)

    print(f"\nРезультат при x = {x}")
    print(f"Сумма = {round(S, 4)}")
    print(f"Y = {round(y, 4)}")
    print(f"Разница между S и Y: {abs(round(S - y, 4))}\n")


if __name__ == "__main__":
    main()
