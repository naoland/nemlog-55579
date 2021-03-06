# フローチャートをプログラムで書くことのメリット（その2）


## はじめに

過去記事において、フローチャートをプログラムで書くことのメリットを語りました。
今回のこの記事では、実際にメリットの例を紹介していきたいと思います。

### フローチャートをプログラムで書くことのメリット

以前の記事で次のようなご紹介をしました

- 条件によって、チャートの出力を動的に変更できます。これはべたでチャートを書くことでは得られないメリットです。
- 大量の項目を含んだチャート図を出力する。これはチャートツールではなかなかむつかしいと思います。
- チャートの情報はテキストで書きますので、GitHubで管理できます。そのため何を変更したのか確認することも簡単です。
- ツールを使って書いた場合、位置の修正が大変です。プログラミングで行う場合は調整が楽かまたは気にしなくても良いです。
- 作図ツール・サービスはたくさんありますが、ベンダーロックオンの可能性があります。しかしそれらのツールやサービスを使用せずに、コードでチャートを書ければ、`dot`ファイルを出力するツールやライブラリに依存することがあっても、出力された`dot`ファイルもgitで管理すれば、将来においても修正を行ってメンテナンスを継続できます。

### デメリット

- ある程度のプログラミングの知識が必要。今回の場合だと`Python`言語の文法について多少知っている必要があります。
- 細かい位置調整は面倒くさい

## 条件によってチャートの出力を動的に変更

今回の例では、ZEMの最終価格をZaif取引所のAPIから取得して、その結果によって異なるフローチャートを生成しています。

出力形式はPNGやJPG、SVG、PDFなどを指定できますが、今回はpngで出力しています。


### 出力結果

左の図は`XEM`が40円以上、右の図は`XEM`が40円未満の場合です。

![](./images/example_flow1.png)
![](./images/example_flow2.png)

### コードの内容

```python
import sys
from graphviz import Digraph
from zaifapi import ZaifPublicApi, ZaifFuturesPublicApi, ZaifLeverageTradeApi

FILENAME: str = "dist/flow.dot"
DEBUG: bool = True
THRESHOLD: float = 40.0 # 閾値


def last_price(pair: str = "xem_jpy") -> float:
    """指定した通貨ペア（xem_jpyなど）の最終価格を取得して返します。"""
    zaif = ZaifPublicApi()
    result = zaif.last_price(pair)
    # print(type(result["last_price"]))
    if type(result["last_price"]) == float:
        return result["last_price"]
    else:
        return float(result["last_price"])


def flow(price: float, format: str = "png", comment: str = "") -> None:
    """ `price`の価格によって、異なるフローチャートを生成します。"""
    dot = Digraph(format=format, comment=comment)

    dot.node("start", "開始")
    dot.node("step1", "NEM（XEM）の最終価格を取得します", shape="box")
    if price >= THRESHOLD:
        dot.node(
            "step2",
            str(f"取得結果：{price} JPY"),
            shape="oval",
            style="filled",
            fillcolor="lightcyan",
        )
    else:
        dot.node(
            "step2",
            str(f"取得結果：{price} JPY"),
            shape="oval",
            style="filled",
            fillcolor="orange",
        )
    dot.node("step3", "40.0JPY以上ですか？", shape="diamond")
    dot.node("end", "終了")

    dot.edge("start", "step1")
    dot.edge("step1", "step2")
    dot.edge("step2", "step3")
    if price >= THRESHOLD:
        dot.node("step4-y", "売り時を待つ", shape="box")
        dot.edge("step3", "step4-y", label=" YES")
        dot.edge("step4-y", "end")
    else:
        dot.node("step4-n", "買い増しを検討する", shape="box")
        dot.edge("step3", "step4-n", label=" NO")
        dot.edge("step4-n", "end")

    # view=Trueの場合はOSに指定されているデフォルトの画像ビューワーが起動します。
    dot.render(FILENAME, view=False)


if __name__ == "__main__":
    try:
        price = last_price("xem_jpy")
        message = f"XEM現在価格: {price} JPY"
        if DEBUG:
            print(message)
        flow(price, format="png")
    except:
        print(f"エラーが発生しました: {sys.exc_info()}")
```

## 動作確認

自分でも試してみたい方は以下のように進めてください。ぜひ条件を変更して試してみてください。

```python
THRESHOLD: float = 40.0 # 閾値
```

アンドロイドのTermux上でも動作確認済みです。UbuntuなどのLinuxでも動作すると思います（Ubuntu 20.04 LTS上では確認済み）。


任意の場所にリポジトリをダウンロードします。

```
& git clone https://github.com/naoland/nemlog-55579.git
```

ディレクトリを移動します。

```
& cd nemlog-55579
```

Pythonのがインストール済みか確認します。

```
$ make version
```

実行結果

```
 $ make version
/data/data/com.termux/files/usr/bin/python
Python 3.9.1
```

Pythonの仮想環境を作り、必要なライブラリをインストールします。
コマンドが終了するまでに結構時間がかかります。

```
$ make init
```

実行結果の表示はかなり長いので省略します。

なお、上記コマンドは1度だけ実行してください。またコマンドが終了するまでに結構時間がかかります。

Pythonプログラム`flow.py`を実行し、フローチャートの画像を`png`形式の画像ファイルとして出力します。

```
$ make run
```

実行結果

```
$ make run
./venv/bin/python ./flow.py
XEM現在価格: 40.1699 JPY
```

エラーが発生しなかった場合は、`dict`というディレクトリ内に、画像ファイルとドットファイルができているはずです。
ドットファイルについては今回は説明を割愛しますが、`Graphviz`の`dot`コマンドで画像ファイルを生成する際に使用します'

```
dist
├── flow.dot
└── flow.dot.png
```

フローチャートの画像ファイルをアンドロイドのファイラーアプリで閲覧、共有できる場所にコピーします。

注意）Termuxを使用していない場合は、Linuxのファイラーなどでクリックするか、ブラウザにドラッグアンドドロップして画像を表示してください。

```
$ make copy
```

実行結果

```
$ make copy
cp ./dist/flow.dot.png ~/storage/downloads
```

ファイルマネージャーというアンドロい用アプリを使うことを推奨します。関連情報へのリンクを参照してください。

ファイルマネージャーの`ダウンロード`というフォルダーに`flow.dot.png`が表示されているはずなので、それをタップします。次のように表示されると思います。

![](./images/flow.dot.png)


## まとめ

いかがでしたでしょうか？

フローチャートをプログラムによって自動生成することで、条件によって異なる内容のフローチャートを生成できる事がご理解いただけたと思います。

より複雑な条件であったり、外部のサービスから取得したデータによってフローチャートを自動生成する場合は非常に便利です。非常に高価な作図ツールでは、同様のこともできるようではありますが。。

他のフローチャートを自動生成する利点については、またの機会にご紹介したいと思います。


## 関連情報へのリンク

### ファイルマネージャー

- [ファイルマネージャー - Google Play のアプリ](https://play.google.com/store/apps/details?id=com.alphainventor.filemanager)
- [Android向けファイルマネージャーアプリのおすすめ人気ランキング8選【2020年最新版】 | mybest](https://my-best.com/6141#toc-1)

### Graphviz関連

- [Graphviz - Graph Visualization Software - Resources](https://www.graphviz.org/resources/)
- [Graphviz Online](http://dreampuf.github.io/GraphvizOnline/)

### Zaif API

- [techbureau/zaifapi: zaifのAPIを簡単にコール出来るようにしました。](https://github.com/techbureau/zaifapi)

### 作図ツール

- [draw.io](https://www.draw.io/)
- [Free Online Flowchart Maker | Figma](https://www.figma.com/templates/flowchart-maker/)
- [フローチャートやワイヤーフレーム、プレゼン資料まで作れる | Cacoo(カクー)](https://cacoo.com/ja/)

### 過去記事

- [フローチャートをプログラムで書くことのメリット（その1）](https://nemlog.nem.social/blog/55529)