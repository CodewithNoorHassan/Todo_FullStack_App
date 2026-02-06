"""
Monitoring and metrics collection for the TaskMaster API.
"""
import time
import threading
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import json
import psutil
import os


@dataclass
class MetricPoint:
    """Represents a single metric measurement."""
    timestamp: datetime
    name: str
    value: float
    tags: Dict[str, str]


class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MetricsCollector:
    """
    Collects and stores application metrics.
    """
    def __init__(self, max_points: int = 10000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_points))
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def increment_counter(self, name: str, value: float = 1.0, tags: Dict[str, str] = None):
        """Increment a counter metric."""
        with self.lock:
            key = f"{name}_{json.dumps(tags or {}, sort_keys=True)}"
            self.counters[key] += value
            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                name=name,
                value=self.counters[key],
                tags=tags or {}
            )
            self.metrics[name].append(metric_point)

    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Set a gauge metric."""
        with self.lock:
            key = f"{name}_{json.dumps(tags or {}, sort_keys=True)}"
            self.gauges[key] = value
            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                name=name,
                value=value,
                tags=tags or {}
            )
            self.metrics[name].append(metric_point)

    def observe_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Observe a value for a histogram metric."""
        with self.lock:
            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                name=name,
                value=value,
                tags=tags or {}
            )
            self.metrics[name].append(metric_point)

    def get_metric_history(self, name: str, minutes: int = 60) -> List[MetricPoint]:
        """Get metric history for the last N minutes."""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        with self.lock:
            return [mp for mp in self.metrics[name] if mp.timestamp >= cutoff]

    def get_current_value(self, name: str, tags: Dict[str, str] = None) -> Optional[float]:
        """Get the current value of a counter or gauge."""
        key = f"{name}_{json.dumps(tags or {}, sort_keys=True)}"
        if key in self.counters:
            return self.counters[key]
        elif key in self.gauges:
            return self.gauges[key]
        return None

    def collect_system_metrics(self):
        """Collect system-level metrics."""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.set_gauge("system_cpu_percent", cpu_percent)

        # Memory usage
        memory = psutil.virtual_memory()
        self.set_gauge("system_memory_used_bytes", memory.used)
        self.set_gauge("system_memory_available_bytes", memory.available)
        self.set_gauge("system_memory_percent", memory.percent)

        # Process metrics
        process = psutil.Process(os.getpid())
        self.set_gauge("process_memory_rss_bytes", process.memory_info().rss)
        self.set_gauge("process_num_threads", process.num_threads())

        # Disk usage
        disk_usage = psutil.disk_usage('/')
        self.set_gauge("disk_used_bytes", disk_usage.used)
        self.set_gauge("disk_free_bytes", disk_usage.free)
        self.set_gauge("disk_percent", disk_usage.percent)


class APIMetricsMiddleware:
    """
    Middleware to collect API-specific metrics.
    """
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
        self.logger = logging.getLogger(__name__)

    def record_request(self, method: str, endpoint: str, status_code: int, response_time_ms: float):
        """Record metrics for an API request."""
        # Increment request counter
        self.collector.increment_counter(
            "api_requests_total",
            tags={"method": method, "endpoint": endpoint, "status_code": str(status_code)}
        )

        # Record response time
        self.collector.observe_histogram(
            "api_response_time_seconds",
            response_time_ms / 1000.0,  # Convert to seconds
            tags={"method": method, "endpoint": endpoint}
        )

        # Record status code
        self.collector.increment_counter(
            "api_responses_by_status_total",
            tags={"status_code": str(status_code)}
        )

    def record_error(self, endpoint: str, error_type: str):
        """Record metrics for an API error."""
        self.collector.increment_counter(
            "api_errors_total",
            tags={"endpoint": endpoint, "error_type": error_type}
        )


# Global metrics collector instance
metrics_collector = MetricsCollector()
api_middleware = APIMetricsMiddleware(metrics_collector)


def record_api_request(method: str, endpoint: str, status_code: int, response_time_ms: float):
    """Convenience function to record an API request."""
    api_middleware.record_request(method, endpoint, status_code, response_time_ms)


def record_api_error(endpoint: str, error_type: str):
    """Convenience function to record an API error."""
    api_middleware.record_error(endpoint, error_type)


def collect_periodic_metrics():
    """Function to periodically collect system metrics."""
    while True:
        try:
            metrics_collector.collect_system_metrics()
            time.sleep(30)  # Collect every 30 seconds
        except Exception as e:
            logging.error(f"Error collecting system metrics: {e}")


# Start periodic metrics collection in a background thread
metrics_thread = threading.Thread(target=collect_periodic_metrics, daemon=True)
metrics_thread.start()


def get_metrics_summary() -> Dict:
    """
    Get a summary of current metrics.

    Returns:
        Dictionary with current metric values
    """
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": metrics_collector.get_current_value("system_cpu_percent"),
            "memory_percent": metrics_collector.get_current_value("system_memory_percent"),
            "disk_percent": metrics_collector.get_current_value("disk_percent"),
        },
        "api": {
            "requests_last_minute": len(metrics_collector.get_metric_history("api_requests_total", minutes=1)),
            "average_response_time_last_minute": (
                sum(mp.value for mp in metrics_collector.get_metric_history("api_response_time_seconds", minutes=1)) /
                len(metrics_collector.get_metric_history("api_response_time_seconds", minutes=1))
                if metrics_collector.get_metric_history("api_response_time_seconds", minutes=1) else 0
            ),
        }
    }

    return summary


def export_metrics(format: str = "json") -> str:
    """
    Export metrics in the specified format.

    Args:
        format: Export format ('json', 'prometheus')

    Returns:
        Metrics in the specified format
    """
    if format == "json":
        return json.dumps(get_metrics_summary(), default=str, indent=2)
    elif format == "prometheus":
        # Simplified Prometheus format
        prometheus_lines = [
            "# HELP system_cpu_percent Current CPU usage percentage",
            f"# TYPE system_cpu_percent gauge",
            f"system_cpu_percent {metrics_collector.get_current_value('system_cpu_percent') or 0}",
            "",
            "# HELP system_memory_percent Current memory usage percentage",
            f"# TYPE system_memory_percent gauge",
            f"system_memory_percent {metrics_collector.get_current_value('system_memory_percent') or 0}",
            "",
            "# HELP api_requests_total Total API requests",
            f"# TYPE api_requests_total counter",
            f"api_requests_total {metrics_collector.get_current_value('api_requests_total') or 0}",
        ]
        return "\n".join(prometheus_lines)
    else:
        raise ValueError(f"Unsupported export format: {format}")


def setup_logging_with_metrics():
    """
    Set up logging that integrates with metrics collection.
    """
    class MetricsLogHandler(logging.Handler):
        def emit(self, record):
            # Count log levels as metrics
            level = record.levelname.lower()
            metrics_collector.increment_counter(f"log_entries_{level}_total")

    # Add the metrics handler to the root logger
    metrics_handler = MetricsLogHandler()
    logging.getLogger().addHandler(metrics_handler)