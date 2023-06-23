from esrb_model import ESRBModel
from gui import GUI

if __name__ == '__main__':
    esrb_model = ESRBModel('data/esrb_ratings.csv')
    gui = GUI(esrb_model)
