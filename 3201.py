import streamlit as st
import random

# ==========================================
# 설정
# ==========================================

st.set_page_config(
    page_title="⚔️ 미니 RPG",
    page_icon="⚔️",
    layout="centered"
)


# ==========================================
# 몬스터
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

    # 5마리마다 보스
    if (
        st.session_state.kill > 0
        and st.session_state.kill % 5 == 0
    ):

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

    # -------------------------
    # 기본 스탯
    # -------------------------

    st.session_state.hp = 100
    st.session_state.max_hp = 100

    st.session_state.attack = 20

    # ⭐ 방어력
    st.session_state.defense = 5

    # ⭐ 회피율
    st.session_state.evasion = 10

    # -------------------------
    # 성장
    # -------------------------

    st.session_state.level = 1
    st.session_state.gold = 50

    # -------------------------
    # 아이템
    # -------------------------

    st.session_state.potion = 3

    # -------------------------
    # 기록
    # -------------------------

    st.session_state.kill = 0
    st.session_state.boss_kill = 0
    st.session_state.combo = 0

    # -------------------------
    # 장비 레벨
    # -------------------------

    st.session_state.weapon_level = 1
    st.session_state.armor_level = 1
    st.session_state.boots_level = 1

    # -------------------------
    # 전투 상태
    # -------------------------

    st.session_state.defending = False
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

    # ======================================
    # 회피율 판정
    # ======================================

    evasion = st.session_state.evasion

    if random.randint(1, 100) <= evasion:

        st.session_state.message = (
            f"💨 회피 성공! "
            f"({evasion}% 확률)"
        )

        return


    # ======================================
    # 몬스터 기본 공격력
    # ======================================

    damage = random.randint(
        max(
            1,
            st.session_state.monster_damage - 5
        ),
        st.session_state.monster_damage + 5
    )


    # ======================================
    # 보스 필살기
    # ======================================

    if st.session_state.is_boss:

        if random.random() < 0.2:

            damage *= 2

            st.session_state.message = (
                f"💀 보스 필살기! "
                f"{damage}의 피해!"
            )

        else:

            st.session_state.message = (
                f"👑 보스 공격! "
                f"{damage}의 피해!"
            )

    else:

        st.session_state.message = (
            f"👾 몬스터 공격! "
            f"{damage}의 피해!"
        )


    # ======================================
    # 방어력 적용
    # ======================================

    original_damage = damage

    damage -= st.session_state.defense

    damage = max(1, damage)


    # ======================================
    # 방어 자세
    # ======================================

    if st.session_state.defending:

        damage = max(
            1,
            int(damage * 0.4)
        )

        st.session_state.defending = False

        st.session_state.message += (
            " 🛡️ 방어 자세!"
        )


    # ======================================
    # 피해 적용
    # ======================================

    st.session_state.hp -= damage


    # 피해 표시
    st.session_state.message += (
        f" 💔 {damage} 피해"
    )


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


    # ======================================
    # 보스 보상
    # ======================================

    if was_boss:

        reward = random.randint(100, 200)

        st.session_state.gold += reward
        st.session_state.boss_kill += 1

        st.session_state.max_hp += 30
        st.session_state.attack += 10

        # 보스 처치 후 완전 회복
        st.session_state.hp = st.session_state.max_hp

        st.session_state.message = (
            f"👑 보스 처치! "
            f"💰 +{reward}G!"
        )


    # ======================================
    # 일반 몬스터 보상
    # ======================================

    else:

        reward = random.randint(15, 35)

        st.session_state.gold += reward

        st.session_state.message = (
            f"🎉 {st.session_state.monster_name} 처치! "
            f"💰 +{reward}G!"
        )


    # ======================================
    # 처치 수
    # ======================================

    st.session_state.kill += 1
    st.session_state.combo += 1


    # ======================================
    # 레벨 계산
    # ======================================

    old_level = st.session_state.level

    st.session_state.level = (
        st.session_state.kill // 3 + 1
    )


    # ======================================
    # 레벨업
    # ======================================

    if st.session_state.level > old_level:

        st.session_state.max_hp += 20

        st.session_state.attack += 5

        # 레벨업 시 방어력 +2
        st.session_state.defense += 2

        # 레벨업 시 회피율 +1%
        st.session_state.evasion += 1

        # 회피율 최대 50%
        st.session_state.evasion = min(
            50,
            st.session_state.evasion
        )

        st.session_state.hp = (
            st.session_state.max_hp
        )

        st.session_state.message += (
            f" ⭐ LEVEL UP! "
            f"Lv.{st.session_state.level}"
        )


    # 상태 초기화
    st.session_state.defending = False

    # 새 몬스터
    spawn_monster()


# ==========================================
# 일반 공격
# ==========================================

def attack():

    damage = random.randint(
        max(
            1,
            st.session_state.attack - 5
        ),
        st.session_state.attack + 5
    )

    st.session_state.monster_hp -= damage


    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

    else:

        st.session_state.combo = 0

        monster_attack()


# ==========================================
# 강공격
# ==========================================

def strong_attack():

    # 60% 성공
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
                    f"💥 강공격! "
                    f"{damage} 피해!"
                )

    else:

        st.session_state.combo = 0

        monster_attack()

        if not st.session_state.game_over:

            st.session_state.message = (
                "💨 강공격이 빗나갔습니다!"
            )


# ==========================================
# 방어
# ==========================================

def defend():

    st.session_state.defending = True

    monster_attack()

    if not st.session_state.game_over:

        st.session_state.message = (
            "🛡️ 방어 성공! "
            "이번 공격의 피해가 추가로 60% 감소합니다."
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
            f"🧪 물약 사용! "
            f"HP +{actual}"
        )


# ==========================================
# 무기 강화
# ==========================================

def upgrade_weapon():

    cost = st.session_state.weapon_level * 50


    if st.session_state.gold < cost:

        st.session_state.message = (
            f"💰 골드가 부족합니다!"
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
# 방어구 강화
# ==========================================

def upgrade_armor():

    cost = st.session_state.armor_level * 60


    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return


    st.session_state.gold -= cost

    st.session_state.armor_level += 1

    st.session_state.defense += 4

    st.session_state.message = (
        f"🛡️ 방어구 강화 성공! "
        f"방어력 +4"
    )


# ==========================================
# 신발 강화
# ==========================================

def upgrade_boots():

    cost = st.session_state.boots_level * 70


    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return


    st.session_state.gold -= cost

    st.session_state.boots_level += 1

    # 회피율 +3%
    st.session_state.evasion += 3

    # 최대 50%
    st.session_state.evasion = min(
        50,
        st.session_state.evasion
    )

    st.session_state.message = (
        f"👟 신발 강화 성공! "
        f"회피율 +3%"
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
    "공격하고, 방어하고, 회피하면서 "
    "몬스터와 보스를 물리치세요!"
)


# ==========================================
# 플레이어 정보
# ==========================================

st.subheader("🧙 플레이어")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "❤️ HP",
        f"{st.session_state.hp}/"
        f"{st.session_state.max_hp}"
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


# ==========================================
# 스탯
# ==========================================

st.subheader("📊 캐릭터 스탯")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⚔️ 공격력",
        st.session_state.attack
    )

with col2:

    st.metric(
        "🛡️ 방어력",
        st.session_state.defense
    )

with col3:

    st.metric(
        "💨 회피율",
        f"{st.session_state.evasion}%"
    )


st.progress(
    st.session_state.hp /
    st.session_state.max_hp
)


st.divider()


# ==========================================
# 보스 표시
# ==========================================

if st.session_state.is_boss:

    st.error(
        "👑⚠️ BOSS BATTLE ⚠️👑"
    )


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
            "🛡️ 방어",
            use_container_width=True
        ):

            defend()
            st.rerun()


    with col2:

        if st.button(
            "❤️ 회복",
            use_container_width=True
        ):

            heal()
            st.rerun()


    col1, col2 = st.columns(2)

    with col1:

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

st.subheader("🛒 장비 상점")


# 무기
col1, col2, col3 = st.columns(3)

with col1:

    weapon_cost = (
        st.session_state.weapon_level * 50
    )

    st.write(
        f"🗡️ 무기 Lv."
        f"{st.session_state.weapon_level}"
    )

    st.write(
        f"공격력: "
        f"{st.session_state.attack}"
    )

    if st.button(
        f"강화 {weapon_cost}G",
        key="weapon",
        use_container_width=True
    ):

        upgrade_weapon()
        st.rerun()


# 방어구
with col2:

    armor_cost = (
        st.session_state.armor_level * 60
    )

    st.write(
        f"🛡️ 방어구 Lv."
        f"{st.session_state.armor_level}"
    )

    st.write(
        f"방어력: "
        f"{st.session_state.defense}"
    )

    if st.button(
        f"강화 {armor_cost}G",
        key="armor",
        use_container_width=True
    ):

        upgrade_armor()
        st.rerun()


# 신발
with col3:

    boots_cost = (
        st.session_state.boots_level * 70
    )

    st.write(
        f"👟 신발 Lv."
        f"{st.session_state.boots_level}"
    )

    st.write(
        f"회피율: "
        f"{st.session_state.evasion}%"
    )

    if st.button(
        f"강화 {boots_cost}G",
        key="boots",
        use_container_width=True
    ):

        upgrade_boots()
        st.rerun()


# ==========================================
# 물약 상점
# ==========================================

st.write(
    f"🧪 현재 물약: "
    f"{st.session_state.potion}개"
)

if st.button(
    "🧪 물약 구매 20G",
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


# ==========================================
# 기록
# ==========================================

st.divider()

col1, col2 = st.columns(2)

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


# ==========================================
# 게임 오버
# ==========================================

if st.session_state.game_over:

    st.error("💀 GAME OVER")

    st.write(
        f"🏆 총 처치: "
        f"{st.session_state.kill}"
    )

    st.write(
        f"👑 보스 처치: "
        f"{st.session_state.boss_kill}"
    )

    st.write(
        f"⭐ 최종 레벨: "
        f"{st.session_state.level}"
    )

    if st.button(
        "🔄 처음부터 다시 시작",
        use_container_width=True
    ):

        reset_game()
        st.rerun()
