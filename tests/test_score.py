import math

import pytest

from pipeline import score

WEIGHTS = {"stars_gained": 0.40, "times_trending": 0.35, "total_stars": 0.25}


def test_max_norm_scales_to_top_value():
    assert score.max_norm([0, 5, 10]) == [0, 0.5, 1]


def test_max_norm_all_zero_is_zero():
    assert score.max_norm([0, 0]) == [0, 0]


def test_log_norm_compresses_large_counts():
    small, big = score.log_norm([100, 50_000])
    assert big == 1
    assert small == pytest.approx(math.log1p(100) / math.log1p(50_000))
    assert small > 100 / 50_000  # far less crushed than max-normalization


def test_composite_matches_scribes_weights():
    repos = [
        {"stars_gained_30d": 100, "times_trending_30d": 10, "stars": 1000},
        {"stars_gained_30d": 50, "times_trending_30d": 0, "stars": 10},
        {"stars_gained_30d": 0, "times_trending_30d": 5, "stars": 0},
    ]
    score.trending_scores(repos, WEIGHTS, log_total_stars=False)
    assert [r["trend_score"] for r in repos] == [100.0, 20.25, 17.5]
    assert repos[1]["trend_parts"] == {"stars_gained": 0.5, "times_trending": 0.0, "total_stars": 0.01}


def test_assign_rank_is_one_based_in_order():
    repos = [{}, {}, {}]
    score.assign_rank(repos, "trend_rank")
    assert [r["trend_rank"] for r in repos] == [1, 2, 3]
