from esrb_model import ESRBModel
from ui import ui_get_binary_answer, ui_get_range_answer


def _get_drug_alcohol_content():
    drug_alcohol_dict = {'alcohol_reference': ui_get_binary_answer('Are there references to alcohol?'),
                         'drug_reference': ui_get_binary_answer('Are there references to drugs?'),
                         'use_of_alcohol': 0, 'use_of_drugs_and_alcohol': 0}
    if drug_alcohol_dict['alcohol_reference']:
        drug_alcohol_dict['use_of_alcohol'] = ui_get_binary_answer('Is the consumption of alcohol depicted?')
        if drug_alcohol_dict['use_of_alcohol']:
            drug_alcohol_dict['alcohol_reference'] = 0
    if drug_alcohol_dict['use_of_alcohol'] and drug_alcohol_dict['drug_reference']:
        drug_alcohol_dict['use_of_drugs_and_alcohol'] = ui_get_binary_answer('Is the use of drugs depicted?')
        if drug_alcohol_dict['use_of_drugs_and_alcohol']:
            drug_alcohol_dict['use_of_alcohol'] = 0
            drug_alcohol_dict['drug_reference'] = 0
    return drug_alcohol_dict


def _get_violence_content(art_style):
    violence_dict = {'Realistic': ['mild_violence', 'violence'],
                     'Fantasy': ['mild_fantasy_violence', 'fantasy_violence'],
                     'Cartoon': ['mild_cartoon_violence', 'cartoon_violence']}
    if ui_get_binary_answer('Are there any depictions of violence?'):
        level = ui_get_range_answer('What is the maximum level of violence? '
                                    '["0" = Mild, "1" = Average, "2" = Extreme]', range_size=2)
        if level == 2:
            return {'intense_violence': 1}
        else:
            return {violence_dict[art_style][level]: 1}
    return {}


def _get_blood_content(art_style):
    blood_dict = {'Realistic': ['mild_blood', 'blood'],
                  'Fantasy': ['mild_blood', 'blood'],
                  'Cartoon': ['animated_blood', 'animated_blood']}
    if ui_get_binary_answer('Is blood shown in the game?'):
        if art_style == 'Realistic':
            level = ui_get_range_answer('What is the maximum level of blood shown? '
                                        '["0" = Mild, "1" = Average, "2" = Blood and Gore] | ', range_size=2)
        else:
            level = ui_get_binary_answer('Is it more than a mild amount of blood?')
        if level == 2:
            return {'blood_and_gore': 1}
        else:
            return {blood_dict[art_style][level]: 1}
    return {}


def _get_suggestive_content():
    if ui_get_binary_answer('Does the game include any suggestive content?'):
        if ui_get_binary_answer('Is it more than a mild level of suggestive content?'):
            return {'suggestive_themes': 1}
        else:
            return {'mild_suggestive_themes': 1}
    return {}


def _get_sexual_content():
    sexual_content_dict = {}
    if ui_get_binary_answer('Are any sexual content or themes in the game?'):
        sexual_content_dict['sexual_themes'] = 1
        if ui_get_binary_answer('Does it go beyond mire references to sexuality?'):
            if ui_get_binary_answer('Is there a high level of sexual content?'):
                sexual_content_dict['strong_sexual_content'] = 1
            else:
                sexual_content_dict['sexual_content'] = 1
    return sexual_content_dict


def _get_gambling_content():
    return {'simulated_gambling': ui_get_binary_answer('Are there depictions of gambling?')}


def _get_language_content():
    if ui_get_binary_answer('Is there any foul language?'):
        level = ui_get_range_answer('What level of foul language is in the game? '
                                    '["0" = Mild, "1" = Average, "2" = Extreme]', range_size=2)
        if level == 0:
            return {'mild_language': 1}
        elif level == 1:
            return {'language': 1}
        else:
            return {'strong_language': 1}
    return {}


def _get_nudity_content():
    if ui_get_binary_answer('Is there nudity?'):
        if ui_get_binary_answer('Is it more than partial nudity?'):
            return {'nudity': 1}
        else:
            return {'partial_nudity': 1}
    return {}


def _get_crude_humor_content():
    return {'crude_humor': ui_get_binary_answer('Is there any crude humor?')}


def _get_mature_humor_content():
    return {'mature_humor': ui_get_binary_answer('Is there any mature humor?')}


def _get_lyrics_content():
    if ui_get_binary_answer('Is there any music with vocal lyrics that contain foul language?'):
        if ui_get_binary_answer('Is it more than a mild amount of foul language in the lyrics?'):
            return {'lyrics': 1}
        else:
            return {'mild_lyrics': 1}
    return {}


def _get_art_style(art_styles):
    return ui_get_range_answer('What is the art style of the game? '
                               f'["0" = {art_styles[0]}, "1" = {art_styles[1]}, "2" = {art_styles[2]}]', range_size=2)


def _adjust_content_dict(content_dict, *new_values):
    for content in new_values:
        for category, option in content.items():
            content_dict[category] = option


class GameContentGatherer:
    required_content = ESRBModel.relevant_columns
    art_style_dict = {0: 'Realistic', 1: 'Fantasy', 2: 'Cartoon'}

    def __init__(self):
        pass

    @staticmethod
    def gather():
        content_dict = {category: 0 for category in GameContentGatherer.required_content}
        art_style = GameContentGatherer.art_style_dict[_get_art_style(GameContentGatherer.art_style_dict)]
        _adjust_content_dict(content_dict,
                             _get_violence_content(art_style),
                             _get_blood_content(art_style),
                             _get_language_content(),
                             _get_crude_humor_content(),
                             _get_mature_humor_content(),
                             _get_lyrics_content(),
                             _get_suggestive_content(),
                             _get_sexual_content(),
                             _get_nudity_content(),
                             _get_drug_alcohol_content(),
                             _get_gambling_content())
        return content_dict
