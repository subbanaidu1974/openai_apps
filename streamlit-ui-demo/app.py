from huggingface_hub import upload_file
import streamlit as st
import StreamlitCssAPI as myst
import webscrapingAPI as webApi

def main():
    dropdown_options =[
                    "Select Option",
                    "Document Processing (File Upload)",
                    "Website Analysis (RAG)",
                    "Direct Website Processing (Non-RAG)"
                ]
    webApi.WebScrapingAPI.setApikey()
    # UI Interface Calls
    myst.StreamLibAPI.getSideBar("DPAONEAI")
    myst.StreamLibAPI.getChatButtonOnSidebar("New Chat")
    selected_option = myst.StreamLibAPI.getTitleWithDropDown("🌐 DpaOneAI Website Search","DPAONEAI",dropdown_options)
    myst.StreamLibAPI.createNewSession()

    webApi.WebScrapingAPI.initSessionState()
    webApi.WebScrapingAPI.getChatInterfaceMessages()

    #Functionality
    if "Document Processing (File Upload)" in selected_option:
        user_input = myst.StreamLibAPI.getChatInputBox("Upload file or Chat with Pdf...")
        upload_file = myst.StreamLibAPI.fileUploader("Upload file or Chat with Pdf...")
        if upload_file and not user_input:            
            # webApi.WebScrapingAPI.addUserInputToChatHistory("user", "✅ File Uploaded " + upload_file.name,"")
            webApi.WebScrapingAPI.uploadDocument(upload_file)
            # webApi.WebScrapingAPI.addUserInputToChatHistory("assistant",f"✅ File content loaded and chunked! Start chatting below.","")
        if not upload_file and user_input:
            webApi.WebScrapingAPI.addUserInputToChatHistory("assistant","⚠️ Please upload document first!","")                                   
        if user_input:      
            myst.StreamLibAPI.callSpinner()
            webApi.WebScrapingAPI.respondToPromptWithAnswerFromPDF(user_input)    
    else:        
        if "Website Analysis (RAG)" in selected_option:
            user_input = myst.StreamLibAPI.getChatInputBox("Enter website URL or ask a question...")
            
            if user_input:                
                webApi.WebScrapingAPI.addUserInputToChatHistory("user",user_input,"")
                if user_input.startswith(("http://", "https://")):                
                    webApi.WebScrapingAPI.downloadWebsiteContentRag(user_input)
                else:
                    myst.StreamLibAPI.callSpinner()
                    webApi.WebScrapingAPI.respondToPromptWithAnswerRag(user_input)
        if "Direct Website Processing (Non-RAG)" in selected_option:
            user_input = myst.StreamLibAPI.getChatInputBox("Enter website URL or ask a question...")            
            if user_input:                
                webApi.WebScrapingAPI.addUserInputToChatHistory("user",user_input,"")
                if user_input.startswith(("http://", "https://")):                               
                    webApi.WebScrapingAPI.loadWebsiteContent(user_input)
                else:
                    myst.StreamLibAPI.callSpinner()
                    webApi.WebScrapingAPI.respondToPromptWithAnswer(user_input)

if __name__ == "__main__":
    main()
