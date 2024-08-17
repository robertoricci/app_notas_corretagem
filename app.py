import streamlit as st
import pag_home
import pag_import

from streamlit_option_menu import option_menu

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title="Notas Corretagem",  # String or None. Strings get appended with "• Streamlit". 
    page_icon= '',  # String, anything supported by st.image, or None.
)

def main():
        st.write('Hello word')
        pages={
             "Home":page_home,
             "Importar":page_import
        }
        
        with st.sidebar:
            page = option_menu('Menu',['Home','Importar'],
                               icons=['house','pen'],
                               default_index=0,menu_icon='app-indicator',
                                styles={
                                        "container": {"padding": "2!important", "background-color": "#ffffff","margin": "0px" },
                                        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"}, #,"position": "relative","display": "inline"},
                                        "nav-link-selected": {"background-color": "#4a7198"},
        })
   
        pages[page]() 

def page_home():
     pag_home.main()


def page_import():
     pag_import.main()


if __name__ == "__main__":
   main()
