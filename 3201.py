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
# 몬스터 데이터
# 이름, HP, 공격력, 방어력, 회피율, 패링확률
# ==========================================

NORMAL_MONSTERS = [
    ("🟢 슬라임", 40, 7, 2, 5, 5),
    ("🐀 거대 쥐", 45, 8, 2, 12, 8),
    ("🦇 박쥐", 50, 9, 3, 18, 5),
    ("👺 고블린", 65, 11, 5, 8, 12),
    ("🐺 늑대", 70, 13, 4, 15, 10),
    ("🕷️ 거대 거미", 80, 14, 6, 12, 15),
    ("💀 해골 전사", 95, 16, 9, 5, 22),
    ("👻 유령", 100, 18, 5, 25, 10),
    ("🧟 좀비", 110, 19, 10, 3, 18),
    ("🧙 다크 메이지", 120, 22, 7, 15, 20),
    ("🦂 독전갈", 130, 23, 8, 20, 18),
    ("🧛 뱀파이어", 145, 25, 10, 22, 25),
]


# ==========================================
# 보스 데이터
# ==========================================

BOSSES = [
    ("👑 오크 대장", 250, 28, 15, 12, 30),
    ("🔥 불의 마왕", 320, 32, 18, 15, 35),
    ("❄️ 얼음 여왕", 350, 35, 20, 20, 35),
    ("⚡ 번개의 군주", 380, 38, 22, 25, 40),
    ("💀 죽음의 기사", 420, 42, 25, 15, 45),
    ("🐲 고대 드래곤", 500, 50, 30, 20, 50),
]


# ==========================================
# 다음 레벨 필요 경험치
# ==========================================

def required_exp():

    return 100 + (
        (st.session_state.level - 1) * 50
    )


# ==========================================
# 경험치 획득
# ==========================================

def gain_exp(amount):

    st.session_state.exp += amount

    level_up = False

    while st.session_state.exp >= required_exp():

        st.session_state.exp -= required_exp()

        st.session_state.level += 1

        level_up = True

        # 능력치 상승
        st.session_state.max_hp += 20
        st.session_state.attack += 5
        st.session_state.defense += 2

        st.session_state.evasion = min(
            50,
            st.session_state.evasion + 1
        )

        # 레벨업 시 체력 회복
        st.session_state.hp = (
            st.session_state.max_hp
        )

    return level_up


# ==========================================
# 몬스터 생성
# ==========================================

def spawn_monster():

    # 5마리마다 보스
    if (
        st.session_state.kill > 0
        and st.session_state.kill % 5 == 0
    ):

        name, hp, damage, defense, evasion, parry = random.choice(
            BOSSES
        )

        # 레벨에 따른 성장
        hp += (
            st.session_state.level - 1
        ) * 20

        damage += (
            st.session_state.level - 1
        ) * 3

        defense += (
            st.session_state.level - 1
        ) * 2

        evasion = min(
            50,
            evasion + (
                st.session_state.level - 1
            )
        )

        parry = min(
            60,
            parry + (
                st.session_state.level - 1
            )
        )

        st.session_state.monster_name = name
        st.session_state.monster_hp = hp
        st.session_state.monster_max_hp = hp
        st.session_state.monster_damage = damage
        st.session_state.monster_defense = defense
        st.session_state.monster_evasion = evasion
        st.session_state.monster_parry = parry

        st.session_state.is_boss = True

        # 보스 EXP
        st.session_state.monster_exp_min = (
            80 + st.session_state.level * 20
        )

        st.session_state.monster_exp_max = (
            150 + st.session_state.level * 30
        )

    else:

        name, hp, damage, defense, evasion, parry = random.choice(
            NORMAL_MONSTERS
        )

        # 레벨에 따른 성장
        hp += (
            st.session_state.level - 1
        ) * 10

        damage += (
            st.session_state.level - 1
        ) * 2

        defense += (
            st.session_state.level - 1
        )

        evasion = min(
            45,
            evasion + (
                st.session_state.level // 3
            )
        )

        parry = min(
            50,
            parry + (
                st.session_state.level // 4
            )
        )

        st.session_state.monster_name = name
        st.session_state.monster_hp = hp
        st.session_state.monster_max_hp = hp
        st.session_state.monster_damage = damage
        st.session_state.monster_defense = defense
        st.session_state.monster_evasion = evasion
        st.session_state.monster_parry = parry

        st.session_state.is_boss = False

        # 일반 몬스터 EXP
        st.session_state.monster_exp_min = (
            15 + st.session_state.level * 3
        )

        st.session_state.monster_exp_max = (
            35 + st.session_state.level * 6
        )


# ==========================================
# 게임 초기화
# ==========================================

def reset_game():

    # 플레이어 HP
    st.session_state.hp = 100
    st.session_state.max_hp = 100

    # 플레이어 공격
    st.session_state.attack = 20

    # 플레이어 방어
    st.session_state.defense = 5

    # 플레이어 회피
    st.session_state.evasion = 10

    # 레벨
    st.session_state.level = 1

    # 경험치
    st.session_state.exp = 0

    # 골드
    st.session_state.gold = 50

    # 물약
    st.session_state.potion = 3

    # 처치 기록
    st.session_state.kill = 0
    st.session_state.boss_kill = 0
    st.session_state.combo = 0

    # 장비
    st.session_state.weapon_level = 1
    st.session_state.armor_level = 1
    st.session_state.boots_level = 1

    # 전투 상태
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
    # 플레이어 회피
    # ======================================

    if random.randint(
        1,
        100
    ) <= st.session_state.evasion:

        st.session_state.message = (
            f"💨 회피 성공! "
            f"({st.session_state.evasion}%)"
        )

        return


    # ======================================
    # 기본 피해
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
                f"{damage}의 공격!"
            )

        else:

            st.session_state.message = (
                f"👑 보스 공격!"
            )

    else:

        st.session_state.message = (
            "👾 몬스터 공격!"
        )


    # ======================================
    # 방어력
    # ======================================

    damage -= st.session_state.defense

    damage = max(
        1,
        damage
    )


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
            " 🛡️ 방어 성공!"
        )


    # ======================================
    # 피해
    # ======================================

    st.session_state.hp -= damage

    st.session_state.message += (
        f" 💔 {damage} 피해"
    )


    # ======================================
    # 사망
    # ======================================

    if st.session_state.hp <= 0:

        st.session_state.hp = 0

        st.session_state.game_over = True

        st.session_state.message = (
            "💀 당신은 쓰러졌습니다!"
        )


# ==========================================
# 플레이어 공격 처리
# ==========================================

def player_attack(
    damage,
    can_be_parried=True
):

    # ======================================
    # 몬스터 회피
    # ======================================

    if random.randint(
        1,
        100
    ) <= st.session_state.monster_evasion:

        st.session_state.message = (
            f"💨 {st.session_state.monster_name} "
            f"회피 성공! "
            f"({st.session_state.monster_evasion}%)"
        )

        # 회피했으므로 몬스터 반격
        monster_attack()

        return False


    # ======================================
    # 몬스터 패링
    #
    # 강공격은 패링 불가능
    # ======================================

    if can_be_parried:

        if random.randint(
            1,
            100
        ) <= st.session_state.monster_parry:

            counter_damage = random.randint(
                max(
                    1,
                    st.session_state.monster_damage - 5
                ),
                st.session_state.monster_damage + 5
            )

            # 패링 반격은 방어력 적용
            counter_damage = max(
                1,
                counter_damage
                - st.session_state.defense
            )

            st.session_state.hp -= counter_damage

            st.session_state.message = (
                f"⚡ {st.session_state.monster_name} "
                f"패링 성공! "
                f"💥 {counter_damage} 반격!"
            )

            if st.session_state.hp <= 0:

                st.session_state.hp = 0

                st.session_state.game_over = True

            return False


    # ======================================
    # 방어력 적용
    # ======================================

    final_damage = max(
        1,
        damage
        - st.session_state.monster_defense
    )


    # ======================================
    # 피해 적용
    # ======================================

    st.session_state.monster_hp -= final_damage

    st.session_state.message = (
        f"⚔️ {final_damage} 피해!"
    )

    return True


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

    success = player_attack(
        damage,
        can_be_parried=True
    )

    if not success:
        return


    # ======================================
    # 몬스터 처치
    # ======================================

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

    # 강공격 성공 확률
    if random.random() > 0.6:

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )

        st.session_state.combo = 0

        monster_attack()

        return


    damage = random.randint(
        st.session_state.attack + 15,
        st.session_state.attack + 35
    )


    # ======================================
    # 강공격
    #
    # can_be_parried=False
    # ======================================

    success = player_attack(
        damage,
        can_be_parried=False
    )

    if not success:
        return


    # 강공격 성공 메시지
    st.session_state.message = (
        f"💥 강공격 성공! "
        f"{max(1, damage - st.session_state.monster_defense)} 피해!"
    )


    # ======================================
    # 몬스터 처치
    # ======================================

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

    else:

        st.session_state.combo = 0

        monster_attack()


# ==========================================
# 패링
# ==========================================

def parry():

    # 플레이어 패링 성공 확률
    success_rate = 40


    if random.randint(
        1,
        100
    ) <= success_rate:

        counter_damage = random.randint(
            st.session_state.attack,
            st.session_state.attack + 20
        )

        # 몬스터 방어력 적용
        counter_damage = max(
            1,
            counter_damage
            - st.session_state.monster_defense
        )

        st.session_state.monster_hp -= (
            counter_damage
        )

        st.session_state.message = (
            f"⚡ PARRY 성공! "
            f"💥 {counter_damage} 반격!"
        )


        # 처치
        if st.session_state.monster_hp <= 0:

            st.session_state.monster_hp = 0

            monster_defeated()

    else:

        st.session_state.message = (
            "❌ 패링 실패!"
        )

        monster_attack()


# ==========================================
# 방어
# ==========================================

def defend():

    st.session_state.defending = True

    monster_attack()

    if not st.session_state.game_over:

        st.session_state.message = (
            "🛡️ 방어 자세! "
            "받는 피해가 60% 감소합니다."
        )


# ==========================================
# 회복
# ==========================================

def heal():

    amount = random.randint(
        15,
        30
    )

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + amount
    )

    actual = (
        st.session_state.hp - old_hp
    )

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


    if (
        st.session_state.hp
        >= st.session_state.max_hp
    ):

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

    actual = (
        st.session_state.hp - old_hp
    )

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

    cost = (
        st.session_state.weapon_level * 50
    )

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost

    st.session_state.weapon_level += 1

    st.session_state.attack += 10

    st.session_state.message = (
        "🗡️ 무기 강화 성공! "
        "공격력 +10"
    )


# ==========================================
# 방어구 강화
# ==========================================

def upgrade_armor():

    cost = (
        st.session_state.armor_level * 60
    )

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost

    st.session_state.armor_level += 1

    st.session_state.defense += 4

    st.session_state.message = (
        "🛡️ 방어구 강화 성공! "
        "방어력 +4"
    )


# ==========================================
# 신발 강화
# ==========================================

def upgrade_boots():

    cost = (
        st.session_state.boots_level * 70
    )

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost

    st.session_state.boots_level += 1

    st.session_state.evasion = min(
        50,
        st.session_state.evasion + 3
    )

    st.session_state.message = (
        "👟 신발 강화 성공! "
        "회피율 +3%"
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

st.caption(
    "공격 · 방어 · 회피 · 패링을 활용해 "
    "몬스터와 보스를 쓰러뜨리세요!"
)


# ==========================================
# 상단 정보
# ==========================================

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

    # 레벨 바로 아래 EXP 숫자 표시
    st.caption(
        f"EXP: {st.session_state.exp} / "
        f"{required_exp()}"
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

st.subheader("📊 플레이어 스탯")

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
# 보스
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


# ==========================================
# 몬스터 스탯
# ==========================================

st.subheader("👾 적 스탯")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "⚔️ 공격력",
        st.session_state.monster_damage
    )

with col2:

    st.metric(
        "🛡️ 방어력",
        st.session_state.monster_defense
    )

with col3:

    st.metric(
        "💨 회피율",
        f"{st.session_state.monster_evasion}%"
    )

with col4:

    st.metric(
        "⚡ 패링",
        f"{st.session_state.monster_parry}%"
    )


st.caption(
    f"⭐ 처치 시 EXP: "
    f"{st.session_state.monster_exp_min}"
    f" ~ "
    f"{st.session_state.monster_exp_max}"
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

    # ------------------------------
    # 1줄
    # ------------------------------

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
            "💥 강공격",
            help="강공격은 적이 패링할 수 없습니다.",
            use_container_width=True
        ):

            strong_attack()
            st.rerun()


    # ------------------------------
    # 2줄
    # ------------------------------

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
            "⚡ 패링",
            help="40% 확률로 공격을 막고 반격합니다.",
            use_container_width=True
        ):

            parry()
            st.rerun()


    # ------------------------------
    # 3줄
    # ------------------------------

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

st.subheader("🛒 장비 상점")

col1, col2, col3 = st.columns(3)


# ==========================================
# 무기
# ==========================================

with col1:

    cost = (
        st.session_state.weapon_level * 50
    )

    st.write(
        f"🗡️ 무기 Lv."
        f"{st.session_state.weapon_level}"
    )

    st.write(
        f"공격력 "
        f"{st.session_state.attack}"
    )

    if st.button(
        f"강화 {cost}G",
        key="weapon",
        use_container_width=True
    ):

        upgrade_weapon()
        st.rerun()


# ==========================================
# 방어구
# ==========================================

with col2:

    cost = (
        st.session_state.armor_level * 60
    )

    st.write(
        f"🛡️ 방어구 Lv."
        f"{st.session_state.armor_level}"
    )

    st.write(
        f"방어력 "
        f"{st.session_state.defense}"
    )

    if st.button(
        f"강화 {cost}G",
        key="armor",
        use_container_width=True
    ):

        upgrade_armor()
        st.rerun()


# ==========================================
# 신발
# ==========================================

with col3:

    cost = (
        st.session_state.boots_level * 70
    )

    st.write(
        f"👟 신발 Lv."
        f"{st.session_state.boots_level}"
    )

    st.write(
        f"회피율 "
        f"{st.session_state.evasion}%"
    )

    if st.button(
        f"강화 {cost}G",
        key="boots",
        use_container_width=True
    ):

        upgrade_boots()
        st.rerun()


# ==========================================
# 물약 상점
# ==========================================

st.write(
    f"🧪 물약: "
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

    st.write(
        f"⭐ 최종 EXP: "
        f"{st.session_state.exp}"
    )

    if st.button(
        "🔄 처음부터 다시 시작",
        use_container_width=True
    ):

        reset_game()
        st.rerun()
