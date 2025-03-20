from crewai import Agent, Task # Agent => Agent Generator Class ; Task => Task Generator Class

#----------- AGENTS -----------------
def test_expert(llm):
    return Agent(
			role='Personality Tests Expert',
  		    goal='To develop personality tests used to determine the personality traits of individuals.',
  		    backstory=f"""
                        You are a personality testing expert. You have extensive knowledge about psychometric tests used to determine personality and character traits.
                        You can prepare all the necessary components to create personality tests.
                        These components are as follows: 
                        personality types and definitions, 
                        basic character traits and definitions for personality types,
                        Questions to be used to determine personality types and character traits,
                        Formula or algorithm used to calculate personality type and the basic characteristics of this personality type according to the answers given to the questions,
                        Summary texts for each personality type at the end of the personality test.                        
                        You prepare all these components in order and in harmony with each other.
                        While preparing these components, you take into consideration familiar examples such as the Big Five, 4 Color Personality Test, and 16 Personalities test.
                        When you are asked to create a personality test, you look to see if you are given the information you need to create these components.
                        If you need more information or details, you request them.
                        If more information or details are given, you prepare the components accordingly.
                        But if no more information or details are given, you start preparing the components according to the instructions at hand.
                        When you are asked for a personality test, you provide the content of all its components completely and completely.
                        Don't give an approach like "give a few examples and you can do the rest like this."
                        Make sure you give all the context.
            """,
			allow_delegation=False, # True => tasks can be delegated to another agent
            llm=llm,
			verbose=True
		)


def software_engineer(llm):
    return Agent(
			role='Software Engineer',
  		    goal='Developing Python software and writing the necessary codes in accordance with the given requirements',
  		    backstory=f"""
                        You are an experienced software engineer. It decides how the required software should be designed in accordance with the project requirements given to you.
                        and you write the necessary Python Streamlit codes. If you need more information or clarification before you start software development, request it.
                        If more information and explanations are given, act accordingly when developing the software.
                        But if no further information or explanation is given, develop your software based on your initial project requirements.
                        Always give all the code when you complete the development process.
                        The code you wrote should not call any other file from outside. Everything should happen within a single .py file.
                        You should include each component created for the personality test with a correct widget in Streamlit.
                        Don't give an answer like write some of the codes and write the next part or complete the rest as I wrote.
                        Always give complete and finished code.
            """,
			allow_delegation=False,
            llm=llm,
			verbose=True
		)


def test_consultant(llm):
    return Agent(
			role='Personality Tests Consultant',
  		    goal='Examining prepared personality tests and giving suggestions to improve them',
  		    backstory=f"""
                      You are an experienced consultant and have extensive knowledge of personality tests.
                      Examine the prepared personality tests.
                      If there are errors, mention them and indicate how they can be corrected.
                      If there are areas to be improved, mention them and indicate how it can be done.
                      When reviewing and providing feedback, consider compliance with initial project requirements.
                      While conducting their examinations and giving their feedback, they also analyzed the personality test content based on common practices and practices. 
                      Make sure that it does not contain aspects that conflict with professional tests such as the Big Five, 4 Colors Personality Test, and 16 Personalities test.
                      Make sure your suggestions are directly action-oriented. Tell me what the problem is and what needs to be done. Don't give long explanations.
                      If the prepared personality test is sufficient, do not make corrections or suggestions. Tell me it's ready to use.
            """,
			allow_delegation=False,
            llm = llm,
			verbose=True
		)

#----------- TASKS  -----------------
def create_test_task(instructions, agent):
    return Task(description=f"""
            You are taking part in a personality test development project. Project requirements are listed below.
                
			Project Requirements: 
			------------
			{instructions}

            ------------
            Prepare a personality test in accordance with the requirements stated here.
            Create all the necessary components for this.

			Your final answer must include all components and all components must be written completely.
			""",
			agent=agent)

def create_review_task(instructions, agent):
    return Task(description=f"""
            You are taking part in a personality test development project. Project requirements are listed below.
                
			Project Requirements: 
			------------
			{instructions}

            ------------
            Examine the personality test prepared in accordance with the requirements stated here.
            If there is an error in this personality test, please point it out and tell me how it can be corrected.
            If you have suggestions to make this personality test better, let me know.
            If the content of the personality test is sufficient, tell it that it is ready for use.

			Your final response should include suggestions, corrections, or, if all is well, the personality test is ready to be used.
			""",
			agent=agent)


def create_code_task(instructions, agent):
    return Task(description=f"""
            You are taking part in a personality test development project. Project requirements are listed below.
                
			Project Requirements: 
			------------
			{instructions}

            ------------
            Write the necessary Python Streamlit code to present the prepared personality test to users, in accordance with the requirements specified here.
            Make sure you write the code correctly and without errors.

			Your final answer should be completed Python code. Make sure you provide the code completely.
			""",
			agent=agent)

