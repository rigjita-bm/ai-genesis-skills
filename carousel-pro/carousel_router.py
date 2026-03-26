"""
Carousel Mode Router
Интеллектуальный выбор режима дизайна на основе анализа темы
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ModeMatch:
    mode: str
    confidence: float  # 0.0 - 1.0
    reasons: List[str]


class CarouselModeRouter:
    """
    Роутер для интеллектуального выбора режима дизайна Carousel
    Анализирует тему, аудиторию, тональность и контекст
    """
    
    # Режимы и их характеристики
    MODES = {
        'corporate': {
            'name': 'Executive',
            'description': 'B2B, Finance, Consulting — Clean & Trustworthy',
            'colors': ['navy', 'gold', 'blue'],
            'fonts': ['serif', 'libre baskerville'],
            'vibe': 'professional, serious, trustworthy',
            'keywords': [
                'b2b', 'corporate', 'финансы', 'юридические', 'консалтинг', 
                'бухгалтерия', 'недвижимость', 'страхование', 'инвестиции',
                'enterprise', 'business solutions', 'commercial real estate',
                'tax', 'accounting', 'legal', 'law firm', 'corporation'
            ],
            'industries': ['finance', 'legal', 'real estate', 'consulting', 'insurance'],
            'audience': 'business owners, executives, professionals',
            'emotions': ['trust', 'stability', 'authority', 'confidence']
        },
        'startup': {
            'name': 'Velocity',
            'description': 'SaaS, Tech, AI — Bold & Dynamic',
            'colors': ['gradient', 'purple', 'pink', 'neon'],
            'fonts': ['geometric', 'space grotesk', 'modern'],
            'vibe': 'innovative, fast, futuristic, bold',
            'keywords': [
                'saas', 'ai', 'startup', 'технологии', 'приложение', 'автоматизация',
                'software', 'app', 'digital', 'tech', 'innovation', 'disruption',
                'machine learning', 'blockchain', 'web3', 'crypto', 'fintech',
                'platform', 'cloud', 'api', 'development'
            ],
            'industries': ['technology', 'software', 'ai', 'fintech', 'biotech'],
            'audience': 'founders, developers, tech enthusiasts, early adopters',
            'emotions': ['excitement', 'innovation', 'speed', 'ambition']
        },
        'lifestyle': {
            'name': 'Essence',
            'description': 'Beauty, Fashion, Travel — Editorial & Warm',
            'colors': ['terracotta', 'sage', 'warm', 'cream'],
            'fonts': ['playfair display', 'editorial', 'serif'],
            'vibe': 'elegant, editorial, artistic, warm',
            'keywords': [
                'fashion', 'beauty', 'travel', 'food', 'lifestyle', 'мода', 'красота',
                'interior design', 'photography', 'art', 'culture', 'luxury',
                'wellness spa', 'gourmet', 'boutique', ' handcrafted', 'organic',
                'decor', 'style', 'trends', 'inspiration'
            ],
            'industries': ['fashion', 'beauty', 'travel', 'food', 'interior design', 'art'],
            'audience': 'style-conscious consumers, millennials, gen z, creatives',
            'emotions': ['aspiration', 'beauty', 'inspiration', 'desire']
        },
        'wellness': {
            'name': 'Serenity',
            'description': 'Health, Yoga, Organic — Calm & Natural',
            'colors': ['sage green', 'earth', 'sand', 'natural'],
            'fonts': ['cormorant', 'elegant', 'soft'],
            'vibe': 'calm, healing, natural, mindful',
            'keywords': [
                'wellness', 'health', 'yoga', 'meditation', 'organic', 'fitness',
                'mental health', 'nutrition', 'holistic', 'mindfulness', 'zen',
                'spa', 'self-care', 'natural', 'clean eating', 'supplements',
                'pilates', 'healing', 'therapy', 'balance', 'peace'
            ],
            'industries': ['health', 'wellness', 'yoga', 'nutrition', 'mental health', 'spa'],
            'audience': 'health-conscious individuals, yoga practitioners, wellness seekers',
            'emotions': ['calm', 'peace', 'healing', 'balance', 'self-love']
        },
        'creator': {
            'name': 'Bold',
            'description': 'Personal Brand, Coaches — Maximalist & Experimental',
            'colors': ['hot pink', 'neon', 'vibrant', 'rainbow'],
            'fonts': ['anton', 'bold', 'condensed', 'impact'],
            'vibe': 'bold, energetic, confident, attention-grabbing',
            'keywords': [
                'coach', 'creator', 'influencer', 'personal brand', 'мотивация',
                'business coach', 'life coach', 'trainer', 'speaker', 'expert',
                'guru', 'mentor', 'thought leader', 'entrepreneur', 'hustle',
                'success', 'mindset', 'productivity', 'growth', 'personal development'
            ],
            'industries': ['coaching', 'personal development', 'content creation', 'education'],
            'audience': 'aspiring entrepreneurs, self-improvement seekers, fans',
            'emotions': ['motivation', 'confidence', 'power', 'urgency', 'excitement']
        }
    }
    
    def __init__(self):
        self.mode_scores = {}
    
    def analyze(self, topic: str, context: Optional[str] = None) -> ModeMatch:
        """
        Главный метод анализа — определяет лучший режим
        
        Args:
            topic: Тема карусели
            context: Дополнительный контекст (аудитория, цель, тон)
        
        Returns:
            ModeMatch с выбранным режимом, уверенностью и причинами
        """
        text = f"{topic} {context or ''}".lower()
        scores = {mode: 0.0 for mode in self.MODES}
        reasons = {mode: [] for mode in self.MODES}
        
        # 1. Анализ по ключевым словам (вес: 40%)
        keyword_scores = self._analyze_keywords(text)
        for mode, score in keyword_scores.items():
            scores[mode] += score * 0.4
            if score > 0.3:
                reasons[mode].append(f"Ключевые слова ({int(score*100)}%)")
        
        # 2. Анализ индустрии (вес: 25%)
        industry_scores = self._analyze_industry(text)
        for mode, score in industry_scores.items():
            scores[mode] += score * 0.25
            if score > 0.3:
                reasons[mode].append(f"Индустрия ({int(score*100)}%)")
        
        # 3. Анализ тональности (вес: 20%)
        tone_scores = self._analyze_tone(topic)
        for mode, score in tone_scores.items():
            scores[mode] += score * 0.20
            if score > 0.3:
                reasons[mode].append(f"Тональность ({int(score*100)}%)")
        
        # 4. Анализ аудитории (вес: 15%)
        audience_scores = self._analyze_audience(text)
        for mode, score in audience_scores.items():
            scores[mode] += score * 0.15
            if score > 0.3:
                reasons[mode].append(f"Аудитория ({int(score*100)}%)")
        
        # Выбираем лучший режим
        best_mode = max(scores, key=scores.get)
        confidence = scores[best_mode]
        
        # Нормализуем confidence к 0-1
        confidence = min(confidence, 1.0)
        
        return ModeMatch(
            mode=best_mode,
            confidence=confidence,
            reasons=reasons[best_mode][:3]  # Топ-3 причины
        )
    
    def _analyze_keywords(self, text: str) -> Dict[str, float]:
        """Анализ ключевых слов по каждому режиму"""
        scores = {}
        for mode, data in self.MODES.items():
            matches = sum(1 for kw in data['keywords'] if kw in text)
            scores[mode] = min(matches / 3, 1.0)  # Макс 3 совпадения = 100%
        return scores
    
    def _analyze_industry(self, text: str) -> Dict[str, float]:
        """Анализ индустрии"""
        industry_keywords = {
            'finance': ['финанс', 'банк', 'инвест', 'крипто', 'trading', 'forex'],
            'technology': ['tech', 'software', 'ai', 'app', 'digital', 'saas'],
            'legal': ['юрид', 'закон', 'адвокат', 'legal', 'law'],
            'health': ['здоровье', 'витамин', 'питание', 'health', 'medical'],
            'fashion': ['мода', 'стиль', 'одежда', 'fashion', 'style'],
            'coaching': ['коуч', 'наставник', 'ментор', 'coach', 'mentor'],
        }
        
        scores = {mode: 0.0 for mode in self.MODES}
        
        industry_map = {
            'finance': ['corporate'],
            'technology': ['startup'],
            'legal': ['corporate'],
            'health': ['wellness'],
            'fashion': ['lifestyle'],
            'coaching': ['creator'],
        }
        
        for industry, keywords in industry_keywords.items():
            if any(kw in text for kw in keywords):
                for mode in industry_map.get(industry, []):
                    scores[mode] += 0.5
        
        return scores
    
    def _analyze_tone(self, topic: str) -> Dict[str, float]:
        """Анализ тональности по заголовку"""
        scores = {mode: 0.0 for mode in self.MODES}
        topic_lower = topic.lower()
        
        # Признаки агрессивного/мотивирующего тона
        if any(word in topic_lower for word in ['хватит', 'перестань', 'наконец', '立刻', 'срочно']):
            scores['creator'] += 0.8
        
        # Признаки спокойного тона
        if any(word in topic_lower for word in ['как', 'почему', 'руководство', 'guide', 'пошагово']):
            scores['wellness'] += 0.4
            scores['lifestyle'] += 0.3
        
        # Признаки технического тона
        if any(word in topic_lower for word in ['автоматизация', 'система', 'процесс', 'framework']):
            scores['startup'] += 0.6
            scores['corporate'] += 0.4
        
        # Признаки luxury/elegant
        if any(word in topic_lower for word in ['luxury', 'premium', 'exclusive', 'элитный', 'премиум']):
            scores['lifestyle'] += 0.7
        
        return scores
    
    def _analyze_audience(self, text: str) -> Dict[str, float]:
        """Анализ целевой аудитории"""
        scores = {mode: 0.0 for mode in self.MODES}
        
        audience_signals = {
            'corporate': ['ceo', 'founder', 'business owner', 'предприниматель', 'руководитель'],
            'startup': ['developer', 'founder', 'startup', 'tech', 'разработчик'],
            'wellness': ['yoga', 'fitness', 'health', 'mom', 'busy professional'],
            'creator': ['coach', 'creator', 'influencer', 'expert', 'speaker'],
            'lifestyle': ['millennial', 'gen z', 'creative', 'fashion lover'],
        }
        
        for mode, signals in audience_signals.items():
            if any(signal in text for signal in signals):
                scores[mode] += 0.6
        
        return scores
    
    def get_recommendation(self, topic: str, context: Optional[str] = None) -> str:
        """Возвращает красивую рекомендацию для пользователя"""
        match = self.analyze(topic, context)
        mode_data = self.MODES[match.mode]
        
        confidence_text = ""
        if match.confidence >= 0.8:
            confidence_text = "(высокая уверенность)"
        elif match.confidence >= 0.5:
            confidence_text = "(средняя уверенность)"
        else:
            confidence_text = "(требуется уточнение)"
        
        reasons_text = "\n".join([f"  • {reason}" for reason in match.reasons])
        
        return f"""🎨 Рекомендуемый режим: {mode_data['name']} {confidence_text}

{mode_data['description']}

Почему этот режим:
{reasons_text}

Характеристики:
• Цвета: {', '.join(mode_data['colors'][:3])}
• Шрифты: {', '.join(mode_data['fonts'][:2])}
• Настроение: {mode_data['vibe']}
• Эмоции: {', '.join(mode_data['emotions'][:3])}
"""
    
    def get_alternative_modes(self, topic: str, context: Optional[str] = None, top_n: int = 2) -> List[ModeMatch]:
        """Возвращает топ-N альтернативных режимов"""
        match = self.analyze(topic, context)
        
        # Считаем все скоры заново
        text = f"{topic} {context or ''}".lower()
        all_scores = {}
        
        for mode in self.MODES:
            if mode == match.mode:
                continue
            # Упрощённый пересчёт
            score = 0
            data = self.MODES[mode]
            matches = sum(1 for kw in data['keywords'] if kw in text)
            score += min(matches / 3, 1.0) * 0.4
            all_scores[mode] = score
        
        # Сортируем и берём топ-N
        sorted_modes = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        
        alternatives = []
        for mode, score in sorted_modes[:top_n]:
            alternatives.append(ModeMatch(
                mode=mode,
                confidence=score,
                reasons=["Альтернативный стиль"]
            ))
        
        return alternatives


# CLI интерфейс
if __name__ == "__main__":
    import sys
    
    router = CarouselModeRouter()
    
    if len(sys.argv) < 2:
        print("Использование: python carousel_router.py 'Тема карусели' [контекст]")
        print("\nПримеры:")
        print('  python carousel_router.py "AI автоматизация для бизнеса"')
        print('  python carousel_router.py "Йога для начинающих" "аудитория: женщины 25-40"')
        print('  python carousel_router.py "Коучинг по продуктивности" "для предпринимателей"')
        sys.exit(1)
    
    topic = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("🎨 CAROUSEL MODE ROUTER")
    print("=" * 60)
    print(f"\nТема: {topic}")
    if context:
        print(f"Контекст: {context}")
    
    print("\n" + router.get_recommendation(topic, context))
    
    # Показываем альтернативы
    alternatives = router.get_alternative_modes(topic, context)
    if alternatives:
        print("\n🔄 Альтернативные варианты:")
        for alt in alternatives:
            mode_data = router.MODES[alt.mode]
            print(f"  • {mode_data['name']} ({int(alt.confidence * 100)}%)")
