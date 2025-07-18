import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit SecretsからTOML形式で情報を取得
google_cloud_secret = st.secrets["google_cloud"]

# Secretsから必要な情報を構築
service_account_info = {
    "type": google_cloud_secret["type"],
    "project_id": google_cloud_secret["project_id"],
    "private_key_id": google_cloud_secret["private_key_id"],
    "private_key": google_cloud_secret["private_key"],  # 改行が含まれる
    "client_email": google_cloud_secret["client_email"],
    "client_id": google_cloud_secret["client_id"],
    "auth_uri": google_cloud_secret["auth_uri"],
    "token_uri": google_cloud_secret["token_uri"],
    "auth_provider_x509_cert_url": google_cloud_secret["auth_provider_x509_cert_url"],
    "client_x509_cert_url": google_cloud_secret["client_x509_cert_url"],
    "universe_domain": google_cloud_secret["universe_domain"]
}

# サービスアカウント認証情報を`ServiceAccountCredentials`に渡す
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info,
    ["https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"])

# gspreadを使ってGoogle Sheets APIに認証
gc = gspread.authorize(creds)

# タイトル
st.title('北青 機械課 作業日報')
st.caption("メーカー名、工番、作業内容、時間を入力してください。")
day = st.date_input("日付を選択してください")

# 名前
name = st.selectbox(
    '名前',
    ('選択してください', '大地', '山岸', '坂本', '一條', '松本', '将', '出繩'))


# メーカーとその他関連入力フィールドを作成する
def create_input_fields(index):
    customer = st.selectbox(
        f'メーカー{index}',
        ('選択してください', 'ジーテクト', 'ヨロズ', '城山', 'タチバナ', '浜岳', '三池', '東プレ', '千代田', '武部',
         'インフェック', 'その他')
    )

    new_customer = ''
    if customer == 'その他':
        new_customer = st.text_input(f'メーカー名を入力{index}')

    genre = st.selectbox(f'作業内容{index}', ('選択してください', '新規', '改修',
                                              'その他')) if customer != '選択してください' else '選択してください'
    number = st.text_input(f'工番を入力{index}') if genre != '選択してください' else ''
    # 時間入力を小数点形式で設定
    time = st.number_input(f'時間を入力{index}', min_value=0.0, step=0.25, format="%.2f") if number != '' else 0.0

    return customer, new_customer, genre, number, time


# 各メーカーの入力フィールドを表示
inputs = []
for i in range(1, 6):
    customer, new_customer, genre, number, time = create_input_fields(i)
    inputs.append((customer, new_customer, genre, number, time))

# 合計時間
total_time = sum([time for _, _, _, _, time in inputs])

# 合計時間を表示
if total_time != 0:
    st.text(f'合計: {total_time:.2f} 時間')

# シートを開く
sheet = gc.open("python").sheet1

# 送信ボタン
submit_btn = st.button('送信')

if submit_btn:
    st.text('お疲れ様でした！')

    # 入力内容を一つのリストにまとめる
    row_data = [str(day) + name]

    for customer, new_customer, genre, number, time in inputs:
        if customer != '選択してください':
            row_data.extend([new_customer if customer == 'その他' else customer, genre, number, time])

    # 送信
    sheet.append_row(row_data)