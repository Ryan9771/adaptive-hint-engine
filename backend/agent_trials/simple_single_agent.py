from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from instances.llm_instance import LLM_instance
from langchain_core.messages import HumanMessage, SystemMessage


class State(TypedDict):
    student_code: str
    question: str
    skel_code: str
    hint: str


def hint_agent(state: State):
    """
    Generates hints simply by looking at the student's attempt and
    the question.
    """
    llm = LLM_instance.get_instance()

    system_prompt = """
    You are an introductory Kotlin tutor who uses the given exercise question along 
    with the default skeleton code to provide a helpful hint to the student based on their
    code attempt attached.

    You should generate a hint helping the student make progress towards the goal of the
    question without revealing the answer.
    """

    human_prompt = """
    Skeleton code:
    {skel_code}

    Question:
    {question}

    Student's attempt:
    {student_code}
    """

    formatted_human_prompt = human_prompt.format(
        skel_code=state["skel_code"],
        question=state["question"],
        student_code=state["student_code"],
    )

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=formatted_human_prompt),
        ]
    )

    return {"hint": response.content}


class SimpleHintAgent:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(State)

        builder.add_node("hint_agent", hint_agent)

        builder.add_edge(START, "hint_agent")

        builder.add_edge("hint_agent", END)

        self.graph = builder.compile()

    def run(self, state: State):
        config = {"configurable": {"thread_id": "1"}}
        for e in self.graph.stream(input=state, config=config):
            print(e)
