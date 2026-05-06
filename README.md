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
```
import graph_tool.all as gt
g = gt.Graph(directed=False)
```

## リポジトリ内のファイルについて
### gt_convert.py
example.txt のようなテキスト形式のネットワークデータを Graph オブジェクトに変換し、ファイルに保存するプログラム
```
$ python3 gt_convert.py example(拡張子不要)
```
### example.txt
### network_check.py
