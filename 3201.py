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
# 일반 몬스터
# ==========================================

NORMAL_MONSTERS = [
    ("🟢 슬라임", 40, 7),
    ("🐀 거대 쥐", 45, 8),
    ("🦇 박쥐", 50, 9),
    ("👺 고블린", 65, 11),
    ("🐺 늑대", 70, 13),
    ("🕷️ 거대 거미", 80, 14),
    ("💀 해골 전사", 95, 16),
    ("👻 유령", 100, 18),
    ("🧟 좀비", 110, 19),
    ("🧙 다크 메이지", 120, 22),
]


# ==========================================
# 보스
# ==========================================

BOSSES = [
    ("👑 오크 대장", 250, 28),
    ("🔥 불의 마왕", 320, 32),
    ("❄️ 얼음 여왕", 350, 35),
    ("⚡ 번개의 군주", 380, 38),
    ("💀 죽음의 기사", 420, 42),
    ("🐲 고대 드래곤", 500, 50),
]


# ==========================================
# 몬스터 생성
# ==========================================

def spawn_monster():

    if st.session_state.kill > 0 and st.session_state.kill % 5 == 0:

        name, hp, damage = random.choice(BOSSES)

        hp += (st.session_state.level - 1) * 20
        damage += (st.session_state.level - 1) * 3

        st.session_state.monster_name = name
        st.session_state.monster_hp = hp
        st.session_state.monster_max_hp = hp
        st.session_state.monster_damage = damage
        st.session_state.is_boss = True

    else:

        name, hp, damage = random.choice(NORMAL_MONSTERS)

        hp += (st.session_state.level - 1) * 10
        damage += (st.session_state.level - 1) * 2

        st.session_state.monster_name = name
        st.session_state.monster_hp = hp
        st.session_state.monster_max_hp = hp
        st.session_state.monster_damage = damage
        st.session_state.is_boss = False


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
    st.session_state.boss_kill = 0
    st.session_state.combo = 0

    st.session_state.weapon_level = 1

    # 방어/회피 상태
    st.session_state.defending = False
    st.session_state.evading = False

    st.session_state.game_over = False
    st.session_state.is_boss = False

    st.session_state.message = (
        "⚔️ 새로운 모험이 시작되었습니다!"
    )

    spawn_monster()


# ==========================================
# 몬스터 공격
# ==========================================

def monster_attack():

    # -------------------------
    # 회피
    # -------------------------

    if st.session_state.evading:

        st.session_state.evading = False

        if random.random() < 0.5:

            st.session_state.message = (
                "💨 회피 성공! 공격을 완전히 피했습니다!"
            )

            return

        else:

            st.session_state.message = (
                "💨 회피 실패!"
            )


    # -------------------------
    # 기본 공격력
    # -------------------------

    damage = random.randint(
        max(1, st.session_state.monster_damage - 5),
        st.session_state.monster_damage + 5
    )


    # -------------------------
    # 보스 필살기
    # -------------------------

    if st.session_state.is_boss:

        if random.random() < 0.2:

            damage *= 2

            st.session_state.message = (
                f"💀 보스 필살기! {damage}의 피해!"
            )

        else:

            st.session_state.message = (
                f"👑 보스 공격! {damage}의 피해!"
            )

    else:

        st.session_state.message = (
            f"👾 몬스터 공격! {damage}의 피해!"
        )


    # -------------------------
    # 방어
    # -------------------------

    if st.session_state.defending:

        damage = max(1, int(damage * 0.4))

        st.session_state.defending = False

        st.session_state.message += (
            f" 🛡️ 방어 성공! 피해가 감소했습니다."
        )


    # -------------------------
    # 피해 적용
    # -------------------------

    st.session_state.hp -= damage

    if st.session_state.hp <= 0:

        st.session_state.hp = 0
        st.session_state.game_over = True

        st.session_state.message = (
            "💀 당신은 쓰러졌습니다!"
        )


# ==========================================
# 몬스터 처치
# ==========================================

def monster_defeated():

    was_boss = st.session_state.is_boss

    if was_boss:

        reward = random.randint(100, 200)

        st.session_state.gold += reward
        st.session_state.boss_kill += 1

        st.session_state.max_hp += 30
        st.session_state.attack += 10

        st.session_state.hp = st.session_state.max_hp

        st.session_state.message = (
            f"👑 보스 {st.session_state.monster_name} 처치! "
            f"💰 +{reward}G!"
        )

    else:

        reward = random.randint(15, 35)

        st.session_state.gold += reward

        st.session_state.message = (
            f"🎉 {st.session_state.monster_name} 처치! "
            f"💰 +{reward}G!"
        )


    st.session_state.kill += 1
    st.session_state.combo += 1


    # 3마리마다 레벨업
    old_level = st.session_state.level

    st.session_state.level = (
        st.session_state.kill // 3 + 1
    )


    if st.session_state.level > old_level:

        st.session_state.max_hp += 20
        st.session_state.attack += 5
        st.session_state.hp = st.session_state.max_hp

        st.session_state.message += (
            f" ⭐ LEVEL UP! Lv.{st.session_state.level}"
        )


    # 방어/회피 상태 초기화
    st.session_state.defending = False
    st.session_state.evading = False

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

        if not st.session_state.game_over:

            st.session_state.message = (
                f"⚔️ {damage}의 피해를 입혔습니다!"
            )


# ==========================================
# 강공격
# ==========================================

def strong_attack():

    if random.random() <= 0.6:

        damage = random.randint(
            st.session_state.attack + 15,
            st.session_state.attack + 35
        )

        st.session_state.monster_hp -= damage


        if st.session_state.monster_hp <= 0:

            st.session_state.monster_hp = 0

            monster_defeated()

            if not st.session_state.game_over:

                st.session_state.message = (
                    "💥 강공격으로 적을 처치했습니다!"
                )

        else:

            st.session_state.combo = 0

            monster_attack()

            if not st.session_state.game_over:

                st.session_state.message = (
                    f"💥 강공격 성공! {damage} 피해!"
                )

    else:

        st.session_state.combo = 0

        monster_attack()

        if not st.session_state.game_over:

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

    actual = st.session_state.hp - old_hp

    monster_attack()

    if not st.session_state.game_over:

        st.session_state.message = (
            f"❤️ HP +{actual}"
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
            "❤️ HP가 가득합니다!"
        )

        return


    st.session_state.potion -= 1

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + 40
    )

    actual = st.session_state.hp - old_hp

    monster_attack()

    if not st.session_state.game_over:

        st.session_state.message = (
            f"🧪 물약 사용! HP +{actual}"
        )


# ==========================================
# 방어
# ==========================================

def defend():

    st.session_state.defending = True

    st.session_state.evading = False

    monster_attack()

    if not st.session_state.game_over:

        st.session_state.message = (
            "🛡️ 방어 자세! "
            "이번 공격의 피해가 60% 감소합니다."
        )


# ==========================================
# 회피
# ==========================================

def evade():

    st.session_state.evading = True

    st.session_state.defending = False

    monster_attack()

    if not st.session_state.game_over:

        # monster_attack에서 회피 성공 여부를 처리함
        if not st.session_state.evading:

            # 회피 상태가 사라졌다는 것은 공격이 끝났다는 의미
            pass

        st.session_state.message = (
            "💨 회피를 시도했습니다!"
        )


# ==========================================
# 무기 강화
# ==========================================

def upgrade_weapon():

    cost = st.session_state.weapon_level * 50

    if st.session_state.gold < cost:

        st.session_state.message = (
            f"💰 골드가 부족합니다! "
            f"{cost}G가 필요합니다."
        )

        return


    st.session_state.gold -= cost

    st.session_state.weapon_level += 1
    st.session_state.attack += 10

    st.session_state.message = (
        f"🗡️ 무기 강화 성공! "
        f"Lv.{st.session_state.weapon_level}"
    )


# ==========================================
# 게임 시작
# ==========================================

if "hp" not in st.session_state:

    reset_game()


# ==========================================
# 제목
# ==========================================

st.title("⚔️ 미니 RPG")

st.write(
    "공격만 하지 말고 방어와 회피를 활용해서 몬스터와 보스를 쓰러뜨려보세요!"
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


st.progress(
    st.session_state.hp /
    st.session_state.max_hp
)


# ==========================================
# 현재 상태
# ==========================================

if st.session_state.defending:

    st.warning("🛡️ 현재 방어 상태입니다!")

if st.session_state.evading:

    st.warning("💨 현재 회피 준비 상태입니다!")


st.divider()


# ==========================================
# 보스
# ==========================================

if st.session_state.is_boss:

    st.error("👑⚠️ BOSS BATTLE ⚠️👑")


# ==========================================
# 몬스터
# ==========================================

st.subheader(
    st.session_state.monster_name
)

st.write(
    f"❤️ HP: "
    f"{st.session_state.monster_hp}/"
    f"{st.session_state.monster_max_hp}"
)

st.progress(
    max(0, st.session_state.monster_hp)
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
# 전투 버튼
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
            "🛡️ 방어",
            use_container_width=True
        ):

            defend()
            st.rerun()


    with col2:

        if st.button(
            "💨 회피 (50%)",
            use_container_width=True
        ):

            evade()
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
    f"🗡️ 무기 Lv.{st.session_state.weapon_level}"
)

st.write(
    f"⚔️ 공격력: {st.session_state.attack}"
)


# ==========================================
# 기록
# ==========================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🔥 연속 처치",
        st.session_state.combo
    )

with col2:

    st.metric(
        "👑 보스 처치",
        st.session_state.boss_kill
    )

with col3:

    if st.session_state.is_boss:
        st.metric("⚠️ 현재", "BOSS")
    else:
        st.metric("⚠️ 현재", "일반")


# ==========================================
# 게임 오버
# ==========================================

if st.session_state.game_over:

    st.error("💀 GAME OVER")

    st.write(
        f"🏆 총 처치: {st.session_state.kill}"
    )

    st.write(
        f"👑 보스 처치: {st.session_state.boss_kill}"
    )

    st.write(
        f"⭐ 최종 레벨: {st.session_state.level}"
    )

    if st.button(
        "🔄 처음부터 다시 시작",
        use_container_width=True
    ):

        reset_game()
        st.rerun()
