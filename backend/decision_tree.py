import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt


# Load the generated dataset
data = pd.read_csv('generated_clusters.csv')

# Separate features (X) and target (y)
X = data.drop('PERSONA', axis=1)  # Features are all columns except 'PERSONA'
y = data['PERSONA']  # Target is the 'PERSONA' column

# Define categorical columns
categorical_cols = ['STRONG_LOCATION', 'INCOME_LEVEL', 'LOCATION_TYPE', 'VEHICLE_PREFERENCES_1', 'VEHICLE_PREFERENCES_2', 'SERVICE_PREFERENCES', 'BRAND_LOYALTY', 'DIGITAL_ENGAGEMENT', 'PSYCHOLOGICAL_TRAITS_1', 'PSYCHOLOGICAL_TRAITS_2']

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ('encoder', OneHotEncoder(), categorical_cols)
], remainder='passthrough')

# Define the decision tree classifier
clf = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', DecisionTreeClassifier(random_state=42))
])

# Split the dataset into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the decision tree classifier on the training data
clf.fit(X_train, y_train)

plt.figure(figsize=(20, 10))
plot_tree(clf.named_steps['classifier'], feature_names=clf.named_steps['preprocessor'].transformers_[0][1].get_feature_names_out(), class_names=y.unique(), filled=True)
plt.title("Decision Tree")
plt.show()

# Make predictions on the testing data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Generate and print the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{conf_matrix}")

# Generate and print the classification report
class_report = classification_report(y_test, y_pred)
print(f"Classification Report:\n{class_report}")
