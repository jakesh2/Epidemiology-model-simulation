import streamlit as st
from ui_components import build_ui

# Set the page configuration as the first Streamlit command
st.set_page_config(page_title="Epidemielody models", layout="wide")

def main():
    
    build_ui()

if __name__ == "__main__":
    main()
