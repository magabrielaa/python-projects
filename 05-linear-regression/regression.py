'''
Linear regression

Gabriela Ayala

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Class for representing a dataset, performs train/test
        splitting.

        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        parameters_dict = util.load_json_file(dir_path, "parameters.json")
        self.feature_idx = parameters_dict["feature_idx"]
        self.name = parameters_dict["name"]
        self.target_idx = parameters_dict["target_idx"]
        self.training_fraction = parameters_dict["training_fraction"]
        self.seed = parameters_dict["seed"]
        self.labels, data = util.load_numpy_array(dir_path, "data.csv")

        # do standardization before train_test_split
        if parameters_dict["standardization"] == "yes":
            data = self.standardize_features(data)

        self.training_data, self.testing_data = train_test_split(data,
            train_size=self.training_fraction, test_size=None,
            random_state=self.seed)

    # data standardization
    def standardize_features(self, data):
        '''
        Standardize features to have mean 0.0 and standard deviation 1.0.
        Inputs:
          data (2D NumPy array of float/int): data to be standardized
        Returns (2D NumPy array of float/int): standardized data
        '''
        mu = data.mean(axis=0)
        sigma = data.std(axis=0)
        return (data - mu) / sigma

class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, feature_idx):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            feature_idx: a list of the feature indices for the columns (of the
              original data array) used in the model.
        '''

        self.dataset = dataset
        self.feature_idx = feature_idx
        self.target_idx = dataset.target_idx
        X_train = util.prepend_ones_column(dataset.training_data[:, self.feature_idx])
        y_train = dataset.training_data[:, self.target_idx] 
        self.beta = util.linear_regression(X_train, y_train)
        self.R2 = self.calc_R2(dataset.training_data)


    def __repr__(self):
        '''
        Format model as a string.
        '''

        features = np.array(self.dataset.labels)[self.feature_idx]
        target = self.dataset.labels[self.target_idx]

        s = str(target) + " ~ " + str(round(self.beta[0], 6)) 
        
        for i in range(len(features)):
            s += " + " + str(round(self.beta[i + 1], 6)) +  " * " + str(features[i]) 
        
        return s


    def calc_R2(self, dataset):
        '''
        Calculate the model's Coefficient of Determination R2.
        '''
        X = util.prepend_ones_column(dataset[:, self.feature_idx])
        y = dataset[:, self.target_idx] 
        y_hat = util.apply_beta(self.beta, X)
        mean_y = np.mean(y)
        var_y = (1/y.size) * np.sum((y - mean_y) ** 2)
        var_yhat = (1/y.size) * np.sum((y - y_hat) ** 2)

        return 1 - (var_yhat / var_y)


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''

    return [Model(dataset, [feature]) for feature in dataset.feature_idx]    


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the feature variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the feature variables
    '''

    return Model(dataset, dataset.feature_idx)


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''

    best_m = None

    for i, feature1 in enumerate(dataset.feature_idx):
        for feature2 in dataset.feature_idx[i + 1:]:
            m = Model(dataset, [feature1, feature2])
            if not best_m or m.R2 > best_m.R2:
                best_m = m
    
    return best_m


def forward_selection(dataset):
    '''
    Given a dataset with P feature variables, uses forward selection to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''
    
    best_feats = []
    feats_not_used = dataset.feature_idx[:]
    best_models = []

    for _ in range(len(dataset.feature_idx)):
        best_m = None
        for feat in feats_not_used:
            m = Model(dataset, best_feats + [feat])
            if not best_m or m.R2 > best_m.R2:
                best_m = m
                best_far = feat
        best_feats.append(best_far)
        feats_not_used.remove(best_far)
        best_models.append(best_m)
                     
    return best_models


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''
  
    return model.calc_R2(dataset.testing_data)

