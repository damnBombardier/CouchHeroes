# game_engine/engine.py
"""
Модуль игрового движка ZPG.
Здесь будет логика автоматического продвижения героев.
"""
import random
import logging
from heroes.models import Hero

logger = logging.getLogger(__name__)

class GameEngine:
    """
    Основной класс игрового движка.
    """

    @staticmethod
    def process_hero_turn(hero: Hero):
        """
        Обрабатывает один "ход" героя.
        В реальном проекте это будет намного сложнее,
        с учетом состояния, инвентаря, квестов и т.д.
        """
        try:
            action_log = hero.get_random_action()
            logger.info(f"Герой {hero.name}: {action_log}")
            
            # Здесь можно добавить логику изменения состояния героя,
            # получения опыта, золота, перехода в другое состояние и т.д.
            
            # Пример простого изменения состояния
            if "монстром" in action_log:
                hero.state = 'fight'
            elif "отдыхает" in action_log:
                hero.state = 'rest'
            else:
                hero.state = 'adventure'
                
            hero.save()
            
            return action_log
        except Exception as e:
            logger.error(f"Ошибка при обработке хода героя {hero.name}: {e}")
            return f"Ошибка при обработке хода героя {hero.name}"

    @staticmethod
    def run_global_events():
        """
        Запускает глобальные события (например, "Новогодвилль").
        Пока заглушка.
        """
        events = [
            "В мире наступает весна!",
            "Объявлен конкурс на лучший квест!",
            "Наблюдается повышенная активность монстров.",
        ]
        event = random.choice(events)
        logger.info(f"Глобальное событие: {event}")
        return event

# Экземпляр движка
engine = GameEngine()
