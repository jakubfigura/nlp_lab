import numpy as np
import pandas as pd

class Needleman_Wunsch:

    def __init__(self, seq1: str, seq2: str, penalty: int):
        self.seq1 = seq1
        self.seq2 = seq2
        self.penalty = penalty
        self.answer = None
        self.alignment_score = None
        self.AlignmentA = None
        self.AlignmentB = None
    

    def score(self, ch1, ch2):
        if ch1 == ch2:
            return 1
        else:
            return -1
        

    def create_matrix(self):

        A = "-" + self.seq1
        B = "-" + self.seq2
        self.seq1 = A
        self.seq2 = B
        
        lengthA = len(A)
        lengthB = len(B)

        trace_matrix = np.zeros(shape = (lengthB, lengthA))

        for i in range(lengthA):
            trace_matrix[0][i] = self.penalty * i
        for j in range(lengthB):
            trace_matrix[j][0] = self.penalty * j

        for i in range(1, lengthA):
            for j in range(1, lengthB):
                match = trace_matrix[j-1][i-1] + self.score(A[i], B[j])
                delete = trace_matrix[j-1][i] + self.penalty
                insert = trace_matrix[j][i-1] + self.penalty
                trace_matrix[j][i] = max(match, delete, insert)
        
        result = trace_matrix[-1][-1]
        self.answer = trace_matrix
        self.alignment_score = result


    def trace_back(self):
        AlignmentA = ""
        AlignmentB = ""
        A = self.seq1
        B = self.seq2
        i = len(A) - 1
        j = len(B) - 1

        while (i > 0) or (j > 0):
            if i == 0:
                AlignmentA = "-" + AlignmentA
                AlignmentB = B[j] + AlignmentB
                j -= 1
            elif j == 0:
                AlignmentA = A[i] + AlignmentA
                AlignmentB = "-" + AlignmentB
                i -= 1
            elif self.answer[j][i] == self.answer[j-1][i-1] + self.score(A[i], B[j]):
                AlignmentA = A[i] + AlignmentA
                AlignmentB = B[j] + AlignmentB
                i -= 1
                j -= 1
            elif self.answer[j][i] == self.answer[j][i - 1] + self.penalty:
                AlignmentA = A[i] + AlignmentA
                AlignmentB = "-" + AlignmentB
                i -= 1
            else:
                AlignmentA = "-" + AlignmentA
                AlignmentB = B[j] + AlignmentB
                j -= 1
        self.AlignmentA = AlignmentA
        self.AlignmentB = AlignmentB





file = "grimm-letters.txt"
df = pd.read_csv(file, sep='\t', header=None, names=["ID", "TEXT", "SOURCE", "DATE"])

TEXTS = df["TEXT"]
IDS = df['ID'].astype("str")

textA = {IDS[i]: TEXTS[i] for i in range(len(TEXTS)) if IDS[i][0]== "1"}
textB = {IDS[i]: TEXTS[i] for i in range(len(TEXTS)) if IDS[i][0]== "2"}
textC = {IDS[i]: TEXTS[i] for i in range(len(TEXTS)) if IDS[i][0]== "3"}

for i in range(1, len(textA)+1):
    A = textA[f"11001000{i}"]
    B = textC[f"31001000{i}"]
    nw = Needleman_Wunsch(A, B, penalty=-1)
    nw.create_matrix()
    nw.trace_back()
    print("="*20)
    print(nw.AlignmentA)
    print(nw.AlignmentB)
    print(f"Wynik dopasowania: {nw.alignment_score}")
    print("="*20)













