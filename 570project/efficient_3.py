import sys
# from resource import *
import time
import psutil
import os

delta = 30
alpha = [[0, 110, 48, 94],
         [110, 0, 118, 48],
         [48, 118, 0, 110],
         [94, 48, 110, 0]]
to_idx = {"A": 0, "C": 1, "G": 2, "T": 3}


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def make_str(strs):
    str = strs[0].strip()
    for i in strs[1:]:
        i = i.strip()
        str = str[:int(i) + 1] + str + str[int(i) + 1:]
    return str


def alignment(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for i in range(m + 1)]
    for j in range(1, n + 1):
        dp[0][j] = j * delta
    for i in range(1, m + 1):
        dp[i][0] = i * delta
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(dp[i - 1][j] + delta,
                           dp[i][j - 1] + delta,
                           dp[i - 1][j - 1] + alpha[to_idx[s1[i - 1]]][to_idx[s2[j - 1]]])
    return dp


def back_track(s1, s2, dp):
    i = len(s1)
    j = len(s2)
    x = ""
    y = ""
    while i > 0 and j > 0:
        if dp[i][j] == dp[i - 1][j - 1] + alpha[to_idx[s1[i - 1]]][to_idx[s2[j - 1]]]:
            x = s1[i - 1] + x
            y = s2[j - 1] + y
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + delta:
            x = s1[i - 1] + x
            y = "_" + y
            i -= 1
        elif dp[i][j] == dp[i][j - 1] + delta:
            x = "_" + x
            y = s2[j - 1] + y
            j -= 1
    while i > 0:
        x = s1[i - 1] + x
        y = "_" + y
        i -= 1
    while j > 0:
        x = "_" + x
        y = s2[j - 1] + y
        j -= 1
    return x, y


# only return 1D array
def se_alignment(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0, 0] for k in range(m + 1)]
    # initial
    for i in range(1, m + 1):
        dp[i][0] = i * delta
    ind = 1
    last = 0
    for j in range(1, n + 1):
        dp[0][ind] = j * delta
        for i in range(1, m + 1):
            dp[i][ind] = min(dp[i - 1][last] + alpha[to_idx[s1[i - 1]]][to_idx[s2[j - 1]]],
                             dp[i - 1][ind] + delta,
                             dp[i][last] + delta)
        last = ind
        ind = (ind + 1) % 2
    return [row[last] for row in dp]


# only return 1D array
# read string in reverse order
def backward_se_alignment(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0, 0] for k in range(m + 1)]
    # initial
    for i in range(1, m + 1):
        dp[i][0] = i * delta
    ind = 1
    last = 0
    for j in range(1, n + 1):
        dp[0][ind] = j * delta
        for i in range(1, m + 1):
            dp[i][ind] = min(dp[i - 1][last] + alpha[to_idx[s1[m - i]]][to_idx[s2[n - j]]],
                             dp[i - 1][ind] + delta,
                             dp[i][last] + delta)
        last = ind
        ind = (ind + 1) % 2
    return [row[last] for row in dp]


# return string in each recursion
def divide_conquer(s1, s2):
    m = len(s1)
    n = len(s2)

    if m <= 2 or n <= 2:
        dp = alignment(s1, s2)
        return back_track(s1, s2, dp)

    front = se_alignment(s1, s2[:n // 2])
    back = backward_se_alignment(s1, s2[n // 2:])
    idx = -1
    min_score = sys.maxsize
    for i in range(m + 1):
        if front[i] + back[m - i] < min_score:
            min_score = front[i] + back[m - i]
            idx = i

    left_str = divide_conquer(s1[:idx], s2[:n // 2])
    right_str = divide_conquer(s1[idx:], s2[n // 2:])
    x = left_str[0] + right_str[0]
    y = left_str[1] + right_str[1]
    return [x, y]


def score_cal(s1, s2):
    score = 0
    for i in range(len(s1)):
        if s1[i] == '_' or s2[i] == '_':
            score += delta
        else:
            score += alpha[to_idx[s1[i]]][to_idx[s2[i]]]

    return score


if __name__ == '__main__':
    input = open(sys.argv[1])
    # input = open("input1.txt")
    # output = open("o1.txt", "w")
    lines = input.readlines()
    for i in range(1, len(lines) + 1):
        if lines[i][0] in "ACTG":
            input_x = lines[:i]
            input_y = lines[i:]
            break
    str_x = make_str(input_x)
    str_y = make_str(input_y)
    start_time = time.time()
    # print(str_x)
    # print(str_y)
    match_x, match_y = divide_conquer(str_x, str_y)
    score = score_cal(match_x, match_y)

    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    space = process_memory()

    f = open(sys.argv[2], "w")
    result = str(score) + "\n" + match_x + "\n" + match_y + "\n" + str(time_taken) + "\n" + str(space)
    f.write(result)

#     # print(match_x)
#     # print(match_y)
#     # print(dp[-1][-1])
#     # print(time_taken)
#     # print(space)


# # generate data for plot
# if __name__ == '__main__':
#     dir = sys.argv[1]
#     output_dict = {}
#     counter = 1

#     for filename in os.listdir(dir):
#         f = os.path.join(dir, filename)
#         print(f)

#         input = open(f)
#         # input = open("input1.txt")
#         # output = open("o1.txt", "w")
#         lines = input.readlines()
#         for i in range(1, len(lines) + 1):
#             if lines[i][0] in "ACTG":
#                 input_x = lines[:i]
#                 input_y = lines[i:]
#                 break
#         str_x = make_str(input_x)
#         str_y = make_str(input_y)
#         start_time = time.time()
#         # print(str_x)
#         # print(str_y)
#         match_x, match_y = divide_conquer(str_x, str_y)
#         score = score_cal(match_x, match_y)

#         end_time = time.time()
#         time_taken = (end_time - start_time) * 1000
#         space = process_memory()

#         input.close()
#         # f.close()
#         counter += 1
#         output_dict[len(str_x) + len(str_y)] = str(len(str_x) + len(str_y)) + "," + str(time_taken) + "," + str(space)

#     output_str = ""
#     for key in sorted(output_dict):
#         output_str += output_dict[key] + "\n"
#     output_file = open("output_e.txt", "w")
#     output_file.write(output_str)
#     output_file.close()
