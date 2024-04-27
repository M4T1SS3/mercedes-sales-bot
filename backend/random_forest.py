import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt

def import_data():
    data = pd.read_csv('generated_clusters.csv')

    print(len(data))
    print(data.shape)
    print(data.head())

    print("Read data")

    return data

def preprocess_data(data):
    # Perform one-hot encoding for categorical columns
    data_encoded = pd.get_dummies(data, drop_first=True)

    # Separate features (X) and target (y)
    X = data_encoded.drop(columns=['PERSONA'])
    y = data_encoded['PERSONA']

    return X, y

if __name__ == "__main__":
    # Step 1: Import and preprocess the data
    data = import_data()
    X, y = preprocess_data(data)

    # Step 2: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    # Step 3: Define the Random Forest classifier
    clf_rf = RandomForestClassifier(random_state=100)

    # Step 4: Define the parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 5]
    }

    # Step 5: Perform GridSearchCV to find the best hyperparameters
    grid_search = GridSearchCV(clf_rf, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    # Step 6: Get the best model from GridSearchCV
    best_rf = grid_search.best_estimator_
    print("Best Parameters:", grid_search.best_params_)

    # Step 7: Evaluate the best model on the test set
    y_pred = best_rf.predict(X_test)

    # Step 8: Display evaluation metrics
    print("Optimized Random Forest Performance:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
