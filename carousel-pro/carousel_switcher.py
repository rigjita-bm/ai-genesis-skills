"""
Adaptive Carousel Integration for Telegram Bot
Автоматическое переключение карусели по контексту бизнеса
"""

import sys
sys.path.insert(0, '/root/.openclaw/skills/skills/carousel-pro')

from adaptive_carousel import AdaptiveCarousel

class CarouselContextSwitcher:
    """
    Контекстный переключатель каруселей для Telegram бота
    """
    
    def __init__(self):
        self.carousel = AdaptiveCarousel()
        self.active_carousels = {}  # user_id -> carousel_data
    
    def detect_and_switch(self, user_message: str, user_id: int = None) -> dict:
        """
        Анализирует сообщение пользователя и переключает карусель
        
        Args:
            user_message: Текст от пользователя
            user_id: ID пользователя для сохранения контекста
            
        Returns:
            Данные карусели с выбранным режимом и слайдами
        """
        # Определяем нишу и режим
        result = self.carousel.generate_adaptive_carousel(user_message)
        
        # Сохраняем контекст
        if user_id:
            self.active_carousels[user_id] = {
                'niche': result['niche'],
                'mode': result['design_mode'],
                'slides': result['slides'],
                'context': user_message
            }
        
        return result
    
    def get_carousel_summary(self, user_id: int) -> str:
        """Возвращает сводку о текущей карусели"""
        if user_id not in self.active_carousels:
            return "Нет активной карусели"
        
        data = self.active_carousels[user_id]
        niche = data['niche']
        mode = data['mode']
        
        summary = f"""🎯 <b>Адаптивная карусель активна</b>

📍 <b>Ниша:</b> {niche['name']}
🎨 <b>Режим:</b> {mode['name']}
🌈 <b>Цвет:</b> {mode['palette']['BRAND_PRIMARY']}
📊 <b>Слайдов:</b> {len(data['slides'])}

<b>Структура:</b>
"""
        for slide in data['slides']:
            summary += f"\n  {slide['number']}. {slide['title']}"
        
        return summary


# Singleton для использования в боте
carousel_switcher = CarouselContextSwitcher()


def handle_carousel_request(user_message: str, user_id: int = None) -> dict:
    """
    Handler для Telegram бота
    
    Usage:
        result = handle_carousel_request("У меня салон красоты", user_id=123)
        # Returns carousel data with auto-selected mode and slides
    """
    return carousel_switcher.detect_and_switch(user_message, user_id)


if __name__ == "__main__":
    # Demo
    print("🔄 Carousel Context Switcher Demo\n")
    
    test_messages = [
        "Привет! У меня салон красоты в Манхэттене",
        "Разрабатываем SaaS для ресторанов",
        "Веду блог про фитнес и здоровье"
    ]
    
    for msg in test_messages:
        print(f"\n👤 Пользователь: \"{msg}\"")
        result = handle_carousel_request(msg, user_id=1)
        
        print(f"🤖 Бот определил:")
        print(f"   Ниша: {result['niche']['name']} ({result['design_mode']['name']})")
        print(f"   Слайды: {len(result['slides'])}")
