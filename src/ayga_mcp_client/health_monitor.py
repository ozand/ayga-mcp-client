"""Enhanced health monitoring with historical data and performance tracking."""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict
import asyncio


class HealthStatus:
    """Parser health status tracking."""

    STATUS_UP = "up"
    STATUS_DEGRADED = "degraded"
    STATUS_DOWN = "down"

    def __init__(self):
        self.parser_status: Dict[str, Dict[str, Any]] = {}
        self.parser_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.incidents: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def add_check_result(
        self,
        parser_id: str,
        status: str,
        response_time_ms: float,
        error: Optional[str] = None,
    ):
        """Record a health check result."""
        timestamp = datetime.now(timezone.utc)

        # Initialize parser status if not exists
        if parser_id not in self.parser_status:
            self.parser_status[parser_id] = {
                "parser_id": parser_id,
                "status": self.STATUS_UP,
                "last_check": timestamp.isoformat(),
                "uptime_24h": 100.0,
                "uptime_7d": 100.0,
                "uptime_30d": 100.0,
                "avg_response_time_ms": 0.0,
                "incident_count_24h": 0,
                "last_error": None,
                "last_error_time": None,
            }

        # Update current status
        current = self.parser_status[parser_id]
        current["last_check"] = timestamp.isoformat()
        current["status"] = status
        current["avg_response_time_ms"] = response_time_ms

        if error:
            current["last_error"] = error
            current["last_error_time"] = timestamp.isoformat()

        # Add to history
        check_record = {
            "timestamp": timestamp.isoformat(),
            "status": status,
            "response_time_ms": response_time_ms,
            "error": error,
        }
        self.parser_history[parser_id].append(check_record)

        # Track incident if down or degraded
        if status in [self.STATUS_DOWN, self.STATUS_DEGRADED]:
            incident = {
                "timestamp": timestamp.isoformat(),
                "status": status,
                "error": error or "Unknown issue",
            }
            self.incidents[parser_id].append(incident)

        # Clean old history (keep last 30 days)
        cutoff = timestamp - timedelta(days=30)
        self.parser_history[parser_id] = [
            r for r in self.parser_history[parser_id]
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]
        self.incidents[parser_id] = [
            i for i in self.incidents[parser_id]
            if datetime.fromisoformat(i["timestamp"]) > cutoff
        ]

    def calculate_uptime(self, parser_id: str, period_hours: int) -> float:
        """Calculate uptime percentage for a period."""
        if parser_id not in self.parser_history:
            return 100.0

        cutoff = datetime.now(timezone.utc) - timedelta(hours=period_hours)
        recent_checks = [
            r for r in self.parser_history[parser_id]
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]

        if not recent_checks:
            return 100.0

        up_count = sum(1 for r in recent_checks if r["status"] == self.STATUS_UP)
        return (up_count / len(recent_checks)) * 100.0

    def get_incident_count(self, parser_id: str, period_hours: int) -> int:
        """Count incidents in a period."""
        if parser_id not in self.incidents:
            return 0

        cutoff = datetime.now(timezone.utc) - timedelta(hours=period_hours)
        recent_incidents = [
            i for i in self.incidents[parser_id]
            if datetime.fromisoformat(i["timestamp"]) > cutoff
        ]

        return len(recent_incidents)

    def get_parser_status(self, parser_id: str) -> Optional[Dict[str, Any]]:
        """Get current status for a parser."""
        if parser_id not in self.parser_status:
            return None

        current = self.parser_status[parser_id].copy()

        # Calculate uptimes
        current["uptime_24h"] = round(self.calculate_uptime(parser_id, 24), 2)
        current["uptime_7d"] = round(self.calculate_uptime(parser_id, 24 * 7), 2)
        current["uptime_30d"] = round(self.calculate_uptime(parser_id, 24 * 30), 2)

        # Count incidents
        current["incident_count_24h"] = self.get_incident_count(parser_id, 24)
        current["incident_count_7d"] = self.get_incident_count(parser_id, 24 * 7)
        current["incident_count_30d"] = self.get_incident_count(parser_id, 24 * 30)

        return current

    def get_all_status(self) -> Dict[str, Any]:
        """Get status for all parsers."""
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "parsers": {},
        }

        for parser_id in self.parser_status.keys():
            result["parsers"][parser_id] = self.get_parser_status(parser_id)

        # Calculate overall stats
        if result["parsers"]:
            all_uptime_24h = [p["uptime_24h"] for p in result["parsers"].values()]
            all_uptime_7d = [p["uptime_7d"] for p in result["parsers"].values()]
            all_incidents_24h = [p["incident_count_24h"] for p in result["parsers"].values()]

            result["overall"] = {
                "total_parsers": len(result["parsers"]),
                "parsers_up": sum(1 for p in result["parsers"].values() if p["status"] == self.STATUS_UP),
                "parsers_degraded": sum(1 for p in result["parsers"].values() if p["status"] == self.STATUS_DEGRADED),
                "parsers_down": sum(1 for p in result["parsers"].values() if p["status"] == self.STATUS_DOWN),
                "avg_uptime_24h": round(sum(all_uptime_24h) / len(all_uptime_24h), 2),
                "avg_uptime_7d": round(sum(all_uptime_7d) / len(all_uptime_7d), 2),
                "total_incidents_24h": sum(all_incidents_24h),
            }
        else:
            result["overall"] = {
                "total_parsers": 0,
                "parsers_up": 0,
                "parsers_degraded": 0,
                "parsers_down": 0,
                "avg_uptime_24h": 100.0,
                "avg_uptime_7d": 100.0,
                "total_incidents_24h": 0,
            }

        return result


class HealthMonitor:
    """Enhanced health monitoring for parsers."""

    # Response time thresholds (ms)
    RESPONSE_TIME_GOOD = 5000
    RESPONSE_TIME_DEGRADED = 15000

    def __init__(self):
        self.status_tracker = HealthStatus()

    async def check_parser_health(
        self,
        parser_id: str,
        check_func,
    ) -> Dict[str, Any]:
        """Check health of a specific parser."""
        start_time = asyncio.get_event_loop().time()

        try:
            # Execute health check function
            await check_func()

            # Calculate response time
            response_time_ms = (asyncio.get_event_loop().time() - start_time) * 1000

            # Determine status based on response time
            if response_time_ms > self.RESPONSE_TIME_DEGRADED:
                status = HealthStatus.STATUS_DEGRADED
                error = f"Slow response time ({response_time_ms:.0f}ms)"
            else:
                status = HealthStatus.STATUS_UP
                error = None

            # Record result
            self.status_tracker.add_check_result(
                parser_id=parser_id,
                status=status,
                response_time_ms=response_time_ms,
                error=error,
            )

            return self.status_tracker.get_parser_status(parser_id)

        except Exception as e:
            # Parser is down
            response_time_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            error = str(e)

            self.status_tracker.add_check_result(
                parser_id=parser_id,
                status=HealthStatus.STATUS_DOWN,
                response_time_ms=response_time_ms,
                error=error,
            )

            return self.status_tracker.get_parser_status(parser_id)

    async def check_all_parsers(
        self,
        parser_ids: List[str],
        check_func_map: Dict[str, callable],
    ) -> Dict[str, Any]:
        """Check health of all parsers."""
        # Run checks in parallel
        tasks = []
        for parser_id in parser_ids:
            if parser_id in check_func_map:
                task = self.check_parser_health(parser_id, check_func_map[parser_id])
                tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        return self.status_tracker.get_all_status()

    def get_status(self) -> Dict[str, Any]:
        """Get current status without performing checks."""
        return self.status_tracker.get_all_status()

    def get_parser_status(self, parser_id: str) -> Optional[Dict[str, Any]]:
        """Get status for a specific parser without performing check."""
        return self.status_tracker.get_parser_status(parser_id)


# Performance thresholds for different parsers
PARSER_THRESHOLDS = {
    "perplexity": {
        "response_time_good": 10000,  # 10s
        "response_time_degraded": 20000,  # 20s
    },
    "chatgpt": {
        "response_time_good": 8000,
        "response_time_degraded": 15000,
    },
    "claude": {
        "response_time_good": 10000,
        "response_time_degraded": 20000,
    },
    "gemini": {
        "response_time_good": 8000,
        "response_time_degraded": 15000,
    },
    "copilot": {
        "response_time_good": 5000,
        "response_time_degraded": 10000,
    },
    "grok": {
        "response_time_good": 5000,
        "response_time_degraded": 10000,
    },
    "deepseek": {
        "response_time_good": 8000,
        "response_time_degraded": 15000,
    },
    "google_search": {
        "response_time_good": 2000,
        "response_time_degraded": 5000,
    },
    "bing_search": {
        "response_time_good": 2000,
        "response_time_degraded": 5000,
    },
    "duckduckgo": {
        "response_time_good": 2000,
        "response_time_degraded": 5000,
    },
    "youtube_search": {
        "response_time_good": 3000,
        "response_time_degraded": 7000,
    },
}


def get_parser_thresholds(parser_id: str) -> Dict[str, float]:
    """Get performance thresholds for a parser."""
    return PARSER_THRESHOLDS.get(
        parser_id,
        {
            "response_time_good": 5000,
            "response_time_degraded": 15000,
        }
    )
