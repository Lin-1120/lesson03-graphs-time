
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
except Exception:
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
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                      "일관객: %{y:,}명<extra></extra>"
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
# 그래프 2. 기간 전체 일관객 합계 상위 5편 비교
# --------------------------------------------------
st.divider()
st.header("2. 일관객 합계가 가장 큰 영화 5편")

top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

top5_movie_names = top5_movies["영화명"].tolist()

top5_df = df[df["영화명"].isin(top5_movie_names)].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    title="기간 전체 일관객 합계 상위 5편의 날짜별 일관객 변화"
)

fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "영화: %{fullData.name}<br>"
                  "일관객: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "이 기간 동안 일관객 합계가 가장 컸던 5편의 흥행 추이를 날짜별로 비교할 수 있습니다."
)


# --------------------------------------------------
# 그래프 3. 날짜별 10위권 일관객 합계
# --------------------------------------------------
st.divider()
st.header("3. 날짜별 10위권 일관객 합계")

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    },
    title="날짜별 박스오피스 10위권 일관객 합계"
)

fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "10위권 일관객 합계: %{y:,}명<extra></extra>"
)

annotations = []

for _, row in top3_days.iterrows():
    annotations.append(
        dict(
            x=row["날짜"],
            y=row["일관객"],
            text=(
                f"{row['날짜'].strftime('%Y-%m-%d')}"
                f"<br>{row['일관객']:,}명"
            ),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-50,
            font=dict(size=12),
            bgcolor="white",
            bordercolor="gray",
            borderwidth=1,
            borderpad=4
        )
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    annotations=annotations
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "날짜에 따라 박스오피스 10위권 전체의 관객 규모가 어떻게 변했는지 알 수 있습니다."
)


# --------------------------------------------------
# 그래프 4. 영화별 기간 전체 일관객 TOP 10
# --------------------------------------------------
st.divider()
st.header("4. 영화별 기간 전체 일관객 TOP 10")

movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        기록일수=("날짜", "nunique")
    )
    .reset_index()
)

top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)

top10_movies = top10_movies.sort_values("일관객합계", ascending=True)

fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    labels={
        "일관객합계": "기간 전체 일관객",
        "영화명": "영화"
    },
    title="기간 전체 일관객 TOP 10",
    custom_data=["기록일수"]
)

fig4.update_traces(
    hovertemplate="<b>%{y}</b><br>"
                  "기간 전체 일관객: %{x:,}명<br>"
                  "10위권에 든 날수: %{customdata[0]}일"
                  "<extra></extra>"
)

fig4.update_layout(
    xaxis_title="기간 전체 일관객 수(명)",
    yaxis_title="영화",
    yaxis=dict(
        categoryorder="array",
        categoryarray=top10_movies["영화명"].tolist()
    )
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "이 기간 동안 10위권에 등장한 영화 중 전체 일관객이 많았던 영화와 10위권에 머문 날수를 함께 비교할 수 있습니다."
)


# --------------------------------------------------
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# --------------------------------------------------
st.divider()
st.header("5. 월 × 요일별 일관객 합계")

# 요일 이름
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일번호"] = heatmap_df["날짜"].dt.weekday
heatmap_df["요일"] = heatmap_df["요일번호"].map(
    dict(enumerate(weekday_names))
)

# 월 × 요일별 일관객 합계
monthly_weekday = (
    heatmap_df
    .groupby(["월", "요일번호", "요일"], as_index=False)["일관객"]
    .sum()
)

# 월 × 요일 형태로 변환
heatmap_pivot = (
    monthly_weekday
    .pivot(
        index="월",
        columns="요일번호",
        values="일관객"
    )
)

# 월요일 → 일요일 순서로 정렬
heatmap_pivot = heatmap_pivot.reindex(
    columns=range(7)
)

# 숫자 요일을 한글 요일로 변경
heatmap_pivot.columns = weekday_names

# 히트맵용 데이터프레임
heatmap_plot_df = heatmap_pivot.reset_index()

# Plotly용 긴 형태로 변환
heatmap_long = heatmap_plot_df.melt(
    id_vars="월",
    value_vars=weekday_names,
    var_name="요일",
    value_name="일관객"
)

fig5 = px.density_heatmap(
    heatmap_long,
    x="요일",
    y="월",
    z="일관객",
    category_orders={
        "요일": weekday_names,
        "월": list(range(1, 13))
    },
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일관객 합계"
    },
    title="월 × 요일별 박스오피스 10위권 일관객 합계",
    text_auto=".2s"
)

fig5.update_traces(
    hovertemplate="월: %{y}월<br>"
                  "요일: %{x}<br>"
                  "일관객 합계: %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    yaxis=dict(
        autorange="reversed"
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "어떤 월과 요일에 박스오피스 10위권의 일관객이 많이 모였는지 한눈에 비교할 수 있습니다."
)


# --------------------------------------------------
# 앞으로 추가할 그래프 영역
# --------------------------------------------------
st.divider()

st.header("6. 다음 그래프")
st.info("앞으로 새로운 시간 관련 그래프가 이곳에 추가됩니다.")


st.divider()

st.header("7. 다음 그래프")
st.info("앞으로 새로운 시간 관련 그래프가 이곳에 추가됩니다.")
