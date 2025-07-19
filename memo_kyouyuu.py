import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

############################################
day1 = "日付を選択してください"
name = "入力してください"
m_name = "入力してください"
number = "入力してください"
day2 = "日付を選択してください"
memo = "入力してください"

############################################
st.title("金型メモ共有アプリ")
st.text("型の改修内容や期限、出荷、トライ日程などメモ帳として使用してください")
st.text("記入日、記入者名、メーカー、工番等、期限や日程、内容の順に入力してください")
st.text("共有シートを開き、完了したものや取り消したいものはチェックをつけると取り消し線が入ります")

day1 = st.date_input("日付を選択してください")

name = st.text_input(
    "記入者名",
    "入力してください")
