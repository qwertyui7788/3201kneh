import streamlit as st
import random
import math


# ==========================================
# Streamlit 설정
# ==========================================

st.set_page_config(
    page_title="⚔️ 미니 RPG",
    page_icon="⚔️",
    layout="centered"
)


# ==========================================
# 몬스터 목록
# 이름, HP, 공격력, 방어력, 회피율, 패링율
# ==========================================

NORMAL_MONSTERS = [
    ("🟢 슬라임", 40, 7, 2, 5, 5),
    ("🐀 거대 쥐", 45, 8, 2, 8, 6),
    ("🦇 박쥐", 50, 9, 3, 12, 5),
    ("👺 고블린", 65, 11, 4, 8, 10),
    ("🐺 늑대", 70, 13, 4, 12, 8),
    ("🕷️ 거대 거미", 80, 14, 5, 12, 12),
    ("💀 해골 전사", 95, 16, 7, 5, 18),
    ("👻 유령", 100, 18, 5, 20, 10),
    ("🧟 좀비", 110, 19, 8, 3, 15),
    ("🧙 다크 메이지", 120, 22, 7, 15, 18),
    ("🦂 독전갈", 130, 23, 8, 18, 16),
    ("🧛 뱀파이어", 145, 25, 10, 20, 22),
]


# ==========================================
# 보스
# ==========================================

BOSSES = [
    ("👑 오크 대장", 250, 28, 14, 12, 28),
    ("🔥 불의 마왕", 320, 32, 17, 15, 32),
    ("❄️ 얼음 여왕", 350, 35, 19, 20, 35),
    ("⚡ 번개의 군주", 380, 38, 21, 25, 38),
    ("💀 죽음의 기사", 420, 42, 24, 15, 42),
    ("🐲 고대 드래곤", 500, 50, 28, 20, 48),
]


# ==========================================
# 필요한 경험치
# ==========================================

def required_exp():

    return 100 + (
        (st.session_state.level - 1) * 50
    )


# ==========================================
# 숫자 표시용
# ==========================================

def nice_number(value):

    if isinstance(value, int):
        return str(value)

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.1f}"


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

        # 레벨업 기본 능력치
        st.session_state.max_hp += 25
        st.session_state.attack += 6
        st.session_state.defense += 3

        st.session_state.hp = (
            st.session_state.max_hp
        )

        # 회피율은 최대 60%
        st.session_state.evasion = min(
            60,
            st.session_state.evasion + 1
        )

    return level_up


# ==========================================
# 몬스터 생성
# ==========================================

def spawn_monster():

    # --------------------------------------
    # 5마리마다 보스
    # --------------------------------------

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
            55,
            evasion + (
                st.session_state.level - 1
            )
        )

        parry = min(
            65,
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

        st.session_state.monster_exp_min = (
            100 + st.session_state.level * 20
        )

        st.session_state.monster_exp_max = (
            180 + st.session_state.level * 30
        )

    else:

        name, hp, damage, defense, evasion, parry = random.choice(
            NORMAL_MONSTERS
        )

        # 레벨에 따른 성장
        hp += (
            st.session_state.level - 1
        ) * 8

        damage += (
            st.session_state.level - 1
        ) * 2

        defense += (
            st.session_state.level - 1
        )

        evasion = min(
            50,
            evasion + (
                st.session_state.level // 3
            )
        )

        parry = min(
            55,
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

        st.session_state.monster_exp_min = (
            20 + st.session_state.level * 4
        )

        st.session_state.monster_exp_max = (
            45 + st.session_state.level * 7
        )


# ==========================================
# 게임 초기화
# ==========================================

def reset_game():

    # --------------------------------------
    # 기본 능력치
    # --------------------------------------

    st.session_state.hp = 150
    st.session_state.max_hp = 150

    st.session_state.attack = 30
    st.session_state.defense = 8
    st.session_state.evasion = 15

    # --------------------------------------
    # 물약으로 증가한 누적 수치
    # --------------------------------------

    st.session_state.potion_attack_bonus = 0
    st.session_state.potion_defense_bonus = 0
    st.session_state.potion_evasion_bonus = 0

    # --------------------------------------
    # 레벨 / EXP
    # --------------------------------------

    st.session_state.level = 1
    st.session_state.exp = 0

    # --------------------------------------
    # 골드
    # --------------------------------------

    st.session_state.gold = 150

    # --------------------------------------
    # 물약
    # --------------------------------------

    st.session_state.hp_potion = 5
    st.session_state.attack_potion = 1
    st.session_state.defense_potion = 1
    st.session_state.evasion_potion = 1

    # --------------------------------------
    # 기록
    # --------------------------------------

    st.session_state.kill = 0
    st.session_state.boss_kill = 0
    st.session_state.combo = 0

    # --------------------------------------
    # 장비
    # --------------------------------------

    st.session_state.weapon_level = 1
    st.session_state.armor_level = 1
    st.session_state.boots_level = 1

    # --------------------------------------
    # 전투 상태
    # --------------------------------------

    st.session_state.defending = False
    st.session_state.game_over = False
    st.session_state.is_boss = False

    st.session_state.message = (
        "⚔️ 새로운 모험이 시작되었습니다!"
    )

    # 새로운 몬스터 생성
    spawn_monster()


# ==========================================
# 몬스터 공격
# ==========================================

def monster_attack():

    if st.session_state.game_over:
        return

    # --------------------------------------
    # 플레이어 회피
    # --------------------------------------

    if random.randint(
        1,
        100
    ) <= st.session_state.evasion:

        st.session_state.message = (
            f"💨 공격을 회피했습니다! "
            f"({nice_number(st.session_state.evasion)}%)"
        )

        return


    # --------------------------------------
    # 몬스터 기본 공격력
    # --------------------------------------

    damage = random.randint(
        max(
            1,
            st.session_state.monster_damage - 5
        ),
        st.session_state.monster_damage + 5
    )


    # --------------------------------------
    # 보스 필살기
    # --------------------------------------

    if st.session_state.is_boss:

        if random.random() < 0.2:

            damage *= 2

            st.session_state.message = (
                f"💀 보스 필살기! "
                f"{damage}의 공격!"
            )

        else:

            st.session_state.message = (
                "👑 보스 공격!"
            )

    else:

        st.session_state.message = (
            "👾 몬스터 공격!"
        )


    # --------------------------------------
    # 플레이어 방어력 적용
    # --------------------------------------

    damage -= st.session_state.defense

    damage = max(
        1,
        damage
    )


    # --------------------------------------
    # 방어 자세
    # --------------------------------------

    if st.session_state.defending:

        damage = max(
            1,
            int(damage * 0.4)
        )

        st.session_state.defending = False

        st.session_state.message += (
            " 🛡️ 방어 성공!"
        )


    # --------------------------------------
    # HP 감소
    # --------------------------------------

    st.session_state.hp -= damage

    st.session_state.message += (
        f" 💔 {damage} 피해"
    )


    # --------------------------------------
    # 사망
    # --------------------------------------

    if st.session_state.hp <= 0:

        st.session_state.hp = 0

        st.session_state.game_over = True

        st.session_state.message = (
            "💀 당신은 쓰러졌습니다!"
        )


# ==========================================
# 플레이어 공격
# ==========================================

def player_attack(
    damage,
    can_be_parried=True
):

    # --------------------------------------
    # 몬스터 회피
    # --------------------------------------

    if random.randint(
        1,
        100
    ) <= st.session_state.monster_evasion:

        st.session_state.message = (
            f"💨 {st.session_state.monster_name} "
            f"회피 성공! "
            f"({st.session_state.monster_evasion}%)"
        )

        monster_attack()

        return False


    # --------------------------------------
    # 몬스터 패링
    #
    # 강공격은 패링 불가능
    # --------------------------------------

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


    # --------------------------------------
    # 몬스터 방어력 적용
    # --------------------------------------

    final_damage = max(
        1,
        damage
        - st.session_state.monster_defense
    )

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
            int(st.session_state.attack) - 5
        ),
        int(st.session_state.attack) + 5
    )

    success = player_attack(
        damage,
        can_be_parried=True
    )

    if not success:
        return

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

    # 강공격 명중률 60%
    if random.random() > 0.6:

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )

        st.session_state.combo = 0

        monster_attack()

        return


    damage = random.randint(
        int(st.session_state.attack) + 15,
        int(st.session_state.attack) + 35
    )


    # 강공격은 패링 불가능
    success = player_attack(
        damage,
        can_be_parried=False
    )

    if not success:
        return


    final_damage = max(
        1,
        damage
        - st.session_state.monster_defense
    )

    st.session_state.message = (
        f"💥 강공격! "
        f"{final_damage} 피해!"
    )


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

    success_rate = 40

    if random.randint(
        1,
        100
    ) <= success_rate:

        counter_damage = random.randint(
            int(st.session_state.attack),
            int(st.session_state.attack) + 20
        )

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
# 체력 물약
#
# 물약 사용 시 몬스터 공격 없음
# ==========================================

def use_hp_potion():

    if st.session_state.hp_potion <= 0:

        st.session_state.message = (
            "🧪 체력 물약이 없습니다!"
        )

        return


    if st.session_state.hp >= st.session_state.max_hp:

        st.session_state.message = (
            "❤️ HP가 가득합니다!"
        )

        return


    st.session_state.hp_potion -= 1

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.max_hp,
        st.session_state.hp + 50
    )

    actual = (
        st.session_state.hp - old_hp
    )

    # 공격받지 않음
    st.session_state.message = (
        f"🧪 체력 물약 사용! "
        f"❤️ HP +{actual}"
    )


# ==========================================
# 공격력 물약
#
# 현재 공격력의 30% 증가
# ==========================================

def use_attack_potion():

    if st.session_state.attack_potion <= 0:

        st.session_state.message = (
            "⚔️ 힘의 물약이 없습니다!"
        )

        return


    st.session_state.attack_potion -= 1

    old_attack = st.session_state.attack

    increase = old_attack * 0.30

    st.session_state.attack += increase

    st.session_state.potion_attack_bonus += increase

    st.session_state.message = (
        f"⚔️ 힘의 물약 사용! "
        f"공격력 +{nice_number(increase)}"
    )


# ==========================================
# 방어력 물약
#
# 현재 방어력의 30% 증가
# ==========================================

def use_defense_potion():

    if st.session_state.defense_potion <= 0:

        st.session_state.message = (
            "🛡️ 방어의 물약이 없습니다!"
        )

        return


    st.session_state.defense_potion -= 1

    old_defense = st.session_state.defense

    increase = old_defense * 0.30

    st.session_state.defense += increase

    st.session_state.potion_defense_bonus += increase

    st.session_state.message = (
        f"🛡️ 방어의 물약 사용! "
        f"방어력 +{nice_number(increase)}"
    )


# ==========================================
# 회피율 물약
#
# 현재 회피율의 30% 증가
# ==========================================

def use_evasion_potion():

    if st.session_state.evasion_potion <= 0:

        st.session_state.message = (
            "💨 민첩의 물약이 없습니다!"
        )

        return


    # 최대 60%
    if st.session_state.evasion >= 60:

        st.session_state.message = (
            "💨 회피율이 이미 최대입니다!"
        )

        return


    st.session_state.evasion_potion -= 1

    old_evasion = st.session_state.evasion

    increase = old_evasion * 0.30

    new_evasion = min(
        60,
        old_evasion + increase
    )

    actual_increase = (
        new_evasion - old_evasion
    )

    st.session_state.evasion = new_evasion

    st.session_state.potion_evasion_bonus += (
        actual_increase
    )

    st.session_state.message = (
        f"💨 민첩의 물약 사용! "
        f"회피율 +{nice_number(actual_increase)}%"
    )


# ==========================================
# 몬스터 처치
# ==========================================

def monster_defeated():

    was_boss = st.session_state.is_boss


    # --------------------------------------
    # 골드 보상
    # --------------------------------------

    if was_boss:

        reward = random.randint(
            200,
            350
        )

        st.session_state.boss_kill += 1

        # 보스 보너스
        st.session_state.max_hp += 30
        st.session_state.attack += 10

        st.session_state.hp = (
            st.session_state.max_hp
        )

    else:

        reward = random.randint(
            30,
            60
        )


    st.session_state.gold += reward

    # --------------------------------------
    # 처치 기록
    # --------------------------------------

    st.session_state.kill += 1

    st.session_state.combo += 1

    # --------------------------------------
    # 랜덤 EXP
    # --------------------------------------

    exp_amount = random.randint(
        st.session_state.monster_exp_min,
        st.session_state.monster_exp_max
    )

    level_up = gain_exp(
        exp_amount
    )

    # --------------------------------------
    # 메시지
    # --------------------------------------

    if was_boss:

        st.session_state.message = (
            f"👑 보스 처치! "
            f"💰 +{reward}G "
            f"⭐ EXP +{exp_amount}"
        )

    else:

        st.session_state.message = (
            f"🎉 {st.session_state.monster_name} "
            f"처치! "
            f"💰 +{reward}G "
            f"⭐ EXP +{exp_amount}"
        )


    if level_up:

        st.session_state.message += (
            f" 🎉 LEVEL UP! "
            f"Lv.{st.session_state.level}"
        )


    st.session_state.defending = False

    # 새로운 몬스터
    spawn_monster()


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
        60,
        st.session_state.evasion + 3
    )

    st.session_state.message = (
        "👟 신발 강화 성공! "
        "회피율 +3%"
    )


# ==========================================
# 초기 실행
# ==========================================

if "hp" not in st.session_state:

    reset_game()


# ==========================================
# 제목
# ==========================================

st.title("⚔️ 미니 RPG")

st.caption(
    "공격 · 방어 · 회피 · 패링 · 물약으로 "
    "몬스터와 보스를 쓰러뜨리세요!"
)


# ==========================================
# 기본 정보
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "❤️ HP",
        f"{nice_number(st.session_state.hp)}/"
        f"{nice_number(st.session_state.max_hp)}"
    )

with col2:

    st.metric(
        "⭐ LEVEL",
        st.session_state.level
    )

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
# HP 바
# ==========================================

st.progress(
    max(
        0.0,
        min(
            1.0,
            st.session_state.hp
            / st.session_state.max_hp
        )
    )
)


# ==========================================
# 플레이어 스탯
# ==========================================

st.subheader("📊 플레이어 스탯")

col1, col2, col3 = st.columns(3)


with col1:

    attack_bonus = (
        st.session_state.potion_attack_bonus
    )

    if attack_bonus > 0:

        attack_label = (
            f"{nice_number(st.session_state.attack)} "
            f"(+{nice_number(attack_bonus)})"
        )

    else:

        attack_label = nice_number(
            st.session_state.attack
        )

    st.metric(
        "⚔️ 공격력",
        attack_label
    )


with col2:

    defense_bonus = (
        st.session_state.potion_defense_bonus
    )

    if defense_bonus > 0:

        defense_label = (
            f"{nice_number(st.session_state.defense)} "
            f"(+{nice_number(defense_bonus)})"
        )

    else:

        defense_label = nice_number(
            st.session_state.defense
        )

    st.metric(
        "🛡️ 방어력",
        defense_label
    )


with col3:

    evasion_bonus = (
        st.session_state.potion_evasion_bonus
    )

    if evasion_bonus > 0:

        evasion_label = (
            f"{nice_number(st.session_state.evasion)}% "
            f"(+{nice_number(evasion_bonus)}%)"
        )

    else:

        evasion_label = (
            f"{nice_number(st.session_state.evasion)}%"
        )

    st.metric(
        "💨 회피율",
        evasion_label
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
# 몬스터 정보
# ==========================================

st.subheader(
    st.session_state.monster_name
)

st.write(
    f"❤️ HP: "
    f"{nice_number(st.session_state.monster_hp)}/"
    f"{nice_number(st.session_state.monster_max_hp)}"
)

st.progress(
    max(
        0.0,
        min(
            1.0,
            st.session_state.monster_hp
            / st.session_state.monster_max_hp
        )
    )
)


# ==========================================
# 적 스탯
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
    f"⭐ 처치 EXP: "
    f"{st.session_state.monster_exp_min}"
    f" ~ "
    f"{st.session_state.monster_exp_max}"
)


# ==========================================
# 전투 메시지
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
            "💥 강공격",
            help="강공격은 적의 패링을 무시합니다.",
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
            "⚡ 패링",
            help="40% 확률로 공격을 막고 반격합니다.",
            use_container_width=True
        ):

            parry()
            st.rerun()


    # ======================================
    # 물약
    # ======================================

    st.subheader("🧪 물약")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            f"❤️ 체력 물약 "
            f"({st.session_state.hp_potion})",
            use_container_width=True
        ):

            use_hp_potion()
            st.rerun()


        if st.button(
            f"⚔️ 힘의 물약 "
            f"({st.session_state.attack_potion})",
            use_container_width=True
        ):

            use_attack_potion()
            st.rerun()


    with col2:

        if st.button(
            f"🛡️ 방어의 물약 "
            f"({st.session_state.defense_potion})",
            use_container_width=True
        ):

            use_defense_potion()
            st.rerun()


        if st.button(
            f"💨 민첩의 물약 "
            f"({st.session_state.evasion_potion})",
            use_container_width=True
        ):

            use_evasion_potion()
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
        f"{nice_number(st.session_state.attack)}"
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
        f"{nice_number(st.session_state.defense)}"
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
        f"{nice_number(st.session_state.evasion)}%"
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

st.subheader("🏪 물약 상점")

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "❤️ 체력 물약 구매 - 20G",
        use_container_width=True
    ):

        if st.session_state.gold >= 20:

            st.session_state.gold -= 20

            st.session_state.hp_potion += 1

            st.session_state.message = (
                "❤️ 체력 물약을 구매했습니다!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


    if st.button(
        "⚔️ 힘의 물약 구매 - 60G",
        use_container_width=True
    ):

        if st.session_state.gold >= 60:

            st.session_state.gold -= 60

            st.session_state.attack_potion += 1

            st.session_state.message = (
                "⚔️ 힘의 물약을 구매했습니다!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


with col2:

    if st.button(
        "🛡️ 방어의 물약 구매 - 60G",
        use_container_width=True
    ):

        if st.session_state.gold >= 60:

            st.session_state.gold -= 60

            st.session_state.defense_potion += 1

            st.session_state.message = (
                "🛡️ 방어의 물약을 구매했습니다!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


    if st.button(
        "💨 민첩의 물약 구매 - 70G",
        use_container_width=True
    ):

        if st.session_state.gold >= 70:

            st.session_state.gold -= 70

            st.session_state.evasion_potion += 1

            st.session_state.message = (
                "💨 민첩의 물약을 구매했습니다!"
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
