from typing import Dict, Tuple

import click


def to_multi_parameter(ctx: click.Context, opt: click.Option, raw_values: Tuple[str]) -> Dict[str, str]:
    """多値を取る文字列型のパラメータのパースを行う。

    コマンドでの指定形式は、`cmd --multi-parameter param1=value1 param2=value2` の形式を想定する。
    このメソッドでは上記入力をパースし、次の形式の辞書に変換する。

    .. code-block: python

        {
            'param1': 'value1',
            'param2': 'value2',
        }

    Args:
        ctx (click.Context): click の実行時 context
        param (click.Option): click の仕様上必要だが用途は不明。
        raw_values (Tuple[str]): 入力値

    Returns:
        Dict[str, str]: パース結果
    """
    result = {}
    for raw_value in raw_values:
        key, *value = raw_value.split('=')
        value = '='.join(value)
        result[key] = value
    return result
