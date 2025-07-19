import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Streamlit secrets から認証情報を取得
service_account_info = st.secrets["google_cloud"]

# 認証オブジェクトを作成
creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
    )

#  gspread クライアント作成
client = gspread.authorize(creds)

# スプレッドシートを開く（名前）
#sheet = client.open("memo_kyouyuu").sheet1

# スプレッドシートを開く（id）
sheet = client.open_by_key("1owRvyJDQj2Na_4ENEyJ7gooabtTzUM2GjqBcw-_HoqM").sheet1


############################################
day1 = str()
name = "入力してください"
m_name = "入力してください"
number = "入力してください"
day2 = str()
memo = "入力してください"

############################################
st.title("金型メモ共有アプリ")
st.text("型の改修内容や期限、出荷、トライ日程などメモ帳として使用してください")
st.text("記入日、記入者名、メーカー、工番等、期限や日程、内容の順に入力してください")
st.text("共有シートを開き、完了したものや取り消したいものはチェックをつけると取り消し線が入ります")

day1 = st.date_input("記入日を選択してください")

name = st.text_input(
    "記入者名",placeholder="入力してください")

m_name = st.text_input(
    "メーカー",placeholder="入力してください")

number = st.text_input(
    "工番等",placeholder="入力してください")

day2 = st.date_input("日付を選択してください")

memo = st.text_input(
    "内容",placeholder="入力してください")

############ 送信ボタン################
submit_btn = st.button('送信')

if submit_btn:
    try:
        response = sheet.append_row([str(day1), name, m_name, number, str(day2), memo])
        st.success("送信完了！")
        st.write("書き込み成功:", response)
    except Exception as e:
        st.error(f"スプレッドシートへの書き込みに失敗しました: {e}")
