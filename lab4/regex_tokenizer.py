from tqdm import tqdm
import regex as re

GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""


class RegexTokenizer:

    def __init__(self, pattern = None):
        self.pattern = GPT4_SPLIT_PATTERN if pattern is None else pattern
        self.compiled_pattern = re.compile(self.pattern)
        self.ids = []
        self.merges = dict()
        self.vocab = dict()

    @staticmethod
    def get_stats(tokens):
        stats = dict()
        for pair in zip(tokens, tokens[1:]):
            stats[pair] = stats.get(pair, 0) + 1
        return stats
    
    @staticmethod
    def compress(tokens, pair, new_token):
        i = 0
        n = len(tokens)
        compressed_tokens = []
        while i < n:
            if i < n - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                compressed_tokens.append(new_token)
                i += 2
            else: 
                compressed_tokens.append(tokens[i])
                i+=1
        return compressed_tokens
    

    def train(self, text, vocab_size = None, verbose = False):
        text_chunks = re.findall(self.compiled_pattern, text)
        idx = 256
        if vocab_size is None:
            vocab_size = 276
        num_merges = vocab_size - idx
        self.ids = [list(ch.encode("utf-8")) for ch in text_chunks]
        

        for _ in tqdm(range(num_merges)):
            stats = {}
            for chunk_ids in self.ids:
                chunk_stats = RegexTokenizer.get_stats(chunk_ids)
                for pair, count in chunk_stats.items():
                    stats[pair] = stats.get(pair, 0) + count

            if not stats:
                break

            pair = max(stats, key=stats.get)
            self.ids = [RegexTokenizer.compress(chunk_ids, pair, idx) for chunk_ids in self.ids]
            self.merges[pair] = idx
            idx += 1
        self.vocab = {idx: bytes([idx]) for idx in range(256)}

        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]


    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        while True:
            stats = RegexTokenizer.get_stats(tokens)
            pair = min(stats, key = lambda p : self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens = RegexTokenizer.compress(tokens, pair, idx)
        return tokens
        

    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        return text
    












