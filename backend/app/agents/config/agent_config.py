"""Agent configuration and registry"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    level: int
    supervisor: str = None
    workers: List[str] = None
    description: str = ""
    max_retries: int = 3
    timeout_seconds: int = 300


# Hierarchical Agent Structure
AGENT_HIERARCHY = {
    # Level 0: Master Orchestrator
    "compliance_agent": AgentConfig(
        name="Compliance Agent",
        level=0,
        supervisor=None,
        workers=["ba_supervisor", "dev_supervisor", "qa_supervisor"],
        description="Master orchestrator for regulatory compliance automation",
        timeout_seconds=600
    ),

    # Level 1: Supervisors
    "ba_supervisor": AgentConfig(
        name="BA Supervisor",
        level=1,
        supervisor="compliance_agent",
        workers=["interpreter_agent"],
        description="Supervises business analysis and requirement interpretation"
    ),

    "dev_supervisor": AgentConfig(
        name="Dev Supervisor",
        level=1,
        supervisor="compliance_agent",
        workers=["architect_agent"],
        description="Supervises development and code generation"
    ),

    "qa_supervisor": AgentConfig(
        name="QA Supervisor",
        level=1,
        supervisor="compliance_agent",
        workers=["auditor_agent"],
        description="Supervises quality assurance and testing"
    ),

    # Level 2: Worker Agents
    "interpreter_agent": AgentConfig(
        name="Interpreter Agent",
        level=2,
        supervisor="ba_supervisor",
        workers=[],
        description="Interprets regulatory requirements and creates business rules"
    ),

    "architect_agent": AgentConfig(
        name="Architect Agent",
        level=2,
        supervisor="dev_supervisor",
        workers=[],
        description="Designs data architecture and generates SQL/Python code"
    ),

    "auditor_agent": AgentConfig(
        name="Auditor Agent",
        level=2,
        supervisor="qa_supervisor",
        workers=[],
        description="Validates code, runs tests, and ensures compliance"
    ),
}


def get_agent_config(agent_id: str) -> AgentConfig:
    """Get configuration for a specific agent"""
    return AGENT_HIERARCHY.get(agent_id)


def get_agents_by_level(level: int) -> List[AgentConfig]:
    """Get all agents at a specific level"""
    return [config for config in AGENT_HIERARCHY.values() if config.level == level]


def get_worker_agents(supervisor_id: str) -> List[AgentConfig]:
    """Get all worker agents for a supervisor"""
    supervisor_config = AGENT_HIERARCHY.get(supervisor_id)
    if not supervisor_config or not supervisor_config.workers:
        return []

    return [AGENT_HIERARCHY[worker_id] for worker_id in supervisor_config.workers
            if worker_id in AGENT_HIERARCHY]
