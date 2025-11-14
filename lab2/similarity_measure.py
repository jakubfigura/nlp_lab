import numpy as np
import pandas as pd


def score(ch1, ch2):
    if ch1 == ch2:
        return 1
    else:
        return -1
    

def create_matrix(seq1, seq2, penalty = -1):

    A = "-" + seq1
    B = "-" + seq2
    
    lengthA = len(A)
    lengthB = len(B)

    trace_matrix = np.zeros(shape = (lengthB, lengthA))

    for i in range(lengthA):
        trace_matrix[0][i] = penalty * i
    for j in range(lengthB):
        trace_matrix[j][0] = penalty * j

    for i in range(1, lengthA):
        for j in range(1, lengthB):
            match = trace_matrix[j-1][i-1] + score(A[i], B[j])
            delete = trace_matrix[j-1][i] + penalty
            insert = trace_matrix[j][i-1] + penalty
            trace_matrix[j][i] = max(match, delete, insert)
    
    result = trace_matrix[-1][-1]

    return trace_matrix, result

def trace_back(answer, A, B, penalty = -1):
    AligmentA = ""
    AligmentB = ""
    A = "-" + A
    B = "-" + B
    i = len(A) - 1
    j = len(B) - 1

    while (i > 0) and (j > 0):
        if (i > 0 and j > 0 and answer[j][i]==answer[j-1][i-1] + score(A[i], B[j])):
            AligmentA = A[i] + AligmentA
            AligmentB = B[j] + AligmentB
            i = i - 1
            j = j - 1
        elif (i > 0 and answer[j][i] == answer[j][i - 1] + penalty):
            AligmentA = A[i] + AligmentA
            AligmentB = "-" + AligmentB
            i = i - 1
        else:
            AligmentA = "-" + AligmentA
            AligmentB = B[j] + AligmentB
            j = j - 1
    
    return AligmentA, AligmentB


file = "grimm-letters.txt"
df = pd.read_csv(file, sep='\t', header=None, names=["ID", "TEXT", "SOURCE", "DATE"])
print(df.head())

TEXTS = df["TEXT"]
print(TEXTS)

A = TEXTS[6]
B = TEXTS[19]

answer, result = create_matrix(A, B)
A1, B1 = trace_back(answer, A, B)
print(result)
print(A1)
print(B1)








