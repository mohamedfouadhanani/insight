from Decision_tree import DecisionTree
import numpy as np
from collections import Counter

class RandomForest:
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, n_feature=None):
        self.n_trees = n_trees
        self.max_depth=max_depth
        self.min_samples_split=min_samples_split
        self.n_features=n_feature
        self.trees = []
        self.feature_indx_trees = []
    
    def fit(self, X, y):
        self.trees = []
        self.feature_indx_trees = []
        for _ in range(self.n_trees):
            tree = DecisionTree(max_depth=self.max_depth, min_samples_split=self.min_samples_split,
                            n_features=self.n_features)
            
            # split dataset to sub features
            idxs = self._bootstrap_features(X)
            self.feature_indx_trees.append(idxs)
            tree.fit(X[:, idxs], y)
            self.trees.append(tree)

    def _bootstrap_features(self, X):
        nb_features = X.shape[1]
        idxs = np.random.choice(nb_features, 15, replace=True)
        return idxs

    def _most_common_label(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common

    def predict(self, X):
        predictions = np.array([self.trees[i].predict(X[:, self.feature_indx_trees[i]]) for i in range(len(self.trees))])
        tree_preds = np.swapaxes(predictions, 0, 1)
        predictions = np.array([self._most_common_label(pred) for pred in tree_preds])
        return predictions

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

if __name__ == "__main__":
    
    # import the dataset
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    # get the class
    df = pd.read_excel(file_content)
    y = df["Attrition"].to_numpy()

    df = df.drop("Attrition", axis=1)
    df = df.drop("Unnamed: 0", axis=1)
    
    X = df.to_numpy()

    # spliting data : train (80%), test (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


    # Rf = RandomForest(n_trees=20)
    Rf = RandomForest(n_trees=15)
    Rf.fit(X_train, y_train)
    predictions = Rf.predict(X_test)

    acc =  accuracy(y_test, predictions)
    print("Accuracy of RF : ", acc)

