#!/usr/bin/env python3

import sys
import math

from common import read_input, print_tour


def distance(city1, city2): # 2つの都市の直線距離を計算(greedy_tourで使う)
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1]) # math.hypot : √(x² + y²) を計算する


def total_distance(tour, cities): # 指定された順番で都市を回ったときの総距離を計算
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) # tour : greedy_tourの返り値
               for i in range(len(tour)))


def greedy_tour(cities): # 貪欲法
    N = len(cities) # 都市の総数
    dist = [[distance(cities[i], cities[j]) for j in range(N)] for i in range(N)] # 都市間の距離をdistに保存
    """
    3つの都市なら
    dist = [
    [0.0, 5.0, 2.0],
    [5.0, 0.0, 3.0],
    [2.0, 3.0, 0.0]
    ]
    """
    current_city = 0 # 出発地点として0番目の都市をcurrent_cityに代入
    unvisited = set(range(1, N)) # まだ訪れていない都市の集合
    tour = [current_city] # 訪問順を記録するリスト

    while unvisited: # 全都市訪れるまで
        next_city = min(unvisited, key=lambda city: dist[current_city][city]) # 最も近い都市をnext_cityに代入
        unvisited.remove(next_city) # 訪問済にする
        tour.append(next_city) # 訪問順リストを更新
        current_city = next_city # 現在地を更新

    return tour # 訪問順リストを返す


def two_opt(tour, cities): # 2-opt(交差を解消し、経路を短縮)
    improved = True # 改善があったかを判定するフラグ
    while improved: # 前回のループで改善があったら
        improved = False # フラグをFalseに
        for i in range(1, len(tour) - 3): # 訪問順リストの中で1点目の位置を決める
            for j in range(i + 2, len(tour)): # 2点目の位置を決める
                
                prefix = tour[:i] # iより前の部分（変更しない）
                reversed_segment = tour[i:j] # iからj-1までの部分（これをあとで逆順にする）
                suffix = tour[j:] # j以降の部分（変更しない）
                reversed_segment = reversed_segment[::-1] # 中央部分だけ逆順にする
                new_tour = prefix + reversed_segment + suffix # 新しいツアーを結合

                if total_distance(new_tour, cities) < total_distance(tour, cities): # もしnew_tourの方が良さそうなら
                    tour = new_tour # リストを更新
                    improved = True # フラグをTrueに
    return tour # 改善した後の訪問順リストを返す


def solve(cities):
    tour = greedy_tour(cities)
    optimized_tour = two_opt(tour, cities)
    return optimized_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)