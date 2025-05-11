# Musical Genre Classification

**Authors:** Aleix Francia Albert, Natalia Blaszczyk  
**Keywords:** MFCC, audio signal processing, music information retrieval, speech recognition, spectral features, audio classification, chroma, tempo, rhythm

## Abstract

As the volume of digital audio content continues to grow, there is an increasing demand for robust and efficient techniques to analyze and organize sound. One of the most widely adopted approaches in the field of audio signal processing is the use of Mel Frequency Cepstral Coefficients (MFCCs), which provide a compact representation of the spectral properties of audio in a form that approximates human auditory perception.

This project presents an overview of the MFCC extraction process and explores its applications in speech recognition, music classification, and audio recommendation systems. In addition, several complementary audio features are considered—including RMS energy, spectral contrast, chroma features, tempo, and rhythm patterns—to enhance the effectiveness of music information retrieval systems.

## Project Description

This repository contains the code and experimental results for a music genre classification system based on machine learning techniques applied to audio features. The primary goal is to compare the effectiveness of different classifiers and feature selection methods in accurately identifying musical genres.

## Features Used

- **MFCCs (Mel Frequency Cepstral Coefficients)**
- **Chroma Features**
- **Spectral Contrast**
- **RMS Energy**
- **Zero-Crossing Rate**
- **Tempo**
- **Rhythm Patterns**

These features are extracted using `librosa`, a Python library for audio analysis.

## Models Evaluated

We evaluated three classifiers:

- **Support Vector Machines (SVM)**
- **k-Nearest Neighbors (KNN)**
- **Random Forest**

### Feature Selection Techniques

- Forward Sequential Feature Selector  
- Backward Sequential Feature Selector  
- Recursive Feature Elimination (RFE)  
- Recursive Feature Elimination with Cross-Validation (RFECV)

## Results Summary

| Classifier     | Feature Selection         | Best Accuracy |
|----------------|---------------------------|----------------|
| **SVM (RBF)**  | RFECV                     | **0.73**       |
| KNN            | All Features              | 0.638          |
| Random Forest  | All Features              | 0.663          |

The Support Vector Machine with an RBF kernel and RFECV feature selection achieved the highest accuracy, outperforming KNN and Random Forest, especially when using optimized feature subsets.

