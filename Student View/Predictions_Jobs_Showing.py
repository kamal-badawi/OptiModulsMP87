# WICHTIGER HINWEIS:
# Für die Erstellung von der Job-Listen (Linkedin) gilt das folgende Video als Grundlage
# https://www.youtube.com/watch?v=-H-JCgvV0z8&list=LL&index=3
def run_predictions_jobs_showing(language_index ,all_unique_jobs, job_location ,posted_time_dict ,selected_posted_time):
    import streamlit as st
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()



    # Erstelle eine dicke Linie Funktion (dashed) zwei mal
    def draw_dashed_line_double_one(groesse):
        st.markdown(f"<hr style='border: {groesse}px dashed #009999;margin-bottom: 0;'>", unsafe_allow_html=True)
        st.markdown(f"<hr style='border: {groesse}px dashed black;margin: 0;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (dashed) zwei mal
    def draw_dashed_line_double_two(groesse):
        st.markdown(f"<hr style='border: {groesse}px dashed black;margin-bottom: 0;'>", unsafe_allow_html=True)
        st.markdown(f"<hr style='border: {groesse}px dashed #009999;margin: 0;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (dashed)
    def draw_dashed_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px dashed black;'>", unsafe_allow_html=True)

    start = 0  # Starting point for pagination
    posted_time = posted_time_dict.get(selected_posted_time)

    for job_title in all_unique_jobs:


        try:
            dummy_col_one ,title_col ,dummy_col_two = st.columns(3)
            with dummy_col_one:
                # Eine horizontale null Pixel Linie hinzufügen
                draw_dashed_line_double_one(2)
                st.markdown(
                    f"""
                                    <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                        ㅤ
                                    </div>
                                        """,
                    unsafe_allow_html=True
                )
                # Eine horizontale zwei Pixel Linie hinzufügen
                draw_dashed_line_double_two(2)

                st.write('')
                st.write('')

            with title_col:
                # Eine horizontale zwei Pixel Linie hinzufügen
                draw_dashed_line_double_two(2)
                st.markdown(
                    f"""
                    <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                        {job_title}
                    </div>
                        """,
                    unsafe_allow_html=True
                )
                # Eine horizontale zwei Pixel Linie hinzufügen
                draw_dashed_line_double_one(2)

                st.write('')
                st.write('')

            with dummy_col_two:
                # Eine horizontale null Pixel Linie hinzufügen
                draw_dashed_line_double_one(2)
                st.markdown(
                    f"""
                                    <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                        ㅤ
                                    </div>
                                        """,
                    unsafe_allow_html=True
                )
                # Eine horizontale zwei Pixel Linie hinzufügen
                draw_dashed_line_double_two(2)

                st.write('')
                st.write('')


            # Construct the URL for LinkedIn job search
            list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_title}&location={job_location}&start={start}&f_TPR={posted_time}"

            # Send a GET request to the URL and store the response
            response = requests.get(list_url)

            # Get the HTML, parse the response and find all list items(jobs postings)
            list_data = response.text
            list_soup = BeautifulSoup(list_data, "html.parser")
            page_jobs = list_soup.find_all("li")

            # Create an empty list to store the job postings
            id_list = []
            # Itetrate through job postings to find job ids
            for job in page_jobs:
                base_card_div = job.find("div", {"class": "base-card"})
                job_id = base_card_div.get("data-entity-urn").split(":")[3]
                id_list.append(job_id)

            # Initialize an empty list to store job information
            all_jobs = []

            # Loop through the list of job IDs and get each URL
            for job_id in id_list:
                # Construct the URL for each job using the job ID
                job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

                # Send a GET request to the job URL and parse the reponse
                job_response = requests.get(job_url)
                job_soup = BeautifulSoup(job_response.text, "html.parser")

                # st.write(job_soup)

                # Create a dictionary to store job details
                job_post = {}

                # Extrahiere das Firmenlogo
                try:
                    image_tag = job_soup.find("img", {
                        "class": "artdeco-entity-image artdeco-entity-image--square-5"
                    })

                    job_post["company_logo"] = image_tag.get("data-delayed-url", "").strip() if image_tag else None
                except:
                    job_post["company_logo"] = None


                # Extrahiere die Job-Beschreibung
                try:
                    job_post["job_title"] = job_soup.find("h2", {
                        "class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
                except:
                    job_post["job_title"] = None


                # Extrahiere den Firmennamen
                try:
                    job_post["company_name"] = job_soup.find("a", {
                        "class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
                except:
                    job_post["company_name"] = None


                # Extrahiere den Job-Ort
                try:
                    job_post["job_location"] = job_soup.find("span", {
                        "class": "topcard__flavor topcard__flavor--bullet"}).text.strip()
                except:
                    job_post["job_location"] = None




                # Extrahiere das Veröffentlichungsdatum
                try:
                    job_post["posted"] = job_soup.find("span", {
                        "class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
                except:
                    job_post["posted"] = None


                # Extrahiere Bewerber_Anazhl
                try:
                    job_post["count_of_applicants"] = job_soup.find("span", {
                        "class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
                except:
                    job_post["count_of_applicants"] = None


                # Append the job details to the all_jobs
                all_jobs.append(job_post)

            all_jobs_df = pd.DataFrame(all_jobs)


            all_jobs_df.columns = ['Firmenlogo' ,'Job-Titel', 'Unternehmen' ,'Ort', 'Veröffentlichungsdatum', 'Bewerbungsanzahl']

            all_jobs_df['Veröffentlichungsdatum'].fillna('Less than  24 hours', inplace=True)
            all_jobs_df['Bewerbungsanzahl'].fillna('Less than or equal to 25 applicants' ,inplace=True)

            count_of_jobs = len(all_jobs_df['Job-Titel'])

            counter = 0
            for index, row in all_jobs_df.iterrows():
                counter = counter + 1
                log_col, company_col, job_title_col, job_location_col, time_posted_col, count_apps_col = st.columns(6)

                with log_col:

                    # Logo
                    hover_style_company_logo = """
                        <style>
                        .company_logo {
                            transition: opacity 0.8s ease;
                            animation: schuetteln 3s infinite linear;
                        }
                        @keyframes schuetteln {
                        0% { transform: translateX(0); }
                        20% { transform: translateX(15px); }
                        40% { transform: translateX(-15px); }
                        60% { transform: translateX(15px); }
                        80% { transform: translateX(-15px); }
                        100% { transform: translateX(0); }
                    }


                        </style>
                    """

                    # Apply the custom CSS
                    st.markdown(hover_style_company_logo, unsafe_allow_html=True)


                    logo_url = row['Firmenlogo']
                    if logo_url:
                        st.markdown(
                            f'<div><img src="{logo_url}" class="company_logo"></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="company_logo">Kein Logo verfügbar</div>',
                            unsafe_allow_html=True
                        )

                with company_col:
                    st.markdown(f"**{row['Unternehmen']}**", unsafe_allow_html=True)


                with job_title_col:
                    st.markdown(f"**{row['Job-Titel']}**", unsafe_allow_html=True)


                with job_location_col:
                    st.markdown(f"**{row['Ort']}**", unsafe_allow_html=True)


                with time_posted_col:
                    st.markdown(f"**{row['Veröffentlichungsdatum']}**", unsafe_allow_html=True)


                with count_apps_col:
                    st.markdown(f"**{row['Bewerbungsanzahl']}**", unsafe_allow_html=True)


                if counter < count_of_jobs and count_of_jobs is not None:
                    # Eine horizontale zwei Pixel dashed Linie hinzufügen
                    draw_dashed_line(2)


        except:
            st.warning \
                (f'Aktuell sind keine Jobs für **{job_title}** im ausgewählten Zeitraum (**{selected_posted_time}**) verfügbar.')





