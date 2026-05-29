import time
import string
import random


class URLShortener:
    """
    Класс для сокращения ссылок, реализующий кэширование с вытеснением
    по алгоритму LFU (Least Frequently Used) / LRU (Least Recently Used).
    """

    def __init__(self, capacity: int):
        """
        Инициализация сокращателя.

        Args:
            capacity (int): Максимальное количество ссылок в памяти.
        """
        self.capacity = capacity
        # Хэш-таблицы для обеспечения поиска за нелинейное время O(1)
        self.short_to_long = {}
        self.long_to_short = {}

        # Статистика: {short_url_code: {"clicks": int, "created_at": float}}
        self.stats = {}

    def _generate_short_code(self) -> str:
        """Генерирует уникальный случайный код из 6 символов."""
        chars = string.ascii_letters + string.digits
        while True:
            code = "".join(random.choice(chars) for _ in range(6))
            if code not in self.short_to_long:
                return code

    def shorten(self, long_url: str) -> str:
        """
        Возвращает короткий URL по длинному.
        Если лимит превышен, удаляет самую неиспользуемую ссылку.
        """
        if long_url in self.long_to_short:
            return self.long_to_short[long_url]

        # Контроль памяти: удаление при превышении лимита
        if len(self.short_to_long) >= self.capacity:
            self._evict_least_used()

        code = self._generate_short_code()
        self.short_to_long[code] = long_url
        self.long_to_short[long_url] = code
        self.stats[code] = {"clicks": 0, "created_at": time.time()}
        return code

    def get_original(self, short_url: str) -> str:
        """
        Возвращает оригинальный URL по короткому и обновляет счетчик переходов.
        """
        code = short_url.split("/")[-1]
        if code not in self.short_to_long:
            return "URL not found"

        self.stats[code]["clicks"] += 1
        return self.short_to_long[code]

    def _evict_least_used(self):
        """
        Внутренний метод очистки. Находит и удаляет ссылку,
        к которой обращались реже всего. При равенстве - самую старую.
        """
        # Сортировка O(N) применяется только в момент переполнения, сам поиск O(1)
        victim_code = min(
            self.stats.keys(),
            key=lambda k: (self.stats[k]["clicks"], self.stats[k]["created_at"])
        )

        long_url = self.short_to_long[victim_code]
        del self.short_to_long[victim_code]
        del self.long_to_short[long_url]
        del self.stats[victim_code]