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

texts = {IDS[i]: TEXTS[i] for i in range(len(TEXTS))}

scores = dict()

print("="*80)
print("PORÓWNANIE TEKST 1 Z TEKST 2")
print("="*80)

for keyA, valueA in textA.items():
    A = textA[keyA]
    scores_A_B = dict()

    for keyB, valueB in textB.items():
        B = textB[keyB]
        nw = Needleman_Wunsch(A, B, penalty=-1)
        nw.create_matrix()
        nw.trace_back()
        scores_A_B[nw.alignment_score] = (keyB, nw.AlignmentA, nw.AlignmentB)
        scores[nw.alignment_score] = [nw.AlignmentA, nw.AlignmentB]

    if scores_A_B:
        best_score = max(scores_A_B.keys())
        keyB, alignmentA, alignmentB = scores_A_B[best_score]
        print(f"\nLinia {keyA} (Tekst A) -> Linia {keyB} (Tekst B)")
        print(f"Alignment Score: {best_score}")
        print(f"Wyrównanie A: {alignmentA}")
        print(f"Wyrównanie B: {alignmentB}")

print("\n" + "="*80)
print("PORÓWNANIE TEKST 1 Z TEKST 3")
print("="*80)

for keyA, valueA in textA.items():
    A = textA[keyA]
    scores_A_C = dict()

    for keyC, valueC in textC.items():
        C = textC[keyC]
        nw = Needleman_Wunsch(A, C, penalty=-1)
        nw.create_matrix()
        nw.trace_back()
        scores_A_C[nw.alignment_score] = (keyC, nw.AlignmentA, nw.AlignmentB)

    if scores_A_C:
        best_score = max(scores_A_C.keys())
        keyC, alignmentA, alignmentC = scores_A_C[best_score]
        print(f"\nLinia {keyA} (Tekst A) -> Linia {keyC} (Tekst C)")
        print(f"Alignment Score: {best_score}")
        print(f"Wyrównanie A: {alignmentA}")
        print(f"Wyrównanie C: {alignmentC}")

print("\n" + "="*80)
print("PORÓWNANIE TEKST 2 Z TEKST 3")
print("="*80)

for keyB, valueB in textB.items():
    B = textB[keyB]
    scores_B_C = dict()

    for keyC, valueC in textC.items():
        C = textC[keyC]
        nw = Needleman_Wunsch(B, C, penalty=-1)
        nw.create_matrix()
        nw.trace_back()
        scores_B_C[nw.alignment_score] = (keyC, nw.AlignmentA, nw.AlignmentB)

    if scores_B_C:
        best_score = max(scores_B_C.keys())
        keyC, alignmentB, alignmentC = scores_B_C[best_score]
        print(f"\nLinia {keyB} (Tekst B) -> Linia {keyC} (Tekst C)")
        print(f"Alignment Score: {best_score}")
        print(f"Wyrównanie B: {alignmentB}")
        print(f"Wyrównanie C: {alignmentC}")
