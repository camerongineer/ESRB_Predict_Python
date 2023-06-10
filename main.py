from data_visualizer import DataVisualizer
from esrb_model import ESRBModel
from game_content_gatherer import GameContentGatherer
from gui import GUI
from rating import Rating, get_category_by_criteria, Level
from ui import ui_print


def _display_accuracy_percentage(model):
    ui_print(f'\nThis program currently has an accuracy rate of {int(model.accuracy_score * 100)}%'
             f' and continues to improve as new data is gathered.\n')


def _display_predicted_rating(model):
    predicted_rating = model.predict_rating(GameContentGatherer.gather())[0]
    rating_description = [rating.description for rating in Rating if rating.name == predicted_rating][0]
    ui_print(f'\nThe predicted rating of this game is "{rating_description}".\n')


def _menu(model):
    ui_print('Welcome to ESRB Rating Predictor')
    ui_print('This program will predict the rating of a video-game based on similar'
             ' content in previously rated game releases.\n')
    while True:
        ui_print('Please select from the list of options below')
        ui_print('1: Get the predicted ESRB rating of a game')
        ui_print('2: Display program accuracy information')
        ui_print('0: Exit\n')
        ui_print('Please type ["0", "1", or "2"]: ', end='')
        user_input = input().lower().strip()
        if user_input == '1':
            _display_predicted_rating(model)
        elif user_input == '2':
            _display_accuracy_percentage(model)
        elif user_input == '3':
            DataVisualizer.get_bar_chart(model, get_category_by_criteria(), all_types=True)
            DataVisualizer.get_pie_chart(model, get_category_by_criteria(), all_types=True)
            # DataVisualizer.get_confusion_matrix(model)
        elif user_input == '0':
            ui_print('Bye!')
            break
        else:
            ui_print('\nInvalid Option!\n')


if __name__ == '__main__':
    esrb_model = ESRBModel('data/esrb_ratings.csv')
    gui = GUI(esrb_model)
