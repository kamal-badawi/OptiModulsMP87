import Data_Preview_Elective_Modules_from_Module_Handbook


def run_data_preview_root(language_index,title):
    import streamlit as st
    import Data_Loading_Elective_Modules_from_Module_Handbook
    import Data_Preview_Columns_Info
    import Data_Preview_Model_Training_Data
    import Data_Preview_Student_Mandatory_Modules_Grades_Data
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

    options = ['Modell-Training Daten für Notenprognose',
               'Wahlpflichtfächer Informations aus dem Modulhandbuch',
               'Spalten Informationen',
               'Studenten Daten (Noten von Pflichtfächern)']
    data_type = st.sidebar.selectbox(label = 'Welche Daten möchten Sie laden?',
                             options=options)




    # Modell-Training Daten für Notenprognose und Stärken
    if data_type == options[0]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                {data_type}
            </div>
                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Data_Preview_Model_Training_Data.run_data_preview_model_training_data(language_index,data_type)
        



    # Wahlpflichtfächer Informations aus dem Modulhandbuch
    elif data_type == options[1]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                {data_type}
            </div>
                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Data_Preview_Elective_Modules_from_Module_Handbook.run_preview_loading_elective_modules_from_module_handbook(language_index,data_type)



    # Spalten Informationen
    elif data_type == options[2]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                    {data_type}
                </div>
                    """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')
        Data_Preview_Columns_Info.run_data_preview_columns_info(language_index,data_type)



    # Studenten Daten (Noten von Pflichtfächern)
    elif data_type == options[3]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                {data_type}
            </div>
                """,
            unsafe_allow_html=True
        )
        st.sidebar.write('')
        st.sidebar.write('')

        Data_Preview_Student_Mandatory_Modules_Grades_Data.run_data_preview_student_mandatory_modules_grades_data(language_index,data_type)


