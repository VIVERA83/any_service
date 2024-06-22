class TestGetMemes:
    def test_get_all_memes(self, client):
        response = client.get("/memes")
        assert response.status_code == 200

    def test_create_one_team(self, client):
        response = client.get("/memes")
        print(response.status_code)
        assert response.status_code == 200
        # received = response.json()
        # expected = {"id": 1, "name": "Scuderia Ferrari"}

        # assert received == expected
