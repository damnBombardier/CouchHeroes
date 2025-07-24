# game_engine/engine.py (фрагмент)
# ... (предыдущий код)
import random
import logging
from heroes.models import Hero
from events.models import Quest, HeroQuest # Импортируем новые модели
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

class GameEngine:
    """
    Основной класс игрового движка.
    """

    @staticmethod
    def process_hero_turn(hero: Hero):
        """
        Обрабатывает один "ход" героя.
        Учитывает состояние, здоровье, опыт, уровень, квесты.
        """
        try:
            # Герой мертв - ничего не делает
            if hero.state == 'dead':
                # Возможно, добавить шанс воскрешения или просто ждать
                return f"{hero.name} мертв и не может действовать."

            # --- Обработка квестов ---
            # Проверим, есть ли у героя активные квесты
            active_quests = hero.quests.filter(status='in_progress')
            if active_quests.exists():
                # Простая логика: герой работает над квестом
                quest_entry = active_quests.first() # Берем первый активный
                quest = quest_entry.quest
                
                # Прогресс квеста
                progress_gain = random.randint(1, 3)
                quest_entry.progress += progress_gain
                quest_entry.save()
                
                # Проверка завершения квеста (простая логика)
                # Предположим, квест завершается при прогрессе 10
                if quest_entry.progress >= 10:
                    return GameEngine._complete_quest(hero, quest_entry)
                else:
                    return f"{hero.name} работает над квестом '{quest.title}'. Прогресс: {quest_entry.progress}/10"
            
            # --- Обработка состояний ---
            
            # Герой отдыхает - восстанавливает здоровье
            if hero.state == 'rest':
                heal_amount = random.randint(5, 15)
                hero.health = min(hero.max_health, hero.health + heal_amount)
                hero.state = 'adventure' # После отдыха снова в приключение
                hero.save()
                return f"{hero.name} отдыхает и восстанавливает {heal_amount} здоровья. Здоровье: {hero.health}/{hero.max_health}"

            # Герой в бою
            if hero.state == 'fight':
                # Простая логика боя
                damage_to_hero = random.randint(5, 20)
                damage_to_monster = random.randint(10, 25)
                
                hero.health = max(0, hero.health - damage_to_hero)
                
                # Проверка, победил ли герой или монстр
                if random.random() > 0.5: # 50% шанс победы героя
                    # Герой победил
                    exp_gain = random.randint(10, 30)
                    gold_gain = random.randint(1, 10)
                    hero.experience += exp_gain
                    hero.gold += gold_gain
                    hero.monsters_killed += 1
                    hero.state = 'adventure'
                    hero.save()
                    log = f"{hero.name} победил монстра! Получено {exp_gain} опыта и {gold_gain} золота."
                    
                    # Проверка на уровень
                    level_up_log = GameEngine._check_level_up(hero)
                    if level_up_log:
                        log += f" {level_up_log}"
                    return log
                else:
                    # Монстр победил или бой продолжается
                    hero.save()
                    if hero.health == 0:
                        hero.state = 'dead'
                        hero.deaths += 1
                        hero.save()
                        return f"{hero.name} был побежден в бою и погиб."
                    else:
                        return f"{hero.name} сражается с монстром. Получено {damage_to_hero} урона. Здоровье: {hero.health}/{hero.max_health}"
            
            # Герой в состоянии приключения - выполняет случайные действия
            action_log = hero.get_random_action()
            logger.info(f"Герой {hero.name}: {action_log}")
            
            # Обработка специфических действий
            if "золота" in action_log:
                gold_found = random.randint(1, 5)
                hero.gold += gold_found
                action_log = f"{hero.name} находит немного золота! +{gold_found} золота. Всего: {hero.gold}"
            
            elif "монстром" in action_log:
                hero.state = 'fight'
                action_log = f"{hero.name} сталкивается с монстром! Начинается бой."
            
            elif "задание" in action_log or "квест" in action_log.lower():
                # Попытка начать новый квест
                new_quest_log = GameEngine._start_random_quest(hero)
                if new_quest_log:
                    action_log = new_quest_log
                # Если квест не начался, герой остается в состоянии приключения
            
            elif "рыбалку" in action_log:
                 # Простой пример квеста/действия
                 fish_caught = random.choice([True, False])
                 if fish_caught:
                     hero.gold += 2
                     action_log = f"{hero.name} ловит рыбу и продает её за 2 золота."
                 else:
                     action_log = f"{hero.name} сидит у реки, но рыба не клюёт."
            
            # Простая проверка на отдых (если здоровье ниже 30%)
            if hero.health < hero.max_health * 0.3:
                if random.random() < 0.3: # 30% шанс пойти отдыхать
                    hero.state = 'rest'
                    action_log += f" {hero.name} чувствует усталость и решает отдохнуть."

            hero.save()
            return action_log
            
        except Exception as e:
            logger.error(f"Ошибка при обработке хода героя {hero.name}: {e}")
            return f"Ошибка при обработке хода героя {hero.name}"

    @staticmethod
    def _start_random_quest(hero: Hero):
        """
        Пытается начать случайный доступный квест для героя.
        """
        # Найдем доступные квесты (системные или одобренные пользовательские)
        available_quests = Quest.objects.filter(
            required_level__lte=hero.level,
            is_approved=True
        ).exclude(
            heroquest__hero=hero # Исключаем уже начатые героем
        )
        
        if not available_quests.exists():
            return None # Нет доступных квестов
            
        quest = random.choice(available_quests)
        
        # Создаем запись о квесте для героя
        HeroQuest.objects.create(
            hero=hero,
            quest=quest,
            status='in_progress',
            started_at=timezone.now()
        )
        
        return f"{hero.name} получает новое задание: '{quest.title}'!"

    @staticmethod
    def _complete_quest(hero: Hero, hero_quest: HeroQuest):
        """
        Завершает квест и выдает награду герою.
        """
        quest = hero_quest.quest
        hero_quest.status = 'completed'
        hero_quest.completed_at = timezone.now()
        hero_quest.save()
        
        # Выдаем награду
        hero.experience += quest.reward_experience
        hero.gold += quest.reward_gold
        hero.quests_completed += 1
        hero.save()
        
        log = f"{hero.name} успешно завершает квест '{quest.title}'! Получено {quest.reward_experience} опыта и {quest.reward_gold} золота."
        
        # Проверка на уровень
        level_up_log = GameEngine._check_level_up(hero)
        if level_up_log:
            log += f" {level_up_log}"
            
        # После завершения квеста герой снова в приключениях
        hero.state = 'adventure'
        hero.save()
        
        return log

    @staticmethod
    def _check_level_up(hero: Hero):
        """
        Проверяет, набрал ли герой достаточно опыта для повышения уровня.
        """
        # Простая формула для уровня
        required_exp = hero.level * 100
        if hero.experience >= required_exp:
            hero.level += 1
            hero.experience -= required_exp
            # Увеличиваем максимальное здоровье при повышении уровня
            hp_increase = random.randint(10, 20)
            hero.max_health += hp_increase
            hero.health = hero.max_health # Полное восстановление при level-up
            hero.save()
            return f"{hero.name} достигает уровня {hero.level}! Максимальное здоровье увеличено на {hp_increase}."
        return None

    @staticmethod
    def run_global_events():
        """
        Запускает глобальные события.
        """
        events = [
            "В мире наступает весна! Все герои чувствуют прилив сил.",
            "Объявлен конкурс на лучший квест! Участники получают бонус к опыту.",
            "Наблюдается повышенная активность монстров. Осторожнее в путешествиях!",
            "В тавернах появляются слухи о реликтовом артефакте.",
            "Штормовое предупреждение! Герои в дороге должны быть格外 осторожны.",
            "С Новогодвиллем! В воздухе витает праздничное настроение.",
        ]
        event = random.choice(events)
        logger.info(f"Глобальное событие: {event}")
        return event

# Экземпляр движка
engine = GameEngine()
