import graph_tool.all as gt
import sys

# ネットワーク(.gt形式)を読み込む
args = sys.argv
if len(args) > 1:
    g = gt.load_graph(args[1])
    
    N = g.num_vertices()
    M = g.num_edges()
    print(f"ノード数: {int(N)}, リンク数: {int(M)}")
    
    if g.is_directed():
        print("このネットワークは有向グラフです")
    else:
        print("このネットワークは無向グラフです")
    
    position = gt.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    gt.graph_draw(g, pos=position, output_size=(1000, 1000));
    
    # GC確認
    GC = gt.GraphView(g, vfilt=gt.label_largest_component(g))
    N_gc = GC.num_vertices()
    if N != N_gc:
        print("GCに属していないノードが存在します")
    
    # 多重リンクの確認
    self_loop = 0
    multiple_edge = 0
    for v in g.vertices():
        # 自己ループの検出
        if g.edge(v, v) is not None:
            print(f"ノード {int(v)} に自己ループが存在します")
            self_loop += 1
        
        # 多重リンクの検出
        for u in range(int(v) + 1, N):
            edges = list(g.edge(int(v), u, all_edges=True))
            if len(edges) > 1:
                print(f"ノード {int(v)} と {u} の間に多重リンクが存在します")
                multiple_edge += 1
    
    print(f"自己ループは {int(self_loop)} 個あります")
    print(f"多重リンクは {int(multiple_edge)} 個あります") 
