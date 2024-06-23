import os
import uuid

from tests import BASE_DIR
from tests.fixtures import meme1_id, title_1


class TestGetMemes:
    async def test_memes(self, client, data_1, data_2, data_3):
        """Проверка получения всех мемов."""

        response = client.get("/memes")
        assert response.status_code == 200
        assert 3 == len(response.json()), f"Ожидает 3 мема. Получено: {response.json()}"
        assert (
                data_1 == response.json()[0]
        ), f"Ожидает {data_1}. Получено: {response.json()[0]}"
        assert (
                data_2 == response.json()[1]
        ), f"Ожидает {data_2}. Получено: {response.json()[0]}"
        assert (
                data_3 == response.json()[2]
        ), f"Ожидает {data_3}. Получено: {response.json()[0]}"

    async def test_memes_page_1(self, client, data_1, data_2, data_3, data_4, data_5):
        """Проверка получения всех мемов c пагинацией.
        Пагинация начинается с 2 страницы на 2 мема."""

        response = client.get("/memes?page=2&page_size=2")
        assert 2 == len(response.json()), f"Response: {response.json()}"
        assert data_3 == response.json()[0]
        assert data_4 == response.json()[1]

    async def test_memes_page_2(self, client, data_1, data_2, data_3, data_4, data_5):
        """Проверка получения всех мемов c пагинацией.
        Пагинация начинается с 3 страницы на 2 мема."""

        response = client.get("/memes?page=3&page_size=2")
        assert 1 == len(response.json()), f"Ожидает 1 мем. Получено: {response.json()}"
        assert (
                data_5 == response.json()[0]
        ), f"Ожидает {data_5}. Получено: {response.json()[0]}"


class TestCreateMeme:
    async def test_create(self, client):
        """Проверка создания мема."""

        boundary = uuid.uuid4().hex
        response = client.post(
            "/memes",
            files={"file": open(os.path.join(BASE_DIR, "tests/data/test.jpg"), "rb")},
            data={"text": title_1},
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        assert response.status_code == 200, f"Response: {response.json()}"
        assert response.json().get("status") == "Оk", "Ожидает Оk"
        assert "Мем добавлен, id" in response.json().get("message")


class TestDeleteMeme:
    def test_delete(self, client, data_1):
        """Проверка удаления мема."""
        response = client.delete(f"/memes/{meme1_id}")
        assert response.status_code == 200, f"Response: {response.json()}"
        assert response.json().get("status") == "Оk"

    def test_delete_not_found(self, client):
        """Проверка удаления несуществующего мема."""
        response = client.delete(f"/memes/{meme1_id}")
        assert response.status_code == 400


class TestUpdateMeme:
    def test_update_image(self, client, data_1):
        """Проверка обновления картинки мема."""
        boundary = uuid.uuid4().hex
        response = client.put(
            f"/memes/{meme1_id}",
            files={"file": open(os.path.join(BASE_DIR, "tests/data/test.jpg"), "rb")},
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        assert response.status_code == 200, f"Response: {response.json()}"
        assert response.json().get("status") == "Оk"

    def test_update_all(self, client, data_1):
        """Проверка обновления полностью мема."""

        boundary = uuid.uuid4().hex
        response = client.put(
            f"/memes/{meme1_id}",
            files={"file": open(os.path.join(BASE_DIR, "tests/data/test.jpg"), "rb")},
            data={"text": title_1},
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        assert response.status_code == 200, f"Response: {response.json()}"
        assert response.json().get("status") == "Оk"

    def test_update_not_found(self, client):
        """Проверка обновления несуществующего мема."""
        response = client.put(f"/memes/{meme1_id}", data={"text": title_1})
        assert response.status_code == 400
