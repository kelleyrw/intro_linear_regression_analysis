from typing import Tuple

import numpy as np
import pandas as pd
import pytest

from lra.simple_linear_regression import se_Beta1

from .simple_linear_regression import *


@pytest.fixture()
def df() -> pd.DataFrame:
    """
    data from example 2.1 (Rocket Data)
    """

    columns = ["n", "strength", "age"]
    data = [
        (1, 2158.7, 15.5),
        (2, 1678.15, 23.75),
        (3, 2316.0, 8.0),
        (4, 2061.3, 17.0),
        (5, 2207.5, 5.5),
        (6, 1708.3, 19.0),
        (7, 1784.7, 24.0),
        (8, 2575.0, 2.5),
        (9, 2357.9, 7.5),
        (10, 2256.7, 11.0),
        (11, 2165.2, 13.0),
        (12, 2399.55, 3.75),
        (13, 1779.8, 25.0),
        (14, 2336.75, 9.75),
        (15, 1765.3, 22.0),
        (16, 2053.5, 18.0),
        (17, 2414.4, 6.0),
        (18, 2200.5, 12.5),
        (19, 2654.2, 2.0),
        (20, 1753.7, 21.5),
    ]
    return pd.DataFrame(columns=columns, data=data)


@pytest.fixture()
def data(df) -> Tuple[np.array, np.array]:
    x = df.age.values.reshape(-1, 1)
    y = df.strength.values.reshape(-1, 1)
    return x, y


def test_S_xx(data):
    expected = 1106.56
    x, y = data
    Sxx = S_xx(x)
    assert np.isclose(Sxx, expected)


def test_S_xy(data):
    expected = -41_112.65
    x, y = data
    Sxy = S_xy(x, y)
    assert np.isclose(Sxy, expected)


def test_Beta_0(data):
    expected = 2_627.82
    x, y = data
    b0 = Beta_0(x, y)
    assert np.isclose(b0, expected)


def test_Beta_1(data):
    expected = -37.15
    x, y = data
    b1 = Beta_1(x, y, 2)
    assert np.isclose(b1, expected)


def test_y_hat(data):
    x, y = data
    expected = 2627.82 - 37.15 * x
    yhat = y_predicted(x, y, 2)
    assert np.allclose(yhat, expected)


def test_SSE(data):
    x, y = data
    expected = 166_402.65
    obs = SSE(x, y, 2)
    assert np.allclose(obs, expected)


def test_SSR(data):
    x, y = data
    expected = 1_527_334.95
    obs = SSR(x, y, 2)
    assert np.allclose(obs, expected)


def test_SST(data):
    x, y = data
    expected = 1_693_737.60
    obs = SST(y, 2)
    assert np.allclose(obs, expected)


def test_MSE(data):
    x, y = data
    expected = 9244.59
    obs = MSE(x, y, 2)
    assert np.allclose(obs, expected)


def test_se_Beta1(data):
    x, y = data
    expected = 2.89
    obs = se_Beta1(x, y, 2)
    assert np.allclose(obs, expected)


def test_TScore(data):
    x, y = data
    expected = -12.85
    obs = TScore(x, y, 2)
    assert np.allclose(obs, expected)


def test_TValue(data):
    x, y = data
    expected = 2.101
    expected = 1.66e-10
    n = len(x)
    obs = TValue(dof=n - 2, alpha=0.05, ndec=3)
    assert np.allclose(obs, expected)


def test_PValue(data):
    x, y = data
    expected = 1.66e-10
    n = len(x)
    obs = PValueT(x, y, 10)
    print(obs * 1e10, expected * 1e10)
    print(obs, expected)
    assert np.allclose(obs, expected)


def test_ANOVA(data):
    x, y = data
    obs = ANOVA(x, y, 0.05, 2)
    print(obs)
