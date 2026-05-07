# graph-tool を使ったネットワーク分析プログラム

## graph-tool とは？
ネットワーク科学の研究者 Dr. Peixoto が開発した Python のモジュール。<br>
内部は C++ で実装されているため、よく知られたネットワーク分析ツールである NetworkX よりも高速に動作する。<br>
公式HP: https://graph-tool.skewed.de/

## 導入方法
pip コマンドでインストールはできない。<br>
Ubuntu や Arch などのよく使われる Linux ディストリビューションではパッケージマネージャを用いたインストールが可能。<br>
例）Debian 系
```
# apt -y install python3-graph-tool
```

## 基本の処理
```python
import graph_tool.all as gt

# ネットワークを表すGraphオブジェクトのインスタンス(無向)を生成
g = gt.Graph(directed=False)

# .gtファイルからネットワークデータを読み込む場合
g = gt.load_graph("hoge.gt")

# .gtファイルにネットワークデータを書き込む
g.save("foobaa.gt")

# ノード, リンクを追加
v0 = g.add_vertex()
v1 = g.add_vertex()
e0 = g.add_edge(v0, v1)

# ノード, リンクの削除
g.remove_vertex(v0)
g.remove_edge(e0)

# ノード, リンクの走査
for v in g.vertices():
    print(f"vertex: {int(v)}")

for e in g.edges():
    print(f"edge: {int(e.source())} - {int(e.target())}")

# ネットワークを描画(graph-toolの強みの1つ)
gt.graph_draw(g)
```

## リポジトリ内のファイルについて
### gt_convert.py
example.txt のようなテキスト形式のネットワークデータを Graph オブジェクトに変換し、ファイルに保存するプログラム<br>
出力される .gt 形式のファイルはバイナリファイル。
```
$ python3 gt_convert.py example(拡張子不要)
```
### example.txt
```
0 1
0 2
0 3
0 3
1 2
2 2
4 5
```
テキスト形式のネットワークデータのよくあるフォーマット。<br>
`a b` と書かれていたら、a というノードと b というノードの間にリンクが存在する。<br>
今回は無向ネットワークを想定。<br>
![example.png](example.png)
### network_check.py
