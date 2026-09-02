from langgraph.graph import StateGraph, END
from graph.state import MedicalState
from agents.analyzer_agent import analyzer_agent
from agents.recommender_agent import recommender_agent
from agents.scheduler_agent import scheduler_agent
from agents.notifier_agent import notifier_agent


def create_medical_workflow():
    """
    LangGraph workflow

    Flow:
    1. Analyze report → Check severity
    2. If normal → End
    3. If mild/critical → Recommend doctors
    4. User selects doctor (handled externally)
    5. Schedule appointment
    6. Send notifications
    """

    # Initialize graph with state schema
    workflow = StateGraph(MedicalState)

    # Add nodes (agents)
    workflow.add_node("analyze", analyzer_agent.analyze)
    workflow.add_node("recommend", recommender_agent.recommend)
    workflow.add_node("schedule", scheduler_agent.schedule)
    workflow.add_node("notify", notifier_agent.notify)

    # Define routing logic
    def route_after_analysis(state: MedicalState) -> str:
        """
        Conditional routing based on severity
        """
        severity = state.get("severity", "mild")

        if severity == "normal":
            # Normal reports don't need doctor consultation
            return "end_workflow"
        else:
            # Mild or critical cases need doctor recommendation
            return "recommend"

    # Set entry point
    workflow.set_entry_point("analyze")

    # Add conditional edges (routing logic)
    workflow.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "end_workflow": END,
            "recommend": "recommend"
        }
    )

    # Add sequential edges (after doctor selection in UI)
    workflow.add_edge("recommend", END)  # Pause for user selection

    # Compile the graph
    app = workflow.compile()

    return app


# Create the workflow instance
medical_workflow = create_medical_workflow()