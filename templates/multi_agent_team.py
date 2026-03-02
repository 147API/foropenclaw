"""
Multi-Agent Team Template

Inspired by Fu Sheng's practice: 8 agents working together to manage operations.

This template shows how to build a team of AI agents that collaborate
to handle complex workflows.

Use cases:
- Company operations (like Fu Sheng)
- Content production pipeline
- Customer service team
- Research & development
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class AgentTask:
    """Task assigned to an agent."""
    task_id: str
    agent_id: str
    description: str
    priority: int  # 1-5, 5 is highest
    status: str  # pending, in_progress, completed, failed
    created_at: str
    completed_at: str = None
    result: Any = None

class BaseAgent:
    """Base class for all agents in the team."""
    
    def __init__(self, agent_id: str, name: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.tasks = []
    
    def can_handle(self, task_type: str) -> bool:
        """Check if this agent can handle the task type."""
        return task_type in self.capabilities
    
    def assign_task(self, task: AgentTask):
        """Assign a task to this agent."""
        self.tasks.append(task)
        task.status = "pending"
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Execute a task. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement execute_task")
    
    def get_status(self) -> Dict:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": self.capabilities,
            "pending_tasks": len([t for t in self.tasks if t.status == "pending"]),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"])
        }

class EmailAgent(BaseAgent):
    """
    Agent specialized in email processing.
    
    Capabilities:
    - Triage emails (100 emails in 30 seconds)
    - Categorize by priority
    - Draft responses
    - Flag urgent items
    """
    
    def __init__(self):
        super().__init__(
            agent_id="email_agent",
            name="Email Agent",
            capabilities=["email_triage", "email_response", "email_categorization"]
        )
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Process emails."""
        task.status = "in_progress"
        
        # Simulate email processing
        # In production, integrate with email API
        result = {
            "processed": 100,
            "urgent": 5,
            "important": 20,
            "normal": 75,
            "time_taken_seconds": 30
        }
        
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()
        task.result = result
        
        return result

class CalendarAgent(BaseAgent):
    """
    Agent specialized in calendar management.
    
    Capabilities:
    - Schedule meetings
    - Find available slots
    - Send invites
    - Handle conflicts
    """
    
    def __init__(self):
        super().__init__(
            agent_id="calendar_agent",
            name="Calendar Agent",
            capabilities=["meeting_scheduling", "availability_check", "conflict_resolution"]
        )
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Handle calendar tasks."""
        task.status = "in_progress"
        
        # Simulate meeting scheduling
        result = {
            "meeting_scheduled": True,
            "time": "2026-03-03 14:00",
            "attendees": ["person1@example.com", "person2@example.com"],
            "invites_sent": True
        }
        
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()
        task.result = result
        
        return result

class CommunicationAgent(BaseAgent):
    """
    Agent specialized in team communication.
    
    Capabilities:
    - Send personalized messages
    - Collect feedback
    - Coordinate teams
    - Generate reports
    """
    
    def __init__(self):
        super().__init__(
            agent_id="communication_agent",
            name="Communication Agent",
            capabilities=["messaging", "feedback_collection", "team_coordination"]
        )
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Handle communication tasks."""
        task.status = "in_progress"
        
        # Example: Send personalized messages to 611 people (like Fu Sheng)
        result = {
            "messages_sent": 611,
            "personalized": True,
            "delivery_rate": 0.99,
            "response_rate": 0.45
        }
        
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()
        task.result = result
        
        return result

class ContentAgent(BaseAgent):
    """
    Agent specialized in content creation.
    
    Capabilities:
    - Write articles
    - Generate social media posts
    - Create reports
    - Optimize content
    """
    
    def __init__(self):
        super().__init__(
            agent_id="content_agent",
            name="Content Agent",
            capabilities=["article_writing", "social_media", "report_generation"]
        )
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Create content."""
        task.status = "in_progress"
        
        # Simulate content creation
        result = {
            "content_type": "article",
            "word_count": 1500,
            "quality_score": 0.92,
            "seo_optimized": True
        }
        
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()
        task.result = result
        
        return result

class AnalyticsAgent(BaseAgent):
    """
    Agent specialized in data analysis.
    
    Capabilities:
    - Track metrics
    - Generate insights
    - Create dashboards
    - Predict trends
    """
    
    def __init__(self):
        super().__init__(
            agent_id="analytics_agent",
            name="Analytics Agent",
            capabilities=["metrics_tracking", "insight_generation", "trend_analysis"]
        )
    
    def execute_task(self, task: AgentTask) -> Dict:
        """Analyze data."""
        task.status = "in_progress"
        
        # Simulate analytics
        result = {
            "metrics": {
                "engagement_rate": 0.15,
                "growth_rate": 0.08,
                "conversion_rate": 0.03
            },
            "insights": [
                "Engagement up 20% this week",
                "Best posting time: 9-11 AM"
            ]
        }
        
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()
        task.result = result
        
        return result

class AgentTeam:
    """
    Orchestrates multiple agents working together.
    
    Example: Fu Sheng's 8-agent team managing company operations.
    """
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
    
    def add_agent(self, agent: BaseAgent):
        """Add an agent to the team."""
        self.agents.append(agent)
        print(f"✅ Added {agent.name} to the team")
    
    def assign_task(self, description: str, task_type: str, priority: int = 3) -> bool:
        """
        Assign a task to the appropriate agent.
        
        Returns True if task was assigned, False if no agent can handle it.
        """
        # Find capable agent
        for agent in self.agents:
            if agent.can_handle(task_type):
                task = AgentTask(
                    task_id=f"task_{len(self.task_queue)}",
                    agent_id=agent.agent_id,
                    description=description,
                    priority=priority,
                    status="pending",
                    created_at=datetime.utcnow().isoformat()
                )
                
                agent.assign_task(task)
                self.task_queue.append(task)
                print(f"📋 Assigned task to {agent.name}: {description}")
                return True
        
        print(f"❌ No agent can handle task type: {task_type}")
        return False
    
    def execute_all_tasks(self):
        """Execute all pending tasks."""
        print("\n🚀 Executing all tasks...\n")
        
        for agent in self.agents:
            pending = [t for t in agent.tasks if t.status == "pending"]
            
            for task in pending:
                print(f"⚙️  {agent.name} executing: {task.description}")
                result = agent.execute_task(task)
                self.completed_tasks.append(task)
                print(f"✅ Completed in {result.get('time_taken_seconds', 'N/A')}s")
    
    def get_team_status(self) -> Dict:
        """Get status of entire team."""
        return {
            "team_size": len(self.agents),
            "total_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "agents": [agent.get_status() for agent in self.agents]
        }
    
    def generate_report(self) -> str:
        """Generate team performance report."""
        status = self.get_team_status()
        
        report = "📊 Agent Team Performance Report\n"
        report += "=" * 50 + "\n\n"
        report += f"Team Size: {status['team_size']} agents\n"
        report += f"Total Tasks: {status['total_tasks']}\n"
        report += f"Completed: {status['completed_tasks']}\n\n"
        report += "Agent Status:\n"
        
        for agent_status in status['agents']:
            report += f"  • {agent_status['name']}: "
            report += f"{agent_status['completed_tasks']} completed, "
            report += f"{agent_status['pending_tasks']} pending\n"
        
        return report

# Example usage: Fu Sheng's 8-agent team
if __name__ == "__main__":
    print("🦞 Building Fu Sheng-style Agent Team\n")
    
    # Create team
    team = AgentTeam()
    
    # Add agents (like Fu Sheng's 8 agents)
    team.add_agent(EmailAgent())
    team.add_agent(CalendarAgent())
    team.add_agent(CommunicationAgent())
    team.add_agent(ContentAgent())
    team.add_agent(AnalyticsAgent())
    
    print("\n" + "=" * 50)
    print("Assigning tasks...\n")
    
    # Assign tasks
    team.assign_task("Process 100 emails", "email_triage", priority=5)
    team.assign_task("Schedule meeting with team", "meeting_scheduling", priority=4)
    team.assign_task("Send personalized messages to 611 employees", "messaging", priority=5)
    team.assign_task("Write weekly report", "article_writing", priority=3)
    team.assign_task("Analyze engagement metrics", "metrics_tracking", priority=3)
    
    # Execute all tasks
    team.execute_all_tasks()
    
    # Generate report
    print("\n" + "=" * 50)
    print(team.generate_report())
    
    print("\n💡 This is how Fu Sheng manages operations with AI agents!")
