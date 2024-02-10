import os
import random

import openai
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_popular_article(top_n: int = 15) -> list[dict[str, str]]:
    response_articles = requests.get(os.environ.get("API_ENDPOINT")).json()["articles"]
    selected_articles = random.sample(response_articles, k=len(response_articles)) 
    recent_articles = selected_articles[:top_n]
    return recent_articles


def choose_rails_article(recent_artilce: list[dict[str, str]]) -> list[dict[str, str]]:
    title_list = [article["title"] for article in recent_artilce]

    message = f"""
    RubyonRailsに関する記事を紹介するエキスパートです。
    以下は、RubyとRuby on railsに関する記事のタイトルリストです。
    エキスパートの観点から、活用方法や学び、tipsをシェアする記事を選定しなさい。
    選定基準と、記事リストは以下です。
    アウトプットは、テキストは一切不要で、記事タイトルのみ返してください。

    【選定基準】
    ・Rubyに関する記事またはRuby on railsに関する記事

    【記事リスト】
    {title_list}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
    )
    rails_article_title = response["choices"][0]["message"]["content"]

    rails_article = [
        article for article in recent_artilce if article["title"] in rails_article_title
    ]

    return rails_article[0]


def summary_tweet(rails_article: list[dict[str, str]]) -> str:
    personality = f"""
    あなたはRubyとRuby on railsのプロです。
    次の記事タイトルに対して、プロの観点から、活用方法や学びをシェアします。
    
    回答フォーマットは以下です。
    タイトルのみが出力できれば良いです。
    説明文等は必要ありません。

    ※注意事項
    返答は140字以内で構成してください。
    繰り返します140字以内でお願いします!!!!!!   

    【回答フォーマット】
    🛑Ruby on Railsの記事を紹介🛑
    🗣[記事のタイトル名]

    https://zenn.dev/neet/articles/{rails_article["slug"]}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": rails_article["title"]},
        ],
    )
    return response["choices"][0]["message"]["content"]