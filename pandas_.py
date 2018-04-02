import pandas as pd


def str2period(x, tostring=False):
    """
    Convert string into pandas.Period
    ex) 99991231 -> 9999-12-31
    """
    if x is not None:
        ret = pd.Period(year=x // 10000, month=x // 100 % 100, day=x % 100, freq='D')
    else:
        ret = None

    if tostring and ret is not None:
        ret = str(ret)

    return ret


def str2boolean(df, col):
    """
    Convert string 'True'/'False' into boolean
    :param df: DataFrame
    :param col: column
    :return: DataFrame
    """
    df[col] = df[col].apply(lambda x: True if x == 'True' else False)
    return df
