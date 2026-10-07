import streamlit as st
import random

# -------------------------
# Streamlit 설정
# -------------------------
st.set_page_config(
    page_title="미니 RPG",
    page_icon="⚔️",
    layout="centered"
)

# -------------------------
# 게임 초기화
# -------------------------
def reset_game():
    st.session_state.hp = 100
    st.session_state.max_hp = 100
    st.session_state.monster_hp = 50
    st.session_state.max_monster_hp = 50
    st.session_state.level = 1
    st.session_state.gold = 0
    st.session_state.game_over = False
    st.session_state.message = "⚔️ 슬라임이 나타났습니다!"


if "hp" not in st.session_state:
    reset_game()


# -------------------------
# 공격
# -------------------------
def attack():
    damage = random.randint(10, 20)
    st.session_state.monster_hp -= damage

    if st.session_state.monster_hp <= 0:
        st.session_state.monster_hp = 0

        gold = random.randint(10, 20)

        st.session_state.gold += gold
        st.session_state.level += 1

        # 레벨업
        st.session_state.max_hp += 10
        st.session_state.hp = st.session_state.max_hp

        # 새로운 몬스터
        st.session_state.max_monster_hp = (
            50 + st.session_state.level * 10
        )
        st.session_state.monster_hp = (
            st.session_state.max_monster_hp
        )

        st.session_state.message = (
            f"🎉 몬스터 처치! "
            f"💰 {gold}골드 획득! "
            f"⭐ 레벨 {st.session_state.level}!"
        )

    else:
        monster_attack()

        st.session_state.message = (
            f"⚔️ {damage}의 피해를 입혔습니다!"
        )


# -------------------------
# 강공격
# -------------------------
def strong_attack():

    if random.random() < 0.6:

        damage = random.randint(20, 35)

        st.session_state.monster_hp -= damage

        if st.session_state.monster_hp <= 0:
            st.session_state.monster_hp = 0

            st.session_state.level += 1
            st.session_state.gold += 30
            st.session_state.max_hp += 10
            st.session_state.hp = st.session_state.max_hp

            st.session_state.max_monster_hp = (
                50 + st.session_state.level * 10
            )

            st.session_state.monster_hp = (
                st.session_state.max_monster_hp
            )

            st.session_state.message = (
                "💥 강공격으로 몬스터를 처치했습니다! "
                "💰 30골드 획득!"
            )

        else:
            monster_attack()

            st.session_state.message = (
                f"💥 강공격 성공! {damage} 피해!"
            )

    else:
        monster_attack()

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )


# -------------------------
# 회복
# -------------------------
def heal():

    amount = random.randint(10, 25)

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + amount
    )

    actual = st.session_state.hp - old_hp

    monster_attack()

    st.session_state.message = (
        f"❤️ 체력을 {actual} 회복했습니다."
    )


# -------------------------
# 몬스터 공격
# -------------------------
def monster_attack():

    damage = random.randint(5, 15)

    st.session_state.hp -= damage

    if st.session_state.hp <= 0:
        st.session_state.hp = 0
        st.session_state.game_over = True


# -------------------------
# 게임 화면
# -------------------------
st.title("⚔️ 미니 RPG")

st.write(
    "몬스터를 쓰러뜨리고 레벨을 올려보세요!"
)

st.divider()

# 플레이어 정보
st.subheader("🧙 플레이어")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "❤️ HP",
        f"{st.session_state.hp}/{st.session_state.max_hp}"
    )

with col2:
    st.metric(
        "⭐ LEVEL",
        st.session_state.level
    )

with col3:
    st.metric(
        "💰 GOLD",
        st.session_state.gold
    )

st.progress(
    st.session_state.hp / st.session_state.max_hp
)

st.divider()

# 몬스터
st.subheader("👾 몬스터")

st.write(
    f"HP: {st.session_state.monster_hp}/"
    f"{st.session_state.max_monster_hp}"
)

st.progress(
    st.session_state.monster_hp /
    st.session_state.max_monster_hp
)

st.divider()

# 메시지
st.info(st.session_state.message)


# -------------------------
# 전투 버튼
# -------------------------
if not st.session_state.game_over:

    st.subheader("행동")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "⚔️ 공격",
            use_container_width=True
        ):
            attack()
            st.rerun()

    with col2:
        if st.button(
            "💥 강공격",
            use_container_width=True
        ):
            strong_attack()
            st.rerun()

    with col3:
        if st.button(
            "❤️ 회복",
            use_container_width=True
        ):
            heal()
            st.rerun()


# -------------------------
# 게임 오버
# -------------------------
if st.session_state.game_over:

    st.error("💀 게임 오버!")

    if st.button(
        "🔄 다시 시작",
        use_container_width=True
    ):
        reset_game()
        st.rerun()
