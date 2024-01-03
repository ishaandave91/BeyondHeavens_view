import time

import streamlit as st
from mysql.connector import Error
import database_connection as db
import base64
import video_playback
from email_validator import validate_email, EmailNotValidError

st.set_page_config(layout='wide', page_title='Beyond Heavens- view page')

user_email = st.text_input(label='Email ID:',
                           placeholder='Add recording name here...',
                           key='email_id')


est_connection = db.EstablishConnection()
connection = est_connection.database_connection()


def validate_email_address(email_address_input):
    try:
        v = validate_email(email_address_input)
        return "VALID"
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return str(e)


def count_existing_files(email_id):
    try:
        cursor = connection.cursor()
        count_query = f"""
            SELECT count(*) FROM videos
            WHERE receiveremailid = "{email_id}"
            AND DATE(senddate) = CURRENT_DATE();
        """
        cursor.execute(count_query)
        row_count = cursor.fetchall()[0][0]
        cursor.close()
        return row_count
    except Error as e:
        st.error(f"Error: {e}")
    return 0


def extract_records(email_id):
    try:
        cursor = connection.cursor()
        records_query = f"""
            SELECT id, filename, content, receiveremailid, senddate FROM videos 
            WHERE receiveremailid = "{email_id}";
        """

        cursor.execute(records_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except Error as e:
        st.error(f"Error: {e}")
    return []


# def render_video(fetched_records):
#     for filename, content, receiveremailid, senddate in fetched_records:
#         try:
#             button_name = filename
#             col3, col4 = st.columns(2)
#             with col3:
#                 watch_btn_key = f'watch_btn_{filename}'
#                 watch_button_clicked = st.button(f"Watch: {button_name}", use_container_width=True,
#                                                  key=watch_btn_key)
#             with col4:
#                 st.write("**Recipient:** ", receiveremailid)
#                 st.write("**Scheduled send date & time:** ", senddate)
#
#             st.write("<hr>", unsafe_allow_html=True)
#
#             if watch_button_clicked:
#                 decoded_content = base64.b64decode(content)
#                 video_frame = st.video(decoded_content, format="video/mp4", start_time=0)
#                 close_btn_key = f'close_vid_{filename}'
#                 close_button_clicked = st.button("Close", use_container_width=True,
#                                                  key=close_btn_key)
#                 if close_button_clicked:
#                     del close_button_clicked
#                     del video_frame
#         except Exception as e:
#             st.error(f"Error encoding video content: {e}")
#             return None


def main():
    if user_email != '':
        email_address_status = validate_email_address(user_email)
        if email_address_status == 'VALID':
            available_video_count = count_existing_files(user_email)
            if available_video_count > 0:
                del st.session_state['email_id']
                del st.session_state['submit']
                st.write("You have below recordings available for viewing:")
                available_records = extract_records(user_email)
                rend_video = video_playback.Video(available_records)
                rend_video.render_video()
            else:
                st.title("No uploaded files!")
        else:
            st.warning(f"Incorrect email!. {email_address_status}")


submit_button = st.button("Submit", key='submit', on_click=main)

