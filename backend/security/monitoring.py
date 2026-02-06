"""
Security monitoring and alerting for the TaskMaster API.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SecurityEventType(Enum):
    """Types of security events that can be monitored."""
    LOGIN_ATTEMPT = "login_attempt"
    FAILED_AUTHENTICATION = "failed_authentication"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_ACCESS_VIOLATION = "data_access_violation"
    ANOMALOUS_BEHAVIOR = "anomalous_behavior"


class SecurityMonitor:
    """
    Security monitoring system for tracking and alerting on security events.
    """
    def __init__(self, logger_name: str = "security_monitor"):
        self.logger = logging.getLogger(logger_name)
        self.alert_thresholds = {
            SecurityEventType.FAILED_AUTHENTICATION: 5,  # per minute
            SecurityEventType.UNAUTHORIZED_ACCESS: 10,   # per minute
            SecurityEventType.RATE_LIMIT_EXCEEDED: 20,   # per minute
        }
        self.event_counts = {}
        self.alert_callbacks = []

    def log_event(self, event_type: SecurityEventType, details: Dict, ip_address: Optional[str] = None):
        """
        Log a security event.

        Args:
            event_type: Type of security event
            details: Details about the event
            ip_address: IP address associated with the event
        """
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "details": details,
            "ip_address": ip_address,
        }

        # Log the event
        self.logger.warning(f"SECURITY EVENT: {json.dumps(event_data)}")

        # Track event counts for threshold checking
        key = f"{event_type.value}:{ip_address or 'unknown'}"
        current_time = datetime.utcnow()

        if key not in self.event_counts:
            self.event_counts[key] = []

        # Remove events older than 1 minute
        self.event_counts[key] = [
            timestamp for timestamp in self.event_counts[key]
            if current_time - timestamp < timedelta(minutes=1)
        ]

        # Add current event
        self.event_counts[key].append(current_time)

        # Check if threshold is exceeded
        threshold = self.alert_thresholds.get(event_type)
        if threshold and len(self.event_counts[key]) >= threshold:
            self.trigger_alert(event_type, details, ip_address)

    def trigger_alert(self, event_type: SecurityEventType, details: Dict, ip_address: Optional[str]):
        """
        Trigger an alert for a security event that exceeded thresholds.

        Args:
            event_type: Type of security event
            details: Details about the event
            ip_address: IP address associated with the event
        """
        alert_message = f"""
SECURITY ALERT
============
Time: {datetime.utcnow().isoformat()}
Event: {event_type.value}
IP Address: {ip_address}
Details: {json.dumps(details, indent=2)}

Threshold exceeded: {len(self.event_counts.get(f'{event_type.value}:{ip_address or 'unknown'}', []))}
events in the last minute.
"""

        self.logger.critical(alert_message)

        # Call registered alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(event_type, details, ip_address)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")

    def add_alert_callback(self, callback):
        """
        Add a callback function to be called when alerts are triggered.

        Args:
            callback: Function to call when an alert is triggered
        """
        self.alert_callbacks.append(callback)

    def get_security_report(self) -> Dict:
        """
        Get a summary report of security events.

        Returns:
            Dictionary with security event statistics
        """
        total_events = sum(len(counts) for counts in self.event_counts.values())

        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_security_events": total_events,
            "events_by_type": {},
            "recent_events": [],  # Would be populated with recent events
        }

        # Count events by type
        for key, counts in self.event_counts.items():
            event_type, ip = key.split(':', 1)
            if event_type not in report["events_by_type"]:
                report["events_by_type"][event_type] = 0
            report["events_by_type"][event_type] += len(counts)

        return report


# Global security monitor instance
security_monitor = SecurityMonitor()


def log_failed_auth(ip_address: str, username: Optional[str] = None, reason: str = "unknown"):
    """
    Convenience function to log failed authentication attempts.

    Args:
        ip_address: IP address of the request
        username: Username that failed authentication
        reason: Reason for authentication failure
    """
    details = {
        "username": username,
        "reason": reason,
        "source": "authentication_system"
    }
    security_monitor.log_event(
        SecurityEventType.FAILED_AUTHENTICATION,
        details,
        ip_address
    )


def log_unauthorized_access(ip_address: str, endpoint: str, user_id: Optional[int] = None):
    """
    Convenience function to log unauthorized access attempts.

    Args:
        ip_address: IP address of the request
        endpoint: Endpoint that was accessed
        user_id: User ID if known, None if not authenticated
    """
    details = {
        "endpoint": endpoint,
        "user_id": user_id,
        "source": "access_control"
    }
    security_monitor.log_event(
        SecurityEventType.UNAUTHORIZED_ACCESS,
        details,
        ip_address
    )


def log_rate_limit_exceeded(ip_address: str, identifier: str, limit: int, window: int):
    """
    Convenience function to log rate limit exceeded events.

    Args:
        ip_address: IP address of the request
        identifier: Rate limit identifier
        limit: Rate limit that was exceeded
        window: Time window in seconds
    """
    details = {
        "identifier": identifier,
        "limit": limit,
        "window_seconds": window,
        "source": "rate_limiter"
    }
    security_monitor.log_event(
        SecurityEventType.RATE_LIMIT_EXCEEDED,
        details,
        ip_address
    )


def get_security_health_status() -> Dict:
    """
    Get the current security health status of the system.

    Returns:
        Dictionary with security health information
    """
    report = security_monitor.get_security_report()

    # Determine health status based on event counts
    high_risk_events = 0
    for event_type, count in report["events_by_type"].items():
        if event_type in [e.value for e in [SecurityEventType.FAILED_AUTHENTICATION,
                                          SecurityEventType.UNAUTHORIZED_ACCESS,
                                          SecurityEventType.RATE_LIMIT_EXCEEDED]]:
            high_risk_events += count

    if high_risk_events > 50:
        status = "CRITICAL"
    elif high_risk_events > 20:
        status = "WARNING"
    elif high_risk_events > 0:
        status = "MONITORING"
    else:
        status = "HEALTHY"

    report["health_status"] = status
    report["high_risk_event_count"] = high_risk_events

    return report


# Email alert callback example
def email_alert_callback(event_type: SecurityEventType, details: Dict, ip_address: Optional[str]):
    """
    Example callback to send email alerts for security events.
    """
    # This would be configured with actual email settings in production
    pass


# Register the email callback
security_monitor.add_alert_callback(email_alert_callback)