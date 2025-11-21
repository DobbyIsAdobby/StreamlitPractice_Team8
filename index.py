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
st.subheader("Task 2: 데이터 표시하기")
st.write("데이터프레임")

df= pd.read_csv("penguins.csv", encoding="utf-8")
st.dataframe(df)

# Task 3
st.subheader("Task 3: 차트 그리기")
df= pd.read_csv("penguins.csv")
all_cols= df.columns.tolist()

st.markdown("""
    <style>
    h1, h2, h3, h4, h5, h6 {
        font-weight: 400 !important;  /* 일반 두께 */
    }
    </style>
""", unsafe_allow_html=True)
with st.expander("###### 📍모든 컬럼 목록"):
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
st.subheader("Task 4: 인터랙티브 필터")
# AI 활용

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
st.subheader('Task5: 파일 업로드')

uploaded_file = st.file_uploader("Upload Your data", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.write("Uploaded Data")
    st.write(df)

# Task 6 - AI 활용
st.subheader("Task 6: 레이아웃 구성 (Layout)")

# 1. Expander (접고 펼치기)
with st.expander("Task 6 설명 보기 (클릭하세요)"):
    st.write("""
    이 영역은 **Expander**입니다. 
    공간을 절약하거나 부가적인 설명을 숨겨둘 때 유용합니다.
    - **Columns**: 화면을 세로로 분할합니다.
    - **Tabs**: 탭을 사용하여 내용을 구분합니다.
    """)

# 데이터가 있는지 확인 (Task 5나 Task 2에서 df가 로드되었을 것임)
if 'df' in locals() and not df.empty:
    
    # 2. Tabs (탭 구성)
    tab1, tab2, tab3 = st.tabs(["📊 요약 지표 (Columns)", "📋 데이터 미리보기", "📝 텍스트 분석"])

    # Tab 1: 요약 지표 (Columns 사용)
    with tab1:
        st.subheader("주요 수치 요약")
        
        # 숫자형 데이터만 선택해서 평균 계산 (에러 방지)
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        
        if not numeric_df.empty:
            # 3. Columns (화면 분할) - 3개의 컬럼으로 나눔
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # 첫 번째 컬럼: 첫 번째 숫자형 컬럼의 평균
                col_name = numeric_df.columns[0]
                avg_val = numeric_df[col_name].mean()
                st.metric(label=f"평균 {col_name}", value=f"{avg_val:.2f}")

            with col2:
                # 두 번째 컬럼 (데이터가 있다면)
                if len(numeric_df.columns) > 1:
                    col_name = numeric_df.columns[1]
                    avg_val = numeric_df[col_name].mean()
                    st.metric(label=f"평균 {col_name}", value=f"{avg_val:.2f}")

            with col3:
                # 세 번째 컬럼: 전체 데이터 개수
                st.metric(label="전체 데이터 수", value=f"{len(df)} 개")
        else:
            st.warning("요약할 숫자형 데이터가 없습니다.")

    # Tab 2: 데이터 미리보기
    with tab2:
        st.subheader("원본 데이터 (상위 5개)")
        st.dataframe(df.head())

    # Tab 3: 기타 텍스트
    with tab3:
        st.subheader("데이터 컬럼 정보")
        st.write(df.columns.tolist())

else:
    st.error("데이터가 로드되지 않았습니다. Task 5에서 파일을 업로드하거나 Task 2 코드를 확인하세요.")

# Task 7 - AI 활용
st.subheader("Task 7: 종합 대시보드 (Dashboard)")

# 데이터가 없는 경우를 대비해 다시 로드 (안전장치)
if 'df' not in locals():
    df = pd.read_csv("penguins.csv")

# 1. 사이드바 구성 (필터링 컨트롤)
st.sidebar.header("🔍 대시보드 필터 (Task 7)")

# 사이드바: 종(Species) 선택
species_list = df['species'].unique().tolist()
selected_species = st.sidebar.multiselect(
    "종을 선택하세요", 
    species_list, 
    default=species_list # 기본값: 전체 선택
)

# 사이드바: 섬(Island) 선택
island_list = df['island'].unique().tolist()
selected_island = st.sidebar.multiselect(
    "서식지(섬)를 선택하세요", 
    island_list, 
    default=island_list
)

# 2. 데이터 필터링 로직
filtered_dashboard_df = df[
    (df['species'].isin(selected_species)) & 
    (df['island'].isin(selected_island))
]

# 3. 메인 화면 구성
if filtered_dashboard_df.empty:
    st.warning("선택된 조건에 맞는 데이터가 없습니다.")
else:
    # (1) KPI 지표 (Metrics) - 3단 컬럼
    st.subheader("📊 핵심 지표")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric("검색된 펭귄 수", f"{len(filtered_dashboard_df)} 마리")
    
    with kpi2:
        avg_mass = filtered_dashboard_df['body_mass_g'].mean()
        st.metric("평균 몸무게", f"{avg_mass:.1f} g")
        
    with kpi3:
        avg_bill = filtered_dashboard_df['bill_length_mm'].mean()
        st.metric("평균 부리 길이", f"{avg_bill:.1f} mm")
    
    st.markdown("---") # 구분선

    # (2) 차트 영역 - 2단 컬럼
    st.subheader("📈 데이터 시각화")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.caption("종별 개체수 (Bar Chart)")
        # 종별 개수 계산
        species_counts = filtered_dashboard_df['species'].value_counts()
        st.bar_chart(species_counts)
        
    with chart_col2:
        st.caption("부리 길이 vs 깊이 (Scatter Plot)")
        # Altair를 이용한 산점도
        scatter_chart = alt.Chart(filtered_dashboard_df).mark_circle().encode(
            x='bill_length_mm',
            y='bill_depth_mm',
            color='species',
            tooltip=['species', 'island', 'bill_length_mm']
        ).interactive()
        st.altair_chart(scatter_chart, use_container_width=True)

    # (3) 상세 데이터 (Expander)
    with st.expander("📋 상세 데이터 보기 (클릭)"):
        st.dataframe(filtered_dashboard_df)