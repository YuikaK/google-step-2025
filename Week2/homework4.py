import random, sys, time
start = time.perf_counter()

# 実行結果をexecution_result.txtに記録した

def calculate_hash(key): 
    assert type(key) == str
    hash = 0
    p = 128 # ASCCIIコードで表現できる最大の数
    mod = 2147483647 # 大きな素数

    for c in key:
        hash = (hash * p + ord(c)) % mod # 元のhash値をp倍してUnicode値に足して素数で割った余り
    return hash

def next_prime(n): # nの次の素数を探す関数
        print("next_prime called with n:", n, file=sys.stderr) # デバッグ用
        def is_prime(x): # 素数かどうかを判定する関数
            if x < 2:
                return False
            for i in range(2, int(x ** 0.5) + 1): # 2以上√x以下の整数(素数ではない場合、2から√xまでの間に必ず約数が存在するため)
                if x % i == 0: # 割り切れたとき
                    return False
            return True # 素数だったとき

        while True:
            if is_prime(n): # 素数だったとき
                return n
            n += 1

class Item: # 連結リストのノード　Itemクラス
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next

class HashTable: # ハッシュテーブルクラス

    # Initialize the hash table.
    def __init__(self): # コンストラクタ　インスタンスが作られたときに一度だけ実行される
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size # bucketsを初期化
        self.item_count = 0 # 要素数

    def put(self, key, value): # ハッシュテーブルに新しい要素を追加したか、既存のキーの値を更新したかを確認する関数
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size # ハッシュ値を計算しbucket_sizeで割った余りをbucket_indexに代入
        item = self.buckets[bucket_index] # (buckets_index-1)番目の要素を取得し、itemに代入
        while item:
            if item.key == key: # 現在のitemが探しているkeyと一致したとき
                item.value = value # valueを上書き
                return False # 既存のキーを更新したのでFalseを返す
            item = item.next # 見つからなければ次のノードに移動
        new_item = Item(key, value, self.buckets[bucket_index]) # 新しいItemを作成する
        self.buckets[bucket_index] = new_item # bucketsの(buckets_index-1)番目の要素をnew_itemに更新する
        self.item_count += 1 # 登録されたアイテム数を1増やす
        if self.item_count > self.bucket_size * 0.7: # 要素数がbucket_sizeの70%を上回ったら
            self.rehash(self.bucket_size * 2) # テーブルサイズを2倍に
        return True # 新規追加なのでTrueを返す

    def get(self, key): # ハッシュテーブルから要素を取得する関数
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True) # 見つかれば item.value と Trueを返す
            item = item.next # 見つからなければ次のノードに移動
        return (None, False) # 見つからなければ(None, False)

    def delete(self, key): # ハッシュテーブルから要素を削除する関数
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        prev = None # 1つ前のノードを記録するための変数
        while item:
            if item.key == key:
                if prev is None: #削除対象が先頭ノードだったとき
                    self.buckets[bucket_index] = item.next # 削除対象の次のノードに置き換えることで削除
                else: # 先頭以外だった場合
                    prev.next = item.next # 途中のノードを削除
                self.item_count -= 1
                if self.bucket_size > 97 and self.item_count < self.bucket_size * 0.3: # 要素数が97以上かつbucket_sizeの30%を下回ったら
                    self.rehash(max(97, self.bucket_size // 2)) # テーブルサイズを半分にする 97より小さくならないようにする
                return True # 削除したのでTrueを返す
            prev = item # 現在のノードをprevにする
            item = item.next
        return False # 削除していないのでFalseを返す

    def size(self):
        return self.item_count # 格納してある要素数を返す

    def check_size(self): # ハッシュテーブルのサイズと要素数のバランスが適切か否か
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)

    def rehash(self, new_bucket_size): # 再ハッシュ関数
        print("rehash called with new_bucket_size:", new_bucket_size, file=sys.stderr)
        new_bucket_size = next_prime(new_bucket_size)  # 次の素数の大きさに調整
        new_buckets = [None] * new_bucket_size # 新しい素数の大きさでbucketsを初期化

        for old_item in self.buckets: # 今のbucketsの中を見る
            while old_item:
                new_index = calculate_hash(old_item.key) % new_bucket_size # ハッシュ値の再計算（新バケットサイズで）
                new_item = Item(old_item.key, old_item.value, new_buckets[new_index]) # 新しいItemを先頭に追加していく
                new_buckets[new_index] = new_item
                old_item = old_item.next

        self.buckets = new_buckets # bucketsを新しいものに更新
        self.bucket_size = new_bucket_size # サイズも更新

# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")

def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()

end = time.perf_counter() #計測終了
print('{:.2f}'.format(end-start))