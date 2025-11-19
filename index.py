import streamlit as st
import pandas as pd
import altair as alt

st.title("Streamlit 기본 실습")

# Task 1
st.subheader("Task 1: 기본 UI 컴포넌트")

# 입력 받을 텍스트(이름)
st.text_input("이름을 입력하세요")
# 나이 슬라이더
age = st.slider("나이", min_value=0, max_value=100)

# 좋아하는 색
color = st.selectbox("좋아하는 색", ["빨강", "초록", "파랑"])

# 체크박스
agree = st.checkbox("이용 약관에 동의합니다")

# 버튼
st.button("제출")

# Task2
st.header("Task 2: 데이터 표시하기")
st.write("데이터프레임")

df= pd.read_csv("penguins.csv", encoding="utf-8")
st.dataframe(df)

# Task 3
st.header("Task 3: 차트 그리기")
df= pd.read_csv("penguins.csv")
all_cols= df.columns.tolist()

st.markdown("""
    <style>
    h1, h2, h3, h4, h5, h6 {
        font-weight: 400 !important;  /* 일반 두께 */
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("###### 📍모든 컬럼 목록")
st.markdown("\n".join([f"- **{col}**" for col in all_cols]))

selected_col= st.selectbox("그래프로 볼 컬럼을 선택하세요: ", all_cols)
st.markdown(f"###### > 선택된 칼럼: {selected_col}")

if pd.api.types.is_numeric_dtype(df[selected_col]):
    st.subheader("[선 그래프]")
    st.line_chart(df[selected_col])

    st.subheader("[막대 그래프]")
    st.bar_chart(df[selected_col])

    st.subheader("[영역 그래프]")
    st.area_chart(df[selected_col])

else:
    counts= df[selected_col].value_counts()

    st.subheader("[범주형 막대 그래프]")
    st.bar_chart(counts)

# Task 4
st.write("Task 4: 인터랙티브 필터")
# AI 활용

#st.title("🐧 Penguin Dataset Interactive Filter & Visualization (Altair Only)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, na_values=["NA", ".", ""])

    st.subheader("📌 원본 데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("🎛️ 인터랙티브 필터")

    filtered_df = df.copy()

    # 1) species
    if "species" in df.columns:
        species_opt = sorted(df["species"].dropna().unique())
        species_sel = st.multiselect("Species 선택", species_opt, default=species_opt)
        filtered_df = filtered_df[filtered_df["species"].isin(species_sel)]

    # 2) island
    if "island" in df.columns:
        island_opt = sorted(df["island"].dropna().unique())
        island_sel = st.multiselect("Island 선택", island_opt, default=island_opt)
        filtered_df = filtered_df[filtered_df["island"].isin(island_sel)]

    # 3) bill_length_mm
    if "bill_length_mm" in df.columns:
        if df["bill_length_mm"].dropna().shape[0] > 0:
            mn, mx = df["bill_length_mm"].min(), df["bill_length_mm"].max()
            val = st.slider("Bill Length (mm)", float(mn), float(mx), (float(mn), float(mx)))
            filtered_df = filtered_df[filtered_df["bill_length_mm"].between(val[0], val[1])]

    # 4) bill_depth_mm
    if "bill_depth_mm" in df.columns:
        if df["bill_depth_mm"].dropna().shape[0] > 0:
            mn, mx = df["bill_depth_mm"].min(), df["bill_depth_mm"].max()
            val = st.slider("Bill Depth (mm)", float(mn), float(mx), (float(mn), float(mx)))
            filtered_df = filtered_df[filtered_df["bill_depth_mm"].between(val[0], val[1])]

    # 5) flipper_length_mm
    if "flipper_length_mm" in df.columns:
        if df["flipper_length_mm"].dropna().shape[0] > 0:
            mn, mx = df["flipper_length_mm"].min(), df["flipper_length_mm"].max()
            val = st.slider("Flipper Length (mm)", int(mn), int(mx), (int(mn), int(mx)))
            filtered_df = filtered_df[filtered_df["flipper_length_mm"].between(val[0], val[1])]

    # 6) body_mass_g
    if "body_mass_g" in df.columns:
        if df["body_mass_g"].dropna().shape[0] > 0:
            mn, mx = df["body_mass_g"].min(), df["body_mass_g"].max()
            val = st.slider("Body Mass (g)", int(mn), int(mx), (int(mn), int(mx)))
            filtered_df = filtered_df[filtered_df["body_mass_g"].between(val[0], val[1])]

    # 7) sex
    if "sex" in df.columns:
        sex_opt = sorted(df["sex"].dropna().unique())
        sex_sel = st.multiselect("Sex 선택", sex_opt, default=sex_opt)
        filtered_df = filtered_df[filtered_df["sex"].isin(sex_sel)]

    st.subheader("📊 필터링된 데이터")
    st.dataframe(filtered_df)

    # 데이터가 없을 경우
    if filtered_df.empty:
        st.warning("⚠️ 필터 결과 데이터가 없습니다. 필터 값을 조정하세요!")
        st.stop()

    # --- 컬럼 리스트 ---
    numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_cols = ["species", "island", "sex"]

    st.subheader("📈 시각화")

    chart_type = st.selectbox("시각화 유형 선택", ["Scatter Plot", "Histogram", "Box Plot"])

    # ===================== Scatter Plot =====================
    if chart_type == "Scatter Plot":
        if len(numeric_cols) < 2:
            st.error("Scatter Plot을 위해서는 숫자 컬럼이 2개 이상 필요합니다.")
        else:
            x = st.selectbox("X축 선택", numeric_cols, index=0)
            y = st.selectbox("Y축 선택", numeric_cols, index=1)
            color = st.selectbox("색 기반 그룹", categorical_cols)

            chart = (
                alt.Chart(filtered_df.dropna())
                .mark_circle(size=80)
                .encode(
                    x=x,
                    y=y,
                    color=color,
                    tooltip=list(filtered_df.columns)
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)

    # ===================== Histogram =====================
    elif chart_type == "Histogram":
        if len(numeric_cols) == 0:
            st.error("Histogram을 위한 숫자 컬럼이 필요합니다.")
        else:
            col = st.selectbox("컬럼 선택", numeric_cols)

            chart = (
                alt.Chart(filtered_df.dropna(subset=[col]))
                .mark_bar()
                .encode(
                    x=alt.X(col, bin=True),
                    y="count()"
                )
            )
            st.altair_chart(chart, use_container_width=True)

    # ===================== Box Plot =====================
    elif chart_type == "Box Plot":
        if len(numeric_cols) == 0:
            st.error("Box Plot을 위한 숫자 컬럼이 필요합니다.")
        else:
            y = st.selectbox("Y축 선택", numeric_cols)
            x = st.selectbox("그룹 선택", categorical_cols)

            chart = (
                alt.Chart(filtered_df.dropna(subset=[y, x]))
                .mark_boxplot()
                .encode(
                    x=x,
                    y=y,
                    color=x
                )
            )
            st.altair_chart(chart, use_container_width=True)



# Task 5
st.title('Task5: 파일 업로드')

uploaded_file = st.file_uploader("Upload Your data", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.write("Uploaded Data")
    st.write(df)

