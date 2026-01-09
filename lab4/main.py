from tokenizer import BasicTokenizer
from regex_tokenizer import RegexTokenizer
from bs4 import BeautifulSoup
import pickle
import tiktoken
import sys


def XML_PARSER(file_path):
    with open(file_path, 'r', encoding="UTF-8") as f:
        xml_file = f.read()
    bs_data = BeautifulSoup(xml_file, 'xml')
    full_text = bs_data.get_text()
    return full_text

def save_model(model : BasicTokenizer, file_name):
    with open(f'{file_name}.pkl', 'wb') as f:
        pickle.dump(model, f)

def load_model(file_path):
    with open(file_path, 'rb') as f:
        tokenizer = pickle.load(f) 
    return tokenizer

def train_tokenizers():
    path = "POL0063_prus_lalka.xml"
    text = XML_PARSER(path)
    basic_prus_tokenizer = BasicTokenizer()
    basic_prus_tokenizer.train(text, 1000)

    save_model(basic_prus_tokenizer, "basic_prus")

    regex_prus_tokenizer = RegexTokenizer()
    regex_prus_tokenizer.train(text, 1000)

    save_model(regex_prus_tokenizer, "regex_prus")


    path = "taylorswift.txt"
    with open(path, "r") as f: 
        text_ts = f.read()
    
    basic_ts_tokenizer = RegexTokenizer()
    basic_ts_tokenizer.train(text_ts, 500)

    save_model(basic_ts_tokenizer, "basic_ts")


    regex_ts_tokenizer = RegexTokenizer()
    regex_ts_tokenizer.train(text_ts, 500)

    save_model(regex_ts_tokenizer, "regex_ts")

def main():
    arguments = sys.argv
    if len(arguments) > 1:
        if arguments[1] == "train":
            train_tokenizers()
        else:
            raise ValueError("Add 'train' as a flag if you want to train Tokenizers")
    
    BPtok = load_model("basic_prus.pkl")
    RPtokenizer = load_model('regex_prus.pkl')

    basic_ts_tokenizer = load_model('basic_ts.pkl')
    regex_ts_tokenizer = load_model('regex_ts.pkl')



    while True:
        print("Chose tokenizer from list:")
        print("Basic_Prus_Tokenizer: 0")
        print("Regex_Prus_Tokenizer: 1")
        print("Basic_TS_Tokenizer: 2")
        print("Regex_TS_Tokenizer: 3")
        print("Tiktokenizer: 4")
        print("Close: 5")
        number = int(input())
        if number == 0:
            print("Tokenizer chosen press enter, to went back")
            while True:
                text = input()
                if text == "":
                    break
                encoding = BPtok.encode(text)
                print(encoding)
                print(f"Compresion: {(1 - (len(encoding) / len(text))):.2%}")
                assert BPtok.decode((BPtok.encode(text))) == text

        if number == 1:
            print("Tokenizer chosen press enter, to went back")
            while True:
                text = input()
                if text == "":
                    break
                encoding = RPtokenizer.encode(text)
                print(encoding)
                print(f"Compresion: {(1 - (len(encoding) / len(text))):.2%}")
                assert RPtokenizer.decode(RPtokenizer.encode(text)) == text

        if number == 2:
            print("Tokenizer chosen press enter, to went back")
            while True:
                text = input()
                if text == "":
                    break
                encoding = basic_ts_tokenizer.encode(text)
                print(encoding)
                print(f"Compresion: {(1 - (len(encoding) / len(text))):.2%}")
                assert basic_ts_tokenizer.decode(basic_ts_tokenizer.encode(text)) == text


        if number == 3:
            print("Tokenizer chosen press enter, to went back")
            while True:
                text = input()
                if text == "":
                    break
                encoding = regex_ts_tokenizer.encode(text)
                print(encoding)
                print(f"Compresion: {(1 - (len(encoding) / len(text))):.2%}")
                assert regex_ts_tokenizer.decode(regex_ts_tokenizer.encode(text)) == text


        if number == 4:
            print("Tokenizer chosen press enter, to went back")
            while True:
                text = input()
                if text == "":
                    break
                enc = tiktoken.get_encoding("o200k_base")
                encoding = enc.encode(text)
                print(encoding)
                print(f"Compresion: {(1 - (len(encoding) / len(text))):.2%}")
                print(enc.decode(enc.encode(text)) == text)

        
        if number == 5:
            break




if __name__ == "__main__":
    main()









