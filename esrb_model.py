import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def _train(model):
    x = model.dataset[ESRBModel.relevant_columns]
    y = model.dataset[ESRBModel.target_column]

    train_X, test_X, train_y, test_y = train_test_split(x, y, test_size=0.19, random_state=0)

    train_X = model.scaler.fit_transform(train_X)
    model.fit(train_X, train_y)

    pred_y = model.predict(model.scaler.transform(test_X))
    model.confusion_matrix = confusion_matrix(test_y, pred_y)
    model.accuracy_score = accuracy_score(test_y, pred_y)


class ESRBModel(LogisticRegression):
    relevant_columns = ['alcohol_reference', 'animated_blood', 'blood', 'blood_and_gore', 'cartoon_violence',
                        'crude_humor', 'drug_reference', 'fantasy_violence', 'intense_violence', 'language', 'lyrics',
                        'mature_humor', 'mild_blood', 'mild_cartoon_violence', 'mild_fantasy_violence',
                        'mild_language', 'mild_lyrics', 'mild_suggestive_themes', 'mild_violence', 'nudity',
                        'partial_nudity', 'sexual_content', 'sexual_themes', 'simulated_gambling', 'strong_language',
                        'strong_sexual_content', 'suggestive_themes', 'use_of_alcohol', 'use_of_drugs_and_alcohol',
                        'violence']
    target_column = 'esrb_rating'

    def __init__(self, filename):
        super().__init__(random_state=0)
        self.filename = filename
        self.dataset = pd.read_csv(filename)
        self.scaler = StandardScaler()
        self.confusion_matrix = None
        self.accuracy_score = None
        _train(self)

    def predict_rating(self, content_dict):
        content_df = pd.DataFrame(content_dict, index=[0])
        return self.predict(self.scaler.transform(content_df))
