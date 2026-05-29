import unittest
from shortener import URLShortener
import time


class TestURLShortener(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр с лимитом 2 для удобства тестирования вытеснения
        self.shortener = URLShortener(capacity=2)

    def test_shorten_and_retrieve(self):
        """Проверка базового функционала: сокращение и получение оригинала."""
        long_url = "https://vk.com/feed"
        code = self.shortener.shorten(long_url)
        self.assertEqual(self.shortener.get_original(code), long_url)

    def test_duplicate_shorten(self):
        """При дублировании длинного URL должен возвращаться один и тот же код."""
        url = "https://github.com"
        code1 = self.shortener.shorten(url)
        code2 = self.shortener.shorten(url)
        self.assertEqual(code1, code2)

    def test_click_tracking(self):
        """Проверка подсчета кликов по ссылке."""
        code = self.shortener.shorten("https://example.com")
        self.shortener.get_original(code)
        self.shortener.get_original(code)
        self.assertEqual(self.shortener.stats[code]["clicks"], 2)

    def test_eviction_logic(self):
        """Проверка удаления непопулярной/старой ссылки при переполнении лимита."""
        code1 = self.shortener.shorten("url1")
        time.sleep(0.01)  # Имитация задержки создания
        code2 = self.shortener.shorten("url2")

        # Накручиваем клики для url2 (делаем популярным)
        self.shortener.get_original(code2)

        # Добавляем 3-ю ссылку (лимит = 2). Должен удалиться url1 (0 кликов)
        code3 = self.shortener.shorten("url3")

        self.assertEqual(self.shortener.get_original(code1), "URL not found")
        self.assertEqual(self.shortener.get_original(code2), "url2")
        self.assertEqual(self.shortener.get_original(code3), "url3")


if __name__ == '__main__':
    unittest.main()