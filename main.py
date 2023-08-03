from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.llms import OpenAI



llm = OpenAI(temperature=1, openai_api_key=token,max_tokens = 1024)







def load_chain_ingredients():
    template = """Your job is to come up with a recipe with ingredients and instructions from the ingredients list that the users suggests.
    % INGREDIENTS LIST
    {ingredients_list}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["ingredients_list"], template=template)

    location_chain = LLMChain(llm=llm, prompt=prompt_template)
    return location_chain



loc_chain = load_chain_ingredients()

overall_chain = SimpleSequentialChain(chains=[loc_chain], verbose=True)

st.set_page_config(page_title=" ChefInTech", page_icon=":chef:")
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    
    input_text = st.chat_input("", key="input")
    input_2 = "recipe"
    input_3 = "ingredients"
    input_4 = "and"
    input_5 =  "with"
    input_6 = "instruction"
    input_text = " ".join([input_text,input_2,input_5,input_3,input_4,input_5,input_6])
    
    return input_text
    

user_input = get_text()

if user_input:
    output = overall_chain.run(input=user_input)

    #st.session_state.past.append(user_input)
    #st.session_state.generated.append(output)
    st.write(output)
if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
