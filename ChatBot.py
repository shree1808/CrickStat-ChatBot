import streamlit as st
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

# pip install -qU langchain-ollama
# pip install langchain

# with st.form("llm-form"):
#     text = st.text_area("Enter your question or statement:")
#     submit = st.form_submit_button("Submit")

model_name = "llama3.2"
ollama_url = "http://localhost:11434/"

llm = ChatOllama(model = model_name, 
                    base_url = ollama_url,
                    temperature=0.8,
                    num_predict=256,
                    stream=False)

template="""
        Give me performance insights for player {player_name} in {format_type}
        across all the matches, tours and ICC tournaments in the {year}
        """

prompt = PromptTemplate(
                    input_variables = ["player_name", "format_type", "year"],
                    template = template
                    )
    

def generate_response(message):
    # Messages for the Ollama Model
    messages = [
        ("system", "Act as a Cricket genius who knows all about Cricket Scores and all Individual Players"),
        ("human", formatted_prompt),
    ]

    response = llm.invoke(messages)

    return response.content

st.set_page_config(page_title="CrickStat",
                    page_icon='🏏',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("🏏 CrickStat 🏏")

st.subheader(" AI Powered application for quick player insights ")

st.write(" Just enter the player name and the format. This is a platform offered with cross questioning capability ")


## Now For Creating the Input Buttons ##

player_name = st.text_input("Enter the Player Name")

col1, col2 = st.columns([5,5])

with col1:
    format_type = st.selectbox('Select the Format Type', ('One-Day International', 'Test', 'T-20 International', 'IPL'), index = 0)
    st.write('Selected Format is:', format_type)

with col2:
    year = st.slider('Enter the Year Range', 2000, 2025)
    st.write('Selected Year :', year)

## Submit Button ##

submit=st.button("Generate")

print(st.session_state)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

## Final response ##
if submit:

    formatted_prompt = prompt.format(
                    player_name = player_name, 
                    format_type = format_type , 
                    year = year)
    
    response = generate_response(formatted_prompt)
    
    st.session_state['chat_history'].append({"user": formatted_prompt, "ollama": response})
    st.write(response)


## Displaying and Storing Previous Chats ##
st.write("## Chat History")
for chat in reversed(st.session_state['chat_history']):
    st.write(f"**🧑 User**: {chat['user']}")
    st.write(f"**🏏 Assistant**: {chat['ollama']}")
    st.write("---")


## Displaying the Previous Chats' ##

# for role, messages in st.session_state['chat_history']:
#     if role == 'human':
#         st.markdown(f'**You** : {messages}')
#     else:
#         st.markdown(f'**Assistant** : {messages}')    

## Credits
# https://github.com/laxmimerit/ollama-chatbot/blob/main/1.simple_chatbot/1.simple_chatbot.py
# https://github.com/krishnaik06/Complete-Langchain-Tutorials/blob/main/Blog%20Generation/app.py