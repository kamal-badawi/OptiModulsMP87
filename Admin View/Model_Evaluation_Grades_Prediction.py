def run_model_evaluation_grades_prediction(language_index):
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    import streamlit as st
    import pandas as pd

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Lade die Test- und Prediction-Daten
    @st.cache_data
    def get_data(path):
        data = pd.read_excel(path)
        return data

    # Metric für die 3 Metrics erstellen
    def make_evaluation_metric(evaluation_metric_name, optimal_value, score):
        import streamlit as st

        st.markdown(
            f"""
                <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                    <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                        {evaluation_metric_name}  
                    </h1>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;min-height:250px;'>
                        <span style='color:#FFD700;'>
                        <span style='color:#FFD700; '>‎ 
                        </span>
                        {optimal_value}
                        </span>
                    </h1>
                    <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{score:.5f}</h1>
                </div>
                """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')


    # y_test laden
    y_test = get_data(r'../Model-Evaluation/Grades-Prediction/y_test_grades_preditcion.xlsx')

    # y_pred laden
    y_pred = get_data(r'../Model-Evaluation/Grades-Prediction/y_pred_grades_preditcion.xlsx')

    # Berechnung der Metriken
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Visualisierung der Metriken
    mse_col, mae_col, r2_col = st.columns(3)
    with mse_col:
        mes_explaination_text = 'A lower MSE indicates better model performance'
        make_evaluation_metric('Mean Squared Error',
                               mes_explaination_text,
                               mse)

    with mae_col:
        mae_explaination_text = 'A lower MAE also indicates better performance'
        make_evaluation_metric('Mean Absolute Error',
                               mae_explaination_text,
                               mae)

    with r2_col:
        r2_explaination_text = 'R² = 1 means perfect predictions'
        make_evaluation_metric('R-squared',
                               r2_explaination_text,
                               r2)

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)

