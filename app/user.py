class User:
    def __init__(self, username, password):
        self.id = None
        self.username = username
        self.password = password

    def create_note(self, title, content, category):
        # создание заметки
        pass

    def delete_note(self, note_id):
        # удаление заметки
        pass

    def get_user_notes(self):
        # получение списка заметок пользователя из базы данных
        pass

    def share_note(self, note, with_user):
        # Когданибудь
        pass
