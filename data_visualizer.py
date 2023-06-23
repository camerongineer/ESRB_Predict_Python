import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FixedFormatter
from sklearn.metrics import ConfusionMatrixDisplay

from rating import Rating, Type


def _get_levels_string(categories):
    category_levels = sorted(list(set([category.level for category in categories])))
    if len(category_levels) == 1:
        return category_levels[0]
    else:
        return ', '.join([str(level.description) for level in category_levels[:-1]]) + f' or {category_levels[-1]}'


def _get_category_type_string(categories, all_types):
    category_types = sorted(list(set([category.content_type.description for category in categories])))
    if len(category_types) == 1:
        return category_types[0]
    else:
        return ', '.join(category_types[:-1]) + (' and ' if all_types else ' or ') + category_types[-1]


def _get_all_types(model, categories):
    content_columns = [category.column for category in categories if category.content_type == Type.CONTENT]
    language_columns = [category.column for category in categories if category.content_type == Type.LANGUAGE]
    sexual_columns = [category.column for category in categories if category.content_type == Type.SEXUAL]
    violence_columns = [category.column for category in categories if category.content_type == Type.VIOLENCE]
    return model.dataset[
        (model.dataset[content_columns].sum(axis=1) > 0 if content_columns else True) &
        (model.dataset[language_columns].sum(axis=1) > 0 if language_columns else True) &
        (model.dataset[sexual_columns].sum(axis=1) > 0 if sexual_columns else True) &
        (model.dataset[violence_columns].sum(axis=1) > 0 if violence_columns else True)
        ]


def _set_chart_columns(model, categories, all_types):
    category_columns = [category.column for category in categories]
    data = _get_all_types(model, categories) if all_types else model.dataset[
        (model.dataset[category_columns].sum(axis=1) > 0)]
    rating_order = ['E', 'ET', 'T', 'M']
    rating_labels = [Rating.E, Rating.ET, Rating.T, Rating.M]
    level_str = _get_levels_string(categories)
    category_types_str = _get_category_type_string(categories, all_types)
    return data, rating_order, rating_labels, level_str, category_types_str


class DataVisualizer:
    @staticmethod
    def get_bar_chart(model, categories, all_types=False):
        data, rating_order, rating_labels, level_str, category_types_str = \
            _set_chart_columns(model, categories, all_types)
        sns.set_style('whitegrid')
        plt.figure(figsize=(14, 10))
        ax = sns.countplot(x='esrb_rating', data=data, order=rating_order)
        ax.xaxis.set_major_formatter(FixedFormatter(rating_labels))

        plt.xlabel('\nESRB Rating', fontdict={'weight': 'bold', 'size': 12})
        plt.ylabel(f'Number of Games with {level_str} {category_types_str}\n',
                   fontdict={'weight': 'bold', 'size': 10})
        plt.title(f'ESRB Rating of Games Containing {level_str}\n{category_types_str}\n',
                  fontdict={'weight': 'bold', 'size': 14})
        plt.show()

    @staticmethod
    def get_confusion_matrix(model):
        rating_labels = [Rating.E, Rating.ET, Rating.T, Rating.M]
        cmd = ConfusionMatrixDisplay(model.confusion_matrix, display_labels=rating_labels)
        fig, ax = plt.subplots(figsize=(11, 12))
        cmd.plot(colorbar=False, ax=ax, xticks_rotation='vertical')
        plt.title('Confusion Matrix\n', fontdict={'weight': 'bold', 'size': 22})
        plt.ylabel('\nTrue Ratings', fontdict={'weight': 'bold', 'size': 14})
        plt.xlabel(f'\nPredicted Ratings ({round(model.accuracy_score * 100)}% accurate)', fontdict={'weight': 'bold', 'size': 14})
        plt.grid(False)
        plt.show()

    @staticmethod
    def get_pie_chart(model, categories, all_types=False):
        data, rating_order, rating_labels, level_str, category_types_str = \
            _set_chart_columns(model, categories, all_types)
        rating_counts = data['esrb_rating'].value_counts()
        plt.figure(figsize=(7, 7))
        plt.pie(rating_counts, labels=[Rating[rating].description for rating in rating_counts.keys()],
                autopct='%1.1f%%')
        plt.title(f'Distribution of ESRB Ratings of Games\nContaining {level_str}\n{category_types_str}\n',
                  fontdict={'weight': 'bold', 'size': 12})
        plt.show()
