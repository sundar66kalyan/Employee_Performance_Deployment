"""
=========================================================
Preprocessing Functions
=========================================================

This module contains reusable preprocessing functions
used for employee performance prediction.

Author : Kalyana Sundar
Project : Employee Performance Analysis
"""

import os
import pandas as pd
import numpy as np

from config.project_config import *

# ==========================================================
# Import Libraries
# ==========================================================

import pandas as pd
import numpy as np

# ==========================================================
# Create Feature Template
# ==========================================================

def create_feature_template(feature_columns):
    """
    Create an empty feature dataframe
    with all required columns.
    """

    template = pd.DataFrame(

        np.zeros((1, len(feature_columns))),

        columns=feature_columns

    )

    return template

# ==========================================================
# Add Numerical Features
# ==========================================================

def add_numerical_features(
    df,
    employee
):
    """
    Add numerical employee information.
    """

    numerical_features = [

        "Age",

        "DistanceFromHome",

        "EmpEducationLevel",

        "EmpEnvironmentSatisfaction",

        "EmpHourlyRate",

        "EmpJobInvolvement",

        "EmpJobLevel",

        "EmpJobSatisfaction",

        "NumCompaniesWorked",

        "EmpLastSalaryHikePercent",

        "EmpRelationshipSatisfaction",

        "TotalWorkExperienceInYears",

        "TrainingTimesLastYear",

        "EmpWorkLifeBalance",

        "ExperienceYearsAtThisCompany",

        "ExperienceYearsInCurrentRole",

        "YearsSinceLastPromotion",

        "YearsWithCurrManager"

    ]

    for column in numerical_features:

        if column in employee:

            df.loc[0, column] = employee[column]

    return df

# ==========================================================
# Add Encoded Features
# ==========================================================

def add_categorical_features(
    df,
    employee
):
    """
    Encode categorical features.
    """

    categorical_columns = [

        "Gender",

        "EducationBackground",

        "MaritalStatus",

        "EmpDepartment",

        "EmpJobRole",

        "BusinessTravelFrequency",

        "OverTime",

        "Attrition"

    ]

    for column in categorical_columns:

        value = employee[column]

        encoded_column = f"{column}_{value}"

        if encoded_column in df.columns:

            df.loc[0, encoded_column] = 1

    return df

# ==========================================================
# Employee Preprocessing
# ==========================================================

def preprocess_employee(

    employee,

    feature_columns

):
    """
    Convert raw employee data into
    model-ready feature dataframe.
    """

    features = create_feature_template(

        feature_columns

    )

    features = add_numerical_features(

        features,

        employee

    )

    features = add_categorical_features(

        features,

        employee

    )

    return features

def load_feature_template():

    feature_df = pd.read_csv(

        os.path.join(

            PROCESSED_DATA_FOLDER,

            "employee_features.csv"

        )

    )

    feature_columns = feature_df.drop(

        columns=["PerformanceRating"]

    ).columns.tolist()

    return feature_columns

