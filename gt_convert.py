'''
テキスト形式のネットワークデータをGraphオブジェクトに変換し、ファイルに保存する
入力: 第1引数 ネットワークデータ名(.txt)
出力: 同名の.gt形式のファイル
'''

import graph_tool.all as gt
import sys

try:
    # 1行に1リンク(`ノード名 ノード名`)が書かれているものとして読み込む
    edge_list = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            if line.startswith('#'):    # コメント行は読み飛ばす
                continue
            nodes = line.split()
            if len(nodes) < 2:          # 空行や不完全な行は読み飛ばす
                continue
            edge_list.append((nodes[0], nodes[1]))    # 3列目以降(重みなど)は無視する

    g = gt.Graph(directed = False)
    v_original_id = g.add_edge_list(edge_list, hashed = True)    # 元のノード名とインデックスの対応
    g.vertex_properties["name"] = v_original_id
    g.save(f"{sys.argv[1][:-4]}.gt")

except Exception as e:
    print(e)
    print(f"$ python3 {sys.argv[0]} [hoge.txt (network data)]")

