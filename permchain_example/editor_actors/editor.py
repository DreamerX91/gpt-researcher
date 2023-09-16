from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from config import Config

CFG = Config()

EDIT_TEMPLATE = """You are an editor. \
You have been tasked with editing the following draft, which was written by a non-expert. \
Please accept the draft if it is good enough to publish, or send it for revision, along with your notes to guide the revision. \
Things you should be checking for:

- This draft MUST fully answer the original question
- This draft MUST be apa format

If not all of the above criteria are met, you should send appropriate revision notes.
"""

critique_prompt = (
    SystemMessagePromptTemplate.from_template(EDIT_TEMPLATE)
    + "Draft:\n\n{draft}"
)
critique_llm = ChatOpenAI(model=CFG.smart_llm_model)
functions = [
    {
        "name": "revise",
        "description": "Sends the draft for revision",
        "parameters": {
            "type": "object",
            "properties": {
                "notes": {
                    "type": "string",
                    "description": "The editor's notes to guide the revision.",
                },
            },
        },
    },
    {
        "name": "accept",
        "description": "Accepts the draft",
        "parameters": {
            "type": "object",
            "properties": {"ready": {"const": True}},
        },
    },
]

#EditorActor = critique_prompt | critique_llm.bind(functions=functions)


class EditorActor:
    @property
    def runnable(self):
        return (
                critique_prompt | critique_llm.bind(functions=functions)
        )