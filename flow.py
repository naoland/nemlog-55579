"""
 ZEMの最終価格をZaif取引所のAPIから取得して、その結果によって異なるフローチャートを生成します。
 出力形式はPNGやJPG、SVG、PDFなどを指定できます。
"""
import sys
from graphviz import Digraph
from zaifapi import ZaifPublicApi, ZaifFuturesPublicApi, ZaifLeverageTradeApi

FILENAME: str = "dist/flow.dot"
DEBUG: bool = True


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
    if price >= 40.0:
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
    if price >= 40.0:
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
