## Polytechnic of Porto, School of Management and Technology 20/21
<a href="https://www.estg.ipp.pt/"><img src="https://user-images.githubusercontent.com/44362304/94424125-9f4d8a00-0181-11eb-84cb-174d8dbde5ec.png" title="ESTG"></a>

(Click on the above image for more school's details)

## Reccomender System using Neo4j and Apriori algorithm (FP-Growth)
![Estgflix Logo](https://user-images.githubusercontent.com/44362304/132983610-2783de71-3def-42b4-b7d2-be9e0de32a33.png)

### School final project

This project comes within the scope of the Final Project course of the Bachelor in Computer Engineering and its main objective is to put into practice all the knowledge acquired throughout the bachelor.

The project's main goal is to create a recommendation system using information stored in Neo4j database and using Apriori algorithm (FP-Growth) to make recommendations based on the explicit data given by the user. 

## Table of Contents

- [Project Overview](#project_overview)
- [Project Screenshots](#project_screenshots)
- [Usage](#usage)
- [Documentation](#documentation)
- [Project Contributors](#project_contributors)
- [License](#license)

<a name="project_overview"></a>
## Project Oveview
![Arquitetura Projeto](https://user-images.githubusercontent.com/44362304/132983689-7fcc80de-16fa-481b-8d50-b5c01f73c7b4.png)

<div style="text-align: right"> In the above image is represented the architecture of the project, where it is possible to observe 4 main tools that are <a href="https://angular.io/" target="_blank"> Angular </a>, <a href="https://flask.palletsprojects.com/en/2.0.x/" target="_blank"> Flask </a>, <a href="https://www.python.org/" target="_blank"> Python </a> and <a href="https://neo4j.com/" target="_blank"> Neo4j </a>.</div>
<p> </p>
<div style="text-align: right"> The project architecture is divided into 2 sides, the <b>client side</b> and the <b>server side.</b> </div>
<p> </p>
<div style="text-align: right"> On the server side (backend), it is in Neo4j that the data of users, movies and the generated association rules are stored and this is responsible for returning the results of the Cypher queries, through the connection with the <a href="https://neo4j.com/docs/python-manual/current/" target="_blank"> Neo4j Python driver </a>. </div>
<p> </p>
<div style="text-align: right"> For the creation of association rules, 2 Python libraries were used, <a href="http://rasbt.github.io/mlxtend/" target="_blank"> MLxtend </a> and <a href="https://pandas.pydata.org/" target="_blank"> Pandas </a>, where Pandas was used to convert data to Dataframe format, which format is used by MLxtend responsible for applying the <a href="https://www.geeksforgeeks.org/ml-frequent-pattern-growth-algorithm/" target="_blank"> FP-Growth algorithm </a> for the generation of association rules. Later Python will write these <a href="https://en.wikipedia.org/wiki/Association_rule_learning" target="_blank"> association rules </a> to a CSV file and will import them into Neo4j, through Cypher queries using the Neo4j Python driver. </div> 
<p> </p>
<div style="text-align: right"> 
Flask communicates with Python in order to obtain all the information it needs and then send it to Angular, through HTTP requests present in the REST API using JSON.
On the client side (frontend), Angular is responsible for transmitting all the information, obtained through communication with Flask, to the user.  </div>

<a name="project_screenshots"></a>
## Project Screenshots
Some of the project screenshots

| Main Menu |
| :---: |
| <img src="https://user-images.githubusercontent.com/44362304/132987379-1affd408-4072-4d94-87dc-592a40b70d42.png" width="800" height="450"> |
| Movie Details |
| <img src="https://user-images.githubusercontent.com/44362304/132987378-80ef5c30-4014-4b31-9004-f7b3a22e89f4.png" width="800" height="450"> |
| User Profile |
| <img src="https://user-images.githubusercontent.com/44362304/132987380-83c1f096-d37e-49fd-962c-36ee45412a79.png" width="800" height="450"> |

<a name="usage"></a>
## Usage

You must meet the following requirements:
- **Python 3.7** installed
- **IDE** (Pycharm, Eclipse ...) installed
- **Neo4j Browser** installed
- **Angular CLI** and **NodeJs** installed

### 1st Step - Creation of graph database:

You need to create the graph database Neo4j with the following structure:
<img src="https://user-images.githubusercontent.com/44362304/132991073-230df9be-d37f-4939-877b-8b83491b4b27.png" width="700" height="350">

<div style="text-align: right"> The User node stores all the associated information of a user and the node has only relationships with the Movie node, the WATCHED relationship represents whether the user has seen the movie or not, and the RATED relationship represents whether the user rated the movie with a certain rating value, or not. </div>
<p></p>
<div style="text-align: right"> The Movie node stores all the information associated with a movie and has the IN_GENRE relationship with the Genre node that represents which genre(s) it belongs to and also has the RECOMMENDS relationship with other nodes of the same type (Movie), where it is through from this relationship that the recommendations are obtained when the user sees the movie.
The confidence property of the RECOMMENDS relationship refers to the trust value between the 2 movies in a given association rule. </div>
<p></p>

**(All the code available to create the graph database is located in web/backend/Neo4JConnection/Neo4jCreationDB.py)**

#### Creation of nodes indexes
<div style="text-align: right"> So first you need to create the node indexes in order to improving the node search. (Check lines 206 to 208 of the Neo4jQueries python file) </div>
<p></p>

#### Creation of nodes

**Important note: Dont forget to comment dbms.directories.import=import in neo4j database's settings otherwise you cannot import the necessary data from the csv files to the database!**
<div style="text-align: right"> After the node indexes are created you need to create the nodes. 

To create the nodes "Genres" you need to import the csv file named "movies_genre.csv" (located in AlgoritmoML/datasets.zip).
(Uncomment line 213 of the Neo4jCreationDB python file)
  
To create the nodes "Movies" you need to import the csv file named "movies.csv" (located in AlgoritmoML/datasets.zip).
(Uncomment line 216 of the Neo4jCreationDB python file)
  
To create the nodes "Users" you need to import the csv file named "userRatings5k.csv" (located in AlgoritmoML/datasets.zip).
(Uncomment line 219 of the Neo4jCreationDB python file)
</div>

#### Creation of nodes relationships

<div style="text-align: right"> Having the nodes created lets create the relationship between them.
  
To create the relationship "IN_GENRE" between the nodes Movie and Genre you need to import the csv file named "movies.csv" (located in AlgoritmoML/datasets.zip/movies.csv).
(Uncomment line 224 of the Neo4jCreationDB python file)  
  
To create the relationship "WATCHED" between the nodes User and Movie you need to import the csv file named "userRatings5k.csv" (located in AlgoritmoML/datasets.zip/userRatings5k.csv).
(Uncomment line 227 of the Neo4jCreationDB python file)
  
To create the relationship "RECOMMENDS" between the nodes Movie you need to import the csv file named "movies.csv" (located in AlgoritmoML/rulesCsv/rules5kUsersImp.csv).
(Uncomment line 230 of the Neo4jCreationDB python file)
</div>

And now we have our graph database created lets go to the next step of the project's usage.

### 2nd Step - Running the backend server:

To run the backend side of the project you need to open your terminal and go to the backend file and run the app.py file on your IDE.


### 3rd Step - Running the frontend server:

To run the client side of the project you need to open your terminal and go to the path "frontend" and then you type "ng serve --open"

### 4nd Step - Start using the app and enjoy the recommender system :)


<a name="documentation"></a>
## Documentation
All the project's code is documented just access to a file you wish to see and you will see all the commentaries necessary to understand the code.

<a name="project_contributors"></a>
## Project Contributors
| João Pereira | Mariana Carvalho (Project Teacher Advisor) |
| :---: |:---:| 
| ![João Pereira](https://avatars2.githubusercontent.com/u/44362304?s=200&u=e779f8e4e1d4788360e7478a675df73f219b42b4&v=3)| <img src="https://user-images.githubusercontent.com/44362304/132983771-337f5b09-09dd-4572-9275-4752fddedc5e.png" width="202" height="202"> |
| <a href="https://github.com/Joaodevgit" target="_blank">`github.com/Joaodevgit`</a> | --- |

<a name="license"></a>
## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2021 © ESTG - Polythecnic of Porto.

