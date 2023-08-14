from parsel import Selector
from src.models.language_model import LanguageModel


def test_request_translate(app_test):
    response = app_test.get("/")
    assert b"O que deseja traduzir" in response.data
    assert bytes("Tradução", "utf8") in response.data
    assert b"ENGLISH" in response.data
    assert b"AFRIKAANS" in response.data
    assert b"MOUSE" not in response.data

    total_options = Selector(text=str(response.data)).css("option")
    assert len(total_options) == len(LanguageModel.find()) * 2


def test_post_translate(app_test):
    response = app_test.post(
        "/",
        data={
            "text-to-translate": "Hello, I like videogame",
            "translate-from": "en",
            "translate-to": "pt",
        },
    )
    assert "Olá, eu gosto de videogame" in response.get_data(as_text=True)


def test_post_reverse(app_test):
    response = app_test.post(
        "/reverse",
        data={
            "text-to-translate": "Hello, I like videogame",
            "translate-from": "en",
            "translate-to": "pt",
        },
    )

    content_html = response.get_data(as_text=True)

    assert "Olá, eu gosto de videogame" in content_html

    selected_option_to = (
        Selector(text=str(content_html))
        .css('select[name="translate-to"] option[selected]::attr(value)')
        .get()
    )

    assert selected_option_to == "en"

    selected_option_from = (
        Selector(text=str(content_html))
        .css('select[name="translate-from"] option[selected]::attr(value)')
        .get()
    )
    assert selected_option_from == "pt"
