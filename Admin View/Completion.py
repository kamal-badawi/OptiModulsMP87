def run_completion(language_index,title):
    import streamlit as st
    import Background_Style
    import time

    Background_Style.run_background_styl()



    st.write('')
    st.write('')
    st.write('')
    st.write('')
    # Vielen Dank für Ihre Aufmerksamkeit
    st.markdown(
        f""" <div style='text-align: center; font-weight: bold; font-size: 3.7vw; color:black;text-shadow: 2px 2px 15px #B8860B;'>
                  Vielen Dank für Ihre Aufmerksamkeit
                   </div>
            """,
        unsafe_allow_html=True
    )



    st.write('')
    st.write('')
    st.write('')
    st.write('')
    # Fragen und Antworten
    st.markdown(
        f""" <div style='text-align: center; font-weight: bold; font-size: 2.7vw; color:black;text-shadow: 2px 2px 15px #B8860B;'>
              Fragen und Antworten
               </div>
        """,
        unsafe_allow_html=True
    )

    while True:
        st.balloons()
        time.sleep(2.5)
