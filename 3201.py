import streamlit as st
import random


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="3201 Mini RPG",
    page_icon="⚔️",
    layout="centered"
)


# =========================================================
# 몬스터 데이터
# 이름, HP, 공격력, 방어력, 회피율, 패링율
# =========================================================

NORMAL_MONSTERS = [
    ("🟢 슬라임", 40, 7, 2, 5, 5),
    ("🐀 거대 쥐", 45, 8, 2, 8, 6),
    ("🦇 박쥐", 50, 9, 3, 12, 5),
    ("👺 고블린", 60, 11, 4, 8, 10),
    ("🐺 늑대", 70, 13, 4, 12, 8),
    ("🕷️ 거대 거미", 80, 14, 5, 12, 12),
    ("💀 해골 전사", 95, 16, 7, 5, 18),
    ("👻 유령", 100, 18, 5, 20, 10),
    ("🧟 좀비", 110, 19, 8, 3, 15),
    ("🧙 다크 메이지", 120, 22, 7, 15, 18),
    ("🦂 독전갈", 130, 23, 8, 18, 16),
    ("🧛 뱀파이어", 145, 25, 10, 20, 22),
]


# =========================================================
# 보스
# 10 / 20 / 30 / 40 / 50 / 60 / 70
# =========================================================

BOSSES = [
    ("👑 오크 대장", 250, 28, 14, 12, 28),
    ("🔥 불의 마왕", 320, 32, 17, 15, 32),
    ("❄️ 얼음 여왕", 350, 35, 19, 20, 35),
    ("⚡ 번개의 군주", 380, 38, 21, 25, 38),
    ("💀 죽음의 기사", 420, 42, 24, 15, 42),
    ("🐉 고대 드래곤", 500, 50, 28, 20, 48),
    ("🌑 마왕 아르카논", 700, 65, 35, 25, 60),
]


BOSS_SCHEDULE = {
    10: 0,
    20: 1,
    30: 2,
    40: 3,
    50: 4,
    60: 5,
    70: 6,
}


# =========================================================
# 숫자 표시
# =========================================================

def fmt(value):
    if isinstance(value, int):
        return str(value)

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.1f}"


# =========================================================
# 현재 스탯
# =========================================================

def attack_stat():
    return (
        st.session_state.base_attack
        + st.session_state.attack_bonus
    )


def defense_stat():
    return (
        st.session_state.base_defense
        + st.session_state.defense_bonus
    )


def evasion_stat():
    return min(
        60,
        st.session_state.base_evasion
        + st.session_state.evasion_bonus
    )


# =========================================================
# 필요 경험치
# =========================================================

def required_exp():
    return 100 + (st.session_state.level - 1) * 50


# =========================================================
# 경험치 획득
# =========================================================

def gain_exp(amount):

    st.session_state.exp += amount

    level_up = False

    while st.session_state.exp >= required_exp():

        st.session_state.exp -= required_exp()

        st.session_state.level += 1

        level_up = True

        # HP는 증가시키지 않음
        st.session_state.base_attack += 5
        st.session_state.base_defense += 2

    return level_up


# =========================================================
# 게임 초기화
# =========================================================

def reset_game():

    # 플레이어 기본 능력치
    st.session_state.base_max_hp = 200
    st.session_state.hp = 200

    # 요청한 초기 능력치
    st.session_state.base_attack = 50
    st.session_state.base_defense = 15
    st.session_state.base_evasion = 15

    # 물약 임시 보너스
    st.session_state.attack_bonus = 0
    st.session_state.defense_bonus = 0
    st.session_state.evasion_bonus = 0

    st.session_state.attack_turns = 0
    st.session_state.defense_turns = 0
    st.session_state.evasion_turns = 0

    # 레벨 / EXP
    st.session_state.level = 1
    st.session_state.exp = 0

    # 골드
    st.session_state.gold = 300

    # Wave
    st.session_state.kill = 0

    # 보스
    st.session_state.boss_kill = 0
    st.session_state.boss_stages_cleared = []

    # 장비
    st.session_state.weapon_level = 1
    st.session_state.armor_level = 1
    st.session_state.boots_level = 1

    # 물약
    st.session_state.hp_potion = 3
    st.session_state.attack_potion = 1
    st.session_state.defense_potion = 1
    st.session_state.evasion_potion = 1

    # 전투
    st.session_state.defending = False
    st.session_state.game_over = False

    # 강공격 쿨타임
    st.session_state.strong_attack_cooldown = 0

    # 메시지
    st.session_state.message = "⚔️ 모험을 시작합니다!"

    # 몬스터 데이터
    st.session_state.monster_name = ""
    st.session_state.monster_hp = 0
    st.session_state.monster_max_hp = 0
    st.session_state.monster_damage = 0
    st.session_state.monster_defense = 0
    st.session_state.monster_evasion = 0
    st.session_state.monster_parry = 0

    st.session_state.monster_exp_min = 0
    st.session_state.monster_exp_max = 0

    st.session_state.is_boss = False

    # 첫 몬스터
    spawn_monster()


# =========================================================
# 랜덤 이벤트
# 일반 Wave에서만 8%
# 보스 Wave에서는 발생하지 않음
# =========================================================

def random_event():

    wave = st.session_state.kill + 1

    # 보스 Wave
    if wave in BOSS_SCHEDULE:
        return

    # 8% 확률
    if random.random() > 0.08:
        return

    event = random.choice([
        "gold",
        "potion",
        "fountain",
        "blessing",
        "ambush",
        "luck",
    ])

    # -----------------------------------------
    # 보물
    # -----------------------------------------

    if event == "gold":

        gold = random.randint(50, 120)

        st.session_state.gold += gold

        st.session_state.message = (
            f"💰 이벤트 발생!\n\n"
            f"숨겨진 보물을 발견했습니다!\n"
            f"+{gold}G"
        )

    # -----------------------------------------
    # 랜덤 물약
    # -----------------------------------------

    elif event == "potion":

        potion = random.choice([
            "hp",
            "attack",
            "defense",
            "evasion",
        ])

        if potion == "hp":

            st.session_state.hp_potion += 1
            name = "❤️ 체력 물약"

        elif potion == "attack":

            st.session_state.attack_potion += 1
            name = "⚔️ 힘의 물약"

        elif potion == "defense":

            st.session_state.defense_potion += 1
            name = "🛡️ 방어의 물약"

        else:

            st.session_state.evasion_potion += 1
            name = "💨 민첩의 물약"

        st.session_state.message = (
            f"🧪 이벤트 발생!\n\n"
            f"{name}을 발견했습니다!"
        )

    # -----------------------------------------
    # 회복의 샘
    # -----------------------------------------

    elif event == "fountain":

        heal = int(
            st.session_state.base_max_hp * 0.20
        )

        old_hp = st.session_state.hp

        st.session_state.hp = min(
            st.session_state.base_max_hp,
            st.session_state.hp + heal
        )

        actual = st.session_state.hp - old_hp

        st.session_state.message = (
            f"💧 회복의 샘을 발견했습니다!\n"
            f"❤️ +{actual} HP"
        )

    # -----------------------------------------
    # 전투의 축복
    # -----------------------------------------

    elif event == "blessing":

        bonus = int(attack_stat() * 0.10)

        st.session_state.attack_bonus = bonus
        st.session_state.attack_turns = 5

        st.session_state.message = (
            f"⚔️ 전투의 축복!\n"
            f"공격력 +{bonus}\n"
            f"(5턴)"
        )

    # -----------------------------------------
    # 기습
    # -----------------------------------------

    elif event == "ambush":

        damage = random.randint(5, 15)

        damage = max(
            1,
            damage - int(defense_stat())
        )

        st.session_state.hp -= damage

        st.session_state.message = (
            f"👻 기습을 당했습니다!\n"
            f"💔 {damage} 피해"
        )

    # -----------------------------------------
    # 행운
    # -----------------------------------------

    elif event == "luck":

        gold = random.randint(30, 80)
        exp = random.randint(20, 50)

        st.session_state.gold += gold

        level_up = gain_exp(exp)

        st.session_state.message = (
            f"🍀 행운의 이벤트!\n"
            f"💰 +{gold}G\n"
            f"⭐ +{exp} EXP"
        )

        if level_up:
            st.session_state.message += (
                f"\n🎉 LEVEL UP! "
                f"Lv.{st.session_state.level}"
            )

    if st.session_state.hp <= 0:

        st.session_state.hp = 0
        st.session_state.game_over = True


# =========================================================
# 몬스터 생성
# =========================================================

def spawn_monster():

    wave = st.session_state.kill + 1

    # =====================================================
    # 보스
    # =====================================================

    if wave in BOSS_SCHEDULE:

        index = BOSS_SCHEDULE[wave]

        name, hp, damage, defense, evasion, parry = (
            BOSSES[index]
        )

        # 레벨에 따른 보스 강화
        level_scale = st.session_state.level - 1

        hp += level_scale * 20
        damage += level_scale * 3
        defense += level_scale * 2

        st.session_state.is_boss = True

        st.session_state.monster_name = name
        st.session_state.monster_hp = int(hp)
        st.session_state.monster_max_hp = int(hp)
        st.session_state.monster_damage = int(damage)
        st.session_state.monster_defense = int(defense)
        st.session_state.monster_evasion = evasion
        st.session_state.monster_parry = parry

        st.session_state.monster_exp_min = (
            150 + index * 50
        )

        st.session_state.monster_exp_max = (
            250 + index * 70
        )

        return

    # =====================================================
    # 일반 몬스터
    # =====================================================

    name, hp, damage, defense, evasion, parry = (
        random.choice(NORMAL_MONSTERS)
    )

    # Wave가 올라갈수록 강화
    hp += wave * 3
    damage += wave * 0.45
    defense += wave * 0.20
    evasion += wave * 0.08
    parry += wave * 0.08

    # 플레이어 레벨에 따른 강화
    level_scale = st.session_state.level - 1

    hp += level_scale * 8
    damage += level_scale * 2
    defense += level_scale
    evasion += level_scale * 0.5
    parry += level_scale * 0.3

    evasion = min(55, evasion)
    parry = min(60, parry)

    st.session_state.is_boss = False

    st.session_state.monster_name = name
    st.session_state.monster_hp = int(hp)
    st.session_state.monster_max_hp = int(hp)
    st.session_state.monster_damage = int(damage)
    st.session_state.monster_defense = int(defense)
    st.session_state.monster_evasion = round(evasion, 1)
    st.session_state.monster_parry = round(parry, 1)

    # 보스 처치 수에 따라 보상 증가
    boss_bonus = st.session_state.boss_kill

    st.session_state.monster_exp_min = (
        20
        + st.session_state.level * 4
        + boss_bonus * 15
        + wave // 3
    )

    st.session_state.monster_exp_max = (
        45
        + st.session_state.level * 7
        + boss_bonus * 25
        + wave // 2
    )

    # 일반 Wave에만 이벤트
    random_event()


# =========================================================
# 턴 처리
# =========================================================

def advance_turn():

    # 강공격 쿨타임
    if st.session_state.strong_attack_cooldown > 0:

        st.session_state.strong_attack_cooldown -= 1

    # 공격력 물약
    if st.session_state.attack_turns > 0:

        st.session_state.attack_turns -= 1

        if st.session_state.attack_turns <= 0:

            st.session_state.attack_turns = 0
            st.session_state.attack_bonus = 0

    # 방어력 물약
    if st.session_state.defense_turns > 0:

        st.session_state.defense_turns -= 1

        if st.session_state.defense_turns <= 0:

            st.session_state.defense_turns = 0
            st.session_state.defense_bonus = 0

    # 회피율 물약
    if st.session_state.evasion_turns > 0:

        st.session_state.evasion_turns -= 1

        if st.session_state.evasion_turns <= 0:

            st.session_state.evasion_turns = 0
            st.session_state.evasion_bonus = 0


# =========================================================
# 몬스터 공격
# =========================================================

def monster_attack():

    if st.session_state.game_over:
        return

    # 플레이어 회피
    if random.random() * 100 < evasion_stat():

        st.session_state.message = (
            f"💨 공격을 회피했습니다! "
            f"({fmt(evasion_stat())}%)"
        )

        st.session_state.defending = False

        advance_turn()

        return

    damage = random.randint(
        max(
            1,
            int(st.session_state.monster_damage) - 5
        ),
        int(st.session_state.monster_damage) + 5
    )

    # 보스 공격
    if st.session_state.is_boss:

        if random.random() < 0.20:

            damage *= 2

            st.session_state.message = (
                f"💀 보스 필살기!\n"
                f"💥 {damage} 피해!"
            )

        else:

            st.session_state.message = (
                "👑 보스의 공격!"
            )

    else:

        st.session_state.message = (
            f"👾 "
            f"{st.session_state.monster_name}의 공격!"
        )

    # 방어력 적용
    damage = max(
        1,
        int(damage - defense_stat())
    )

    # 방어 중이면 60% 감소
    if st.session_state.defending:

        damage = max(
            1,
            int(damage * 0.4)
        )

        st.session_state.message += (
            " 🛡️ 방어 성공!"
        )

    st.session_state.defending = False

    st.session_state.hp -= damage

    st.session_state.message += (
        f" 💔 {damage} 피해"
    )

    advance_turn()

    if st.session_state.hp <= 0:

        st.session_state.hp = 0
        st.session_state.game_over = True


# =========================================================
# 플레이어 공격 판정
# =========================================================

def player_attack(damage, can_be_parried=True):

    # 적 회피
    if random.random() * 100 < (
        st.session_state.monster_evasion
    ):

        st.session_state.message = (
            f"💨 "
            f"{st.session_state.monster_name} "
            f"회피 성공!"
        )

        monster_attack()

        return False

    # 적 패링
    if can_be_parried:

        if random.random() * 100 < (
            st.session_state.monster_parry
        ):

            counter = random.randint(
                max(
                    1,
                    int(st.session_state.monster_damage) - 5
                ),
                int(st.session_state.monster_damage) + 5
            )

            counter = max(
                1,
                int(counter - defense_stat())
            )

            st.session_state.hp -= counter

            st.session_state.message = (
                f"⚡ "
                f"{st.session_state.monster_name} "
                f"패링 성공!\n"
                f"💥 {counter} 반격 피해!"
            )

            advance_turn()

            if st.session_state.hp <= 0:

                st.session_state.hp = 0
                st.session_state.game_over = True

            return False

    # 적 방어력 적용
    final_damage = max(
        1,
        int(
            damage
            - st.session_state.monster_defense
        )
    )

    st.session_state.monster_hp -= final_damage

    st.session_state.message = (
        f"⚔️ {final_damage} 피해!"
    )

    return True


# =========================================================
# 몬스터 처치
# =========================================================

def monster_defeated():

    was_boss = st.session_state.is_boss

    # -----------------------------------------
    # 보상
    # -----------------------------------------

    if was_boss:

        wave = st.session_state.kill + 1

        boss_index = BOSS_SCHEDULE.get(wave)

        if (
            boss_index is not None
            and boss_index
            not in st.session_state.boss_stages_cleared
        ):

            st.session_state.boss_stages_cleared.append(
                boss_index
            )

            st.session_state.boss_kill += 1

        gold = random.randint(250, 400)

        gold += st.session_state.boss_kill * 75

        st.session_state.base_attack += 10
        st.session_state.base_defense += 3

        st.session_state.message = (
            f"👑 BOSS 처치!\n"
            f"💰 +{gold}G"
        )

    else:

        gold = random.randint(40, 70)

        # 보스 잡은 만큼 보상 증가
        gold += st.session_state.boss_kill * 30

        gold += st.session_state.kill // 5

        st.session_state.message = (
            f"🎉 "
            f"{st.session_state.monster_name} "
            f"처치!\n"
            f"💰 +{gold}G"
        )

    st.session_state.gold += gold

    # -----------------------------------------
    # EXP
    # -----------------------------------------

    exp = random.randint(
        int(st.session_state.monster_exp_min),
        int(st.session_state.monster_exp_max)
    )

    if not was_boss:

        exp += st.session_state.boss_kill * 15

    level_up = gain_exp(exp)

    st.session_state.message += (
        f"\n⭐ EXP +{exp}"
    )

    if level_up:

        st.session_state.message += (
            f"\n🎉 LEVEL UP!"
            f" Lv.{st.session_state.level}"
        )

    # -----------------------------------------
    # 처치 후 HP 회복
    # 일반 15%, 보스 25%
    # -----------------------------------------

    if was_boss:
        rate = 0.25
    else:
        rate = 0.15

    recovery = int(
        st.session_state.base_max_hp * rate
    )

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.base_max_hp,
        st.session_state.hp + recovery
    )

    actual_recovery = (
        st.session_state.hp - old_hp
    )

    st.session_state.message += (
        f"\n❤️ 처치 보상 회복 "
        f"+{actual_recovery} HP"
    )

    # -----------------------------------------
    # 다음 Wave
    # -----------------------------------------

    st.session_state.kill += 1

    st.session_state.defending = False

    spawn_monster()


# =========================================================
# 일반 공격
# =========================================================

def attack():

    damage = random.randint(
        max(
            1,
            int(attack_stat()) - 5
        ),
        int(attack_stat()) + 5
    )

    success = player_attack(
        damage,
        True
    )

    if not success:
        return

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

    else:

        monster_attack()


# =========================================================
# 강공격
# 70% 성공
# 패링 불가능
# 사용 후 1턴 쿨타임
# =========================================================

def strong_attack():

    if st.session_state.strong_attack_cooldown > 0:

        st.session_state.message = (
            f"💥 강공격 쿨타임!"
            f" {st.session_state.strong_attack_cooldown}턴"
        )

        return

    # 70% 성공
    if random.random() > 0.70:

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )

        # 사용하면 다음 1턴 동안 사용 불가
        st.session_state.strong_attack_cooldown = 1

        monster_attack()

        return

    damage = random.randint(
        int(attack_stat()) + 15,
        int(attack_stat()) + 35
    )

    # 강공격은 패링 불가능
    success = player_attack(
        damage,
        False
    )

    # 다음 1턴 쿨타임
    st.session_state.strong_attack_cooldown = 1

    if not success:
        return

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

    else:

        monster_attack()


# =========================================================
# 패링
# =========================================================

def parry():

    # 플레이어 패링 성공 확률
    success_rate = 40

    if random.random() * 100 < success_rate:

        damage = random.randint(
            int(attack_stat()),
            int(attack_stat()) + 20
        )

        damage = max(
            1,
            int(
                damage
                - st.session_state.monster_defense
            )
        )

        st.session_state.monster_hp -= damage

        st.session_state.message = (
            f"⚡ PARRY 성공!\n"
            f"💥 {damage} 반격 피해!"
        )

        advance_turn()

        if st.session_state.monster_hp <= 0:

            st.session_state.monster_hp = 0

            monster_defeated()

    else:

        st.session_state.message = (
            "❌ 패링 실패!"
        )

        monster_attack()


# =========================================================
# 방어
# =========================================================

def defend():

    st.session_state.defending = True

    monster_attack()


# =========================================================
# 체력 물약
# 사용한 턴에는 공격받지 않음
# =========================================================

def use_hp_potion():

    if st.session_state.hp_potion <= 0:

        st.session_state.message = (
            "🧪 체력 물약이 없습니다!"
        )

        return

    if st.session_state.hp >= (
        st.session_state.base_max_hp
    ):

        st.session_state.message = (
            "❤️ HP가 이미 가득합니다!"
        )

        return

    st.session_state.hp_potion -= 1

    old_hp = st.session_state.hp

    # 최대 HP의 30%
    heal = int(
        st.session_state.base_max_hp * 0.30
    )

    st.session_state.hp = min(
        st.session_state.base_max_hp,
        st.session_state.hp + heal
    )

    actual = st.session_state.hp - old_hp

    st.session_state.message = (
        f"🧪 체력 물약 사용!\n"
        f"❤️ +{actual} HP"
    )

    # 물약 사용 턴에는 몬스터 공격 X
    advance_turn()


# =========================================================
# 공격력 물약
# 현재 스탯의 30%
# 5턴
# =========================================================

def use_attack_potion():

    if st.session_state.attack_potion <= 0:

        st.session_state.message = (
            "⚔️ 힘의 물약이 없습니다!"
        )

        return

    st.session_state.attack_potion -= 1

    bonus = attack_stat() * 0.30

    st.session_state.attack_bonus = bonus
    st.session_state.attack_turns = 5

    st.session_state.message = (
        f"⚔️ 힘의 물약 사용!\n"
        f"+{fmt(bonus)} 공격력\n"
        f"(5턴)"
    )

    advance_turn()


# =========================================================
# 방어력 물약
# 현재 스탯의 30%
# 5턴
# =========================================================

def use_defense_potion():

    if st.session_state.defense_potion <= 0:

        st.session_state.message = (
            "🛡️ 방어의 물약이 없습니다!"
        )

        return

    st.session_state.defense_potion -= 1

    bonus = defense_stat() * 0.30

    st.session_state.defense_bonus = bonus
    st.session_state.defense_turns = 5

    st.session_state.message = (
        f"🛡️ 방어의 물약 사용!\n"
        f"+{fmt(bonus)} 방어력\n"
        f"(5턴)"
    )

    advance_turn()


# =========================================================
# 회피율 물약
# 현재 회피율의 30%
# 5턴
# =========================================================

def use_evasion_potion():

    if st.session_state.evasion_potion <= 0:

        st.session_state.message = (
            "💨 민첩의 물약이 없습니다!"
        )

        return

    current = evasion_stat()

    if current >= 60:

        st.session_state.message = (
            "💨 회피율이 최대입니다!"
        )

        return

    st.session_state.evasion_potion -= 1

    bonus = current * 0.30

    bonus = min(
        bonus,
        60 - st.session_state.base_evasion
    )

    st.session_state.evasion_bonus = bonus
    st.session_state.evasion_turns = 5

    st.session_state.message = (
        f"💨 민첩의 물약 사용!\n"
        f"+{fmt(bonus)}% 회피율\n"
        f"(5턴)"
    )

    advance_turn()


# =========================================================
# 장비 강화
# =========================================================

def upgrade_weapon():

    cost = st.session_state.weapon_level * 50

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost
    st.session_state.weapon_level += 1
    st.session_state.base_attack += 10

    st.session_state.message = (
        "🗡️ 무기 강화 성공!\n"
        "공격력 +10"
    )


def upgrade_armor():

    cost = st.session_state.armor_level * 60

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost
    st.session_state.armor_level += 1
    st.session_state.base_defense += 4

    st.session_state.message = (
        "🛡️ 방어구 강화 성공!\n"
        "방어력 +4"
    )


def upgrade_boots():

    cost = st.session_state.boots_level * 70

    if st.session_state.gold < cost:

        st.session_state.message = (
            "💰 골드가 부족합니다!"
        )

        return

    st.session_state.gold -= cost
    st.session_state.boots_level += 1

    st.session_state.base_evasion = min(
        60,
        st.session_state.base_evasion + 3
    )

    st.session_state.message = (
        "👟 신발 강화 성공!\n"
        "회피율 +3%"
    )


# =========================================================
# 최초 실행
# =========================================================

if "base_attack" not in st.session_state:

    reset_game()


# =========================================================
# UI
# =========================================================

st.title("⚔️ 3201 Mini RPG")

st.caption(
    "공격 · 강공격 · 방어 · 패링 · 회피 · 물약 · 이벤트 · 보스"
)


wave = st.session_state.kill + 1


# =========================================================
# 상단 정보
# =========================================================

st.header(f"🌊 Wave {wave}")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "❤️ HP",
        f"{fmt(st.session_state.hp)} / "
        f"{fmt(st.session_state.base_max_hp)}"
    )


with col2:

    st.metric(
        "⭐ LEVEL",
        st.session_state.level
    )

    st.caption(
        f"EXP "
        f"{st.session_state.exp} / "
        f"{required_exp()}"
    )


with col3:

    st.metric(
        "💰 GOLD",
        st.session_state.gold
    )


with col4:

    st.metric(
        "👑 BOSS",
        f"{st.session_state.boss_kill} / 7"
    )


# =========================================================
# HP 바
# =========================================================

st.progress(
    max(
        0.0,
        min(
            1.0,
            st.session_state.hp
            / st.session_state.base_max_hp
        )
    )
)


# =========================================================
# 다음 보스
# =========================================================

next_boss = None

for boss_wave in BOSS_SCHEDULE:

    if boss_wave >= wave:

        next_boss = boss_wave

        break


if next_boss:

    if next_boss == wave:

        st.warning(
            f"👑 Wave {wave} BOSS!"
        )

    else:

        st.caption(
            f"⚠️ 다음 보스: Wave {next_boss}"
        )

else:

    st.success(
        "🏆 모든 보스를 처치했습니다!"
    )


# =========================================================
# 플레이어 스탯
# =========================================================

st.subheader("📊 플레이어 스탯")


col1, col2, col3 = st.columns(3)


with col1:

    attack_text = fmt(attack_stat())

    if st.session_state.attack_turns > 0:

        attack_text += (
            f" (+{fmt(st.session_state.attack_bonus)})"
            f" [{st.session_state.attack_turns}턴]"
        )

    st.metric(
        "⚔️ 공격력",
        attack_text
    )


with col2:

    defense_text = fmt(defense_stat())

    if st.session_state.defense_turns > 0:

        defense_text += (
            f" (+{fmt(st.session_state.defense_bonus)})"
            f" [{st.session_state.defense_turns}턴]"
        )

    st.metric(
        "🛡️ 방어력",
        defense_text
    )


with col3:

    evasion_text = (
        f"{fmt(evasion_stat())}%"
    )

    if st.session_state.evasion_turns > 0:

        evasion_text += (
            f" (+{fmt(st.session_state.evasion_bonus)}%)"
            f" [{st.session_state.evasion_turns}턴]"
        )

    st.metric(
        "💨 회피율",
        evasion_text
    )


st.divider()


# =========================================================
# 몬스터
# =========================================================

if st.session_state.is_boss:

    st.error("👑⚠️ BOSS BATTLE ⚠️👑")


st.subheader(
    st.session_state.monster_name
)


st.write(
    f"❤️ HP: "
    f"{fmt(st.session_state.monster_hp)} / "
    f"{fmt(st.session_state.monster_max_hp)}"
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


# =========================================================
# 적 스탯
# =========================================================

st.subheader("👾 적 스탯")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⚔️ 공격",
        fmt(st.session_state.monster_damage)
    )


with col2:

    st.metric(
        "🛡️ 방어",
        fmt(st.session_state.monster_defense)
    )


with col3:

    st.metric(
        "💨 회피",
        f"{fmt(st.session_state.monster_evasion)}%"
    )


with col4:

    st.metric(
        "⚡ 패링",
        f"{fmt(st.session_state.monster_parry)}%"
    )


st.caption(
    f"⭐ EXP: "
    f"{fmt(st.session_state.monster_exp_min)}"
    f" ~ "
    f"{fmt(st.session_state.monster_exp_max)}"
)


st.info(
    st.session_state.message
)


# =========================================================
# 전투 버튼
# =========================================================

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

        cooldown = (
            st.session_state.strong_attack_cooldown
        )

        if cooldown > 0:

            text = (
                f"💥 강공격 "
                f"[{cooldown}턴 쿨타임]"
            )

        else:

            text = "💥 강공격 (70%)"


        if st.button(
            text,
            disabled=cooldown > 0,
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
            use_container_width=True
        ):

            parry()
            st.rerun()


    # =====================================================
    # 물약
    # =====================================================

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


# =========================================================
# 장비 상점
# =========================================================

st.divider()

st.subheader("🛒 장비 상점")


col1, col2, col3 = st.columns(3)


with col1:

    cost = st.session_state.weapon_level * 50

    st.write(
        f"🗡️ 무기 Lv."
        f"{st.session_state.weapon_level}"
    )

    st.write(
        f"기본 공격력: "
        f"{fmt(st.session_state.base_attack)}"
    )

    if st.button(
        f"강화 {cost}G",
        key="weapon",
        use_container_width=True
    ):

        upgrade_weapon()
        st.rerun()


with col2:

    cost = st.session_state.armor_level * 60

    st.write(
        f"🛡️ 방어구 Lv."
        f"{st.session_state.armor_level}"
    )

    st.write(
        f"기본 방어력: "
        f"{fmt(st.session_state.base_defense)}"
    )

    if st.button(
        f"강화 {cost}G",
        key="armor",
        use_container_width=True
    ):

        upgrade_armor()
        st.rerun()


with col3:

    cost = st.session_state.boots_level * 70

    st.write(
        f"👟 신발 Lv."
        f"{st.session_state.boots_level}"
    )

    st.write(
        f"기본 회피율: "
        f"{fmt(st.session_state.base_evasion)}%"
    )

    if st.button(
        f"강화 {cost}G",
        key="boots",
        use_container_width=True
    ):

        upgrade_boots()
        st.rerun()


# =========================================================
# 물약 상점
# =========================================================

st.subheader("🏪 물약 상점")


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "❤️ 체력 물약 20G",
        use_container_width=True
    ):

        if st.session_state.gold >= 20:

            st.session_state.gold -= 20
            st.session_state.hp_potion += 1

            st.session_state.message = (
                "❤️ 체력 물약 구매!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


    if st.button(
        "⚔️ 힘의 물약 60G",
        use_container_width=True
    ):

        if st.session_state.gold >= 60:

            st.session_state.gold -= 60
            st.session_state.attack_potion += 1

            st.session_state.message = (
                "⚔️ 힘의 물약 구매!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


with col2:

    if st.button(
        "🛡️ 방어의 물약 60G",
        use_container_width=True
    ):

        if st.session_state.gold >= 60:

            st.session_state.gold -= 60
            st.session_state.defense_potion += 1

            st.session_state.message = (
                "🛡️ 방어의 물약 구매!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


    if st.button(
        "💨 민첩의 물약 70G",
        use_container_width=True
    ):

        if st.session_state.gold >= 70:

            st.session_state.gold -= 70
            st.session_state.evasion_potion += 1

            st.session_state.message = (
                "💨 민첩의 물약 구매!"
            )

        else:

            st.session_state.message = (
                "💰 골드가 부족합니다!"
            )

        st.rerun()


# =========================================================
# 게임 오버
# =========================================================

if st.session_state.game_over:

    st.divider()

    st.error("💀 GAME OVER")

    st.write(
        f"도달 Wave: {wave}"
    )

    st.write(
        f"보스 처치: "
        f"{st.session_state.boss_kill}/7"
    )

    st.write(
        f"최종 레벨: "
        f"{st.session_state.level}"
    )

    if st.button(
        "🔄 처음부터 다시 시작",
        use_container_width=True
    ):

        reset_game()
        st.rerun()
