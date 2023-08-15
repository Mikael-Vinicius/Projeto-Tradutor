from flask import Blueprint, render_template
# from deep_translator import GoogleTranslator
from models.language_model import LanguageModel
# from models.history_model import HistoryModel


translate_controller = Blueprint("translate_controller", __name__)


# Reqs. 4 e 5
@translate_controller.route("/", methods=["GET", "POST"])
def index():
    languages = LanguageModel.list_dicts()
    translate_from = "Português"
    translate_to = "Ingles"
    text_to_translate = "O que deseja traduzir"
    translated = "Tradução"
    return render_template("index.html", languages=languages,
                           text_to_translate=text_to_translate,
                           translate_from=translate_from,
                           translate_to=translate_to,
                           translated=translated)


# Req. 6
@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    raise NotImplementedError
