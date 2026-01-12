"""Enhanced error handling with detailed error context and troubleshooting."""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime


# Error codes and their definitions
ERROR_CODES = {
    "TIMEOUT": {
        "severity": "medium",
        "can_retry": True,
        "suggestions": [
            "Increase timeout from 90 to 120 seconds",
            "Try simpler query",
            "Check if parser service is experiencing delays"
        ]
    },
    "AUTH_FAILED": {
        "severity": "critical",
        "can_retry": False,
        "suggestions": [
            "Verify your API key is valid",
            "Check if API key has expired",
            "Ensure REDIS_API_KEY environment variable is set"
        ]
    },
    "RATE_LIMIT": {
        "severity": "medium",
        "can_retry": True,
        "suggestions": [
            "Wait for rate limit to reset",
            "Reduce query frequency",
            "Consider upgrading to Pro tier for higher limits"
        ]
    },
    "PARSER_NOT_FOUND": {
        "severity": "medium",
        "can_retry": False,
        "suggestions": [
            "Check parser ID spelling",
            "Use list_parsers to see available parsers",
            "Verify parser is supported"
        ]
    },
    "INVALID_QUERY": {
        "severity": "low",
        "can_retry": True,
        "suggestions": [
            "Ensure query is not empty",
            "Check query encoding (UTF-8)",
            "Try shorter query"
        ]
    },
    "CONNECTION_ERROR": {
        "severity": "high",
        "can_retry": True,
        "suggestions": [
            "Check internet connection",
            "Verify API endpoint is accessible",
            "Try again in a few moments"
        ]
    },
    "PARSER_ERROR": {
        "severity": "high",
        "can_retry": False,
        "suggestions": [
            "Parser execution failed on backend",
            "Query may be incompatible with parser",
            "Try different parser"
        ]
    },
    "SERVICE_UNAVAILABLE": {
        "severity": "high",
        "can_retry": True,
        "suggestions": [
            "Parser service is temporarily down",
            "Check status page for updates",
            "Try alternative parser"
        ]
    }
}


# Parser-specific error context
PARSER_CONTEXT = {
    "perplexity": {
        "name": "Perplexity AI",
        "docs_url": "https://www.perplexity.ai/",
        "common_issues": {
            "timeout": "Deep Research queries can take 60-120 seconds",
            "rate_limit": "Free tier: 5 queries/day, Pro: 600 queries/day"
        }
    },
    "chatgpt": {
        "name": "ChatGPT",
        "docs_url": "https://platform.openai.com/",
        "common_issues": {
            "timeout": "Complex queries may take 30-60 seconds",
            "rate_limit": "Rate limits depend on your API tier"
        }
    },
    "claude": {
        "name": "Claude AI",
        "docs_url": "https://docs.anthropic.com/",
        "common_issues": {
            "timeout": "Long context queries may take 45-90 seconds",
            "rate_limit": "Rate limits depend on your API tier"
        }
    },
    "gemini": {
        "name": "Google Gemini",
        "docs_url": "https://ai.google.dev/",
        "common_issues": {
            "timeout": "Multimodal queries may take longer",
            "rate_limit": "15 queries/minute for free tier"
        }
    },
    "copilot": {
        "name": "Microsoft Copilot",
        "docs_url": "https://learn.microsoft.com/en-us/bing/copilot/",
        "common_issues": {
            "timeout": "Web search queries: 15-30 seconds",
            "rate_limit": "Standard Microsoft rate limits apply"
        }
    },
    "grok": {
        "name": "Grok AI",
        "docs_url": "https://x.ai/",
        "common_issues": {
            "timeout": "Real-time data queries: 20-40 seconds",
            "rate_limit": "Premium subscribers have higher limits"
        }
    },
    "deepseek": {
        "name": "DeepSeek",
        "docs_url": "https://www.deepseek.com/",
        "common_issues": {
            "timeout": "Technical queries: 30-60 seconds",
            "rate_limit": "Check current rate limits"
        }
    },
    "google_search": {
        "name": "Google Search",
        "docs_url": "https://developers.google.com/custom-search/",
        "common_issues": {
            "timeout": "Search queries: 5-15 seconds",
            "rate_limit": "100 queries/day for free tier"
        }
    },
    "bing_search": {
        "name": "Bing Search",
        "docs_url": "https://www.microsoft.com/en-us/bing/apis/",
        "common_issues": {
            "timeout": "Search queries: 5-15 seconds",
            "rate_limit": "1000 queries/month for free tier"
        }
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "docs_url": "https://duckduckgo.com/",
        "common_issues": {
            "timeout": "Search queries: 5-10 seconds",
            "rate_limit": "No strict rate limit"
        }
    },
    "youtube_search": {
        "name": "YouTube Search",
        "docs_url": "https://developers.google.com/youtube/",
        "common_issues": {
            "timeout": "Video metadata: 5-15 seconds",
            "rate_limit": "100 units/day for free tier"
        }
    }
}


class ErrorHandler:
    """Enhanced error handling with detailed context."""

    @staticmethod
    def detect_error_code(error_message: str, parser_id: str) -> str:
        """Detect error code from error message and context."""
        error_lower = error_message.lower()

        # Timeout errors
        if "timeout" in error_lower or "timed out" in error_lower:
            return "TIMEOUT"

        # Authentication errors
        if "auth" in error_lower or "unauthorized" in error_lower or "401" in error_lower:
            return "AUTH_FAILED"

        # Rate limit errors
        if "rate limit" in error_lower or "429" in error_lower or "too many requests" in error_lower:
            return "RATE_LIMIT"

        # Parser not found
        if "not found" in error_lower and "parser" in error_lower:
            return "PARSER_NOT_FOUND"

        # Invalid query
        if "empty query" in error_lower or "invalid query" in error_lower:
            return "INVALID_QUERY"

        # Connection errors
        if "connection" in error_lower or "network" in error_lower:
            return "CONNECTION_ERROR"

        # Service unavailable
        if "unavailable" in error_lower or "503" in error_lower or "502" in error_lower:
            return "SERVICE_UNAVAILABLE"

        # Default parser error
        return "PARSER_ERROR"

    @staticmethod
    def get_parser_context(parser_id: str) -> Optional[Dict[str, Any]]:
        """Get parser-specific context."""
        return PARSER_CONTEXT.get(parser_id)

    @staticmethod
    def create_enhanced_error(
        error_message: str,
        parser_id: Optional[str] = None,
        task_id: Optional[str] = None,
        original_error: Optional[Exception] = None
    ) -> Dict[str, Any]:
        """Create enhanced error response with detailed context."""

        # Detect error code
        error_code = ErrorHandler.detect_error_code(error_message, parser_id or "")
        error_info = ERROR_CODES.get(error_code, ERROR_CODES["PARSER_ERROR"])

        # Build enhanced error response
        enhanced_error = {
            "error": error_message,
            "error_code": error_code,
            "severity": error_info["severity"],
            "can_retry": error_info["can_retry"],
            "suggestions": error_info["suggestions"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Add parser-specific context if available
        if parser_id:
            parser_context = ErrorHandler.get_parser_context(parser_id)
            if parser_context:
                enhanced_error["parser"] = {
                    "id": parser_id,
                    "name": parser_context["name"],
                    "docs_url": parser_context["docs_url"]
                }

                # Add parser-specific tips based on error code
                if error_code in parser_context.get("common_issues", {}):
                    enhanced_error["parser_tip"] = parser_context["common_issues"][error_code]

        # Add task ID if available
        if task_id:
            enhanced_error["task_id"] = task_id

        # Add documentation link
        enhanced_error["docs"] = "https://redis.ayga.tech/docs/errors/" + error_code.lower()

        # Add retry information if applicable
        if error_code == "RATE_LIMIT":
            enhanced_error["retry_after_seconds"] = 60  # Default retry after
        elif error_code == "TIMEOUT":
            enhanced_error["retry_after_seconds"] = 0  # Can retry immediately with longer timeout

        return enhanced_error

    @staticmethod
    def format_error(error_dict: Dict[str, Any]) -> str:
        """Format enhanced error as readable text."""
        lines = []
        lines.append(f"❌ Error: {error_dict['error']}")
        lines.append(f"   Code: {error_dict['error_code']}")
        lines.append(f"   Severity: {error_dict['severity']}")

        if error_dict.get("parser"):
            parser = error_dict["parser"]
            lines.append(f"   Parser: {parser['name']} ({parser['id']})")

        lines.append(f"   Can Retry: {'Yes' if error_dict['can_retry'] else 'No'}")
        lines.append("")
        lines.append("💡 Suggestions:")
        for i, suggestion in enumerate(error_dict["suggestions"], 1):
            lines.append(f"   {i}. {suggestion}")

        if error_dict.get("parser_tip"):
            lines.append("")
            lines.append(f"📌 Tip: {error_dict['parser_tip']}")

        lines.append("")
        lines.append(f"📚 Docs: {error_dict['docs']}")

        return "\n".join(lines)


# Convenience functions for common errors

def create_timeout_error(
    query: str,
    parser_id: str,
    timeout_used: int,
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create timeout error with specific context."""
    return ErrorHandler.create_enhanced_error(
        f"Query timed out after {timeout_used} seconds",
        parser_id=parser_id,
        task_id=task_id
    )

def create_rate_limit_error(
    parser_id: str,
    current_usage: int,
    limit: int,
    retry_after: int = 60,
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create rate limit error with specific context."""
    error = ErrorHandler.create_enhanced_error(
        f"Rate limit exceeded: {current_usage}/{limit} requests",
        parser_id=parser_id,
        task_id=task_id
    )
    error["retry_after_seconds"] = retry_after
    error["current_usage"] = current_usage
    error["limit"] = limit
    return error

def create_auth_error(
    details: str = "Invalid or missing API key",
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create authentication error."""
    return ErrorHandler.create_enhanced_error(
        f"Authentication failed: {details}",
        parser_id=None,
        task_id=task_id
    )

def create_parser_not_found_error(
    parser_id: str,
    available_parsers: List[str]
) -> Dict[str, Any]:
    """Create parser not found error with suggestions."""
    error = ErrorHandler.create_enhanced_error(
        f"Parser '{parser_id}' not found",
        parser_id=parser_id
    )
    error["available_parsers"] = available_parsers

    # Suggest similar parser IDs
    if available_parsers:
        import difflib
        matches = difflib.get_close_matches(parser_id, available_parsers, n=3)
        if matches:
            error["did_you_mean"] = matches

    return error
