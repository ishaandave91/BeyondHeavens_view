import streamlit as st
import base64
from mysql.connector import Error


class Video:
    def __init__(self, fetched_records):
        self.fetched_records = fetched_records
        self.watch_btn_key = ''
        self.watch_button_clicked = False
        self.filename = ""
        self.content = ""
        self.video_frame = ""
        self.close_btn_key = ""
        self.close_button_clicked = False
        self.file_id = -1

    def render_video(self):
        for self.file_id, self.filename, self.content, receiveremailid, senddate in self.fetched_records:
            try:
                button_name = self.filename
                col3, col4 = st.columns(2)
                with col3:
                    self.watch_btn_key = f'watch_btn_{self.file_id}'
                    self.watch_button_clicked = st.button(f"Watch: {button_name}", use_container_width=True,
                                                          key=self.watch_btn_key, on_click=self.watch_video)
                with col4:
                    st.write("**Recipient:** ", receiveremailid)
                    st.write("**Scheduled send date & time:** ", senddate)

                st.write("<hr>", unsafe_allow_html=True)

                # if self.watch_button_clicked:

            except Exception as e:
                st.error(f"Error encoding video content: {e}")
                return None

    def watch_video(self):
        st.write(self.watch_btn_key)
        # which btn key, parse content here and extract that content
        for item in st.session_state:
            if st.session_state[item]:
                try:
                    if str(item).__contains__("watch_btn_"):
                        playback_file_id = item.split("watch_btn_")[1]
                        for file_id, filename, content, receiveremailid, senddate in self.fetched_records:
                            if str(file_id) == playback_file_id:
                                video_content = content
                                decoded_content = base64.b64decode(video_content)
                                self.video_frame = st.video(decoded_content, format="video/mp4", start_time=0)
                                self.close_btn_key = f'close_vid_{playback_file_id}'
                                self.close_button_clicked = st.button("Close", use_container_width=True,
                                                                      key=self.close_btn_key, on_click=self.close_vid)
                except Error:
                    pass

    def close_vid(self):
        self.video_frame = ""
        del self.close_button_clicked
        del self.video_frame
