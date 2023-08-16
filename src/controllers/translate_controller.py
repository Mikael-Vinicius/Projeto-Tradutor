from flask import Blueprint, render_template, request, jsonify
from deep_translator import GoogleTranslator
from models.language_model import LanguageModel
from models.history_model import HistoryModel


translate_controller = Blueprint("translate_controller", __name__)
history_controller = Blueprint("history_controller", __name__)


# Reqs. 4 e 5
@translate_controller.route("/", methods=["GET", "POST"])
def index():
    languages = LanguageModel.list_dicts()
    translate_from = request.form.get("translate-from")
    translate_to = request.form.get("translate-to")
    text_to_translate = request.form.get("text-to-translate")
    translated = (GoogleTranslator(
        source=translate_from,
        target=translate_to
        ).translate(text_to_translate)
        if request.method == "POST"
        else "Tradução"
        )
    history_data = {
        "original_text": text_to_translate,
        "translated_text": translated,
        "source_language": translate_from,
        "target_language": translate_to
    }
    HistoryModel(history_data).save()
    return render_template("index.html", languages=languages,
                           text_to_translate=text_to_translate,
                           translate_from=translate_from,
                           translate_to=translate_to,
                           translated=translated)


# Req. 6
@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    text_to_translate = request.form.get("text-to-translate")
    translate_from = request.form.get("translate-from")
    translate_to = request.form.get("translate-to")

    new_translate_from = translate_to
    new_translate_to = translate_from
    inverted_translation = GoogleTranslator(
        source=translate_from,
        target=translate_to
    ).translate(text_to_translate)
    return render_template("index.html", languages=LanguageModel.list_dicts(),
                           text_to_translate=inverted_translation,
                           translated=inverted_translation,
                           translate_from=new_translate_from,
                           translate_to=new_translate_to
                           )


@history_controller.route("/history/", methods=["GET"])
def get_history():
    history = HistoryModel.list_as_json()

    return jsonify(history), 200
