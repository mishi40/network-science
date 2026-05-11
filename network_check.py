import graph_tool.all as gt
import sys

# ネットワーク(.gt形式)を読み込む
if len(sys.argv) < 2:
    print("引数が不足しています")
    print("ネットワークデータ名(.gt形式)を与えてください")
    sys.exit()

g = gt.load_graph(sys.argv[1])

# 入力されたネットワークの情報を表示
N = g.num_vertices()
M = g.num_edges()
print(f"ノード数: {int(N)}, リンク数: {int(M)}")

if g.is_directed():
    print("このネットワークは有向グラフです")
else:
    print("このネットワークは無向グラフです")

position = gt.sfdp_layout(g, cooling_step = 0.95, epsilon = 1e-2)
gt.graph_draw(g, pos = position, output_size = (1000, 1000));

# 最大連結成分のみであるかを確認し、そうでない場合は抽出
view_LC = gt.label_largest_component(g)    # 最大連結成分に属するかの真偽値のプロパティマップ 
LC = gt.GraphView(g, vfilt = view_LC)      # 最大連結成分のみのビュー
N_lc = LC.num_vertices()
if N != N_lc:
    print("最大連結成分に属していないノードが存在します")
    g = gt.Graph(LC, prune = True)    # ビューを実際のネットワークにする

# 自己ループと多重リンクを除去
gt.remove_self_loops(g)
gt.remove_parallel_edges(g)

# 入力データと異なるネットワークになった場合は描画＆ファイルに保存
N_new = g.num_vertices()
M_new = g.num_edges()
if N != N_new or M != M_new:
    print("整形したネットワークを表示します")
    gt.graph_draw(g, pos = position, output_size = (1000, 1000));
    g.save(f"{sys.argv[1][:-3]}-processed.gt")
