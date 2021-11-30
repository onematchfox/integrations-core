import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.envoy.metrics import METRIC_PREFIX, METRICS

from .common import DEFAULT_INSTANCE, PROMETHEUS_METRICS, requires_new_environment

pytestmark = [requires_new_environment]


SKIP_TAG_ASSERTION = [
    'listener.downstream_cx_total',  # Not all of these metrics contain the address label
]


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, dd_run_check, check):
    c = check(DEFAULT_INSTANCE)
    dd_run_check(c)
    dd_run_check(c)

    for metric in PROMETHEUS_METRICS:
        aggregator.assert_metric("envoy.{}".format(metric))

        collected_metrics = aggregator.metrics(METRIC_PREFIX + metric)
        legacy_metric = METRICS.get(metric)
        if collected_metrics and legacy_metric and metric not in SKIP_TAG_ASSERTION:
            expected_tags = [t for t in legacy_metric.get('tags', []) if t]
            for tag_set in expected_tags:
                assert all(
                    all(any(tag in mt for mt in m.tags) for tag in tag_set) for m in collected_metrics if m.tags
                ), ('tags ' + str(expected_tags) + ' not found in ' + metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
