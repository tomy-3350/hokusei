import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

from hokan import customer

# --- 認証情報読み込み ---
google_cloud_secret = st.secrets["google_cloud"]
service_account_info = {
    "type": google_cloud_secret["type"],
    "project_id": google_cloud_secret["project_id"],
    "private_key_id": google_cloud_secret["private_key_id"],
    "private_key": google_cloud_secret["private_key"],
    "client_email": google_cloud_secret["client_email"],
    "client_id": google_cloud_secret["client_id"],
    "auth_uri": google_cloud_secret["auth_uri"],
    "token_uri": google_cloud_secret["token_uri"],
    "auth_provider_x509_cert_url": google_cloud_secret["auth_provider_x509_cert_url"],
    "client_x509_cert_url": google_cloud_secret["client_x509_cert_url"],
    "universe_domain": google_cloud_secret["universe_domain"]
}

# ✅ キャッシュ付きシート取得関数
@st.cache_resource
def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        service_account_info,
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    gc = gspread.authorize(creds)
    return gc.open("memo_kyouyuu").sheet1

sheet = get_sheet()

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

name = st.text_input("入力してください")
