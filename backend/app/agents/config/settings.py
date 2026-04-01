"""Agent configuration settings"""

from typing import Dict, Any

# Agent execution settings
AGENT_SETTINGS = {
    # Timeout settings (seconds)
    "timeouts": {
        "compliance_agent": 600,  # 10 minutes for full workflow
        "ba_supervisor": 300,     # 5 minutes
        "dev_supervisor": 300,    # 5 minutes
        "qa_supervisor": 300,     # 5 minutes
        "interpreter_agent": 180, # 3 minutes
        "architect_agent": 180,   # 3 minutes
        "auditor_agent": 180,     # 3 minutes
    },

    # Retry settings
    "retries": {
        "max_retries": 3,
        "retry_delay": 5,  # seconds
        "exponential_backoff": True,
    },

    # LLM settings
    "llm": {
        "model": "gpt-4-turbo",
        "temperature": 0.1,  # Low for consistency
        "max_tokens": 4000,
        "top_p": 0.95,
    },

    # Agent behavior
    "behavior": {
        "auto_approve_threshold": 0.95,  # Confidence threshold for auto-approval
        "require_human_review": False,    # Set True to require human approval
        "parallel_execution": True,       # Execute independent tasks in parallel
        "save_intermediate_results": True,
    },

    # Logging
    "logging": {
        "log_level": "INFO",
        "log_agent_inputs": True,
        "log_agent_outputs": True,
        "log_execution_time": True,
    },
}

# Agent capability matrix
AGENT_CAPABILITIES = {
    "compliance_agent": {
        "can_delegate": True,
        "can_approve": True,
        "can_reject": True,
        "requires_supervisor": False,
        "max_parallel_tasks": 3,
    },
    "ba_supervisor": {
        "can_delegate": True,
        "can_approve": True,
        "can_reject": True,
        "requires_supervisor": True,
        "supervisor": "compliance_agent",
        "max_parallel_tasks": 1,
    },
    "dev_supervisor": {
        "can_delegate": True,
        "can_approve": True,
        "can_reject": True,
        "requires_supervisor": True,
        "supervisor": "compliance_agent",
        "max_parallel_tasks": 1,
    },
    "qa_supervisor": {
        "can_delegate": True,
        "can_approve": True,
        "can_reject": True,
        "requires_supervisor": True,
        "supervisor": "compliance_agent",
        "max_parallel_tasks": 1,
    },
    "interpreter_agent": {
        "can_delegate": False,
        "can_approve": False,
        "can_reject": False,
        "requires_supervisor": True,
        "supervisor": "ba_supervisor",
        "max_parallel_tasks": 0,
    },
    "architect_agent": {
        "can_delegate": False,
        "can_approve": False,
        "can_reject": False,
        "requires_supervisor": True,
        "supervisor": "dev_supervisor",
        "max_parallel_tasks": 0,
    },
    "auditor_agent": {
        "can_delegate": False,
        "can_approve": False,
        "can_reject": False,
        "requires_supervisor": True,
        "supervisor": "qa_supervisor",
        "max_parallel_tasks": 0,
    },
}

# Task priority levels
TASK_PRIORITIES = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}

# Workflow stages
WORKFLOW_STAGES = {
    "intake": "Document intake and initial processing",
    "analysis": "Business analysis and requirement extraction",
    "design": "Architecture design and planning",
    "implementation": "Code generation and development",
    "testing": "Quality assurance and validation",
    "review": "Supervisor review and approval",
    "deployment": "Final deployment and documentation",
}


def get_agent_timeout(agent_type: str) -> int:
    """Get timeout for specific agent type."""
    return AGENT_SETTINGS["timeouts"].get(agent_type, 180)


def get_agent_capability(agent_type: str, capability: str) -> Any:
    """Get specific capability for an agent type."""
    return AGENT_CAPABILITIES.get(agent_type, {}).get(capability)


def can_agent_delegate(agent_type: str) -> bool:
    """Check if agent can delegate tasks."""
    return get_agent_capability(agent_type, "can_delegate") or False


def get_agent_supervisor(agent_type: str) -> str:
    """Get supervisor for an agent type."""
    return get_agent_capability(agent_type, "supervisor") or ""


def get_max_retries() -> int:
    """Get maximum number of retries for agent tasks."""
    return AGENT_SETTINGS["retries"]["max_retries"]


def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration."""
    return AGENT_SETTINGS["llm"]
