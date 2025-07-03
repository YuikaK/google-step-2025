"""
def anagram_solution(random_word, dictionary):
    sorted_random_word = sorted(random_word) # ランダムな文字列をソート

    new_dictionary = []
    for word in dictionary:
        new_dictionary.append((sorted(word),word)) # ソートした辞書の単語と元の単語を合わせて保存
    new_dictionary = sorted(new_dictionary,key=lambda x: x[0]) # リストを0番目の要素でソート
    # new_dictionary[i][0]:単語をソートしたリスト
    # new_dictionary[i][1]:元の単語
    anagram = binary_search(new_dictionary, sorted_random_word)
    return anagram
    
def binary_search(sorted_dictionary, sorted_word):
    anagram = []
    left, right = 0, len(sorted_dictionary) - 1
    while left <= right:
        mid = left + (right - left) // 2 
        if sorted_dictionary[mid][0] < sorted_word: # 中央よりあとにあるとき
            left = mid + 1
        elif sorted_dictionary[mid][0] > sorted_word: # 中央より前にあるとき
            right = mid - 1
        else:
            anagram.append(sorted_dictionary[mid][1]) # anagramリストに元の単語を追加
            upper = mid + 1 # 中央よりひとつ後ろの要素も探す
            lower = mid - 1 # 中央よりひとつ前の要素も探す
            while True:
                if upper >= len(sorted_dictionary): # リストの長さを超えるとき
                    break
                if sorted_dictionary[upper][0] != sorted_word: # 単語が異なるとき
                    break
                anagram.append(sorted_dictionary[upper][1])
                upper += 1

            while True:
                if lower < 0: # 範囲外になるとき
                    break
                if sorted_dictionary[lower][0] != sorted_word: # 単語が異なるとき
                    break
                anagram.append(sorted_dictionary[lower][1])
                lower -= 1  
            break
    return anagram
"""

def build_anagram_dict(dictionary): # 辞書型を返す関数
    anagram_dict = {} # key:ソートされた文字列 value:元の単語
    for word in dictionary:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_dict: # 辞書にすでに入っていたら
            anagram_dict[sorted_word].append(word) # keyに元の単語を追加する
        else:
            anagram_dict[sorted_word] = [word] # 入っていなかったら辞書にその言葉を入れる
    return anagram_dict

def anagram_solution(random_word, anagram_dict): # ランダムな文字列が辞書型に含まれているかを調べる関数
    sorted_random_word = ''.join(sorted(random_word)) # ランダムな文字列をソートしてキーを作成
    return anagram_dict.get(sorted_random_word, []) # 辞書からそのキーに対応するリストを取り出す　見つからなければ空リストを返す

def main():
    random_word = input()
    import time
    start = time.perf_counter()
    with open("anagram/words.txt", 'r') as f:
        dictionary = [word.strip() for word in f.readlines()]  
    anagram_dict = build_anagram_dict(dictionary)  # 辞書型に変換
    result = anagram_solution(random_word, anagram_dict)
    print(result)
    end = time.perf_counter() #計測終了
    print('{:.2f}'.format(end-start))

if __name__ == "__main__":
    main()
