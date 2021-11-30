# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest
from envoy.tests.legacy.common import FLAVOR, HOST, requires_legacy_environment

from datadog_checks.envoy import Envoy

pytestmark = [requires_legacy_environment]

METRICS = [
    'envoy.cluster.assignment_stale',
    'envoy.cluster.assignment_timeout_received',
    'envoy.cluster.bind_errors',
    'envoy.cluster.circuit_breakers.cx_open',
    'envoy.cluster.circuit_breakers.cx_pool_open',
    'envoy.cluster.circuit_breakers.rq_open',
    'envoy.cluster.circuit_breakers.rq_pending_open',
    'envoy.cluster.circuit_breakers.rq_retry_open',
    'envoy.cluster.http2.header_overflow',
    'envoy.cluster.http2.headers_cb_no_stream',
    'envoy.cluster.http2.inbound_empty_frames_flood',
    'envoy.cluster.http2.inbound_priority_frames_flood',
    'envoy.cluster.http2.inbound_window_update_frames_flood',
    'envoy.cluster.http2.outbound_control_flood',
    'envoy.cluster.http2.outbound_flood',
    'envoy.cluster.http2.rx_messaging_error',
    'envoy.cluster.http2.rx_reset',
    'envoy.cluster.http2.trailers',
    'envoy.cluster.http2.tx_reset',
    'envoy.cluster.internal.upstream_rq_2xx',
    'envoy.cluster.internal.upstream_rq_completed',
    'envoy.cluster.lb_healthy_panic',
    'envoy.cluster.lb_local_cluster_not_ok',
    'envoy.cluster.lb_recalculate_zone_structures',
    'envoy.cluster.lb_subsets_active',
    'envoy.cluster.lb_subsets_created',
    'envoy.cluster.lb_subsets_fallback',
    'envoy.cluster.lb_subsets_fallback_panic',
    'envoy.cluster.lb_subsets_removed',
    'envoy.cluster.lb_subsets_selected',
    'envoy.cluster.lb_zone_cluster_too_small',
    'envoy.cluster.lb_zone_no_capacity_left',
    'envoy.cluster.lb_zone_number_differs',
    'envoy.cluster.lb_zone_routing_all_directly',
    'envoy.cluster.lb_zone_routing_cross_zone',
    'envoy.cluster.lb_zone_routing_sampled',
    'envoy.cluster.max_host_weight',
    'envoy.cluster.membership_change',
    'envoy.cluster.membership_degraded',
    'envoy.cluster.membership_excluded',
    'envoy.cluster.membership_healthy',
    'envoy.cluster.membership_total',
    'envoy.cluster.original_dst_host_invalid',
    'envoy.cluster.retry_or_shadow_abandoned',
    'envoy.cluster.update_attempt',
    'envoy.cluster.update_empty',
    'envoy.cluster.update_failure',
    'envoy.cluster.update_no_rebuild',
    'envoy.cluster.update_success',
    'envoy.cluster.upstream_cx_active',
    'envoy.cluster.upstream_cx_close_notify',
    'envoy.cluster.upstream_cx_connect_attempts_exceeded',
    'envoy.cluster.upstream_cx_connect_fail',
    'envoy.cluster.upstream_cx_connect_timeout',
    'envoy.cluster.upstream_cx_destroy',
    'envoy.cluster.upstream_cx_destroy_local',
    'envoy.cluster.upstream_cx_destroy_local_with_active_rq',
    'envoy.cluster.upstream_cx_destroy_remote',
    'envoy.cluster.upstream_cx_destroy_remote_with_active_rq',
    'envoy.cluster.upstream_cx_destroy_with_active_rq',
    'envoy.cluster.upstream_cx_http1_total',
    'envoy.cluster.upstream_cx_http2_total',
    'envoy.cluster.upstream_cx_idle_timeout',
    'envoy.cluster.upstream_cx_max_requests',
    'envoy.cluster.upstream_cx_none_healthy',
    'envoy.cluster.upstream_cx_overflow',
    'envoy.cluster.upstream_cx_pool_overflow',
    'envoy.cluster.upstream_cx_protocol_error',
    'envoy.cluster.upstream_cx_rx_bytes_buffered',
    'envoy.cluster.upstream_cx_rx_bytes_total',
    'envoy.cluster.upstream_cx_total',
    'envoy.cluster.upstream_cx_tx_bytes_buffered',
    'envoy.cluster.upstream_cx_tx_bytes_total',
    'envoy.cluster.upstream_flow_control_backed_up_total',
    'envoy.cluster.upstream_flow_control_drained_total',
    'envoy.cluster.upstream_flow_control_paused_reading_total',
    'envoy.cluster.upstream_flow_control_resumed_reading_total',
    'envoy.cluster.upstream_internal_redirect_failed_total',
    'envoy.cluster.upstream_internal_redirect_succeeded_total',
    'envoy.cluster.upstream_rq_2xx',
    'envoy.cluster.upstream_rq_active',
    'envoy.cluster.upstream_rq_cancelled',
    'envoy.cluster.upstream_rq_completed',
    'envoy.cluster.upstream_rq_maintenance_mode',
    'envoy.cluster.upstream_rq_pending_active',
    'envoy.cluster.upstream_rq_pending_failure_eject',
    'envoy.cluster.upstream_rq_pending_overflow',
    'envoy.cluster.upstream_rq_pending_total',
    'envoy.cluster.upstream_rq_per_try_timeout',
    'envoy.cluster.upstream_rq_retry',
    'envoy.cluster.upstream_rq_retry_overflow',
    'envoy.cluster.upstream_rq_retry_success',
    'envoy.cluster.upstream_rq_rx_reset',
    'envoy.cluster.upstream_rq_timeout',
    'envoy.cluster.upstream_rq_total',
    'envoy.cluster.upstream_rq_tx_reset',
    'envoy.cluster.version',
    'envoy.cluster_manager.active_clusters',
    'envoy.cluster_manager.cluster_added',
    'envoy.cluster_manager.cluster_modified',
    'envoy.cluster_manager.cluster_removed',
    'envoy.cluster_manager.warming_clusters',
    'envoy.cluster_manager.cds.update_attempt',
    'envoy.cluster_manager.cds.update_success',
    'envoy.cluster_manager.cds.update_failure',
    'envoy.cluster_manager.cds.update_rejected',
    'envoy.cluster_manager.cds.version',
    'envoy.cluster_manager.cds.control_plane.connected_state',
    'envoy.cluster_manager.cds.control_plane.pending_requests',
    'envoy.cluster_manager.cds.control_plane.rate_limit_enforced',
    'envoy.cluster_manager.cds.update_time',
    'envoy.filesystem.flushed_by_timer',
    'envoy.filesystem.reopen_failed',
    'envoy.filesystem.write_buffered',
    'envoy.filesystem.write_completed',
    'envoy.filesystem.write_total_buffered',
    'envoy.http.downstream_cx_active',
    'envoy.http.downstream_cx_destroy',
    'envoy.http.downstream_cx_destroy_active_rq',
    'envoy.http.downstream_cx_destroy_local',
    'envoy.http.downstream_cx_destroy_local_active_rq',
    'envoy.http.downstream_cx_destroy_remote',
    'envoy.http.downstream_cx_destroy_remote_active_rq',
    'envoy.http.downstream_cx_drain_close',
    'envoy.http.downstream_cx_http1_active',
    'envoy.http.downstream_cx_http1_total',
    'envoy.http.downstream_cx_http2_active',
    'envoy.http.downstream_cx_http2_total',
    'envoy.http.downstream_cx_http3_active',
    'envoy.http.downstream_cx_http3_total',
    'envoy.http.downstream_cx_idle_timeout',
    'envoy.http.downstream_cx_protocol_error',
    'envoy.http.downstream_cx_rx_bytes_buffered',
    'envoy.http.downstream_cx_rx_bytes_total',
    'envoy.http.downstream_cx_ssl_active',
    'envoy.http.downstream_cx_ssl_total',
    'envoy.http.downstream_cx_total',
    'envoy.http.downstream_cx_tx_bytes_buffered',
    'envoy.http.downstream_cx_tx_bytes_total',
    'envoy.http.downstream_flow_control_paused_reading_total',
    'envoy.http.downstream_flow_control_resumed_reading_total',
    'envoy.http.downstream_rq_1xx',
    'envoy.http.downstream_rq_2xx',
    'envoy.http.downstream_rq_3xx',
    'envoy.http.downstream_rq_4xx',
    'envoy.http.downstream_rq_5xx',
    'envoy.http.downstream_rq_active',
    'envoy.http.downstream_rq_http1_total',
    'envoy.http.downstream_rq_http2_total',
    'envoy.http.downstream_rq_http3_total',
    'envoy.http.downstream_rq_non_relative_path',
    'envoy.http.downstream_rq_response_before_rq_complete',
    'envoy.http.downstream_rq_rx_reset',
    'envoy.http.downstream_rq_too_large',
    'envoy.http.downstream_rq_total',
    'envoy.http.downstream_rq_tx_reset',
    'envoy.http.downstream_rq_ws_on_non_ws_route',
    'envoy.http.no_cluster',
    'envoy.http.no_route',
    'envoy.http.rq_direct_response',
    'envoy.http.rq_redirect',
    'envoy.http.rq_total',
    'envoy.http.rs_too_large',
    'envoy.http.tracing.client_enabled',
    'envoy.http.tracing.health_check',
    'envoy.http.tracing.not_traceable',
    'envoy.http.tracing.random_sampling',
    'envoy.http.tracing.service_forced',
    'envoy.listener.downstream_cx_active',
    'envoy.listener.downstream_cx_destroy',
    'envoy.listener.downstream_cx_total',
    'envoy.listener.downstream_pre_cx_active',
    'envoy.listener.downstream_pre_cx_timeout',
    'envoy.listener.http.downstream_rq_1xx',
    'envoy.listener.http.downstream_rq_2xx',
    'envoy.listener.http.downstream_rq_3xx',
    'envoy.listener.http.downstream_rq_4xx',
    'envoy.listener.http.downstream_rq_5xx',
    'envoy.listener.http.downstream_rq_completed',
    'envoy.listener_manager.listener_added',
    'envoy.listener_manager.listener_create_failure',
    'envoy.listener_manager.listener_create_success',
    'envoy.listener_manager.listener_modified',
    'envoy.listener_manager.listener_removed',
    'envoy.listener_manager.total_listeners_active',
    'envoy.listener_manager.total_listeners_draining',
    'envoy.listener_manager.total_listeners_warming',
    'envoy.listener_manager.lds.update_attempt',
    'envoy.listener_manager.lds.update_success',
    'envoy.listener_manager.lds.update_failure',
    'envoy.listener_manager.lds.update_rejected',
    'envoy.listener_manager.lds.update_time',
    'envoy.listener_manager.lds.version',
    'envoy.listener_manager.lds.control_plane.connected_state',
    'envoy.listener_manager.lds.control_plane.pending_requests',
    'envoy.listener_manager.lds.control_plane.rate_limit_enforced',
    'envoy.listener.no_filter_chain_match',
    'envoy.runtime.admin_overrides_active',
    'envoy.runtime.deprecated_feature_use',
    'envoy.runtime.load_error',
    'envoy.runtime.load_success',
    'envoy.runtime.num_keys',
    'envoy.runtime.num_layers',
    'envoy.runtime.override_dir_exists',
    'envoy.runtime.override_dir_not_exists',
    'envoy.server.concurrency',
    'envoy.server.days_until_first_cert_expiring',
    'envoy.server.debug_assertion_failures',
    'envoy.server.hot_restart_epoch',
    'envoy.server.live',
    'envoy.server.memory_allocated',
    'envoy.server.memory_heap_size',
    'envoy.server.parent_connections',
    'envoy.server.state',
    'envoy.server.total_connections',
    'envoy.server.uptime',
    'envoy.server.version',
    'envoy.server.watchdog_mega_miss',
    'envoy.server.watchdog_miss',
    'envoy.vhost.vcluster.upstream_rq_retry',
    'envoy.vhost.vcluster.upstream_rq_retry_limit_exceeded',
    'envoy.vhost.vcluster.upstream_rq_retry_overflow',
    'envoy.vhost.vcluster.upstream_rq_retry_success',
    'envoy.vhost.vcluster.upstream_rq_timeout',
    'envoy.vhost.vcluster.upstream_rq_total',
]

# Metrics only available in our API v2 environment
METRICS_V2 = [
    'envoy.cluster.http2.too_many_header_frames',
]

# Metrics only available in our API v3 environment
METRICS_V3 = [
    'envoy.cluster.upstream_cx_http3_total',
    'envoy.cluster.upstream_rq_max_duration_reached',
    'envoy.http.downstream_cx_length_ms.0percentile',
    'envoy.http.downstream_cx_length_ms.100percentile',
    'envoy.http.downstream_cx_length_ms.25percentile',
    'envoy.http.downstream_cx_length_ms.50percentile',
    'envoy.http.downstream_cx_length_ms.75percentile',
    'envoy.http.downstream_cx_length_ms.90percentile',
    'envoy.http.downstream_cx_length_ms.95percentile',
    'envoy.http.downstream_cx_length_ms.99_5percentile',
    'envoy.http.downstream_cx_length_ms.99_9percentile',
    'envoy.http.downstream_cx_length_ms.99percentile',
    'envoy.http.downstream_rq_time.0percentile',
    'envoy.http.downstream_rq_time.100percentile',
    'envoy.http.downstream_rq_time.25percentile',
    'envoy.http.downstream_rq_time.50percentile',
    'envoy.http.downstream_rq_time.75percentile',
    'envoy.http.downstream_rq_time.90percentile',
    'envoy.http.downstream_rq_time.95percentile',
    'envoy.http.downstream_rq_time.99_5percentile',
    'envoy.http.downstream_rq_time.99_9percentile',
    'envoy.http.downstream_rq_time.99percentile',
    'envoy.listener.downstream_cx_length_ms.0percentile',
    'envoy.listener.downstream_cx_length_ms.100percentile',
    'envoy.listener.downstream_cx_length_ms.25percentile',
    'envoy.listener.downstream_cx_length_ms.50percentile',
    'envoy.listener.downstream_cx_length_ms.75percentile',
    'envoy.listener.downstream_cx_length_ms.90percentile',
    'envoy.listener.downstream_cx_length_ms.95percentile',
    'envoy.listener.downstream_cx_length_ms.99_5percentile',
    'envoy.listener.downstream_cx_length_ms.99_9percentile',
    'envoy.listener.downstream_cx_length_ms.99percentile',
]


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {"stats_url": "http://{}:8001/stats".format(HOST)}
    aggregator = dd_agent_check(instance, rate=True)
    for metric in METRICS:
        aggregator.assert_metric(metric)

    if FLAVOR == 'api_v2':
        for metric in METRICS_V2:
            aggregator.assert_metric(metric)
    else:
        for metric in METRICS_V3:
            aggregator.assert_metric(metric, at_least=0)
    # We can't assert all covered, as some aren't received every time
    aggregator.assert_service_check('envoy.can_connect', Envoy.OK)
