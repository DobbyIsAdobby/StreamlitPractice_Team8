### AI 활용 문답
## Track4

# 질문:
csv 파일을 업로드하는 Streamlit 인터랙티브필터- 데이터필터링 코드를 만들어줘

# 답변:
아래는 CSV 파일 업로드 → 인터랙티브 필터 → 필터링된 데이터 출력
기능만 포함된 가장 깔끔하고 단순한 Streamlit 데이터 필터링 코드입니다.

✅ Streamlit 인터랙티브 데이터 필터링 (파일 업로드 버전)

👉 필터만 포함, 시각화 없음 / 원하는 경우 시각화도 추가해드림

import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Interactive Filter", layout="wide")

st.title("📄 CSV 파일 기반 인터랙티브 데이터 필터링")

# ============================================
# 1) CSV 파일 업로드
# ============================================
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, na_values=["NA", ".", "", " "])

    st.subheader("📌 원본 데이터 미리보기")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("🎛 인터랙티브 필터")
    filtered_df = df.copy()

    # ============================================
    # 2) 범주형 컬럼 자동 필터
    # ============================================
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    st.markdown("### 🔵 범주형 필터")

    for col in categorical_cols:
        unique_vals = sorted(df[col].dropna().unique())
        selected = st.multiselect(f"{col} 선택", unique_vals, default=unique_vals)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

    # ============================================
    # 3) 숫자형 컬럼 자동 범위 필터
    # ============================================
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    st.markdown("### 🔴 수치형 필터")

    for col in numeric_cols:
        non_na = df[col].dropna()
        if len(non_na) > 0:
            min_val = float(non_na.min())
            max_val = float(non_na.max())
            step = 1 if df[col].dtype == "int64" else 0.1

            range_vals = st.slider(
                f"{col} 범위 선택",
                min_val, max_val,
                (min_val, max_val),
                step=step
            )
            filtered_df = filtered_df[filtered_df[col].between(range_vals[0], range_vals[1])]

    # ============================================
    # 4) 필터링 결과 출력
    # ============================================
    st.subheader("📊 필터링된 데이터")
    st.write(f"총 **{len(filtered_df)} 행**이 남았습니다.")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")

📌 이 코드가 제공하는 기능

✔ CSV 업로드
✔ object 타입 → 멀티 셀렉트 필터 자동 생성
✔ numeric 타입 → 범위 슬라이더 자동 생성
✔ 필터링된 데이터 실시간 업데이트
✔ 시각화 없음(원하면 추가 가능)

❓ 시각화 기능(Altair / Plotly)도 추가해드릴까요?

예: Scatter Plot, Histogram, Box Plot 등 가능!

# 질문:
penguins.csv
위 csv 파일에 맞는 Streamlit 인터랙티브필터- 데이터필터링 코드와 시각화를 만들어줘

# 답변:
아래는 당신이 제공한 펭귄 데이터(csv) 구조에 정확히 맞추어 만든
✔ CSV 업로드 기반 인터랙티브 필터
✔ 범주형/수치형 자동 필터링
✔ 시각화(산점도, 히트맵, 히스토그램)
모두 포함된 완성형 Streamlit 애플리케이션 코드입니다.

✅ 📌 Streamlit 인터랙티브 데이터필터 + 시각화 (완성 코드)
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Penguin Data Explorer", layout="wide")

st.title("🐧 Penguin Dataset Interactive Explorer")

# --------------------------------------------------------
# 1. CSV 파일 업로드
# --------------------------------------------------------
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, na_values=["NA", ".", "", " "])

    st.subheader("📌 원본 데이터 미리보기")
    st.dataframe(df.head(), use_container_width=True)

    # --------------------------------------------------------
    # 2. 인터랙티브 필터 UI
    # --------------------------------------------------------
    st.sidebar.header("🎛 데이터 필터")

    filtered_df = df.copy()

    # ----- 범주형 필터 -----
    categorical_cols = ["species", "island", "sex"]

    for col in categorical_cols:
        unique_vals = sorted(filtered_df[col].dropna().unique())
        selected = st.sidebar.multiselect(f"{col}", unique_vals, default=unique_vals)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

    # ----- 수치형 필터 -----
    numeric_cols = ["bill_length_mm", "bill_depth_mm",
                    "flipper_length_mm", "body_mass_g"]

    for col in numeric_cols:
        non_na = df[col].dropna()
        if len(non_na) > 0:
            min_val = float(non_na.min())
            max_val = float(non_na.max())
            range_vals = st.sidebar.slider(
                f"{col} 범위",
                min_val,
                max_val,
                (min_val, max_val)
            )
            filtered_df = filtered_df[
                filtered_df[col].between(range_vals[0], range_vals[1])
            ]

    # --------------------------------------------------------
    # 3. 필터링된 데이터 출력
    # --------------------------------------------------------
    st.subheader("📊 필터링된 데이터")
    st.write(f"총 **{len(filtered_df)} 행**이 남았습니다.")
    st.dataframe(filtered_df, use_container_width=True)

    # --------------------------------------------------------
    # 4. 시각화
    # --------------------------------------------------------
    st.header("📈 시각화")

    # -------------------------
    # (1) 산점도 scatter plot
    # -------------------------
    st.subheader("🟢 Bill Length vs. Bill Depth (by Species)")

    scatter = (
        alt.Chart(filtered_df)
        .mark_circle(size=70)
        .encode(
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            tooltip=list(filtered_df.columns),
        )
        .interactive()
    )
    st.altair_chart(scatter, use_container_width=True)

    # -------------------------
    # (2) flipper_length 히스토그램
    # -------------------------
    st.subheader("🔵 Flipper Length Histogram")

    hist = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            alt.X("flipper_length_mm:Q", bin=True),
            y="count()",
            color="species",
        )
    )
    st.altair_chart(hist, use_container_width=True)

    # -------------------------
    # (3) species 별 평균 body mass bar plot
    # -------------------------
    st.subheader("🟣 Species 별 평균 체중 (Body Mass g)")

    avg_mass = (
        filtered_df.groupby("species")["body_mass_g"]
        .mean()
        .reset_index()
        .dropna()
    )

    bar = (
        alt.Chart(avg_mass)
        .mark_bar()
        .encode(
            x="species:N",
            y="body_mass_g:Q",
            color="species:N",
            tooltip=["species", "body_mass_g"],
        )
    )
    st.altair_chart(bar, use_container_width=True)

else:
    st.info("CSV 파일을 업로드해주세요.")

✅ 이 코드로 가능한 기능들
🎛 인터랙티브 필터
species (Adelie / Chinstrap / Gentoo)
island (Biscoe / Dream / Torgersen)
sex (MALE / FEMALE / NA 제거 가능)
bill_length, bill_depth, flipper_length, body_mass 슬라이더 자동 생성

📈 시각화 제공
산점도
bill_length_mm vs bill_depth_mm
색상 = species
마우스 hover tooltip
히스토그램
flipper_length_mm 분포
종별 색 구분
막대그래프
species별 평균 body mass

✨ 원하시면 추가해드릴 기능
KDE density plot
island별 개체수 비교
scatter matrix
correlation heatmap
box plot (성별/종 비교)
Plotly version 시각화

말해주시면 바로 추가해 드릴게요!