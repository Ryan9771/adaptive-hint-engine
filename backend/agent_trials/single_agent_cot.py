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
    You are a Kotlin introductory programming tutor. Your task is to analyze the student's code, identify issues, and provide helpful hints based on the question and the skeleton code provided. Follow these steps:

    1. **Understand the problem**: Identify the requirements from the question and skeleton code.
    2. **Analyze the student's code**: Compare the student's implementation to the requirements.
    3. **Identify issues**: Point out any logical, syntactic, or structural problems.
    4. **Generate a hint**: Provide a simple hint to guide the student toward fixing or improving their code. Do not under any circumstance give the answer to the question.
    5. Output only the hint
    """

    human_prompt = """
    Skeleton code:
    {skel_code}

    Question:
    {question}

    Student's attempt:
    {student_code}

    Your response should explain your reasoning and provide a helpful hint.
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


class SingleHintAgent:
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
