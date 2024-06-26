from app.models import Anime, AnimeFranchise
from sqlalchemy import select
from app import utils


# TODO: optimize it
async def save_anime_franchises_list(session, data):
    content_ids = [entry["content_id"] for entry in data]

    cache = await session.scalars(
        select(AnimeFranchise).filter(
            AnimeFranchise.content_id.in_(content_ids)
        )
    )

    franchises_cache = {entry.content_id: entry for entry in cache}

    for franchise_data in data:
        if not (
            franchise := franchises_cache.get(franchise_data["content_id"])
        ):
            franchise = AnimeFranchise(content_id=franchise_data["content_id"])

        updated = utils.from_timestamp(franchise_data["updated"])

        if updated == franchise.updated:
            continue

        franchise.scored_by = franchise_data["scored_by"]
        franchise.score = franchise_data["score"]
        franchise.updated = updated

        session.add(franchise)
        await session.commit()

        cache = await session.scalars(
            select(Anime).filter(
                Anime.content_id.in_(franchise_data["franchise_entries"])
            )
        )

        update_anime = []

        for anime in cache:
            anime.franchise_relation = franchise
            update_anime.append(anime)

        session.add_all(update_anime)

        # print("Processed franchise " + franchise_data["content_id"])

    await session.commit()
