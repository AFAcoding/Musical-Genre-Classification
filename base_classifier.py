# -*- coding: utf-8 -*-
"""Base classifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yWzFBvwBqwj0YQv73sju1u3LkfFLeig5

#**3. Base classifier**(KNN)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay,accuracy_score

"""**Load Dataset**"""

df = pd.read_csv("gtzan_features.csv",sep=",")

"""**Split of the dataset**"""

X=df.drop(['class','file_name'],axis=1)
X_mfcc = df[['mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5','mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11']]
X_spectral = df[['spectral_contrast_1', 'spectral_contrast_2','spectral_contrast_3', 'spectral_contrast_4', 'spectral_contrast_5','spectral_contrast_6', 'spectral_contrast_7']]
X_chroma = df[['chroma_1', 'chroma_2','chroma_3', 'chroma_4', 'chroma_5', 'chroma_6', 'chroma_7', 'chroma_8','chroma_9', 'chroma_10', 'chroma_11', 'chroma_12']]
X_rms = df[['rms']]

X_cutom=df[[ 'spectral_contrast_2','spectral_contrast_3', 'spectral_contrast_4', 'spectral_contrast_5','spectral_contrast_6','mfcc_1', 'mfcc_2', 'mfcc_7', 'mfcc_8', 'mfcc_9',  'mfcc_11']] #Feature selection by DCOR

y=df['class']

"""**Split data**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_cus, X_test_cus, y_train_cus, y_test_cus = train_test_split(X_cutom, y, test_size=0.2, random_state=42)
X_train_mfcc, X_test_mfcc, y_train_mfcc, y_test_mfcc = train_test_split(X_mfcc, y, test_size=0.2, random_state=42)
X_train_spectral, X_test_spectral, y_train_spectral, y_test_spectral = train_test_split(X_spectral, y, test_size=0.2, random_state=42)
X_train_chroma, X_test_chroma, y_train_chroma, y_test_chroma = train_test_split(X_chroma, y, test_size=0.2, random_state=42)
X_train_rms, X_test_rms, y_train_rms, y_test_rms = train_test_split(X_rms, y, test_size=0.2, random_state=42)

"""**Normalize data**"""

scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_train = scaler_X.fit_transform(X_train)
X_test = scaler_y.fit_transform(X_test)

X_train_cus = scaler_X.fit_transform(X_train_cus)
X_test_cus = scaler_y.fit_transform(X_test_cus)

X_train_mfcc = scaler_X.fit_transform(X_train_mfcc)
X_test_mfcc = scaler_y.fit_transform(X_test_mfcc)

X_train_spectral = scaler_X.fit_transform(X_train_spectral)
X_test_spectral = scaler_y.fit_transform(X_test_spectral)

X_train_chroma = scaler_X.fit_transform(X_train_chroma)
X_test_chroma = scaler_y.fit_transform(X_test_chroma)

X_train_rms = scaler_X.fit_transform(X_train_rms)
X_test_rms = scaler_y.fit_transform(X_test_rms)

"""**KNN Inicialization**"""

model = KNeighborsClassifier()

# Function to train and evaluate the model
def evaluate_model(X_train, X_test, y_train, y_test, feature_name):
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy for {feature_name}: ", accuracy)

    cross_val_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-validation scores for {feature_name}: ", cross_val_scores)
    print(f"Cross-validation Mean accuracy for {feature_name}: ", cross_val_scores.mean())
    print("------------------------------------------------------------------------------------")

# Evaluate for each feature set
evaluate_model(X_train, X_test, y_train, y_test, "Original Data")
evaluate_model(X_train_cus, X_test_cus, y_train_cus, y_test_cus, "Custom Data")
evaluate_model(X_train_mfcc, X_test_mfcc, y_train_mfcc, y_test_mfcc, "MFCC Data")
evaluate_model(X_train_spectral, X_test_spectral, y_train_spectral, y_test_spectral, "Spectral Data")
evaluate_model(X_train_chroma, X_test_chroma, y_train_chroma, y_test_chroma, "Chroma Data")
evaluate_model(X_train_rms, X_test_rms, y_train_rms, y_test_rms, "RMS Data")

"""**Tune**"""

param_grid = {
    'n_neighbors': range(1, 21),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'minkowski','hamming'],
    'p': [1, 2]  # Only relevant if metric is 'minkowski'
}

# Dictionary of all datasets to evaluate
datasets = {
    "Original Data": (X_train, X_test, y_train, y_test),
    "Custom Data": (X_train_cus, X_test_cus, y_train_cus, y_test_cus),
    "MFCC Data": (X_train_mfcc, X_test_mfcc, y_train_mfcc, y_test_mfcc),
    "Spectral Data": (X_train_spectral, X_test_spectral, y_train_spectral, y_test_spectral),
    "Chroma Data": (X_train_chroma, X_test_chroma, y_train_chroma, y_test_chroma),
    "RMS Data": (X_train_rms, X_test_rms, y_train_rms, y_test_rms)
}

# Store results
results = {}

# Loop through datasets and apply grid search and evaluation
for name, (X_tr, X_te, y_tr, y_te) in datasets.items():
    print(f"\n--- Tuning and Evaluating: {name} ---")

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                               cv=5, n_jobs=-1, verbose=1, scoring='accuracy')
    grid_search.fit(X_tr, y_tr)
    print("Best parameters found:", grid_search.best_params_)

    # Use best model
    best_model = grid_search.best_estimator_

    # Accuracy on test set
    y_pred = best_model.predict(X_te)
    test_accuracy = accuracy_score(y_te, y_pred)

    # Cross-validation scores
    cv_scores = cross_val_score(best_model, X_tr, y_tr, cv=5)
    mean_cv_score = cv_scores.mean()

    print(f"Accuracy for {name}: {test_accuracy:.3f}")
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Cross-validation Mean accuracy: {mean_cv_score:.3f}")
    print("-" * 80)

    # Store
    results[name] = {
        "Test Accuracy": test_accuracy,
        "CV Scores": cv_scores,
        "CV Mean Accuracy": mean_cv_score,
        "Best Params": grid_search.best_params_
    }

summary_df = pd.DataFrame({
    dataset: {
        "Test Accuracy": vals["Test Accuracy"],
        "CV Mean Accuracy": vals["CV Mean Accuracy"]
    } for dataset, vals in results.items()
}).T

print("\nFinal Summary:")
print(summary_df)

"""**Evaluation**

Best parameters found: custom data: {'metric': 'euclidean', 'n_neighbors': 17, 'p': 1, 'weights': 'distance'}
"""

model = KNeighborsClassifier(metric='euclidean', n_neighbors=17, p=1, weights='distance')

model.fit(X_train_cus, y_train_cus)
y_pred = model.predict(X_test_cus)

print(classification_report(y_test_cus, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test_cus, y_pred)

# Display
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
fig, ax = plt.subplots(figsize=(7, 5))  # bigger figure
disp.plot(ax=ax, cmap='Blues', colorbar=False)

# Rotate X labels
plt.xticks(rotation=45)

plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

"""**K impact**"""

# List of k values to test
k_values = range(1, 21)

# Store accuracy results
train_accuracy = []
test_accuracy = []

# Iterate over different values of k
for k in k_values:
    # Create the KNN model with the current k and other parameters
    knn = KNeighborsClassifier(metric='euclidean', n_neighbors=k, p=1, weights='distance')

    # Fit the model on the training data
    knn.fit(X_train_cus, y_train_cus)

    # Predict on the training and test sets
    train_pred = knn.predict(X_train_cus)
    test_pred = knn.predict(X_test_cus)

    # Calculate the accuracy for both training and test sets
    train_accuracy.append(accuracy_score(y_train_cus, train_pred))  # Fix: use y_train_cus instead of X_train_cus
    test_accuracy.append(accuracy_score(y_test_cus, test_pred))

# Plotting the results
plt.figure(figsize=(10, 2))

# Plot the accuracy for training and test sets
plt.plot(k_values, train_accuracy, label="Training Accuracy", color="blue", marker='o')
plt.plot(k_values, test_accuracy, label="Test Accuracy", color="red", marker='x')

# Adding labels and title
plt.xlabel('Number of Neighbors (k)', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Impact of k on KNN Performance', fontsize=14)
plt.legend()

# Show the plot
plt.grid(True)
plt.show()