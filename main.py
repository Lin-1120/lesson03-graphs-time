import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 열 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.stop()


# --------------------------------------------------
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# --------------------------------------------------
st.header("1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique().tolist())

if movie_list:
    selected_movie = st.selectbox(
        "영화를 선택하세요.",
        movie_list
    )

    movie_df = df[df["영화명"] == selected_movie].copy()
    movie_df = movie_df.sort_values("날짜")

    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수"
        },
        title=f"「{selected_movie}」의 날짜별 일관객 변화"
    )

    fig.update_traces(
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**이 그래프로 알 수 있는 것:** "
        "영화의 일관객 수가 날짜에 따라 어떻게 증가하거나 감소했는지 알 수 있습니다."
    )

else:
    st.warning("영화 데이터를 찾을 수 없습니다.")


# --------------------------------------------------
# 앞으로 추가할 그래프 영역
# --------------------------------------------------
st.divider()

st.header("2. 다음 그래프")
st.info("앞으로 새로운 시간 관련 그래프가 이곳에 추가됩니다.")


st.divider()

st.header("3. 다음 그래프")
st.info("앞으로 새로운 시간 관련 그래프가 이곳에 추가됩니다.")
