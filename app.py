import streamlit as st
import requests



S_URL="http://127.0.0.1:8000"

pdf_tab,web_tab,quiz_tab,summary_tab=st.tabs([
    "📄 PDF Reader","🌐 Web Search","❓quiz generator","📝 PDF Summarizer"
])

with pdf_tab:
    st.title("PDF Reader")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_reader"
    )

    question = st.text_input("Ask question from pdf")

    if st.button("Get Answer"):

        if uploaded_file is None:
            st.warning("Please upload a PDF")

        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            res = requests.post(
                f"{S_URL}/pdf_reader",
                params={"question": question},
                files=files
            )

            if res.status_code == 200:
                result = res.json()
                st.success(result["result"])
            else:
                st.error(res.text)
   
with web_tab:
    st.title("Web Search Assistant") 
    question=st.text_input(
        "Ask any question",
        key="web_search"
    )
    if st.button("Search Web"):
        res=requests.post(f"{S_URL}/web_search",params={
            "question":question
        })
        result=res.json()
        st.success(result["messages"][-1]["content"])
        
with quiz_tab:
    st.title("❓ Quiz Generator From PDF")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="quiz_pdf"
    )

    if st.button("Generate Quiz"):

        if uploaded_file is None:
            st.warning("Please upload a PDF")

        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            try:
                res = requests.post(
                    f"{S_URL}/quiz_generator",
                    files=files
                )

                result = res.json()

                if "error" in result:
                    st.error(result["error"])

                elif "result" in result:
                    st.success("Quiz Generated Successfully")
                    st.write(result["result"])

                else:
                    st.error("Unexpected response")
                    st.write(result)

            except Exception as e:
                st.error(f"Request Failed: {e}")
with summary_tab:
    st.title("📝 PDF Summarizer")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="summary_pdf"
    )

    if st.button("Summarize PDF"):
        if uploaded_file:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            res = requests.post(
                f"{S_URL}/pdf_summarizer",
                files=files
            )

            result = res.json()
            st.success(result["result"])        

    
        
    
                  
                              
            
        
