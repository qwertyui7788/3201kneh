import streamlit as st
import random

# ==========================================
# Streamlit 설정
# ==========================================

st.set_page_config(
    page_title="⚔️ 미니 RPG",
    page_icon="⚔️",
    layout="centered"
)


# ==========================================
# 게임 초기화
# ==========================================

def reset_game():

    st.session_state.hp = 100
    st.session_state.max_hp = 100

    st.session_state.attack = 20
    st.session_state.level = 1

    st.session_state.gold = 50
    st.session_state.potion = 3

    st.session_state.kill = 0
    st.session_state.combo = 0

    st.session_state.weapon_level = 1

    st.session_state.game_over = False

    spawn_monster()

    st.session_state.message = "⚔️ 모험이 시작되었습니다!"


# ==========================================
# 몬스터 생성
# ==========================================

def spawn_monster():

    monsters = [
        ("🟢 슬라임", 50, 8),
        ("👹 고블린", 70, 12),
        ("💀 해골 전사", 90, 15),
        ("🧙 다크 메이지", 110, 18),
        ("🐉 드래곤", 150, 22)
    ]

    name, hp, damage = random.choice(monsters)

    # 레벨에 따라 강해짐
    hp += st.session_state.level * 10
    damage += st.session_state.level * 2

    st.session_state.monster_name = name
    st.session_state.monster_hp = hp
    st.session_state.monster_max_hp = hp
    st.session_state.monster_damage = damage


# ==========================================
# 몬스터 공격
# ==========================================

def monster_attack():

    damage = random.randint(
        max(1, st.session_state.monster_damage - 5),
        st.session_state.monster_damage + 5
    )

    st.session_state.hp -= damage

    if st.session_state.hp <= 0:

        st.session_state.hp = 0
        st.session_state.game_over = True

        st.session_state.message = (
            "💀 몬스터의 공격을 받고 쓰러졌습니다!"
        )


# ==========================================
# 몬스터 처치
# ==========================================

def monster_defeated():

    reward = random.randint(15, 35)

    st.session_state.gold += reward
    st.session_state.kill += 1
    st.session_state.combo += 1

    # 레벨업
    old_level = st.session_state.level

    st.session_state.level = (
        st.session_state.kill // 3 + 1
    )

    # 레벨업 보너스
    if st.session_state.level > old_level:

        st.session_state.max_hp += 20
        st.session_state.attack += 5
        st.session_state.hp = st.session_state.max_hp

        level_message = (
            f" 🎉 LEVEL UP! Lv.{st.session_state.level}"
        )

    else:
        level_message = ""

    st.session_state.message = (
        f"🎉 {st.session_state.monster_name} 처치! "
        f"💰 +{reward} 골드!"
        f"{level_message}"
    )

    spawn_monster()


# ==========================================
# 일반 공격
# ==========================================

def attack():

    damage = random.randint(
        max(1, st.session_state.attack - 5),
        st.session_state.attack + 5
    )

    st.session_state.monster_hp -= damage

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

    else:

        st.session_state.combo = 0

        monster_attack()

        st.session_state.message = (
            f"⚔️ {damage}의 피해를 입혔습니다!"
        )


# ==========================================
# 강공격
# ==========================================

def strong_attack():

    # 60% 성공
    if random.random() <= 0.6:

        damage = random.randint(
            st.session_state.attack + 15,
            st.session_state.attack + 30
        )

        st.session_state.monster_hp -= damage

        if st.session_state.monster_hp <= 0:

            st.session_state.monster_hp = 0

            monster_defeated()

            st.session_state.message = (
                "💥 강공격으로 몬스터를 처치했습니다!"
            )

        else:

            st.session_state.combo = 0

            monster_attack()

            st.session_state.message = (
                f"💥 강공격 성공! {damage} 피해!"
            )

    else:

        st.session_state.combo = 0

        monster_attack()

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )


# ==========================================
# 회복
# ==========================================

def heal():

    heal_amount = random.randint(15, 30)

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + heal_amount
    )

    actual_heal = st.session_state.hp - old_hp

    monster_attack()

    st.session_state.message = (
        f"❤️ HP를 {actual_heal} 회복했습니다."
    )


# ==========================================
# 물약
# ==========================================

def use_potion():

    if st.session_state.potion <= 0:

        st.session_state.message = (
            "🧪 물약이 없습니다!"
        )

        return

    if st.session_state.hp >= st.session_state.max_hp:

        st.session_state.message = (
            "❤️ 이미 체력이 가득합니다!"
        )

        return

    st.session_state.potion -= 1

    heal_amount = 40

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + heal_amount
    )

    monster_attack()

    st.session_state.message = (
        "🧪 물약을 사용했습니다! HP +40"
    )


# ==========================================
# 무기 강화
# ==========================================

def upgrade_weapon():

    cost = st.session_state.weapon_level * 50

    if st.session_state.gold < cost:

        st.session_state.message = (
            f"💰 골드가 부족합니다! "
            f"필요 골드: {cost}"
        )

        return

    st.session_state.gold -= cost

    st.session_state.weapon_level += 1
    st.session_state.attack += 10

    st.session_state.message = (
        f"🗡️ 무기 강화 성공! "
        f"무기 Lv.{st.session_state.weapon_level}"
    )


# ==========================================
# 처음 실행
# ==========================================

if "hp" not in st.session_state:

    reset_game()


# ==========================================
# 화면
# ==========================================

st.title("⚔️ 미니 RPG")

st.write(
    "몬스터를 쓰러뜨리고 레벨을 올려 최강의 전사가 되어보세요!"
)


# ==========================================
# 플레이어 정보
# ==========================================

st.subheader("🧙 플레이어")

col1, col2, col3, col4 = st.columns(4)

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

with col4:

    st.metric(
        "🏆 처치",
        st.session_state.kill
    )


# HP 바
st.progress(
    st.session_state.hp /
    st.session_state.max_hp
)


st.divider()


# ==========================================
# 몬스터
# ==========================================

st.subheader(
    f"{st.session_state.monster_name}"
)

st.write(
    f"❤️ HP: "
    f"{st.session_state.monster_hp}/"
    f"{st.session_state.monster_max_hp}"
)

st.progress(
    max(
        0,
        st.session_state.monster_hp
    )
    /
    st.session_state.monster_max_hp
)

st.write(
    f"⚔️ 공격력: "
    f"{st.session_state.monster_damage}"
)


# ==========================================
# 메시지
# ==========================================

st.info(
    st.session_state.message
)


# ==========================================
# 전투
# ==========================================

if not st.session_state.game_over:

    st.subheader("⚔️ 전투")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⚔️ 일반 공격",
            use_container_width=True
        ):

            attack()
            st.rerun()

    with col2:

        if st.button(
            "💥 강공격 (60%)",
            use_container_width=True
        ):

            strong_attack()
            st.rerun()


    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "❤️ 회복",
            use_container_width=True
        ):

            heal()
            st.rerun()

    with col2:

        if st.button(
            "🧪 물약 사용",
            use_container_width=True
        ):

            use_potion()
            st.rerun()


# ==========================================
# 상점
# ==========================================

st.divider()

st.subheader("🛒 상점")

st.write(
    f"🧪 물약: {st.session_state.potion}개"
)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🧪 물약 구매 (20G)",
        use_container_width=True
    ):

        if st.session_state.gold >= 20:

            st.session_state.gold -= 20
            st.session_state.potion += 1

            st.session_state.message = (
                "🧪 물약을 구매했습니다!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


with col2:

    cost = st.session_state.weapon_level * 50

    if st.button(
        f"🗡️ 무기 강화 ({cost}G)",
        use_container_width=True
    ):

        upgrade_weapon()
        st.rerun()


st.write(
    f"🗡️ 무기 레벨: "
    f"{st.session_state.weapon_level}"
)

st.write(
    f"⚔️ 현재 공격력: "
    f"{st.session_state.attack}"
)


# ==========================================
# 콤보
# ==========================================

if st.session_state.combo > 0:

    st.success(
        f"🔥 연속 처치 {st.session_state.combo}회!"
    )


# ==========================================
# 게임 오버
# ==========================================

if st.session_state.game_over:

    st.error("💀 GAME OVER")

    st.write(
        f"🏆 최종 처치 수: "
        f"{st.session_state.kill}"
    )

    st.write(
        f"⭐ 최종 레벨: "
        f"{st.session_state.level}"
    )

    if st.button(
        "🔄 다시 시작",
        use_container_width=True
    ):

        reset_game()
        st.rerun()
