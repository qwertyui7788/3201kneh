import streamlit as st
import random

st.set_page_config(
    page_title="미니 RPG",
    page_icon="⚔️"
)

# -------------------------
# 게임 시작
# -------------------------
def start_game():
    st.session_state.player_hp = 100
    st.session_state.max_hp = 100
    st.session_state.attack = 20
    st.session_state.level = 1
    st.session_state.gold = 0

    st.session_state.monster = "슬라임"
    st.session_state.monster_hp = 50
    st.session_state.monster_max_hp = 50

    st.session_state.game_over = False
    st.session_state.log = ["⚔️ 모험이 시작되었습니다!"]


# 처음 실행
if "player_hp" not in st.session_state:
    start_game()


# -------------------------
# 새로운 몬스터
# -------------------------
def new_monster():
    monsters = [
        ("🟢 슬라임", 50),
        ("👹 고블린", 70),
        ("💀 해골", 90),
        ("🐲 드래곤", 120)
    ]

    name, hp = random.choice(monsters)

    # 레벨에 따라 체력 증가
    hp += (st.session_state.level - 1) * 10

    st.session_state.monster = name
    st.session_state.monster_hp = hp
    st.session_state.monster_max_hp = hp


# -------------------------
# 몬스터 공격
# -------------------------
def monster_attack():

    damage = random.randint(5, 15)

    st.session_state.player_hp -= damage

    st.session_state.log.insert(
        0,
        f"👹 {st.session_state.monster}이(가) "
        f"{damage}의 피해를 입혔습니다."
    )

    if st.session_state.player_hp <= 0:
        st.session_state.player_hp = 0
        st.session_state.game_over = True
        st.session_state.log.insert(
            0,
            "💀 당신은 쓰러졌습니다!"
        )


# -------------------------
# 일반 공격
# -------------------------
def normal_attack():

    damage = random.randint(
        st.session_state.attack - 5,
        st.session_state.attack + 5
    )

    st.session_state.monster_hp -= damage

    st.session_state.log.insert(
        0,
        f"⚔️ 공격! {damage}의 피해를 입혔습니다."
    )

    check_monster()


# -------------------------
# 강한 공격
# -------------------------
def strong_attack():

    if random.random() < 0.6:

        damage = random.randint(25, 40)

        st.session_state.monster_hp -= damage

        st.session_state.log.insert(
            0,
            f"💥 강공격 성공! {damage}의 피해!"
        )

        check_monster()

    else:

        st.session_state.log.insert(
            0,
            "💨 강공격이 빗나갔습니다!"
        )

        monster_attack()


# -------------------------
# 회복
# -------------------------
def heal():

    amount = random.randint(15, 30)

    old_hp = st.session_state.player_hp

    st.session_state.player_hp = min(
        st.session_state.max_hp,
        st.session_state.player_hp + amount
    )

    healed = st.session_state.player_hp - old_hp

    st.session_state.log.insert(
        0,
        f"❤️ 체력을 {healed} 회복했습니다."
    )

    monster_attack()


# -------------------------
# 몬스터 처치 확인
# -------------------------
def check_monster():

    if st.session_state.monster_hp <= 0:

        reward = random.randint(10, 30)

        st.session_state.gold += reward
        st.session_state.level += 1

        st.session_state.max_hp += 10
        st.session_state.attack += 3
        st.session_state.player_hp = st.session_state.max_hp

        st.session_state.log.insert(
            0,
            f"🎉 {st.session_state.monster} 처치!"
        )

        st.session_state.log.insert(
            0,
            f"💰 {reward} 골드를 얻었습니다!"
        )

        new_monster()

    else:
        monster_attack()


# -------------------------
# 화면
# -------------------------
st.title("⚔️ 미니 RPG")
st.write("몬스터를 쓰러뜨리고 계속해서 레벨을 올려보세요!")

st.divider()

# 플레이어
st.subheader("🧙 플레이어")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "❤️ 체력",
        f"{st.session_state.player_hp}/{st.session_state.max_hp}"
    )

with col2:
    st.metric(
        "⭐ 레벨",
        st.session_state.level
    )

with col3:
    st.metric(
        "💰 골드",
        st.session_state.gold
    )

st.progress(
    st.session_state.player_hp /
    st.session_state.max_hp
)

st.divider()

# 몬스터
st.subheader(st.session_state.monster)

st.write(
    f"❤️ 몬스터 체력: "
    f"{st.session_state.monster_hp}/"
    f"{st.session_state.monster_max_hp}"
)

st.progress(
    max(0, st.session_state.monster_hp) /
    st.session_state.monster_max_hp
)

st.divider()

# 행동
if not st.session_state.game_over:

    st.subheader("행동을 선택하세요!")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚔️ 공격", use_container_width=True):
            normal_attack()
            st.rerun()

    with col2:
        if st.button("💥 강공격", use_container_width=True):
            strong_attack()
            st.rerun()

    with col3:
        if st.button("❤️ 회복", use_container_width=True):
            heal()
            st.rerun()


# 전투 기록
st.subheader("📜 전투 기록")

for message in st.session_state.log[:10]:
    st.write(message)


# 게임 오버
if st.session_state.game_over:

    st.error("💀 GAME OVER")

    if st.button("🔄 다시 시작", use_container_width=True):
        start_game()
        st.rerun()
