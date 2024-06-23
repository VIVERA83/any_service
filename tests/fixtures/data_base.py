from uuid import UUID

import pytest
from sqlalchemy import text

meme1_id = "57e87c2d-bb27-46a2-9451-af401f7aec16"
meme2_id = "57e87c2d-bb27-46a2-9451-af401f7aec17"
meme3_id = "57e87c2d-bb27-46a2-9451-af401f7aec18"
meme4_id = "57e87c2d-bb27-46a2-9451-af401f7aec19"
meme5_id = "57e87c2d-bb27-46a2-9451-af401f7aec20"

title_1 = "test_1"
title_2 = "test_2"
title_3 = "test_3"
title_4 = "test_4"
title_5 = "test_5"


@pytest.fixture
async def data_1(application):
    await application.postgres.query_execute(
        text(
            f"INSERT INTO meme_center.memes (id, title) "
            f"VALUES ('{meme1_id}', '{title_1}');"
        )
    )
    await application.postgres._engine.dispose()
    return {"id": meme1_id, "title": title_1}


@pytest.fixture
async def data_2(application):
    await application.postgres.query_execute(
        text(
            f"INSERT INTO meme_center.memes (id, title) "
            f"VALUES ('{meme2_id}', '{title_2}');"
        )
    )
    await application.postgres._engine.dispose()
    return {"id": meme2_id, "title": title_2}


@pytest.fixture
async def data_3(application):
    await application.postgres.query_execute(
        text(
            f"INSERT INTO meme_center.memes (id, title) "
            f"VALUES ('{meme3_id}', '{title_3}');"
        )
    )
    await application.postgres._engine.dispose()
    return {"id": meme3_id, "title": title_3}


@pytest.fixture
async def data_4(application):
    await application.postgres.query_execute(
        text(
            f"INSERT INTO meme_center.memes (id, title) "
            f"VALUES ('{meme4_id}', '{title_4}');"
        )
    )
    await application.postgres._engine.dispose()
    return {"id": meme4_id, "title": title_4}


@pytest.fixture
async def data_5(application):
    await application.postgres.query_execute(
        text(
            f"INSERT INTO meme_center.memes (id, title) "
            f"VALUES ('{meme5_id}', '{title_5}');"
        )
    )
    await application.postgres._engine.dispose()
    return {"id": meme5_id, "title": title_5}
