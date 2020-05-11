# UIC Search App

## Deployment 
The web app is deployed on heroku [https://irwebapp-heroku.herokuapp.com/] 
Use this link to view deployed search engine ,or run the code locally using the following Instructions
Source code for console app can be found at [https://github.com/rishabh2605/Information_Retrival]


### Instructions 

#### Pre requisites 
Before you continue, ensure you have met the following requirements:

1. Django==2.2.12
2. nltk==3.4.5
3. numpy==1.18.1
4. pandas==1.0.3
5. pip==20.0.2
6. py==1.8.1
7. pyparsing==2.4.6
8. pytest==5.4.1
9. python-dateutil==2.8.1
10. scikit-learn==0.22.1
11. scipy==1.4.1

these can be installed using
 > pip install -r requirements.txt

#### Requirements
Make sure the files
1. crawler.pk1
2. data_vector.npz
3. page_rank
4. vectorizer 
are present before execution 

#### Execution 
The execution for crawler , pre processing and pagerank will consume almost 2 hrs , hence it is recommended to have 
1. crawler.pk1
2. data_vector.npz
3. page_rank
4. vectorizer  
these files before hand
Navigate to ..\Information_Retrival and run the following command 

> python query.py "Query"



### Usage 

Once the program is executed , the console will display the  search results for the query.
The page will also display a query expansion result it also displays top 30 results.

### Additional Resources web app

To view web app for this project visit [https://irwebapp-heroku.herokuapp.com/]

## Author 
Rishabh Mehta 






