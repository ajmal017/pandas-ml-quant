import numpy as np
import pandas as pd
from numba import guvectorize, float32, int32, float64, int64

from pandas_ml_common.utils import has_indexed_columns


def returns_to_log_returns(returns):
    return np.log(1 + returns)


def log_returns_to_returns(log_returns):
    return (np.e ** log_returns) - 1


@guvectorize([(float32[:], int32, float32[:]),
              (float64[:], int64, float64[:])], '(n),()->(n)')
def wilders_smoothing(arr: np.ndarray, period: int, res: np.ndarray):
    assert period > 0
    alpha = (period - 1) / period
    beta = 1 / period

    res[0:period] = np.nan
    res[period - 1] = arr[0:period].mean()
    for i in range(period, len(arr)):
        res[i] = alpha * res[i-1] + arr[i] * beta


def with_column_suffix(suffix, po, ref_po=None):
    if ref_po is None:
        ref_po = po

    if has_indexed_columns(po):
        if isinstance(po.index, pd.MultiIndex):
            po.columns = pd.MultiIndex.from_tuples([(suffix, *col) for col in ref_po.columns.to_list()])
            return po
        else:
            po.columns = ref_po.columns
            return po.add_suffix(f'_{suffix}')
    else:
        if isinstance(po.name, tuple):
            return po.rename((suffix, *ref_po.name))
        else:
            return po.rename(f'{ref_po.name}_{suffix}')


# return index of bucket of which the future price lies in
def index_of_bucket(value, data):
    if np.isnan(value) or np.isnan(data).any() or np.isinf(value) or np.isinf(value).any():
        return np.nan

    for i, v in enumerate(data):
        if value < v:
            return i

    return len(data)
