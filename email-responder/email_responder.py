#!/usr/bin/env python3
"""
Email Responder Skill for AI Genesis
Автоматические ответы на письма естественным языком через Gmail API
"""

import json
import sys
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Gmail API integration
try:
    sys.path.insert(0, '/root/.openclaw/skills/skills/gog')
    from gog import GmailClient
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    print("⚠️ Gmail client not available")

class EmailResponder:
    """
    Интеллектуальная система ответов на email
    """
    
    # Шаблоны тонов ответа
    TONES = {
        "professional": {
            "name": "Деловой",
            "style": "формальный, вежливый, структурированный",
            "greeting": "Добрый день",
            "closing": "С уважением",
        },
        "friendly": {
            "name": "Дружелюбный", 
            "style": "теплый, разговорный, но профессиональный",
            "greeting": "Привет",
            "closing": "До связи",
        },
        "casual": {
            "name": "Неформальный",
            "style": "простой, прямой, как у знакомых",
            "greeting": "Здравствуй",
            "closing": "Пока",
        }
    }
    
    # Типы писем и стратегии ответа
    EMAIL_TYPES = {
        "inquiry": {
            "keywords": ["интересует", "хочу", "можно", "цена", "стоимость", "как заказать"],
            "strategy": "ответить на вопросы, предложить следующий шаг",
            "priority": "high"
        },
        "complaint": {
            "keywords": ["жалоба", "недоволен", "плохо", "проблема", "ошибка", "возврат"],
            "strategy": "извиниться, предложить решение, компенсацию",
            "priority": "urgent"
        },
        "partnership": {
            "keywords": ["сотрудничество", "партнерство", "предложение", "бизнес", "совместно"],
            "strategy": "выразить интерес, запросить детали, предложить созвон",
            "priority": "high"
        },
        "support": {
            "keywords": ["помощь", "не работает", "вопрос", "как", "подскажите"],
            "strategy": "ответить по существу, дать инструкцию, предложить поддержку",
            "priority": "medium"
        },
        "spam": {
            "keywords": ["рассылка", "реклама", "выигрыш", "бесплатно", "акция", "скидка 90%"],
            "strategy": "игнорировать или отписаться",
            "priority": "low"
        }
    }
    
    def __init__(self, tone: str = "friendly"):
        self.tone = self.TONES.get(tone, self.TONES["friendly"])
        self.gmail = GmailClient() if GMAIL_AVAILABLE else None
        self.response_history = []
    
    def detect_email_type(self, subject: str, body: str) -> Tuple[str, float]:
        """
        Определяет тип письма по содержимому
        
        Returns:
            (email_type, confidence)
        """
        text = (subject + " " + body).lower()
        scores = {}
        
        for email_type, config in self.EMAIL_TYPES.items():
            score = sum(1 for kw in config["keywords"] if kw in text)
            scores[email_type] = score
        
        # Выбираем лучшее совпадение
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]
        
        # Если нет ключевых слов — считаем inquiry по умолчанию
        if confidence == 0:
            return "inquiry", 0
        
        return best_type, confidence
    
    def extract_questions(self, body: str) -> List[str]:
        """
        Извлекает вопросы из текста письма
        """
        # Ищем предложения со знаком вопроса
        questions = re.findall(r'[^.!?]*\?', body)
        # Ищем косвенные вопросы (интересует, хочу знать и т.д.)
        indirect = re.findall(r'(?:интересует|хотел[а]? узнать|скажите|подскажите)[^.!?]*', body, re.IGNORECASE)
        
        return questions + indirect
    
    def extract_sender_info(self, from_header: str) -> Dict[str, str]:
        """
        Извлекает имя и email отправителя
        """
        # Формат: "Имя <email@domain.com>" или просто "email@domain.com"
        match = re.match(r'"?([^"<]+)"?\s*<([^>]+)>', from_header)
        if match:
            return {
                "name": match.group(1).strip(),
                "email": match.group(2).strip()
            }
        return {
            "name": from_header.split('@')[0],
            "email": from_header
        }
    
    def generate_response(self, subject: str, body: str, from_header: str) -> Dict:
        """
        Генерирует ответ на письмо
        
        Returns:
            {
                "subject": str,
                "body": str,
                "email_type": str,
                "priority": str,
                "tone": str,
                "questions_found": int
            }
        """
        sender = self.extract_sender_info(from_header)
        email_type, confidence = self.detect_email_type(subject, body)
        questions = self.extract_questions(body)
        
        # Формируем приветствие
        greeting = f"{self.tone['greeting']}, {sender['name'].split()[0]}!"
        
        # Генерируем тело ответа в зависимости от типа
        body_response = self._generate_body(email_type, questions, body)
        
        # Формируем закрытие
        closing = f"{self.tone['closing']},\nAI Genesis Team"
        
        # Собираем полный ответ
        full_response = f"{greeting}\n\n{body_response}\n\n{closing}"
        
        # Формируем тему ответа
        if subject.lower().startswith("re:"):
            response_subject = subject
        else:
            response_subject = f"Re: {subject}"
        
        return {
            "subject": response_subject,
            "body": full_response,
            "to": sender["email"],
            "email_type": email_type,
            "priority": self.EMAIL_TYPES[email_type]["priority"],
            "tone": self.tone["name"],
            "questions_found": len(questions),
            "sender_name": sender["name"]
        }
    
    def _generate_body(self, email_type: str, questions: List[str], original_body: str) -> str:
        """
        Генерирует тело ответа по типу письма
        """
        if email_type == "inquiry":
            if questions:
                return f"Спасибо за интерес к нашим услугам!\n\nПо вашим вопросам:\n\n" + "\n".join([f"• {q.strip()} — отвечу подробно в ближайшее время." for q in questions[:3]]) + "\n\nДавайте созвонимся на 10-15 минут? Это быстрее, чем переписка. Подскажите, когда вам удобно?"
            else:
                return "Спасибо за письмо! Получил, изучаю детали. В ближайшие пару часов подготовлю развёрнутый ответ с конкретными цифрами и сроками.\n\nЕсли срочно — напишите в Telegram @aigenesis или позвоните."
        
        elif email_type == "complaint":
            return "Приношу извинения за неудобства. Это неприемлемый уровень сервиса для нас.\n\nДавайте решим ситуацию прямо сейчас:\n\n1. Что именно пошло не так?\n2. Какой результат вы ожидали?\n3. Что смогло бы компенсировать сложности?\n\nЛично проконтролирую решение."
        
        elif email_type == "partnership":
            return "Интересное предложение! Открыт к диалогу.\n\nЧтобы быстро понять, подходит ли нам сотрудничество, подскажите:\n\n• Какая модель сотрудничества вы видите?\n• Какие ресурсы/экспертиза у каждой стороны?\n• Какие цели на ближайшие 3-6 месяцев?\n\nМожем созвониться на 20 минут — обсудим голосом быстрее, чем 10 писем."
        
        elif email_type == "support":
            if questions:
                return f"Получил ваш запрос. Разбираюсь.\n\nЧтобы дать точный ответ по вопросам:\n\n" + "\n".join([f"• {q.strip()}" for q in questions[:3]]) + "\n\nПодготовлю инструкцию или настрою решение. Отвечу в течение 2 часов."
            else:
                return "Понял задачу. Работаю над решением. Отвечу с конкретными шагами в течение сегодняшнего дня.\n\nЕсли критично по времени — позвоните, сразу подскажу."
        
        elif email_type == "spam":
            return None  # Не отвечаем на спам
        
        else:
            return "Спасибо за письмо! Получил, изучаю. Отвечу в течение дня."
    
    def draft_response(self, email_data: Dict) -> Optional[Dict]:
        """
        Создаёт черновик ответа на основе данных письма
        
        Args:
            email_data: {
                "subject": str,
                "body": str,
                "from": str (email header),
                "date": str
            }
        """
        return self.generate_response(
            email_data.get("subject", ""),
            email_data.get("body", ""),
            email_data.get("from", "")
        )
    
    def check_and_reply(self, auto_send: bool = False) -> List[Dict]:
        """
        Проверяет Gmail и генерирует ответы на новые письма
        
        Args:
            auto_send: Если True — отправляет автоматически (осторожно!)
        
        Returns:
            Список обработанных писем с ответами
        """
        if not self.gmail:
            print("❌ Gmail client not available")
            return []
        
        # Получаем непрочитанные письма
        unread = self.gmail.get_unread_emails(limit=10)
        
        processed = []
        for email in unread:
            # Генерируем ответ
            response = self.draft_response(email)
            
            if response and response.get("body"):
                processed.append({
                    "original": email,
                    "response": response
                })
                
                if auto_send and response["priority"] in ["medium", "high"]:
                    # Авто-отправка только для не-критичных писем
                    self.gmail.send_email(
                        to=response["to"],
                        subject=response["subject"],
                        body=response["body"]
                    )
                    print(f"✅ Auto-sent reply to {response['to']}")
        
        return processed


# CLI для тестирования
if __name__ == "__main__":
    responder = EmailResponder(tone="friendly")
    
    # Тестовое письмо
    test_email = {
        "subject": "Интересует автоматизация",
        "body": "Добрый день! Меня зовут Алексей, у меня небольшой магазин электроники. Хотел узнать, сколько стоит настроить бота для обработки заказов? И как быстро можно запустить?",
        "from": "Алексей Петров <alex@example.com>"
    }
    
    print("🧪 Тест генерации ответа\n")
    print("=" * 60)
    print(f"Тема: {test_email['subject']}")
    print(f"От: {test_email['from']}")
    print(f"Тело: {test_email['body'][:100]}...")
    print("=" * 60)
    print()
    
    response = responder.draft_response(test_email)
    
    print("📧 СГЕНЕРИРОВАННЫЙ ОТВЕТ:")
    print("=" * 60)
    print(f"Тип письма: {response['email_type']}")
    print(f"Приоритет: {response['priority']}")
    print(f"Тон: {response['tone']}")
    print(f"Вопросов найдено: {response['questions_found']}")
    print("-" * 60)
    print(f"Кому: {response['to']}")
    print(f"Тема: {response['subject']}")
    print("-" * 60)
    print(response['body'])
    print("=" * 60)
