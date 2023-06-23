# ESRB Predict

ESRB Predict is a Python program that uses machine learning to predict ESRB ratings of video games based on a dataset of previously released games and their ratings. The program features a user-friendly GUI built with Tkinter.


## Features

- Predict ESRB ratings of video games based on content categories using machine learning algorithms.
- User-friendly graphical user interface (GUI) for easy interaction.
- Data visualization capabilities to explore the dataset and model results.
- Ability to customize input parameters and explore different prediction scenarios.
- Efficient data processing using the scikit-learn, pandas, matplotlib, and seaborn libraries.


## Required Third-Party Libraries

The following third-party libraries are required:

- scikit-learn (sklearn): A machine learning library.
- pandas: A data manipulation library.
- matplotlib: A plotting library used for creating visualizations.
- seaborn: A more advanced visualization library built on top of matplotlib.

## Installation (Windows)

1. Ensure Python 3.10 (recommended) or higher is installed on your Windows machine. It can be downloaded from the official Python website (https://www.python.org/downloads/).

2. Install the required libraries by opening the command prompt in administrator mode and running the following commands:

   ```
   pip install scikit-learn
   pip install pandas
   pip install matplotlib
   pip install seaborn
   ```


3. Download the project files and extract them to a convenient location on your machine, ensuring the data folder containing "esrb_ratings.csv" is located in the root directory.

4. Open a command prompt and navigate to the root folder of the project.

5. Execute the following command to run the application:

   ```python main.py```

6. The graphical user interface (GUI) of the application will appear, and you can start using it.

## User Guide

Once the application is running, you can use the GUI to interact with the program. Follow the on-screen instructions and provide the necessary inputs to predict ESRB ratings based on the machine learning model and the provided dataset.

