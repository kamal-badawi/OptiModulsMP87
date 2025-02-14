def run_model_evaluation_root(language_index,title):
    import Model_Evaluation_Grades_Prediction
    import Model_Evaluation_Strengths_Prediction
    import streamlit as st
    import Centred_Title
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    # Page Title
    Centred_Title.run_centred_title(title)

    # Logo sidebar
    st.sidebar.image("../Images/OptiModuls Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)


    model_name_options = ['Notenprognose-Modell',
                          'Stärkenprognose-Modell',]

    model_name = st.sidebar.selectbox(label='Welches Modell wollen Sie evaluieren?',
                                     options=model_name_options)


    # Modell-Evaluierung (Notenprognose)
    if model_name == model_name_options[0]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                                            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                                {model_name}
                                            </div>
                                                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')


        Model_Evaluation_Grades_Prediction.run_model_evaluation_grades_prediction(language_index)

    # Modell-Evaluierung (Stärkenprognose)
    elif model_name == model_name_options[1]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                                            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                                {model_name}
                                            </div>
                                                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Model_Evaluation_Strengths_Prediction.run_model_evaluation_strengths_prediction(language_index)
