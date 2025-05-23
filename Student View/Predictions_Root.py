
def run_predictions_root(language_index,title):
    import Predictions_Elective_Subjects_Selection
    import Predictions_Grades_Prediction
    import Predictions_Strengths_Prediction
    import Predictions_Competences_Prediction
    import streamlit as st
    import datetime
    import Process_Button_Styling
    import Background_Style
    import Centred_Title
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


    targets_options = ['Prognose der Wahlpflichtfächernoten',
                          'Prognose der Studentenstärken und Tipps zur gezielten Weiterentwicklung',
                          'Prognose der 4 best-geeigneten Wahlpflichtfächer',
                       'Prognose der Kompetenzen']


    selected_target = st.sidebar.selectbox(label='Was möchten Sie genau tun?',
                                      options=targets_options,
                                           key='selected_target')

    # Prognose der Wahlpflichtfächernoten oder # Prognose der Studentenstärken
    if selected_target == targets_options[0] or selected_target == targets_options[1]:


        student_date_of_birth = st.sidebar.date_input(label='Geburtsdatum:',
                                              value=datetime.date(2000, 1, 1),
                                              key='student_date_of_birth')


        student_matriculation_number = st.sidebar.number_input(label='Matrikelnummer:',
                                                       min_value=5000000,
                                                       max_value=6000000,
                                                       value=5000001,
                                                       key='student_matriculation_number')

    sidebar_button = None
    # Prognose der Wahlpflichtfächernoten
    if selected_target == targets_options[0]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                {selected_target}
                            </div>
                                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')
        if st.sidebar.button('Noten Prognostizieren'):
            sidebar_button = 'grades_prediction'
            Predictions_Grades_Prediction.run_predictions_grades_prediction(language_index, sidebar_button,student_date_of_birth,student_matriculation_number)

    #Prognose der Studentenstärken und Tipps zur gezielten Weiterentwicklung
    elif selected_target == targets_options[1]:

        tipps_options = ['Kompakt',
                           'Detailliert']

        selected_tipps = st.sidebar.selectbox(label='Wie ausführlich sollen die Tipps sein?',
                                               options=tipps_options,
                                               key='selected_tipps')

        selected_tipps = selected_tipps.lower()

        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                        {selected_target}
                                    </div>
                                        """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        if st.sidebar.button('Stärken Prognostizieren'):
            sidebar_button = 'strengths_prediction'
            Predictions_Strengths_Prediction.run_predictions_strengths_prediction(language_index,sidebar_button,student_date_of_birth,student_matriculation_number,selected_tipps)

    # Prognose der 4 best-geeigneten Wahlpflichtfächer
    elif selected_target == targets_options[2]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                        {selected_target}
                                    </div>
                                        """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Predictions_Elective_Subjects_Selection.run_predictions_elective_subjects_selection(language_index)


    # Prognose der Kompetenzen
    elif selected_target == targets_options[3]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                                        {selected_target}
                                    </div>
                                        """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Predictions_Competences_Prediction.run_predictions_competences_prediction(language_index)