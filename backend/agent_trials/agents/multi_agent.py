"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from instances.llm_instance import LLM_instance
from util.types import AttemptContext, FeatureOutput, IssueConfidenceOutput, ConceptProficiencyModel, CodeComparisonOutput, LearningTrajectory, HintDirective, HintOutput

# == INSTANCES ==
llm = LLM_instance.get_instance()
