import streamlit as st
from rag import answer
 
st.set_page_config(page_title="UniBot", page_icon=":mortar_board:")
st.title("UniBot")
st.caption("Ask me about attendance, exams, fees, hostel and library.")
 
# remember the chat between reruns
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# show the chat so far
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


question = st.chat_input("Type your question...")
 
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
 
    with st.chat_message("assistant"):
        with st.spinner("Searching the documents..."):
            reply, chunks = answer(question)
        st.markdown(reply)
        with st.expander("Sources used"):
            for c in chunks:
                st.markdown(f"**{c['source']}**, page {c['page']} "
                            f"(distance {c['distance']:.2f})")
                st.caption(c["text"][:300] + "...")
 
    st.session_state.messages.append({"role": "assistant", "content": reply})
