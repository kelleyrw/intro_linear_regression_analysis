from os import F_TEST
from unittest.mock import DEFAULT

import numpy as np
import pandas as pd
from scipy.stats import f as F
from scipy.stats import t

__all__ = [
    "S_xx",
    "S_xy",
    "Beta_0",
    "Beta_1",
    "y_predicted",
    "SST",
    "SSR",
    "SSE",
    "MSR",
    "MSE",
    "se_Beta1",
    "TScore",
    "TValue",
    "PValueT",
    "TTest",
    "FScore",
    "FValue",
    "PValueF",
    "FTest",
    "ANOVA",
]

DEFAULT_NDEC = 4


def S_xx(x: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = ((x - x.mean()) ** 2).sum()
    return np.round(result, decimals=ndec)


def S_xy(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = (y * (x - x.mean())).sum()
    return np.round(result, decimals=ndec)


def Beta_1(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = S_xy(x, y, ndec) / S_xx(x, ndec)
    return np.round(result, decimals=ndec)


def Beta_0(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = y.mean() - Beta_1(x, y, ndec) * x.mean()
    return np.round(result, decimals=ndec)


def y_predicted(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = Beta_0(x, y) + Beta_1(x, y, ndec) * x
    return np.round(result, decimals=ndec)


def SST(y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    result = ((y - y.mean()) ** 2).sum()
    return np.round(result, decimals=ndec)


def SSR(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    sxy = S_xy(x, y, ndec)
    beta1 = Beta_1(x, y, ndec)
    result = beta1 * sxy
    return np.round(result, decimals=ndec)


def MSR(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    return SSR(x, y, ndec)


def SSE(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    sst = SST(y, ndec)
    sxy = S_xy(x, y, ndec)
    beta1 = Beta_1(x, y, ndec)
    result = sst - beta1 * sxy
    return np.round(result, decimals=ndec)


def MSE(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    sse = SSE(x, y, ndec)
    n = x.shape[0]
    result = sse / (n - 2)
    return np.round(result, decimals=ndec)


def se_Beta1(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    mse = MSE(x, y, ndec)
    sxx = S_xx(x, ndec)
    result = np.sqrt(mse / sxx)
    return np.round(result, decimals=ndec)


def TScore(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    beta1 = Beta_1(x, y, ndec)
    se = se_Beta1(x, y, ndec)
    result = beta1 / se
    return np.round(result, decimals=ndec)


def TValue(dof, alpha, ndec: int = DEFAULT_NDEC) -> np.array:
    return np.round(t(dof).ppf(1 - alpha / 2), ndec)


def PValueT(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    t0 = np.abs(TScore(x, y, ndec))
    n = len(x)
    return 2 * (1 - t(n - 2).cdf(t0))


def TValue(dof, alpha, ndec: int = DEFAULT_NDEC) -> np.array:
    return np.round(t(dof).ppf(1 - alpha / 2), ndec)


def TTest(x: np.array, y: np.array, alpha=0.05, ndec: int = DEFAULT_NDEC) -> np.array:
    t0 = TScore(x, y, ndec)
    n = len(x)
    t_value = TValue(n - 2, alpha, ndec)
    p_value = PValueT(x, y, ndec)
    result = {
        "n": n,
        "t0": np.round(t0, ndec),
        "t_value": np.round(t_value, ndec),
        "p_value": p_value,
        "reject": np.abs(t0) > t_value,
    }
    return result


def FScore(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    mse = MSE(x, y, ndec)
    msr = MSR(x, y, ndec)
    result = msr / mse
    return np.round(result, decimals=ndec)


def FValue(dof, alpha, ndec: int = DEFAULT_NDEC) -> np.array:
    return np.round(F(1, dof).ppf(1 - alpha / 2), ndec)


def PValueF(x: np.array, y: np.array, ndec: int = DEFAULT_NDEC) -> np.array:
    f0 = np.abs(FScore(x, y, ndec))
    n = len(x)
    return 1 - F(1, n - 2).cdf(f0)


def FTest(x: np.array, y: np.array, alpha=0.05, ndec: int = DEFAULT_NDEC) -> np.array:
    f0 = FScore(x, y, ndec)
    n = len(x)
    F_value = FValue(n - 2, alpha, ndec)
    p_value = PValueF(x, y, ndec)
    result = {
        "n": n,
        "f0": np.round(f0, ndec),
        "f_value": np.round(F_value, ndec),
        "p_value": p_value,
        "reject": p_value < alpha,
    }
    return result


def ANOVA(x: np.array, y: np.array, alpha=0.05, ndec: int = DEFAULT_NDEC) -> np.array:
    # fmt: off
    columns = [
        "source",
        "sum_sq",
        "df",
        "mean_sq",
        "F_0",
        "p_value",
        "reject",
    ]
    test = FTest(x, y, alpha, ndec)
    n = test["n"]
    data = [
        (
            "regression",
            SSR(x, y, ndec),
            1,
            MSR(x, y, ndec),
            test["f0"],
            "{:.2e}".format(test["p_value"]),
            test["reject"],
        ),
        (
            "residual",
            SSE(x, y, ndec),
            n-2,
            MSE(x, y, ndec),
            None,
            None,
            None
        ),
        (
            "total",
            SST(y, ndec),
            n-1,
            None,
            None,
            None,
            None
        )
    ]
    # fmt: on
    return pd.DataFrame(data, columns=columns)
