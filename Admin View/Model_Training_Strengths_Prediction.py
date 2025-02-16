def run_model_training_strenghts_prediction(language_index):
    import streamlit as st
    import sqlite3
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler
    from xgboost import XGBRegressor
    from sklearn.multioutput import MultiOutputRegressor
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.linear_model import LinearRegression
    import joblib
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Lade die Spalten-Infos-Daten
    @st.cache_data
    def get_columns_info():
        connection_columns_info = sqlite3.connect(r'../Databases/Columns Info Database.db')

        columns_info_data = pd.read_sql('Select * from columns_info_data',
                                        connection_columns_info)

        columns_info_data.columns = ['id', 'Datum', 'Spalte', 'Beschreibung']
        strenghts_info = list(columns_info_data[columns_info_data['Beschreibung'] == 'Stärke']['Spalte'])
        mandatory_modules_info = list(columns_info_data[columns_info_data['Beschreibung'] == 'Pflichtmodul']['Spalte'])
        elective_modules_info = list(
            columns_info_data[columns_info_data['Beschreibung'] == 'Wahlpflichtmodul']['Spalte'])
        return strenghts_info, mandatory_modules_info, elective_modules_info


    # Lade die Training-Daten
    @st.cache_data
    def get_training_data():
        connection_training_model = sqlite3.connect(r'../Databases/Model Training Database.db')
        training_model_data = pd.read_sql('Select * from model_training_data', connection_training_model)
        training_model_data.columns = modules_de
        return training_model_data

    modules_de = [
                'id',
                'Datum',
                "Einführung in die Wirtschaftsinformatik",
                "Einführung in die Programmierung",
                "Einführung in die Wirtschaftswissenschaften",
                "Mathematik für Wirtschaftsinformatiker 1",
                "Wissenschaftliches Arbeiten",
                "Entwicklung grafischer Bedienoberflächen",
                "Datenbanksysteme",
                "Algorithmen und Datenstrukturen",
                "Rechnungswesen",
                "Mathematik für Wirtschaftsinformatiker 2",
                "Operations Management",
                "Wirtschaftsinformatik-Seminar I (Proseminar)",
                "Softwaretechnik",
                "Grundlagen der Informationssicherheit",
                "Projektmanagement - Planspiel und Fallstudie",
                "Organisationslehre",
                "Wirtschaftsstatistik",
                "Kommerzielle Standardsoftware",
                "Wirtschaftsinformatik-Projekt 1 (Softwaretechnik)",
                "Business Intelligence",
                "Entwicklung betrieblicher Informationssysteme",
                "Wirtschaftsinformatik-Seminar 2 (Hauptseminar)",
                "Wirtschaftsinformatik-Projekt 2",
                "IT-Management",
                "Digitale Geschäftsprozesse",
                "Privat- und Arbeitsrecht sowie Rechtliche Aspekte der Informatik",

                "Analytisches Denken",
                "Problemlösungsfähigkeit",
                "Programmierkenntnisse",
                "Datenbankmanagement",
                "Kommunikationsfähigkeit",
                "IT-Sicherheitsbewusstsein",
                "Organisations- und Projektmanagement",
                "Teamarbeit und Kollaboration",
                "Wirtschaftliches Verständnis",
                "Technologische Innovation",
                "Rechtliches Verständnis",
                "Mathematische Kompetenz",

                "Geschäftsprozessmanagement mit SAP",
                "Predictive Analytics mit Python",
                "Web-Technologie",
                "Agile Methoden in der Praxis",
                "Wirtschaftsprüfung / IT-Prüfung",
                "Angewandte Softwaretechnik mit LEGO Mindstorm",
                "System- und Softwareentwicklung für Fahrerassistenzsysteme",
                "Automotive Data Driven Business",
                "Cyber Security Threat Modelling - VL",
                "Standards und Vorschriften zur IT-Sicherheit",
                "Requirements Engineering",
                "Big Data",
                "Grundlagen der KI",
                "DevOps"
            ]
    training_model_data = get_training_data()
    strenghts_columns, mandatory_modules_columns, elective_modules_columns = get_columns_info()

    # Features und Target Spalten festlegen
    X_columns = mandatory_modules_columns
    y_columns = strenghts_columns

    X_y_columns= X_columns + y_columns

    # Features und Target Daten
    X = training_model_data[X_columns]
    y= training_model_data[y_columns]
    X_y= training_model_data[X_y_columns]

    # Alle Daten
    st.markdown(
        f"""
        <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
            Alle Training-Daten
        </div>
         """,
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    st.write('')

    st.dataframe(X_y)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    # Features
    st.markdown(
        f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                Features-Daten
            </div>
             """,
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    st.write('')
    st.dataframe(X)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    # Targets
    st.markdown(
        f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    Targets-Daten
                </div>
                 """,
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    st.write('')

    st.dataframe(y)

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    Process_Button_Styling.run_process_button_style()
    if st.button("Daten vorverabeiten und Modell traininieren"):
        # st.write(X)
        # st.write(y)
        # st.write(X_y)

        # Fülle die Null-Werte, bzw. nicht geschriebene Pflichtfächer mit IterativeImputer unter Nutzung des BayesianRidge (Linear Regression)
        imputer_X = IterativeImputer(estimator=LinearRegression(),
                                     max_iter=20,
                                     random_state=42)

        # trainiere den Imputer nur mit X-Daten
        imputer_X = imputer_X.fit(X)
        X_imputed = pd.DataFrame(imputer_X.transform(X),
                                 columns=X_columns)

        # Speichere den Imputer lokal  (Features Imputer)
        joblib.dump(imputer_X, r'../Imputers/imputer_X_strengths_prediction.pkl')

        # Features-Imputed
        st.markdown(
            f"""
                                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                    Features-Imputed-Daten
                                </div>
                                 """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        st.dataframe(X_imputed)

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # st.write(X_imputed)

        # Fülle die Null-Werte, bzw. nicht-vorhandenen Stärken mit IterativeImputer unter Nutzung des BayesianRidge (Linear Regression)
        imputer_y = IterativeImputer(estimator=LinearRegression(),
                                     max_iter=20,
                                     random_state=42)

        # trainineire den Imputer mit allen Daten (wegen Zusammenhängen)
        imputer_y = imputer_y.fit(X_y)

        # Ergebnis nur y-Spalten
        y_imputed = pd.DataFrame(imputer_y.transform(X_y),
                                 columns=X_y_columns).loc[:, y_columns]

        # Speichere den Imputer lokal (Targets Imputer)
        joblib.dump(imputer_y, r'../Imputers/imputer_y_strengths_prediction.pkl')

        # Targets-Imputed
        st.markdown(
            f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    Targets-Imputed-Daten
                </div>
                 """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        st.dataframe(y_imputed)

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # Skalierung der Pflichtfächer
        scaler_X = MinMaxScaler()
        scaler_X.fit(X_imputed)
        X_scaled = pd.DataFrame(scaler_X.transform(X_imputed),
                                columns=X_columns)

        # Speichere den Scaler lokal  (Features Imputer)
        joblib.dump(scaler_X, r'../Scalers/scaler_X_strengths_prediction.pkl')

        # Features-Scaled
        st.markdown(
            f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    Features-Scaled-Daten
                </div>
                 """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        st.dataframe(X_scaled)

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # Skalierung der Wahlpflichtfächer
        scaler_y = MinMaxScaler()
        scaler_y.fit(y_imputed)
        y_scaled = pd.DataFrame(scaler_y.transform(y_imputed),
                                columns=y_columns)

        # Speichere den Scaler lokal  (Targets Imputer)
        joblib.dump(scaler_y, r'../Scalers/scaler_y_strengths_prediction.pkl')

        # Targets-Scaled
        st.markdown(
            f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                Targets-Scaled-Daten
            </div>
             """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        st.dataframe(y_scaled)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled,
                                                            y_scaled,
                                                            test_size=0.2,
                                                            random_state=42)

        pipeline = Pipeline([
            ('regressor', MultiOutputRegressor(XGBRegressor(objective='reg:squarederror', n_jobs=-1)))
        ])

        # Hyperparameter-Raster für Modelloptimierung
        param_grid = {
            'regressor__estimator__n_estimators': [50],  # Anzahl der Bäume im Ensemble
            'regressor__estimator__max_depth': [6],  # Maximale Tiefe der Entscheidungsbäume
            'regressor__estimator__learning_rate': [0.1],  # Lernrate für die Modellaktualisierung
            'regressor__estimator__subsample': [0.8],  # Anteil der Stichproben für jeden Baum
            'regressor__estimator__colsample_bytree': [0.8],  # Anteil der Merkmale, die pro Baum verwendet werden
            'regressor__estimator__min_child_weight': [1],  # Minimale Anzahl von Stichproben pro Blatt
            'regressor__estimator__gamma': [0],  # Mindestverlustreduzierung für einen Split
            'regressor__estimator__reg_alpha': [0],  # L1-Regularisierung (Gewicht der Merkmale)
            'regressor__estimator__reg_lambda': [1.0],  # L2-Regularisierung (Gewicht der Merkmale)
        }

        # GridSearchCV mit mehreren Metriken und erweiterter Cross-Validation
        grid_search = GridSearchCV(pipeline,
                                   param_grid,
                                   cv=2,  # Mehr Folds für robustere Ergebnisse
                                   scoring=['neg_mean_squared_error', 'r2', 'neg_mean_absolute_error'],
                                   refit='neg_mean_squared_error',  # Rückgriff auf MSE für das beste Modell
                                   verbose=3)

        # Modell mit den imputed & scaled Daten trainieren
        grid_search.fit(X_train, y_train)

        # Modell beste estimators & parameters
        model_best_estimator = grid_search.best_estimator_
        model_best_params_ = grid_search.best_params_

        # Speichere das beste Modell lokal  (Targets Imputer)
        joblib.dump(grid_search.best_estimator_, r'../ML-Model/bestes_xgboost_modell_strengths_prediction.pkl')

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # Model testen

        # y_test  lokal speichern
        y_pred = grid_search.predict(X_test)

        y_test = y_test.reset_index(drop=True)
        y_test.to_excel(r'../Modellbewertung/Stärkenprognose/y_test.xlsx')

        # y_pred  lokal speichern
        y_pred = pd.DataFrame(y_pred, columns=y_test.columns)
        y_pred.to_excel(r'../Modellbewertung/Stärkenprognose/y_pred.xlsx')

        st.success('Das Modell zur Stärkenprognose wurde erfolgreich trainiert und ist einsatzbereit')
    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
