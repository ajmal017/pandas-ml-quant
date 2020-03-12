from typing import Tuple, List

import pandas as pd

from pandas_ml_common.utils.callable_utils import call_if_not_none
from pandas_ml_common.utils import get_pandas_object, intersection_of_index, loc_if_not_none


def extract_feature_labels_weights(
        df: pd.DataFrame,
        features_and_labels,
        **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]:
    features = get_pandas_object(df, features_and_labels.features, **kwargs).dropna()
    labels = get_pandas_object(df, features_and_labels.labels, **kwargs).dropna()
    targets = call_if_not_none(get_pandas_object(df, features_and_labels.targets, **kwargs), 'dropna')
    sample_weights = call_if_not_none(get_pandas_object(df, features_and_labels.sample_weights, **kwargs), 'dropna')
    common_index = intersection_of_index(features, labels, targets, sample_weights)

    return (
        features.loc[common_index],
        labels.loc[common_index],
        loc_if_not_none(targets, common_index),
        loc_if_not_none(sample_weights, common_index)
    )


def extract_features(df: pd.DataFrame, features_and_labels, **kwargs) -> Tuple[List, pd.DataFrame, pd.DataFrame]:
    features = get_pandas_object(df, features_and_labels.features, **kwargs).dropna()
    targets = call_if_not_none(get_pandas_object(df, features_and_labels.targets, **kwargs), 'dropna')
    common_index = intersection_of_index(features, targets)

    # do a label calculation on a small set of data just to get the prediction columns
    label_columns = get_pandas_object(df[-2:], features_and_labels.labels, **kwargs).columns.to_list()

    return (
        label_columns,
        features.loc[common_index],
        loc_if_not_none(targets, common_index)
    )


def extract(features_and_labels, df, extractor, *args, **kwargs):
    return features_and_labels(df, extractor, *args, **kwargs)

