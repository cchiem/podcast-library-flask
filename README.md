# Podcast Library

## Description

A podcast library app developed as a team project to explore and learn modern web development tools and frameworks.

Key Features:

-   Built using Flask for the backend
-   Frontend developed with **HTML** and **CSS**
-   Containerized and managed with **Docker**
-   Deployed on Google Cloud (GCP) for **continous integration**
-   Enables users to search, organise, and listen to podcasts

This project was a great opportunity to collaborate and deepen my understanding of web technologies, containerization, and cloud deployment.

## Technologies used

<div align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white"/>
</div>

## Getting started

To run this Flask image converter application locally, follow these steps:
**1. Clone this repository**

```bash
git clone https://github.com/your-username/podcast-library-flask.git
cd podcast-library-flask
```

## Installation

**Installation via requirements.txt**

**Windows**

```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**

```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment.

## Execution

**Running the application**

From the _project directory_, and within the activated virtual environment (see _venv\Scripts\activate_ above):

```shell
$ flask run
```

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment.

## Configuration

The _project directory/.env_ file contains variable settings. They are set with appropriate values.

-   `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
-   `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
-   `SECRET_KEY`: Secret key used to encrypt session data.
-   `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
-   `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/code/switkowski/building-a-podcast-recommendation-engine/input
