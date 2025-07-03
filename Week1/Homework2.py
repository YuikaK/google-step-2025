from collections import Counter
import time
start = time.perf_counter()

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# score_checker.pyより
def calculate_score(word): 
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

def read_words(filename): # ファイル読み込み　中身をリストとして返す
    words = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            words.append(line)
    return words

def get_best(sorted_dictionary_words, letters): # すでにソートされた辞書とランダムな文字列を引数に持つ
    letter_counts = Counter(letters) # Counterクラスを用いて文字の出現回数を記録する
    letters_set = set(letters) # ランダムな文字列に含まれる文字の種類だけを取り出す

    for word in sorted_dictionary_words: # スコアが高い順に並んでいるので早く見つかった単語がベストスコアな可能性が高い
        if not set(word).issubset(letters_set): # set(word)：単語に含まれる文字の集合　issubset(letters_set)：すべての文字が入力文字に含まれているか
            continue # 含まれていなかった場合次の単語へ

        word_counts = Counter(word)
        if all(word_counts[c] <= letter_counts[c] for c in word_counts): # すべての文字cについて、word_counts[c] <= letter_counts[c] が成り立つとき
            return calculate_score(word), word  # 最初に見つけた時点でreturn

    return 0, "" #作れる単語が見つからなかった場合

def main():
    data_words = read_words("anagram/large.txt") # "anagram/large.txt" "anagram/medium.txt"
    dictionary_words = read_words("anagram/words.txt")
    sorted_dictionary_words = sorted(dictionary_words, key=calculate_score, reverse=True)
    output_file = "anagram/large_answer.txt" # "anagram/large_answer.txt" "anagram/medium_answer.txt"

    results = []
    for letters in data_words:
        score, best_word = get_best(sorted_dictionary_words, letters)
        results.append(best_word)
    
    # 結果をファイルに出力
    with open(output_file, "w") as f:
        for word in results:
            f.write(word + "\n")

if __name__ == "__main__":
    main()

end = time.perf_counter() #計測終了
print('{:.2f}'.format(end-start))