'''
与えたネットワークデータが分析に適した形であるかを確かめる
入力: 第1引数 ネットワークデータ名(.gt形式)
'''

import graph_tool.all as gt
import sys

try:
    # ネットワーク(.gt形式)を読み込む
    g = gt.load_graph(sys.argv[1])
    
    # 入力されたネットワークの基本的な情報を表示
    N = g.num_vertices()
    M = g.num_edges()
    print(f"ノード数: {int(N)}, リンク数: {int(M)}")
    if g.is_directed():
        print("このネットワークは有向グラフです")
    else:
        print("このネットワークは無向グラフです")
    
    # ネットワークを描画(広がって見えるように)
    gt.graph_draw(g,
                  pos = gt.sfdp_layout(g, cooling_step = 0.95, epsilon = 1e-2),
                  output_size = (1000, 1000))
    
    # 最大連結成分のみであるかを確認し、そうでない場合は抽出
    LC = gt.label_largest_component(g)       # 最大連結成分に属するかの真偽値のプロパティマップ 
    view_LC = gt.GraphView(g, vfilt = LC)    # 最大連結成分のみのビュー
    N_lc = view_LC.num_vertices()
    if N != N_lc:
        g = gt.Graph(view_LC, prune = True)    # ビューを実際のネットワークにする
    
    # 余分なリンクの除去
    gt.remove_self_loops(g)        # 自己ループ
    gt.remove_parallel_edges(g)    # 多重リンク
    
    # 入力データと異なるネットワークになった場合は描画＆ファイルに保存
    M_new = g.num_edges()
    if N != N_lc or M != M_new:
        print("整形したネットワークを表示します")
        print(f"ノード数: {int(N_lc)}, リンク数: {int(M_new)}")
        gt.graph_draw(g,
                      pos = gt.sfdp_layout(g, cooling_step = 0.95, epsilon = 1e-2),
                      output_size = (1000, 1000))
        g.save(f"{sys.argv[1][:-3]}-processed.gt")
    else:
        print("既に分析に適したネットワークです")

except Exception as e:
    print(e)
    print(f"$ python3 {sys.argv[0]} [hoge.gt]")

