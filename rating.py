from enum import Enum


class Rating(Enum):
    E = 'Everyone'
    ET = 'Everyone 10+'
    T = 'Teen'
    M = 'Mature 17+'

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class Type(Enum):
    CONTENT = 'Adult Content'
    LANGUAGE = 'Adult Language'
    SEXUAL = 'Sexual Content'
    VIOLENCE = 'Violence'

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class Level(Enum):
    MILD = 'Mild', 1
    AVERAGE = 'Average', 2
    EXTREME = 'Extreme', 3

    def __init__(self, description, number):
        self.description = description
        self.number = number

    def __str__(self):
        return self.description

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number


class Category(Enum):
    ALCOHOL_REFERENCE = 'alcohol_reference', Level.MILD, Type.CONTENT, 'References to Alcohol'
    ANIMATED_BLOOD = 'animated_blood', Level.MILD, Type.VIOLENCE, 'Animated Blood'
    BLOOD = 'blood', Level.AVERAGE, Type.VIOLENCE, 'Blood'
    BLOOD_AND_GORE = 'blood_and_gore', Level.AVERAGE, Type.VIOLENCE, 'Blood and Gore'
    CARTOON_VIOLENCE = 'cartoon_violence', Level.AVERAGE, Type.VIOLENCE, 'Cartoon Violence'
    CRUDE_HUMOR = 'crude_humor', Level.AVERAGE, Type.LANGUAGE, 'Crude Humor'
    DRUG_REFERENCE = 'drug_reference', Level.MILD, Type.CONTENT, 'References to Drugs'
    FANTASY_VIOLENCE = 'fantasy_violence', Level.AVERAGE, Type.VIOLENCE, 'Fantasy Violence'
    INTENSE_VIOLENCE = 'intense_violence', Level.EXTREME, Type.VIOLENCE, 'Intense Violence'
    LANGUAGE = 'language', Level.AVERAGE, Type.LANGUAGE, 'Adult Language'
    LYRICS = 'lyrics', Level.AVERAGE, Type.LANGUAGE, 'Adult Lyrics'
    MATURE_HUMOR = 'mature_humor', Level.AVERAGE, Type.LANGUAGE, 'Mature Humor'
    MILD_BLOOD = 'mild_blood', Level.MILD, Type.VIOLENCE, 'Mild Blood'
    MILD_CARTOON_VIOLENCE = 'mild_cartoon_violence', Level.MILD, Type.VIOLENCE, 'Mild Cartoon Violence'
    MILD_FANTASY_VIOLENCE = 'mild_fantasy_violence', Level.MILD, Type.VIOLENCE, 'Mild Fantasy Violence'
    MILD_LANGUAGE = 'mild_language', Level.MILD, Type.LANGUAGE, 'Mild Language'
    MILD_LYRICS = 'mild_lyrics', Level.MILD, Type.LANGUAGE, 'Mild Lyrics'
    MILD_SUGGESTIVE_THEMES = 'mild_suggestive_themes', Level.MILD, Type.SEXUAL, 'Mild Suggestive Themes'
    MILD_VIOLENCE = 'mild_violence', Level.MILD, Type.VIOLENCE, 'Mild Violence'
    NUDITY = 'nudity', Level.EXTREME, Type.SEXUAL, 'Nudity'
    PARTIAL_NUDITY = 'partial_nudity', Level.AVERAGE, Type.SEXUAL, 'Partial Nudity'
    SEXUAL_CONTENT = 'sexual_content', Level.AVERAGE, Type.SEXUAL, 'Sexual Content'
    SEXUAL_THEMES = 'sexual_themes', Level.AVERAGE, Type.SEXUAL, 'Sexual Themes'
    SIMULATED_GAMBLING = 'simulated_gambling', Level.AVERAGE, Type.CONTENT, 'Simulated Gambling'
    STRONG_LANGUAGE = 'strong_language', Level.EXTREME, Type.LANGUAGE, 'Strong Adult Language'
    STRONG_SEXUAL_CONTENT = 'strong_sexual_content', Level.EXTREME, Type.SEXUAL, 'Strong Sexual Content'
    SUGGESTIVE_THEMES = 'suggestive_themes', Level.AVERAGE, Type.SEXUAL, 'Suggestive Themes'
    USE_OF_ALCOHOL = 'use_of_alcohol', Level.AVERAGE, Type.CONTENT, 'Use of Alcohol'
    USE_OF_DRUGS_AND_ALCOHOL = 'use_of_drugs_and_alcohol', Level.EXTREME, Type.CONTENT, 'Use of Drugs and Alcohol'
    VIOLENCE = 'violence', Level.AVERAGE, Type.VIOLENCE, 'Violence'

    def __init__(self, column: str, level: Level, content_type: Type, description: str):
        self.column = column
        self.level = level
        self.content_type = content_type
        self.description = description

    def __str__(self):
        return self.description


class Group(Enum):
    BLOOD = Category.BLOOD.description, [Category.MILD_BLOOD, Category.BLOOD, Category.BLOOD_AND_GORE]
    CARTOON_VIOLENCE = Category.CARTOON_VIOLENCE.description, [Category.MILD_CARTOON_VIOLENCE,
                                                               Category.CARTOON_VIOLENCE]
    FANTASY_VIOLENCE = Category.FANTASY_VIOLENCE.description, [Category.MILD_FANTASY_VIOLENCE,
                                                               Category.FANTASY_VIOLENCE]
    LANGUAGE = Category.LANGUAGE.description, [Category.MILD_LANGUAGE, Category.LANGUAGE, Category.STRONG_LANGUAGE]
    LYRICS = Category.LYRICS.description, [Category.MILD_LYRICS, Category.LYRICS]
    NUDITY = Category.NUDITY.description, [Category.PARTIAL_NUDITY, Category.NUDITY]
    SEXUAL = Category.SEXUAL_CONTENT.description, [Category.SEXUAL_CONTENT, Category.STRONG_SEXUAL_CONTENT]
    SUGGESTIVE_THEMES = Category.SUGGESTIVE_THEMES.description, [Category.MILD_SUGGESTIVE_THEMES,
                                                                 Category.SUGGESTIVE_THEMES]
    VIOLENCE = Category.VIOLENCE.description, [Category.MILD_VIOLENCE, Category.VIOLENCE, Category.INTENSE_VIOLENCE]
    USE_OF_DRUG_ALCOHOL = 'Use of Drugs/Alcohol', [Category.USE_OF_ALCOHOL, Category.USE_OF_DRUGS_AND_ALCOHOL]

    def __init__(self, description, group):
        self.description = description
        self.group = group

    def __str__(self):
        return self.description


def get_category_by_criteria(levels=None, content_types=None):
    if not levels or not content_types:
        return None

    filtered_enums = []
    for enum in Category:
        if levels is not None and enum.level not in levels:
            continue
        if content_types is not None and enum.content_type not in content_types:
            continue
        filtered_enums.append(enum)

    return filtered_enums
