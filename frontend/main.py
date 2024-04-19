
import streamlit as st
import requests

def main_page():
    st.title("Main Page")
    if st.button("Go to Upload Page"):
        st.session_state.current_page = 'upload'

def upload_page():
    st.title("Upload and Send Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])
    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file)
        if st.button("Send Image"):
            # Prepare the file to send
            files = {'file': uploaded_file.getvalue()}
            # Assuming the FastAPI server runs on localhost port 8000
            response = requests.post("http://localhost:8000/upload/", files=files)
            st.write(response.json())

def main():
    # Initial setup for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'

    # Page router
    if st.session_state.current_page == 'main':
        main_page()
    elif st.session_state.current_page == 'upload':
        upload_page()

if __name__ == "__main__":
    main()
