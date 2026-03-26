#!/usr/bin/env python3
"""
Adaptive Carousel Engine
Автоматически переключает слайды и дизайн в зависимости от бизнес-контекста
"""

import sys
import json
from pathlib import Path

# Add carousel-pro to path
sys.path.insert(0, '/root/.openclaw/skills/skills/carousel-pro')
from modes import MODES, get_mode

class AdaptiveCarousel:
    """
    Интеллектуальная карусель с авто-переключением режимов
    """
    
    # Бизнес-ниши и их характеристики
    BUSINESS_NICHES = {
        'salon': {
            'name': 'Салон красоты',
            'mode': 'lifestyle',  # Essence - тёплые тона
            'slide_structure': [
                {'type': 'hero', 'title': 'Ваша красота — наш приоритет'},
                {'type': 'problem', 'title': 'Устали от долгого ожидания записи?'},
                {'type': 'solution', 'title': 'Онлайн-запись 24/7'},
                {'type': 'benefits', 'title': 'Экономия времени клиентов'},
                {'type': 'social_proof', 'title': '500+ довольных клиентов'},
                {'type': 'cta', 'title': 'Запишитесь прямо сейчас'}
            ],
            'keywords': ['салон', 'красота', 'маникюр', 'парикмахер', 'косметология', 'spa']
        },
        'restaurant': {
            'name': 'Ресторан/Кафе',
            'mode': 'wellness',  # Serenity - естественные тона
            'slide_structure': [
                {'type': 'hero', 'title': 'Вкус момента'},
                {'type': 'problem', 'title': 'Потерянные заказы и недовольные гости?'},
                {'type': 'solution', 'title': 'Автоматизация бронирования'},
                {'type': 'benefits', 'title': 'Больше гостей, меньше хаоса'},
                {'type': 'features', 'title': 'Интеграция с доставкой'},
                {'type': 'cta', 'title': 'Попробуйте бесплатно'}
            ],
            'keywords': ['ресторан', 'кафе', 'доставка', 'бронирование', 'меню', 'кухня']
        },
        'tech_saas': {
            'name': 'SaaS / Технологии',
            'mode': 'startup',  # Velocity - градиенты
            'slide_structure': [
                {'type': 'hero', 'title': 'Масштабируйтесь без границ'},
                {'type': 'problem', 'title': 'Ручные процессы тормозят рост?'},
                {'type': 'solution', 'title': 'AI-автоматизация'},
                {'type': 'stats', 'title': '10x быстрее обработка лидов'},
                {'type': 'integration', 'title': '100+ интеграций'},
                {'type': 'cta', 'title': 'Запустить пилот'}
            ],
            'keywords': ['saas', 'ai', 'автоматизация', 'crm', 'бот', 'стартап', 'технологии']
        },
        'consulting': {
            'name': 'Консалтинг / Услуги',
            'mode': 'corporate',  # Executive - классика
            'slide_structure': [
                {'type': 'hero', 'title': 'Экспертность без компромиссов'},
                {'type': 'credentials', 'title': '15 лет опыта'},
                {'type': 'methodology', 'title': 'Проверенная система'},
                {'type': 'results', 'title': '$2M+ созданной стоимости'},
                {'type': 'process', 'title': '4 этапа работы'},
                {'type': 'cta', 'title': 'Бесплатная консультация'}
            ],
            'keywords': ['консалтинг', 'бизнес', 'коучинг', 'эксперт', 'стратегия', 'аудит']
        },
        'creator': {
            'name': 'Контент-мейкер / Блогер',
            'mode': 'creator',  # Bold - яркие цвета
            'slide_structure': [
                {'type': 'hero', 'title': 'Выходи на новый уровень'},
                {'type': 'myth', 'title': 'Миф: нужны миллионы подписчиков'},
                {'type': 'truth', 'title': 'Факт: важна вовлечённость'},
                {'type': 'strategy', 'title': 'Моя формула контента'},
                {'type': 'transformation', 'title': 'До → После'},
                {'type': 'cta', 'title': 'Присоединяйся к курсу'}
            ],
            'keywords': ['блог', 'контент', 'инфлюенсер', 'тикток', 'youtube', 'монетизация']
        }
    }
    
    def detect_niche(self, text: str) -> tuple:
        """
        Определяет бизнес-нишу по тексту
        
        Returns:
            (niche_key, confidence, detected_mode)
        """
        text_lower = text.lower()
        scores = {}
        
        for niche_key, niche_data in self.BUSINESS_NICHES.items():
            score = 0
            for keyword in niche_data['keywords']:
                if keyword in text_lower:
                    score += 1
            scores[niche_key] = score
        
        # Находим лучшее совпадение
        best_niche = max(scores, key=scores.get)
        confidence = scores[best_niche]
        
        if confidence == 0:
            # Default fallback
            return 'consulting', 0, 'corporate'
        
        detected_mode = self.BUSINESS_NICHES[best_niche]['mode']
        return best_niche, confidence, detected_mode
    
    def generate_adaptive_carousel(self, business_description: str, topic: str = None) -> dict:
        """
        Генерирует адаптивную карусель под бизнес-контекст
        
        Args:
            business_description: Описание бизнеса
            topic: Тема карусели (опционально)
        
        Returns:
            Полная конфигурация карусели
        """
        # Определяем нишу
        niche, confidence, mode = self.detect_niche(business_description)
        niche_data = self.BUSINESS_NICHES[niche]
        
        # Получаем дизайн-режим (создаём экземпляр класса)
        ModeClass = MODES.get(mode, MODES['corporate'])
        design_mode = ModeClass()
        
        # Формируем результат
        result = {
            'niche': {
                'key': niche,
                'name': niche_data['name'],
                'confidence': confidence
            },
            'design_mode': {
                'key': mode,
                'name': design_mode.name,
                'palette': design_mode.palette,
                'fonts': {
                    'heading': design_mode.heading_font,
                    'body': design_mode.body_font
                }
            },
            'slides': []
        }
        
        # Генерируем слайды с контентом
        for i, slide_template in enumerate(niche_data['slide_structure'], 1):
            slide = {
                'number': i,
                'type': slide_template['type'],
                'title': slide_template['title'],
                'content': self._generate_slide_content(slide_template, topic),
                'design': self._get_slide_design(slide_template['type'], design_mode)
            }
            result['slides'].append(slide)
        
        return result
    
    def _generate_slide_content(self, template: dict, topic: str = None) -> str:
        """Генерирует контент для слайда"""
        slide_type = template['type']
        
        content_map = {
            'hero': 'Приветствие и главный посыл',
            'problem': 'Описание боли целевой аудитории',
            'solution': 'Представление решения',
            'benefits': 'Ключевые выгоды для клиента',
            'social_proof': 'Отзывы и кейсы',
            'cta': 'Призыв к действию',
            'stats': 'Ключевые цифры и метрики',
            'features': 'Функциональные возможности',
            'credentials': 'Доказательство экспертности',
            'methodology': 'Описание подхода',
            'results': 'Достижения и результаты',
            'process': 'Этапы работы',
            'myth': 'Разрушение заблуждения',
            'truth': 'Представление факта',
            'strategy': 'Стратегический подход',
            'transformation': 'Пример изменений',
            'integration': 'Интеграционные возможности'
        }
        
        return content_map.get(slide_type, 'Контент слайда')
    
    def _get_slide_design(self, slide_type: str, mode) -> dict:
        """Определяет дизайн для типа слайда"""
        # Базовые стили для разных типов слайдов
        designs = {
            'hero': {
                'layout': 'centered',
                'background': 'gradient',
                'text_size': 'xl',
                'animation': 'fade_in'
            },
            'problem': {
                'layout': 'left_aligned',
                'background': 'solid',
                'accent': 'warning',
                'animation': 'slide_left'
            },
            'solution': {
                'layout': 'centered',
                'background': 'gradient',
                'accent': 'success',
                'animation': 'scale_up'
            },
            'cta': {
                'layout': 'centered',
                'background': 'gradient',
                'button_style': 'primary',
                'animation': 'pulse'
            }
        }
        
        return designs.get(slide_type, {
            'layout': 'standard',
            'background': 'solid',
            'animation': 'fade_in'
        })
    
    def preview_switching(self, business_description: str):
        """
        Демонстрирует переключение слайдов
        """
        result = self.generate_adaptive_carousel(business_description)
        
        print("=" * 60)
        print(f"🎯 НИША: {result['niche']['name']} (уверенность: {result['niche']['confidence']})")
        print(f"🎨 РЕЖИМ: {result['design_mode']['name']}")
        print(f"   Палитра: {result['design_mode']['palette']}")
        print(f"   Шрифты: {result['design_mode']['fonts']}")
        print("=" * 60)
        print()
        
        print("📊 СТРУКТУРА СЛАЙДОВ:")
        print("-" * 60)
        
        for slide in result['slides']:
            print(f"\n  Слайд {slide['number']}: [{slide['type'].upper()}]")
            print(f"  Заголовок: {slide['title']}")
            print(f"  Дизайн: {slide['design']['layout']} | Анимация: {slide['design']['animation']}")
            print(f"  Контент: {slide['content']}")
        
        print("\n" + "=" * 60)
        print("✅ Адаптивная карусель готова!")
        print("=" * 60)
        
        return result


def main():
    """CLI для тестирования"""
    carousel = AdaptiveCarousel()
    
    # Тестовые сценарии
    test_cases = [
        "У меня салон красоты в Бруклине, хочу автоматизировать запись клиентов",
        "Разрабатываю AI-платформу для автоматизации бизнеса",
        "Веду блог про личностный рост, хочу монетизировать аудиторию",
        "Консультирую рестораны по повышению прибыли",
        "Открываю кафе с доставкой азиатской кухни"
    ]
    
    print("🔄 ADAPTIVE CAROUSEL ENGINE — Демо переключения слайдов\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"ТЕСТ #{i}")
        print(f"Ввод: \"{test}\"")
        print('='*60)
        
        carousel.preview_switching(test)
        input("\n⏎ Нажмите Enter для следующего теста...")


if __name__ == "__main__":
    main()
