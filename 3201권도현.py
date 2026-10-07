import streamlit as st

st.set_page_config(
    page_title="3201 RPG",
    page_icon="⚔️"
)

st.title("⚔️ 3201 RPG")
st.success("Streamlit 정상 실행!")

st.write("게임을 불러오는 중...")

if "hp" not in st.session_state:
    st.session_state.hp = 150

if "gold" not in st.session_state:
    st.session_state.gold = 300

st.write(f"❤️ HP: {st.session_state.hp}")
st.write(f"💰 Gold: {st.session_state.gold}")

if st.button("테스트 공격"):
    st.session_state.hp -= 10
    st.rerun()

if st.button("🔄 재시작"):
    st.session_state.hp = 150
    st.session_state.gold = 300
    st.rerun()
