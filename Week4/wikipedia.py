import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file): # self: インスタンス自身、pages_file: ページの情報が書かれたファイル、links_file: ページ間のリンク情報が書かれたファイル

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {} # ページIDをキーとして持ち、ページのタイトルを値とする辞書

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {} # あるページのIDをキーとして持ち、そのページにリンクされているページのIDのリストを値とする辞書

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ") # rstrip()で文字列の右側の空白を削除、split(" ")で空白で分割
                id = int(id) # ページIDを整数に変換
                assert not id in self.titles, id # ページIDがすでに存在していたらエラー
                self.titles[id] = title # ページIDをキーに、タイトルを値にする辞書に追加
                self.links[id] = [] # リンク先のリストを空のリストで初期化
        print("Finished reading %s" % pages_file) # ページの情報を持ったファイルの読み込みを完了したことを表示


        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")  # rstrip()で文字列の右側の空白を削除、split(" ")で空白で分割
                (src, dst) = (int(src), int(dst)) # src: ページID(source)、 dst: リンク先のページIDのリスト(destination))
                assert src in self.titles, src  # srcがtitlesに存在しない場合はエラー
                assert dst in self.titles, dst  # dstがtitlesに存在しない場合はエラー
                self.links[src].append(dst) # srcをキーとする辞書のリンクリストにdstを追加する
        print("Finished reading %s" % links_file) # リンクの情報を持ったファイルの読み込みを完了したことを表示
        print()


    """
    # Example: Find the longest titles.
    def find_longest_titles(self): # 最も長いタイトルを見つける関数
        titles = sorted(self.titles.values(), key=len, reverse=True) # タイトルを文字数の長さでソート（長い順 reverse = True）
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles): # タイトルの数が15未満で、インデックスがタイトルの個数より小さい間
            if titles[index].find("_") == -1: # アンダースコアが含まれていない場合(-1: 見つからなかったときの値)
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self): # 最もリンクされているページを見つける関数
        link_count = {} # リンクの数を数えるための辞書
        for id in self.titles.keys(): # 全てのキーを取り出してidに代入し、ループ
            link_count[id] = 0 # リンクの数を0で初期化

        for id in self.titles.keys(): # タイトルを値とする辞書からキーを取り出してidに代入し、ループ
            for dst in self.links[id]:  # リンク先のページIDを取り出してdstに代入
                link_count[dst] += 1 # リンク先のページIDの数をカウントする

        print("The most linked pages are:")
        link_count_max = max(link_count.values()) # リンクの数の最大値を取得
        for dst in link_count.keys(): # リンクの数を値とする辞書からキーを取り出してdstに代入し、ループ
            if link_count[dst] == link_count_max: # リンクの数が最大値と等しいとき
                print(self.titles[dst], link_count_max)
        print()
    """


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        prev = {}  # 前のページを記録するための辞書
        shortest_path = [] # 最短経路のリストを初期化
        queue = collections.deque()  # キューを初期化
        start_id = [k for k, v in self.titles.items() if v == start][0]  # 開始ページのIDを取得
        goal_id = [k for k, v in self.titles.items() if v == goal][0]  # 目標ページのIDを取得
        queue.append(start_id)  # 開始ページのIDをキューに追加
        visited = set()  # 訪問済みのページを記録する辞書
        visited.add(start_id)

        while queue: # キューが空でない間
             node = queue.popleft() # キューからノードを取り出す
             if node == goal_id:
                  break # 目標ページに到達したらループを抜ける
             for child in self.links.get(node, []): # 現在のノードからリンクされている子ページを取得
                  if not child in visited: # 子ページが訪問済みでない場合
                       visited.add(child)
                       prev[child] = node # childをキーとする辞書にchildへ来る直前のノードを値として記録
                       queue.append(child) # 子ページをキューに追加
        
        path_id = []  # 最短経路を格納するリスト
        if goal_id in prev: # 目標ページに到達できた場合
            node = goal_id
            while node != start_id: # 目標ページから開始ページまでの経路をたどる
                path_id.append(node) # pathに現在のノードを追加
                node = prev[node]  # 前のページに戻る
            path_id.append(start_id) # 開始ページをpathに追加
            path_id.reverse() # 最短経路を逆順にする
        else: # 目標ページに到達できなかった場合
            print("No path found from '%s' to '%s'." % (start, goal))
            return
        
        shortest_path = [self.titles[id] for id in path_id] # ページIDをタイトルに変換して最短経路を作成
        print("The shortest path from '%s' to '%s' is:" % (start, goal))
        print(shortest_path) # 最短経路を表示
        print()



    def update_pagerank(self, d, items, pagerank, new_pagerank, page_id):
        share = d * pagerank[page_id] / len(items) # リンク先に分配するPageRankの割合を計算
        for dst in items: # リンク先の各ページに対して
            new_pagerank[dst] += share # 分配されたPageRankを加算
    
    def get_newpagerank(self, pagerank):
        d = 0.85
        N = len(self.titles)
        new_pagerank = {id: (1 - d) / N for id in self.titles} # リンクをたどる確率分を初期化

        for page_id in self.titles: # 各ページIDに対してループ
            links = self.links.get(page_id, []) # 現在のページIDからリンクされているページのリストを取得
            if links: # 外部リンクがある場合
                self.update_pagerank(d, links, pagerank, new_pagerank, page_id)
            else:
                self.update_pagerank(d, self.titles, pagerank, new_pagerank, page_id)
            
        return new_pagerank
    
    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        N = len(self.titles) # 総ノード数（ページ数）
        pagerank = {id: 1 / N for id in self.titles} # 各ページの初期PageRankを1/Nで初期化し値とする辞書を作成
        converged = False # 収束フラグをFalseで初期化

        while not converged: # 収束するまでループ
            new_pagerank = self.get_newpagerank(pagerank)
          
            diff = sum((new_pagerank[id] - pagerank[id]) ** 2 for id in self.titles) # newとoldの差の二乗の総和を計算
            if diff < 0.01: # 差が0.01以下なら収束
                converged = True # 収束フラグをTrueに設定

            pagerank = new_pagerank # PageRankを更新

        sorted_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True) # PageRankの値でソート（降順）
        print("Most popular pages:")
        for id, rank in sorted_pages[:15]:  # 上位15件を表示
            print(f"{self.titles[id]}: {rank:.6f}")
        print()


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    # wikipedia.find_shortest_path("A", "F")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
