!pip install pymannkendall
!pip install mplfinance
import pymannkendall as mk
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
df = yf.download("VCB.VN", start="2026-01-01", end="2026-06-27", progress=False)
df.columns = df.columns.droplevel('Ticker')
full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
df = df.reindex(full_date_range)
df = df.ffill()
df['simple_ret'] = df['Close'].pct_change()
df['log_ret'] = np.log(df['Close'] / df['Close'].shift(1))
fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
# Biểu đồ 1: Giá đóng cửa
ax[0].plot(df.index, df['Close'], color='red', label='GIÁ ĐÓNG CỬA')
ax[0].set_title('GIÁ ĐÓNG CỬA CỦA CỔ PHIẾU VCB')
ax[0].set_ylabel('VND')
ax[0].legend()
ax[0].grid(True)
# Biểu đồ 2: Log return
ax[1].plot(df.index, df['log_ret'], color='green', label='Log Return')
ax[1].set_title('VCB Log Return')
ax[1].set_ylabel('Log Return')
ax[1].set_xlabel('Date')
ax[1].legend()
ax[1].grid(True)
plt.tight_layout()
plt.show()
# Vẽ biểu đồ nến
mpf.plot(df, type="candle",
mav=[10, 20],
volume=True,
style="yahoo",
title="GIÁ CỔ PHIẾU VCB TỪ 1/1/2024 - 27/6/2026",
figsize=[10, 5])
#Lấy giá đóng cửa
close_prices = df["Close"].dropna().reset_index(drop=True)
#Thực hiện kiểm định Mann-Kendall
result = mk.original_test(close_prices)
# In kết quả
print("Trend:", result.trend)
print("p-value:", result.p)
print("Tau:", result.Tau)
print("Variance of S:", result.var_s)
# Diễn giải
if result.p < 0.05:
    print("==> Có xu hướng đáng kể về mặt thống kê.")
else:
    print("==> Không có xu hướng rõ ràng.")
  import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pymannkendall as mk
import matplotlib.pyplot as plt
import mplfinance as mpf

# =============================
# CẤU HÌNH TRANG
# =============================
st.set_page_config(
    page_title="Phân tích cổ phiếu bằng Mann-Kendall",
    page_icon="📈",
    layout="wide"
)

# =============================
# LOGO
# =============================
st.image("logo.jpg")

# =============================
# TIÊU ĐỀ
# =============================
st.title("📈 TRỰC QUAN HÓA GIÁ CỔ PHIẾU VÀ KIỂM ĐỊNH MANN-KENDALL")
st.subheader("TS. VŨ ĐỨC BÌNH")

st.markdown("---")

# =============================
# THÔNG TIN ĐẦU VÀO (DẠNG DỌC)
# =============================
st.header("📋 Thông tin đầu vào")

ticker = st.text_input(
    "Mã cổ phiếu",
    value="VCB.VN"
)

start_date = st.date_input(
    "Ngày bắt đầu",
    value=pd.to_datetime("2026-01-01")
)

end_date = st.date_input(
    "Ngày kết thúc",
    value=pd.to_datetime("2026-06-27")
)

run = st.button(
    "📈 Phân tích",
    use_container_width=True
)

# =============================
# CHẠY PHÂN TÍCH
# =============================
if run:

    with st.spinner("Đang tải dữ liệu..."):

        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

    if df.empty:
        st.error("Không tìm thấy dữ liệu.")
        st.stop()

    # =============================
    # XỬ LÝ DỮ LIỆU
    # =============================
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel("Ticker")

    full_date_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    df = df.reindex(full_date_range)

    df = df.ffill()

    df["simple_ret"] = df["Close"].pct_change()

    df["log_ret"] = np.log(
        df["Close"] / df["Close"].shift(1)
    )

    # =============================
    # HIỂN THỊ DỮ LIỆU
    # =============================
    st.subheader("📄 Dữ liệu")

    st.dataframe(df)

    # =============================
    # BIỂU ĐỒ GIÁ & LOG RETURN
    # =============================
    st.subheader("📈 Giá đóng cửa và Log Return")

    fig, ax = plt.subplots(
        2,
        1,
        figsize=(10, 8),
        sharex=True
    )

    ax[0].plot(
        df.index,
        df["Close"],
        color="red",
        linewidth=2,
        label="Close Price"
    )

    ax[0].set_title("Giá đóng cửa")
    ax[0].set_ylabel("VND")
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(
        df.index,
        df["log_ret"],
        color="green",
        linewidth=1.5,
        label="Log Return"
    )

    ax[1].set_title("Log Return")
    ax[1].set_ylabel("Return")
    ax[1].set_xlabel("Date")
    ax[1].legend()
