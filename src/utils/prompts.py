analyst_instructions = """
You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:
1. First, review the research topic: {topic}
2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts  {human_analyst_feedback}
3. Determine the most interesting themes based upon dcumnet or feedbcak above.
4. Pick the top {max_analyst} most interesting themes and create an AI analyst persona for each theme. Each persona should have a unique name, a brief background, and a specific area of expertise related to the theme.
5. Assign one analyst to each theme."""