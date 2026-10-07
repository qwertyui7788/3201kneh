import streamlit as st
import random


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="⚔️ Mini RPG",
    page_icon="⚔️",
    layout="centered"
)


# =========================================================
# 일반 몬스터
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
# Wave 10 / 20 / 30 / 40 / 50 / 60 / 70
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

def n(value):

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
# 필요 EXP
# =========================================================

def required_exp():
    return (
        100
        + (st.session_state.level - 1) * 50
    )


# =========================================================
# 물약 효과 턴 감소
# =========================================================

def decrease_potion_turns():

    if st.session_state.attack_turns > 0:

        st.session_state.attack_turns -= 1

        if st.session_state.attack_turns <= 0:

            st.session_state.attack_turns = 0
            st.session_state.attack_bonus = 0

            st.session_state.message += (
                " ⚔️ 힘의 물약 효과가 끝났습니다!"
            )


    if st.session_state.defense_turns > 0:

        st.session_state.defense_turns -= 1

        if st.session_state.defense_turns <= 0:

            st.session_state.defense_turns = 0
            st.session_state.defense_bonus = 0

            st.session_state.message += (
                " 🛡️ 방어의 물약 효과가 끝났습니다!"
            )


    if st.session_state.evasion_turns > 0:

        st.session_state.evasion_turns -= 1

        if st.session_state.evasion_turns <= 0:

            st.session_state.evasion_turns = 0
            st.session_state.evasion_bonus = 0

            st.session_state.message += (
                " 💨 민첩의 물약 효과가 끝났습니다!"
            )


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

        st.session_state.base_max_hp += 25
        st.session_state.base_attack += 6
        st.session_state.base_defense += 3

        st.session_state.base_evasion = min(
            60,
            st.session_state.base_evasion + 1
        )

        st.session_state.hp = (
            st.session_state.base_max_hp
        )

    return level_up


# =========================================================
# 처치 후 체력 회복
#
# 일반 몬스터 = 최대 HP의 15%
# 보스 = 최대 HP의 25%
# =========================================================

def recover_after_kill(is_boss):

    if is_boss:
        recover_rate = 0.25
    else:
        recover_rate = 0.15

    recover_amount = int(
        st.session_state.base_max_hp
        * recover_rate
    )

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.base_max_hp,
        st.session_state.hp + recover_amount
    )

    actual_recovery = (
        st.session_state.hp - old_hp
    )

    return actual_recovery


# =========================================================
# 게임 초기화
# =========================================================

def reset_game():

    # 기본 스탯
    st.session_state.base_max_hp = 150
    st.session_state.base_attack = 30
    st.session_state.base_defense = 8
    st.session_state.base_evasion = 15

    st.session_state.hp = 150

    # 물약 보너스
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

    # 물약
    st.session_state.hp_potion = 5
    st.session_state.attack_potion = 3
    st.session_state.defense_potion = 3
    st.session_state.evasion_potion = 3

    # Wave
    st.session_state.kill = 0

    # 보스
    st.session_state.boss_kill = 0
    st.session_state.boss_stages_cleared = []

    # 전투
    st.session_state.defending = False
    st.session_state.game_over = False

    # 장비
    st.session_state.weapon_level = 1
    st.session_state.armor_level = 1
    st.session_state.boots_level = 1

    st.session_state.message = (
        "⚔️ 모험을 시작했습니다!"
    )

    spawn_monster()


# =========================================================
# 몬스터 생성
# =========================================================

def spawn_monster():

    # 다음 Wave
    next_wave = st.session_state.kill + 1


    # =====================================================
    # 보스 Wave
    # =====================================================

    if next_wave in BOSS_SCHEDULE:

        boss_index = BOSS_SCHEDULE[next_wave]

        name, hp, damage, defense, evasion, parry = (
            BOSSES[boss_index]
        )

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
            150 + boss_index * 50
        )

        st.session_state.monster_exp_max = (
            250 + boss_index * 70
        )

        return


    # =====================================================
    # 일반 몬스터
    # =====================================================

    name, hp, damage, defense, evasion, parry = (
        random.choice(NORMAL_MONSTERS)
    )

    # Wave가 올라갈수록 강해짐
    wave_scale = st.session_state.kill

    hp += wave_scale * 3
    damage += wave_scale * 0.45
    defense += wave_scale * 0.20
    evasion += wave_scale * 0.08
    parry += wave_scale * 0.08

    # 플레이어 레벨에 따른 추가 강화
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

    # 보스 처치 수에 따른 보상 증가
    boss_bonus = st.session_state.boss_kill

    st.session_state.monster_exp_min = (
        20
        + st.session_state.level * 4
        + boss_bonus * 15
        + wave_scale // 3
    )

    st.session_state.monster_exp_max = (
        45
        + st.session_state.level * 7
        + boss_bonus * 25
        + wave_scale // 2
    )


# =========================================================
# 몬스터 공격
# =========================================================

def monster_attack():

    if st.session_state.game_over:
        return


    # 플레이어 회피
    if random.randint(1, 100) <= evasion_stat():

        st.session_state.message = (
            f"💨 공격을 회피했습니다! "
            f"({n(evasion_stat())}%)"
        )

        decrease_potion_turns()

        return


    damage = random.randint(
        max(
            1,
            st.session_state.monster_damage - 5
        ),
        st.session_state.monster_damage + 5
    )


    # 보스 필살기
    if st.session_state.is_boss:

        if random.random() < 0.20:

            damage *= 2

            st.session_state.message = (
                f"💀 보스 필살기! "
                f"{damage}의 피해!"
            )

        else:

            st.session_state.message = (
                "👑 보스의 공격!"
            )

    else:

        st.session_state.message = (
            f"👾 {st.session_state.monster_name}의 공격!"
        )


    # 방어력
    damage -= defense_stat()

    damage = max(1, damage)


    # 방어 상태
    if st.session_state.defending:

        damage = max(
            1,
            int(damage * 0.4)
        )

        st.session_state.defending = False

        st.session_state.message += (
            " 🛡️ 방어 성공!"
        )


    st.session_state.hp -= damage

    st.session_state.message += (
        f" 💔 {damage} 피해"
    )


    decrease_potion_turns()


    if st.session_state.hp <= 0:

        st.session_state.hp = 0
        st.session_state.game_over = True


# =========================================================
# 플레이어 공격 판정
# =========================================================

def player_attack(
    damage,
    can_be_parried=True
):

    # 적 회피
    if random.randint(
        1,
        100
    ) <= st.session_state.monster_evasion:

        st.session_state.message = (
            f"💨 {st.session_state.monster_name} "
            f"회피 성공! "
            f"({n(st.session_state.monster_evasion)}%)"
        )

        monster_attack()

        return False


    # 적 패링
    # 강공격은 can_be_parried=False
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
                counter_damage - defense_stat()
            )

            st.session_state.hp -= counter_damage

            st.session_state.message = (
                f"⚡ {st.session_state.monster_name} "
                f"패링 성공! "
                f"💥 {counter_damage} 반격!"
            )

            decrease_potion_turns()

            if st.session_state.hp <= 0:

                st.session_state.hp = 0
                st.session_state.game_over = True

            return False


    # 적 방어력
    final_damage = max(
        1,
        int(damage - st.session_state.monster_defense)
    )

    st.session_state.monster_hp -= final_damage

    st.session_state.message = (
        f"⚔️ {final_damage} 피해!"
    )

    return True


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
# 패링 불가능
# =========================================================

def strong_attack():

    # 명중률 60%
    if random.random() > 0.60:

        st.session_state.message = (
            "💨 강공격이 빗나갔습니다!"
        )

        monster_attack()

        return


    damage = random.randint(
        int(attack_stat()) + 15,
        int(attack_stat()) + 35
    )

    success = player_attack(
        damage,
        False
    )

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

    success_rate = 40

    if random.randint(
        1,
        100
    ) <= success_rate:

        counter_damage = random.randint(
            int(attack_stat()),
            int(attack_stat()) + 20
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

        decrease_potion_turns()


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


    if st.session_state.hp >= st.session_state.base_max_hp:

        st.session_state.message = (
            "❤️ HP가 가득합니다!"
        )

        return


    st.session_state.hp_potion -= 1

    old_hp = st.session_state.hp

    st.session_state.hp = min(
        st.session_state.base_max_hp,
        st.session_state.hp + 50
    )

    recovered = (
        st.session_state.hp - old_hp
    )

    st.session_state.message = (
        f"🧪 체력 물약 사용! "
        f"❤️ +{recovered} HP"
    )


# =========================================================
# 공격력 물약
# 현재 공격력의 30%
# =========================================================

def use_attack_potion():

    if st.session_state.attack_potion <= 0:

        st.session_state.message = (
            "⚔️ 힘의 물약이 없습니다!"
        )

        return


    st.session_state.attack_potion -= 1

    current = attack_stat()

    bonus = current * 0.30

    st.session_state.attack_bonus = bonus
    st.session_state.attack_turns = 5

    st.session_state.message = (
        f"⚔️ 힘의 물약 사용! "
        f"+{n(bonus)} 공격력 "
        f"(5턴)"
    )


# =========================================================
# 방어력 물약
# 현재 방어력의 30%
# =========================================================

def use_defense_potion():

    if st.session_state.defense_potion <= 0:

        st.session_state.message = (
            "🛡️ 방어의 물약이 없습니다!"
        )

        return


    st.session_state.defense_potion -= 1

    current = defense_stat()

    bonus = current * 0.30

    st.session_state.defense_bonus = bonus
    st.session_state.defense_turns = 5

    st.session_state.message = (
        f"🛡️ 방어의 물약 사용! "
        f"+{n(bonus)} 방어력 "
        f"(5턴)"
    )


# =========================================================
# 회피율 물약
# 현재 회피율의 30%
# =========================================================

def use_evasion_potion():

    if st.session_state.evasion_potion <= 0:

        st.session_state.message = (
            "💨 민첩의 물약이 없습니다!"
        )

        return


    if evasion_stat() >= 60:

        st.session_state.message = (
            "💨 회피율이 최대치입니다!"
        )

        return


    st.session_state.evasion_potion -= 1

    current = evasion_stat()

    bonus = current * 0.30

    bonus = min(
        bonus,
        60 - current
    )

    st.session_state.evasion_bonus = bonus
    st.session_state.evasion_turns = 5

    st.session_state.message = (
        f"💨 민첩의 물약 사용! "
        f"+{n(bonus)}% 회피율 "
        f"(5턴)"
    )


# =========================================================
# 몬스터 처치
# =========================================================

def monster_defeated():

    was_boss = st.session_state.is_boss


    # =====================================================
    # 보스 처치
    # =====================================================

    if was_boss:

        current_wave = (
            st.session_state.kill + 1
        )

        boss_index = BOSS_SCHEDULE.get(
            current_wave
        )


        # 보스 중복 방지
        if (
            boss_index is not None
            and boss_index
            not in st.session_state.boss_stages_cleared
        ):

            st.session_state.boss_stages_cleared.append(
                boss_index
            )

            st.session_state.boss_kill += 1


        # 보스 골드 보상
        reward = random.randint(
            250,
            400
        )

        reward += (
            st.session_state.boss_kill * 75
        )


        # 보스 처치 성장 보상
        st.session_state.base_max_hp += 30
        st.session_state.base_attack += 10
        st.session_state.base_defense += 3

        # 최대 HP 증가 후 현재 HP도 증가한 최대치 기준으로 유지
        st.session_state.hp = min(
            st.session_state.hp,
            st.session_state.base_max_hp
        )


        st.session_state.message = (
            f"👑 BOSS 처치! "
            f"💰 +{reward}G"
        )


    # =====================================================
    # 일반 몬스터
    # =====================================================

    else:

        boss_bonus = (
            st.session_state.boss_kill
        )

        reward = random.randint(
            40,
            70
        )

        reward += (
            boss_bonus * 30
        )

        reward += (
            st.session_state.kill // 5
        )

        st.session_state.message = (
            f"🎉 {st.session_state.monster_name} "
            f"처치! "
            f"💰 +{reward}G"
        )


    # 골드
    st.session_state.gold += reward


    # =====================================================
    # EXP
    # =====================================================

    exp_amount = random.randint(
        int(st.session_state.monster_exp_min),
        int(st.session_state.monster_exp_max)
    )


    if not was_boss:

        exp_amount += (
            st.session_state.boss_kill * 15
        )


    level_up = gain_exp(
        exp_amount
    )


    st.session_state.message += (
        f" ⭐ EXP +{exp_amount}"
    )


    if level_up:

        st.session_state.message += (
            f" 🎉 LEVEL UP! "
            f"Lv.{st.session_state.level}"
        )


    # =====================================================
    # 처치 후 체력 회복
    #
    # 일반 = 15%
    # 보스 = 25%
    # =====================================================

    recovery = recover_after_kill(
        was_boss
    )


    if was_boss:

        st.session_state.message += (
            f" ❤️ 최대 HP의 25% 회복! "
            f"(+{recovery})"
        )

    else:

        st.session_state.message += (
            f" ❤️ 최대 HP의 15% 회복! "
            f"(+{recovery})"
        )


    # =====================================================
    # Wave 증가
    # =====================================================

    st.session_state.kill += 1

    st.session_state.defending = False


    # =====================================================
    # 최종 보스 처치
    # =====================================================

    if (
        was_boss
        and st.session_state.boss_kill >= 7
    ):

        st.session_state.message += (
            " 🏆 모든 보스를 처치했습니다!"
        )


    # 다음 Wave 생성
    spawn_monster()


# =========================================================
# 무기 강화
# =========================================================

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

    st.session_state.base_attack += 10

    st.session_state.message = (
        "🗡️ 무기 강화 성공! "
        "기본 공격력 +10"
    )


# =========================================================
# 방어구 강화
# =========================================================

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

    st.session_state.base_defense += 4

    st.session_state.message = (
        "🛡️ 방어구 강화 성공! "
        "기본 방어력 +4"
    )


# =========================================================
# 신발 강화
# =========================================================

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

    st.session_state.base_evasion = min(
        60,
        st.session_state.base_evasion + 3
    )

    st.session_state.message = (
        "👟 신발 강화 성공! "
        "기본 회피율 +3%"
    )


# =========================================================
# 최초 실행
# =========================================================

if "base_attack" not in st.session_state:

    reset_game()


# =========================================================
# 제목
# =========================================================

st.title("⚔️ Mini RPG")

st.caption(
    "공격 · 강공격 · 방어 · 패링 · 회피 · 물약 · 보스"
)


# =========================================================
# Wave 표시
# =========================================================

current_wave = (
    st.session_state.kill + 1
)

st.header(
    f"🌊 Wave {current_wave}"
)


# =========================================================
# 기본 정보
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "❤️ HP",
        f"{n(st.session_state.hp)}/"
        f"{n(st.session_state.base_max_hp)}"
    )


with col2:

    st.metric(
        "⭐ LEVEL",
        st.session_state.level
    )

    st.caption(
        f"EXP: "
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
        f"{st.session_state.boss_kill}/7"
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

for wave in BOSS_SCHEDULE:

    if wave > current_wave:

        next_boss = wave
        break


if next_boss is not None:

    st.caption(
        f"⚠️ 다음 보스: Wave {next_boss}"
    )

else:

    st.caption(
        "🏆 모든 보스를 처치했습니다!"
    )


# =========================================================
# 플레이어 스탯
# =========================================================

st.subheader("📊 플레이어 스탯")


col1, col2, col3 = st.columns(3)


with col1:

    bonus = st.session_state.attack_bonus

    if (
        bonus > 0
        and st.session_state.attack_turns > 0
    ):

        label = (
            f"{n(attack_stat())} "
            f"(+{n(bonus)}) "
            f"[{st.session_state.attack_turns}턴]"
        )

    else:

        label = n(
            attack_stat()
        )


    st.metric(
        "⚔️ 공격력",
        label
    )


with col2:

    bonus = st.session_state.defense_bonus

    if (
        bonus > 0
        and st.session_state.defense_turns > 0
    ):

        label = (
            f"{n(defense_stat())} "
            f"(+{n(bonus)}) "
            f"[{st.session_state.defense_turns}턴]"
        )

    else:

        label = n(
            defense_stat()
        )


    st.metric(
        "🛡️ 방어력",
        label
    )


with col3:

    bonus = st.session_state.evasion_bonus

    if (
        bonus > 0
        and st.session_state.evasion_turns > 0
    ):

        label = (
            f"{n(evasion_stat())}% "
            f"(+{n(bonus)}%) "
            f"[{st.session_state.evasion_turns}턴]"
        )

    else:

        label = (
            f"{n(evasion_stat())}%"
        )


    st.metric(
        "💨 회피율",
        label
    )


st.divider()


# =========================================================
# 보스 알림
# =========================================================

if st.session_state.is_boss:

    st.error(
        "👑⚠️ BOSS BATTLE ⚠️👑"
    )


# =========================================================
# 몬스터
# =========================================================

st.subheader(
    st.session_state.monster_name
)


st.write(
    f"❤️ HP: "
    f"{n(st.session_state.monster_hp)}/"
    f"{n(st.session_state.monster_max_hp)}"
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
        n(st.session_state.monster_damage)
    )


with col2:

    st.metric(
        "🛡️ 방어",
        n(st.session_state.monster_defense)
    )


with col3:

    st.metric(
        "💨 회피",
        f"{n(st.session_state.monster_evasion)}%"
    )


with col4:

    st.metric(
        "⚡ 패링",
        f"{n(st.session_state.monster_parry)}%"
    )


st.caption(
    f"⭐ 예상 EXP: "
    f"{n(st.session_state.monster_exp_min)}"
    f" ~ "
    f"{n(st.session_state.monster_exp_max)}"
)


# =========================================================
# 메시지
# =========================================================

st.info(
    st.session_state.message
)


# =========================================================
# 전투
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

        if st.button(
            "💥 강공격",
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


# 무기
with col1:

    cost = (
        st.session_state.weapon_level * 50
    )

    st.write(
        f"🗡️ 무기 Lv."
        f"{st.session_state.weapon_level}"
    )

    # 물약 효과가 적용되지 않은 기본값
    st.write(
        f"기본 공격력 "
        f"{n(st.session_state.base_attack)}"
    )

    if st.button(
        f"강화 {cost}G",
        key="weapon_upgrade",
        use_container_width=True
    ):

        upgrade_weapon()

        st.rerun()


# 방어구
with col2:

    cost = (
        st.session_state.armor_level * 60
    )

    st.write(
        f"🛡️ 방어구 Lv."
        f"{st.session_state.armor_level}"
    )

    # 물약 효과가 적용되지 않은 기본값
    st.write(
        f"기본 방어력 "
        f"{n(st.session_state.base_defense)}"
    )

    if st.button(
        f"강화 {cost}G",
        key="armor_upgrade",
        use_container_width=True
    ):

        upgrade_armor()

        st.rerun()


# 신발
with col3:

    cost = (
        st.session_state.boots_level * 70
    )

    st.write(
        f"👟 신발 Lv."
        f"{st.session_state.boots_level}"
    )

    # 물약 효과가 적용되지 않은 기본값
    st.write(
        f"기본 회피율 "
        f"{n(st.session_state.base_evasion)}%"
    )

    if st.button(
        f"강화 {cost}G",
        key="boots_upgrade",
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
        "❤️ 체력 물약 구매 - 20G",
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
        "⚔️ 힘의 물약 구매 - 60G",
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
        "🛡️ 방어의 물약 구매 - 60G",
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
        "💨 민첩의 물약 구매 - 70G",
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
# 기록
# =========================================================

st.divider()

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🌊 현재 Wave",
        current_wave
    )


with col2:

    st.metric(
        "👑 보스",
        f"{st.session_state.boss_kill}/7"
    )


with col3:

    st.metric(
        "💰 보스 보상 보너스",
        f"+{st.session_state.boss_kill * 30}G"
    )


# =========================================================
# 게임 오버
# =========================================================

if st.session_state.game_over:

    st.error("💀 GAME OVER")

    st.write(
        f"🌊 도달 Wave: "
        f"{current_wave}"
    )

    st.write(
        f"👑 보스 처치: "
        f"{st.session_state.boss_kill}/7"
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
