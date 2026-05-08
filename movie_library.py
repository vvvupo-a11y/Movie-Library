import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Управление фильмами")
        self.root.geometry("900x600")

        # Файл для хранения данных
        self.data_file = "movies.json"

        # Загрузка данных
        self.movies = self.load_movies()

        # Создание интерфейса
        self.create_widgets()

        # Обновление таблицы
        self.refresh_table()

    def load_movies(self):
        """Загрузка фильмов из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except:
                return []
        return []

    def save_movies(self):
        """Сохранение фильмов в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавление фильма", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie,
                                    bg="green", fg="white", font=("Arial", 10, "bold"))
        self.add_button.grid(row=1, column=4, padx=20, pady=5)

        # Рамка для фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5, pady=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5, pady=5)
        self.genre_filter.bind("<KeyRelease>", self.filter_movies)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, padx=5, pady=5)
        self.year_filter = tk.Entry(filter_frame, width=10)
        self.year_filter.grid(row=0, column=3, padx=5, pady=5)
        self.year_filter.bind("<KeyRelease>", self.filter_movies)

        tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters,
                  bg="orange").grid(row=0, column=4, padx=20, pady=5)

        # Таблица для отображения фильмов
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        # Настройка колонок
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")

        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=100)
        self.tree.column("Рейтинг", width=100)

        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка удаления фильма
        delete_frame = tk.Frame(self.root)
        delete_frame.pack(fill="x", padx=10, pady=5)

        self.delete_button = tk.Button(delete_frame, text="Удалить выбранный фильм",
                                       command=self.delete_movie, bg="red", fg="white")
        self.delete_button.pack(side="right", padx=5)

        # Статистика
        self.stats_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.stats_label.pack(pady=5)

    def validate_movie(self, title, genre, year_str, rating_str):
        """Проверка корректности ввода данных"""
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми!")
            return False

        # Проверка года
        try:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1888 or year > current_year + 5:
                messagebox.showerror("Ошибка", f"Год должен быть между 1888 и {current_year + 5}!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False

        return True

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if self.validate_movie(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }

            self.movies.append(movie)
            self.save_movies()
            self.refresh_table()

            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)

            messagebox.showinfo("Успех", f"Фильм '{title}' успешно добавлен!")

    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return

        # Получение названия фильма для подтверждения
        values = self.tree.item(selected[0])['values']
        if values:
            title = values[0]
            if messagebox.askyesno("Подтверждение", f"Удалить фильм '{title}'?"):
                # Поиск и удаление фильма
                for i, movie in enumerate(self.movies):
                    if movie["title"] == title and movie["year"] == int(values[2]):
                        del self.movies[i]
                        break

                self.save_movies()
                self.refresh_table()
                messagebox.showinfo("Успех", "Фильм удален!")

    def filter_movies(self, event=None):
        """Фильтрация фильмов по жанру и году"""
        genre_filter = self.genre_filter.get().strip().lower()
        year_filter = self.year_filter.get().strip()

        filtered_movies = self.movies

        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_int]
            except ValueError:
                # Если год не число, игнорируем фильтр
                pass

        self.update_table_display(filtered_movies)

    def reset_filters(self):
        """Сброс фильтров"""
        self.genre_filter.delete(0, tk.END)
        self.year_filter.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы со всеми фильмами"""
        self.update_table_display(self.movies)

    def update_table_display(self, movies_list):
        """Обновление отображаемых данных в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавление фильмов
        for movie in movies_list:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

        # Обновление статистики
        total = len(movies_list)
        avg_rating = sum(m["rating"] for m in movies_list) / total if total > 0 else 0
        self.stats_label.config(text=f"Всего фильмов: {total} | Средний рейтинг: {avg_rating:.2f}")


def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()


if __name__ == "__main__":
    main()