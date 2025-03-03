import streamlit as st
import StreamlitCssAPI as myst
import webscrapingAPI as webApi

def main():
    dropdown_options =[
                    "Document Processing (File Upload)",
                    "Website Analysis (RAG)",
                    "Direct Website Processing (Non-RAG)"
                ]
    webApi.WebScrapingAPI.setApikey()
    # UI Interface Calls
    myst.StreamLibAPI.getSideBar("DPAONEAI")
    myst.StreamLibAPI.getChatButtonOnSidebar("New Chat")
    selected_option = myst.StreamLibAPI.getTitleWithDropDown("🌐 DpaOneAI Website Search","DPAONEAI",dropdown_options)

    #Functionality
    if "Document Processing (File Upload)" in selected_option:
        pass
    elif "Direct Website Processing (Non-RAG)" in selected_option:
        pass
    elif "Website Analysis (RAG)" in selected_option:        
        webApi.WebScrapingAPI.initSessionState()
        webApi.WebScrapingAPI.getChatInterfaceMessages()
        user_input = myst.StreamLibAPI.getChatInputBox("Enter website URL or ask a question...")
        if user_input:
            webApi.WebScrapingAPI.addUserInputToChatHistory("user",user_input,"")
            if user_input.startswith(("http://", "https://")):                
                webApi.WebScrapingAPI.downloadWebsiteContent(user_input)
            else:
                myst.StreamLibAPI.callSpinner()
                webApi.WebScrapingAPI.respondToPromptWithAnswer(user_input)
            

if __name__ == "__main__":
    main()
