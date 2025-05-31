from langgraph.graph import START, END, StateGraph
from instances.llm_instance import LLM_instance
from langchain_core.messages import HumanMessage
from util.prompts import single_agent_prompt
from util.types import SimpleGraphState


llm = LLM_instance.get_instance()


def hint_agent(state: SimpleGraphState):
    """
    Generates a hint simply by looking at the student's attempt and
    the question.
    """

    formatted_prompt = single_agent_prompt(
        skel_code=state["skel_code"],
        exercise_text=state["exercise_text"],
        student_code=state["student_code"],
        error=state["error"],
        test_results=state["test_results"]
    )

    response = llm.invoke(
        [
            HumanMessage(content=formatted_prompt),
        ]
    )

    return {"hint": response.content}


class SingleHintAgent:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(SimpleGraphState)

        builder.add_node("hint_agent", hint_agent)

        builder.add_edge(START, "hint_agent")

        builder.add_edge("hint_agent", END)

        self.graph = builder.compile()

    def run(self, state: SimpleGraphState):
        return self.graph.invoke(state)
