import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_popular_article(top_n: int = 100) -> list[dict[str, str]]:
    response_articles = requests.get(os.environ.get("API_ENDPOINT")).json()["articles"]
    popular_artilces = sorted(
        response_articles, key=lambda x: x["liked_count"], reverse=True
    )[:top_n]
    # print(popular_artilces)
    return popular_artilces


def choose_ai_article(popular_artilce: list[dict[str, str]]) -> list[dict[str, str]]:
    title_list = [article["title"] for article in popular_artilce]

    message = f"""
    あなたは、RubyとRuby on railsに関する記事を紹介するプロです。
    以下は、RubyとRuby on railsに関する記事のタイトルリストです。
    リストから、最もRuby on railsに関する記事を選択してください。
    選定基準と、記事リストは以下です。
    アウトプットは、テキストは一切不要で、記事タイトルのみ返してください。

    【選定基準】
    ・Ruby on railsに関する記事 またはRubyに関する記事

    【記事リスト】
    {title_list}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
    )
    ai_article_title = response["choices"][0]["message"]["content"]

    ai_article = [
        article for article in popular_artilce if article["title"] in ai_article_title
    ]

    return ai_article[0]


def summary_tweet(ai_article: list[dict[str, str]]) -> str:
    personality = f"""
    あなたはRubyとRuby on railsのプロです。
    次の記事タイトルに対して、プロの観点から、活用方法や学びをシェアします。
    
    回答フォーマットは以下です。

    返答は140字以内で構成してください。
    繰り返します140字以内でお願いします!!!!!!   

    【回答フォーマット】
    🛑Ruby on Railsの記事を紹介🛑
    [記事のタイトル名]

    Railsのxxxについて学習できます!

    ・キーワード
    xxx, xxx,

    https://zenn.dev/neet/articles/{ai_article["slug"]}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": ai_article["title"]},
        ],
    )
    return response["choices"][0]["message"]["content"]