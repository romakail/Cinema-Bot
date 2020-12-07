import os
import typing as tp

import aiohttp
from googlesearch import search
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

NUMBER_OF_LINKS = 3

TMDB_TOKEN = "25304f41deeabe898a91c1c2fc800978"
SEARCH_BASE_URL = "https://api.themoviedb.org/3/search/movie?api_key="
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"
SAD_KEANU_REEVES_URL = "https://s00.yaplakal.com/pics/pics_original/1/0/5/13674501.jpg"
SEARCH_POSTFIX = " смотреть онлайн бесплатно в хорошем качестве"

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)


async def get_movie_info(movie_name: str) -> tp.Union[tp.Dict[str, tp.Any], None]:
    request_url = \
        SEARCH_BASE_URL \
        + TMDB_TOKEN \
        + "&query=" \
        + "+".join(movie_name.split(" "))

    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as response:
            print(f"Status : {response.status}")
            print("Content-type:", response.headers['content-type'])

            json_body = await response.json()
    if len(json_body["results"]) == 0:
        return None
    else:
        return json_body["results"][0]


async def search_google_link(query: str, num_links: int) -> tp.Union[tp.List[str], None]:
    try:
        return list(search(query, tld="co.in", lang="ru", num=num_links, stop=num_links, pause=2))
    except StopIteration:
        return None


async def get_hearts_part(movie_info: tp.Dict[str, tp.Any]) -> str:
    if "vote_average" in movie_info and movie_info["vote_average"] is not None:
        return "\n" + "❤" * round(movie_info["vote_average"]) + "💔" * (10 - round(movie_info["vote_average"]))
    else:
        return ""


async def get_overview_part(movie_info: tp.Dict[str, tp.Any]) -> str:
    if "overview" in movie_info and movie_info["overview"] is not None:
        return "\n\n" + movie_info["overview"]
    else:
        return ""


async def get_link_part(movie_info: tp.Dict[str, tp.Any]) -> str:
    if "original_title" in movie_info and movie_info["original_title"] is not None:
        links = await search_google_link(movie_info["original_title"] + SEARCH_POSTFIX, NUMBER_OF_LINKS)
        if links is not None:
            return "\n\n" + "\n".join(links)

    return "\nSorry, I haven't found the link =("


async def get_poster_url(movie_info: tp.Dict[str, tp.Any]) -> tp.Union[str, None]:
    if "poster_path" in movie_info and movie_info["poster_path"] is not None:
        return IMAGE_BASE_URL + movie_info["poster_path"]
    else:
        return None


async def generate_response_text_and_picture(message: types.Message) -> tp.Tuple[tp.Optional[str], tp.Union[str, None]]:
    movie_info = await get_movie_info(message.text)
    print(movie_info)

    if movie_info is None or "original_language" not in movie_info or movie_info['original_language'] is None:
        return "Sorry, I haven't found this movie =(", SAD_KEANU_REEVES_URL

    response_text: str = movie_info["original_title"]
    response_text += await get_hearts_part(movie_info)
    response_text += await get_overview_part(movie_info)
    response_text += await get_link_part(movie_info)

    return response_text, await get_poster_url(movie_info)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm CinemaBot!\nI can find a link on a movie you need.")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Simply write a name of a movie, and I'll show you everything I know about it")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def basic_response(message: types.Message):
    # print("Photo : ", message.photo)
    response_text, response_picture = await generate_response_text_and_picture(message)
    if response_text is not None:
        await message.reply(response_text, reply=False)
    if response_picture is not None:
        await message.reply_photo(response_picture, reply=False)


@dp.message_handler()
async def default_response(message: types.Message):
    await message.reply("Sorry friend, I don't know how to help you", reply=False)


if __name__ == '__main__':
    executor.start_polling(dp)
