import numpy as np
from collections import Counter
import dill

class Node:
    def __init__(self, feature=None, thresholds=None,children=None,*,value=None):
        self.feature = feature
        self.children = children
        self.thresholds = thresholds
        self.value = value
        
    def is_leaf_node(self):
        return self.value is not None


class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split=min_samples_split
        self.max_depth=max_depth
        self.n_features=n_features
        self.root=None

    def fit(self, X, y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1],self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        if n_labels == 0:
            return Node(value=-1)

        # check the stopping condition
        if (depth>=self.max_depth or n_labels==1 or n_samples<self.min_samples_split):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # array feat_indxs of (29,)
        feat_idxs = np.random.choice(n_feats, self.n_features, replace=False)

        # find the best split
        best_feature, best_thresh = self._best_split(X, y, feat_idxs)

        # create child nodes
        children_idxs = self._split(X[:, best_feature])
        children = []
        for i in range(len(children_idxs)):
            child = self._grow_tree(X[children_idxs[i], :], y[children_idxs[i]], depth+1)
            children.append(child)
        thresholds = np.unique(X[:, best_feature])
        return Node(best_feature, thresholds, children)


    def _best_split(self, X, y, feat_idxs):
        best_gain = -1
        split_idx, split_threshold = None, None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            gain = self._information_gain(y, X_column)

            if gain > best_gain:
                best_gain = gain
                split_idx = feat_idx

        return split_idx, split_threshold


    def _information_gain(self, y, X_column):
        # parent entropy
        parent_entropy = self._entropy(y)

        # create children
        children_idxs = self._split(X_column)
        for i in range(len(children_idxs)):
            if len(children_idxs[i]) == 0:
                return 0

        n = len(y)
        n_child = []
        for i in range(len(children_idxs)):
            n_child.append(len(children_idxs[i]))
        
        e_child = []
        for i in range(len(children_idxs)):
            e_child.append(self._entropy(y[children_idxs[i]]))

        child_entropy = 0
        for i in range(len(n_child)):    
            child_entropy = child_entropy + (n_child[i]/n) * e_child[i]
        
        # calculate the IG
        information_gain = parent_entropy - child_entropy
        return information_gain

    def _split(self, X_column):
        values = np.unique(X_column)
        i = 0
        children_idxs = []
        for val in values:
            idx_val = np.argwhere(X_column <= val).flatten()
            children_idxs.append(idx_val)
        return children_idxs


    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p>0])


    def _most_common_label(self, y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value

        for i in range(node.thresholds.shape[0]):
            if x[node.feature] == node.thresholds[i]:
                return self._traverse_tree(x, node.children[i])

from sklearn.model_selection import train_test_split
import pandas as pd

def accuracy(y_test, y_pred):
    return np.sum(y_test == y_pred) / len(y_test)


def get_model():
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    df = pd.read_excel(file_content)
    
    # get class attribut
    y = df["Attrition"].to_numpy()
    # print("shape of Y : ", y.shape)

    df = df.drop("Attrition", axis=1)
    df = df.drop("Unnamed: 0", axis=1)

    # X with 29 features
    X = df.to_numpy()
    # print("shape of X : ", X.shape)

    # split the dataset into training set (80%) and testing set (20%)  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    Dt = DecisionTree(max_depth=10)
    
    Dt.fit(X_train, y_train)
    
    return Dt

if __name__ == "__main__":
    
    # import the preprocessed dataset
    with open("Dataset1_pretraitement_complet.xlsx", "rb") as file:
        file_content = file.read()
    
    df = pd.read_excel(file_content)
    
    # get class attribut
    y = df["Attrition"].to_numpy()
    print("shape of Y : ", y.shape)

    df = df.drop("Attrition", axis=1)
    df = df.drop("Unnamed: 0", axis=1)

    # X with 29 features
    X = df.to_numpy()
    print("shape of X : ", X.shape)

    # split the dataset into training set (80%) and testing set (20%)  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    Dtree = DecisionTree(max_depth=10)
    
    Dtree.fit(X_train, y_train)

    predictions = Dtree.predict(X_test)

    acc = accuracy(y_test, predictions)
    print("la precision est de : ", acc)


