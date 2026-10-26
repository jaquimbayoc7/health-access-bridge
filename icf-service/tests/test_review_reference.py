"""Contraste de las funciones estadisticas propias de la validacion clinica (HU-07g) con librerias de referencia.

Se omiten solas si no estan scikit-learn o statsmodels (no son dependencias del servicio).
"""
import math

import pytest

from icf.review import cohen_kappa_binary, weighted_kappa, wilson_interval
from icf.stability import fleiss_kappa_binary

proportion = pytest.importorskip("statsmodels.stats.proportion")
inter_rater = pytest.importorskip("statsmodels.stats.inter_rater")
metrics = pytest.importorskip("sklearn.metrics")
np = pytest.importorskip("numpy")

Z_ONE_SIDED = 1.959964  # alfa unilateral de 2,5 %


@pytest.mark.parametrize("n", [5, 24, 60, 120])
def test_wilson_matches_statsmodels(n):
    for k in range(n + 1):
        low, high = proportion.proportion_confint(k, n, alpha=0.05, method="wilson")
        mine = wilson_interval(k, n)
        assert mine[0] == pytest.approx(low, abs=6e-4) and mine[1] == pytest.approx(high, abs=6e-4)


@pytest.mark.parametrize("p0", [0.4, 0.6, 0.8])
@pytest.mark.parametrize("n", [10, 30, 60, 120])
def test_wilson_lower_limit_is_the_one_sided_score_test(n, p0):
    """'Limite inferior de Wilson >= p0' equivale a rechazar H0: p <= p0 con la prueba de puntuacion (alfa unilateral 2,5 %)."""
    for k in range(n + 1):
        lower = proportion.proportion_confint(k, n, alpha=0.05, method="wilson")[0]
        z = (k / n - p0) / math.sqrt(p0 * (1 - p0) / n)
        assert (lower >= p0) == (z >= Z_ONE_SIDED), (k, n, p0)


def test_cohen_kappa_binary_matches_sklearn():
    rng = np.random.default_rng(7)
    for n in (12, 40, 150):
        a, b = rng.integers(0, 2, n), rng.integers(0, 2, n)
        expected = metrics.cohen_kappa_score(a, b)
        assert cohen_kappa_binary(list(zip(a.astype(bool), b.astype(bool)))) == pytest.approx(expected, abs=1e-3)


def test_weighted_kappa_linear_matches_sklearn():
    rng = np.random.default_rng(11)
    for n in (15, 60, 200):
        a = rng.integers(0, 5, n)
        b = np.clip(a + rng.integers(-2, 3, n), 0, 4)
        expected = metrics.cohen_kappa_score(a, b, weights="linear", labels=list(range(5)))
        assert weighted_kappa(list(zip(a.tolist(), b.tolist()))) == pytest.approx(expected, abs=1e-3)


def test_fleiss_kappa_binary_matches_statsmodels():
    rng = np.random.default_rng(3)
    for raters in (3, 5):
        yes = rng.integers(0, raters + 1, 40)
        table = np.column_stack([raters - yes, yes])
        expected = inter_rater.fleiss_kappa(table, method="fleiss")
        assert fleiss_kappa_binary(yes.tolist(), raters) == pytest.approx(expected, abs=1e-3)
