import streamlit as st
import random
import time

# -------------------------
# 기본 설정
# -------------------------
st.set_page_config(
    page_title="🐍 뱀 게임",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 뱀 게임")

# 게임판 크기
WIDTH = 15
HEIGHT = 15


# -------------------------
# 게임 초기화
# -------------------------
def init_game():
    st.session_state.snake = [(7, 7)]
    st.session_state.direction = (0, 1)
    st.session_state.food = create_food()
    st.session_state.score = 0
    st.session_state.game_over = False


# -------------------------
# 먹이 생성
# -------------------------
def create_food():
    while True:
        food = (
            random.randint(0, HEIGHT - 1),
            random.randint(0, WIDTH - 1)
        )

        if food not in st.session_state.snake:
            return food


# -------------------------
# 게임 시작
# -------------------------
if "snake" not in st.session_state:
    init_game()


# -------------------------
# 방향 버튼
# -------------------------
st.write("### 방향키")

col1, col2, col3 = st.columns(3)

with col2:
    if st.button("⬆️", use_container_width=True):
        if st.session_state.direction != (1, 0):
            st.session_state.direction = (-1, 0)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️", use_container_width=True):
        if st.session_state.direction != (0, 1):
            st.session_state.direction = (0, -1)

with col2:
    if st.button("⬇️", use_container_width=True):
        if st.session_state.direction != (-1, 0):
            st.session_state.direction = (1, 0)

with col3:
    if st.button("➡️", use_container_width=True):
        if st.session_state.direction != (0, -1):
            st.session_state.direction = (0, 1)


# -------------------------
# 게임 진행
# -------------------------
if not st.session_state.game_over:

    direction = st.session_state.direction
    head = st.session_state.snake[0]

    new_head = (
        head[0] + direction[0],
        head[1] + direction[1]
    )

    # 벽 충돌
    if (
        new_head[0] < 0
        or new_head[0] >= HEIGHT
        or new_head[1] < 0
        or new_head[1] >= WIDTH
    ):
        st.session_state.game_over = True

    # 자기 몸 충돌
    elif new_head in st.session_state.snake:
        st.session_state.game_over = True

    else:
        st.session_state.snake.insert(0, new_head)

        # 먹이를 먹었는지 확인
        if new_head == st.session_state.food:
            st.session_state.score += 1
            st.session_state.food = create_food()
        else:
            st.session_state.snake.pop()


# -------------------------
# 점수
# -------------------------
st.write(f"### 점수: {st.session_state.score}")


# -------------------------
# 게임판 출력
# -------------------------
board = ""

for y in range(HEIGHT):
    for x in range(WIDTH):

        position = (y, x)

        if position == st.session_state.snake[0]:
            board += "🟢"

        elif position in st.session_state.snake:
            board += "🟩"

        elif position == st.session_state.food:
            board += "🍎"

        else:
            board += "⬜"

    board += "\n"


st.code(board, language="text")


# -------------------------
# 게임 오버
# -------------------------
if st.session_state.game_over:
    st.error("💀 게임 오버!")

    if st.button("🔄 다시 시작", use_container_width=True):
        init_game()
        st.rerun()

else:
    # 자동으로 게임 진행
    time.sleep(0.25)
    st.rerun()
