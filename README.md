# Neeva - News bias evaluator

## Description

The main goal of the system is to provide a simple and efficient way to determine whether text from news articles potentially contain some form of bias.

The system uses machine learning to evaluate each sentence of a text and return a score as well as an evaluation for each sentence. More details are provided in the **Machine Learning Concept** section.

---

## Major Dependencies

| Dependency | Version | 
| --- | --- | 
| [Django](https://www.djangoproject.com/download/) | `4.1` |
| [Scikit-learn](https://scikit-learn.org/stable/) | `1.1.3` | 
| [Pandas](https://pandas.pydata.org) | `1.5.1` | 
| [Tensorflow](https://www.tensorflow.org/?hl=en) | `2.9` | 
| [Docker](https://www.docker.com) | `20.10.17` |


---

## Machine Learning Concept

### Original dataset

Data source
Planned data source:

> https://www.kaggle.com/datasets/timospinde/mbic-a-media-bias-annotation-dataset

This data source in particular was chosen due to the process of labelling  the dataset
adhered to determining if text is biassed can be subjective and dependent on the views of
who is labelling the data. This dataset takes the human-labelling approach, specifically , 10
annotators reviewed each entry and the identification of bias was based on the individual
words and sentence as a whole. Furthermore, this dataset provides information on
characteristics and the background of its 1345 annotators. Due to these conditions, we
believe that the labelling process leads to the creation of a reliable source that can be used
to make accurate predictions.

### Retraining the model

Due to the size of the dataset (1700), we aim to use semi-supervised learning to increase our dataset.
We will gather more articles and once we have enough collected data, we will use the
current model to label the sentences within these articles. The sentences with a high
accuracy will then be added to the training dataset. The sentences  with  a low accuracy will
be added to the testing dataset and will be tested on the new model, which will help us
determine the impact of the newly added data on the model. This evaluation will be the
deciding factor in whether we update the model or keep the existing version. We would
need to extract all the features from the new data, which would lead to arduousness in our
monitoring stage. The features we select for our initial model will be influenced by this
phase of the system.

## Pipeline

Workflow diagram
![Workflow pipeline](/assets/DevOps_pipeline.png)

ML model diagram
![ML pipeline](/assets/ML_Model_pipeline.png)

Deployment diagram
![Deployment pipeline](/assets/Deployment.png)

## How to setup local development with the cloudSQL database:
To be able to communicate to the cloudSQL database while developing locally, the following steps have to be carried out (based on: https://cloud.google.com/python/django/kubernetes-engine#connect_sql_locally) :
1. Download and configure gcloud locally: https://cloud.google.com/sdk/docs/install-sdk
2. Authenticate and acquire the credentials for the API: ```gcloud auth application-default login```
3. Download the cloudSQL proxy: ```wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy```
4. Make the cloudSQL proxy executable: ```chmod +x cloud_sql_proxy```
5. Run the proxy in a terminal via: ```./cloud_sql_proxy -instances="dit825:europe-north1:dit825-cloudsql"=tcp:5432```
6. Open a second terminal, and set the following variables: ```export DATABASE_NAME=dit825
export DATABASE_USER=dit825-cloudsql
export DATABASE_PASSWORD=<ON_SLACK>```
7. Run the migrations and start the server as per usual (**Run this in the same terminal where the environment variables from the previous step were set!**): ```python manage.py makemigrations && python manage.py migrate --database=cloudSQL && python manage.py runserver 0.0.0.0:8000```

NOTE: the following steps are specific to linux. The following [page](https://cloud.google.com/python/django/kubernetes-engine#connect_sql_locally) includes mac and windows variations of the same steps.

## cloudSQL navigation:
1. Once navigated to the cloudSQL dit825 project page, select the "activate cloud shell" (terminal icon) on the top right: ![image](/uploads/0c72a7a1c6a7d365950fb953316c37a7/image.png)
2. input: ```gcloud sql connect dit825-cloudsql --database=dit825  --user=dit825-cloudsql``` in the terminal to gain access. A password prompt will appear - the password is shared on slack.
3. Select "authorize" if the following popup appears:  ![image](/uploads/38c394ad9ab6258830134933fb356c4d/image.png)
4. Finally, commands such as: 
```\dt # displays all relations (tables) inside of the database)``` and ```SELECT * FROM <table name>``` 
can be used to navigate/query data.

# Contribution rules

- PR templates
- Commit templates
- Bug template

## Visuals
WIP: Add visuals when available 

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
- Younis Akel 
- Christopher Axt 
- Vernita Gouws
- Alexandre Rancati-Palmer

## License
The project is following the same licence as the original dataset
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Project status

### Inception and Planning Phase:
**Sprint0**: All members involved in planning and design of the system. Completed the following tasks: 

- [x] Project setup
- [x] Project planning
- [x] Project design

**Sprint1**: All members involved in planning and design of the system. Completed the following tasks:

- [x] Project documentation
- [x] Assignment 1

**Sprint2**: Implementation phase - All members involved in implementation of the system. Sprint2 includes the following tasks:

- [x] Integrate Jira with gitlab - *Christopher*
- [x] Create issues on Jira using project requirements - *Alexandre, Younis*
- [x] Set up django project - *Alexandre*
- [x] Create prototype of the system - *Christopher*
- [x] Implement prototype of the system - *Alexandre*
- [x] Set up docker build - *Christopher*
- [x] Research cloud provider possibilities and architecture of the system on the cloud - *Younis*
- [x] Create a basic ML model - *Vernita*
- [x] Configure ML model upload to cloud provider - *Vernita*
- [x] Set up CI app build - *Alexandre* 
- [x] Set up database for the ML model - *Christopher*
- [x] Configure cloud provider - *Younis*
- [x] Configure automated deployment - *Younis*
- [x] Create models for the database - *Christopher*
- [x] Set up docker image registration - *Alexandre*
- [x] Implement python tools - *Vernita*
- [x] Implement simple unit tests - *Vernita*
- [x] Set up CD pipeline with Kubernetes - *Younis*
- [x] Update Readme with project detail - *Alexandre*
- [x] Update Readme with Sprint tasks and documentation - *Vernita*
- [ ] Add testing to dockerfile - *Vernita*
- [x] Update deployment diagram - *Younis*
