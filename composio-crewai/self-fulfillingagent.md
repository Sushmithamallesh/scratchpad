# Agent tooling
Approach to self-fulfilling agents
- Conversation between two agents. Only one agent executes the task. The other agent is responsible for providing the necessary tools to complete the task. 
Approach 1:
      - Agent1: Performs RAG/search over the APIs and provides the necessary tools to complete the task. It can to a certain extent anticipate the task and provide the tools. But it can't be 100% accurate. 
      - Agent2: Performs the task and talks back to Agent1 to incase the tools provided by Agent1 are not sufficient.

Approach 2:
      - Agent1: Performs RAG/search over the APIs and provides the necessary tools to complete the task. It also provides a search API over the all the tools realted to the category of the task.
      - Agent2: Performs the task. In case the tool is not sufficient tp perform the task. It has to use the search API to find the tools that can be used to perform the task. It will not talk back to Agent1 to incase the tools provided by Agent1 are not sufficient.

Approach 3:




githublargebeta_reposcreateforauthenticateduser