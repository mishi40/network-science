'''
ネットワークデータの各種指標を計算する
入力: 第1引数 ネットワークデータ名(.gt形式),
      第2引数 次数分布の軸スケール(x, yの順に0で線形, 1で対数, 省略時は"00")
出力: ノード数N, 総リンク数M, 平均次数<k>, 最小次数k_min, 最大次数k_max,
      直径D, 平均経路長<L>, 次数分布P(k)(matplotlib)
'''

import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import sys

try:
    g = gt.load_graph(sys.argv[1])
    
    N = g.num_vertices()
    M = g.num_edges()
    
    # D と <L> は連結なネットワークでのみ意味を持つ指標
    # 次数関連
    deg = g.get_total_degrees(g.get_vertices())
    k_ave = float(np.mean(deg))      # 無向ネットワークでは 2M/N と一致する
    k_min = int(np.min(deg))
    k_max = int(np.max(deg))
    count = np.bincount(deg)         # インデックスkの要素が次数kのノード数
    k_list = np.nonzero(count)[0]    # ノードが1つ以上存在するkのみ残す
    Pk = count[k_list] / N
    
    # 最短経路長(全ノードから幅優先探索を行う)
    _, hist = gt.label_components(g)
    if len(hist) > 1:
        print(f"warning: このネットワークには複数の連結成分が存在します")
        print("         D と <L> は到達可能なノードのペアのみで計算します")
    INF = np.iinfo(np.int32).max    # graph-toolは到達不可能な距離をこの値で表す
    D = 0
    d_sum = 0
    n_pairs = 0
    for v in g.vertices():
        d = gt.shortest_distance(g, source = v).a
        d = d[(d > 0) & (d < INF)]    # 自分自身(距離0)と到達不可能なペアを除く
        if d.size == 0:
            continue
        D = max(D, int(np.max(d)))
        d_sum += int(np.sum(d))
        n_pairs += d.size
    L_ave = d_sum / n_pairs
    
    # 各指標を出力
    print(f"N:\t{N}")
    print(f"M:\t{M}")
    print(f"<k>:\t{k_ave:.4f}")
    print(f"k_min:\t{k_min}")
    print(f"k_max:\t{k_max}")
    print(f"D:\t{D}")
    print(f"<L>:\t{L_ave:.4f}")
    
    # 次数分布を描画
    plt.rcParams["font.size"] = 14
    plt.figure(figsize = (7, 7))
    plt.plot(k_list, Pk, marker = "o", linestyle = "-")
    scale = sys.argv[2] if len(sys.argv) > 2 else "00"    # 軸スケールの設定
    plt.xscale("log" if scale[0] == "1" else "linear")
    plt.yscale("log" if scale[1] == "1" else "linear")
    plt.xlabel("$k$")
    plt.ylabel("$P(k)$")
    plt.grid(True)
    plt.show()

except Exception as e:
    print(e)
    print(f"$ python3 {sys.argv[0]} [hoge.gt] [00|01|10|11 (plot mode)]")

