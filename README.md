# OpenTargets Biomedical Association Search Engine

## Overview


This proyect consist of creating a website that uses `http.server` Python library to search associations between target and diseases.
This software allows researchers and students to query target genes or specific diseases and filter them interactively based on an overall association score threshold.
The purpose of this proyect is to understand how programming works in network enviorments and to become more familiar with the role of biomedical engineering.

---

## Technical Project Architecture

The structure of the website is divided into files with variables, auxiliary functions for the server, instance functions for the requested data, the HTML files, and the main server:

* **`servidor.py`**: It's the project's main engine. Our HTTP server is a class inherited from `BaseHTTPRequestHandler` and handles GET and POST requests given through forms or URLs. The server can respond to each type of error by returning a message and the error type. Furthermore, it's programmed to run continuously unless interrupted with Control-C.


* **`auxiliary functions`**:
 - `get_query.py`: It is the Python file responsible for requesting data in JSON format from the OPENTARGETS API via a POST request, transforming and returning it in dictionaries.
 - `tables.py`: Using the functions within this file, we will extract the nested data from the dictionary provided by the API and convert it into objects using the classes developed in the previous exercise. These functions filter the data based on the score entered in the form, provided the query was submitted using that score. Finally, they will return the HTML tables and the dictionary containing the filtered data, which will then be converted to JSON format if the user requests to download the data.
 - `auxfunctions.py`:These are functions that help save code.

* **`html files`**:
 - `index.html`: The main frontend landing page. It features an ergonomic user dashboard with multiple structural input forms specifically tailored for biological identifiers and threshold evaluation limits.
 - `targetresults.html`:This is the file that will be displayed if an independent search is performed on diseases associated with the target.
 - `diseaseresults.html`:This is the file that will be displayed if an independent search is performed on the targets associated with the disease.
 - `results.html`:This HTML file is responsible for displaying all the tables created through the queries.
 - `author.html`: This HTML displays the author's information and contains a link that takes us to the original practice on GitLab and another link that takes us to other personal practices on GitHub.
* **`variables`**:These are the files that contain variables essential for website development, such as the relevant queries that allow us to tell the OpenTarget API the data structure we want. They also include messages for different types of errors.

---

## Endpoints & Communication Protocol

The web server actively monitors traffic on a local port and responds strictly to the following execution tree:

### 1. Static Content Routing
* **`GET /` or `GET /index.html`**: Serves the root dashboard, giving users access to the primary interactive data-entry panels.
* **`GET /author`**: Renders a dedicated identity template disclosing the developer's academic credentials and metadata.

### 2. Deep Biological Queries
* **`GET /searchTarget?target=<TARGET_ID>&disease=<DISEASE_ID>&score=<MIN_SCORE>`**
    * **Behavior**: Takes a target query (e.g., an Ensembl Gene ID like `ENSG00000157764`), executes a remote query against the GraphQL schema, and isolates all matching associated diseases.
    * **Output**: Renders an interactive table displaying the Disease ID, Disease Name, Associated Score, and an organized collection of Phenotypic Elements, while filtering out any records below the specified `<MIN_SCORE>`.
* **`GET /searchDisease?target=<TARGET_ID>&disease=<DISEASE_ID>&score=<MIN_SCORE>`**
    * **Behavior**: Takes a disease query (e.g., an EFO ID like `EFO_0000616`), requests its target network connections, and parses data into an organized layout.
    * **Output**: Generates rows mapping Target Approved Symbols, Target Biotypes, global scores, and structural Chemical Tractability modalities.

---

## Advanced HTTP Error Handling & Resilience

To prevent crashing and to comply with web communication rules, the `do_GET` workflow implements a multi-tiered validation pipeline:

* **`HTTP 200 OK`**: Triggered when the transaction completes smoothly, data exists, and the visual page is correctly assembled for the client.
* **`HTTP 400 Bad Request`**: Controlled via a localized structural `try/except` guard clause immediately at the entrance of query evaluations. If the user intentionally or accidentally alters the URL parameters manually, breaking the query string syntax or omitting required keys (`target`, `disease`, `score`), the exception captures the crash, cancels the operation, and responds with a clean error message.
* **`HTTP 404 Not Found`**: Triggered under two separate scenarios:
    1.  *URL Route Missing*: If the requested path does not map to any recognized resource on the server.
    2.  *Empty Dataset Query*: If the user inputs a structurally valid identifier code but that gene or disease returns zero records from the OpenTargets database, the table builder outputs an empty string (`lines == ""`). The system immediately captures this state, stops processing the HTML page template, and writes an informative 404 biological data error instead.

---

## Data source


As mentioned earlier, the data source used was the OpenTargets API, rather than the JSON format commonly suggested. This is because obtaining data from a reliable database is more dependable than using custom-created JSON. Furthermore, web servers handling biomedical data operate in this way. The OpenTargets API contains thousands upon thousands of data points on a vast number of genes, giving us a significant advantage over consulting the limited data available in custom-created JSON.

## Types of tables

There are different types of tables depending on the URL request:
The tables visible with the /searchTarget search show the characteristics of the diseases associated with that target, and vice versa with the /searchDisease search. 
When you search for a disease using a filter score in the form, it returns all the data for the associated target and the average score of all the evidence compiled by the association. The same happens when you enter a disease in the query. 
To make the data more reliable, we have created two lists of "datatype" attributes for the evidence to classify it as genetic or indirect. This allows us to reduce the score for indirect evidence.

## Other server features

The server includes a download option to obtain data from observable tables in JSON files. To achieve this, code has been implemented that, after filtering the data, generates a nested dictionary and transforms it into JSON format available for download.

The server has been configured to use the POST method for querying data, thus avoiding displaying search results in the URL and making the request more secure. The server calls its POST method in the Python program, and once the form data is processed, it uses the same methodology as the GET method to perform the query and return the data table.

## Test

Several unit tests have also been incorporated to verify the code's efficiency through numerous trials. These tests check that the server runs or shuts down and responds correctly to various requests and errors.

## Association classes

We've also added classes that allow us to make associations. To learn more about them, you can follow the link below to the practice exercise that explains them in more detail. https://gitlab.eif.urjc.es/jmcondo/practica-programacion-2.git

## Conclusions and lessons learned

In conclusion, this project has utilized the HTTP protocol and its GET and POST methods for various queries of diseases and associated targets. We have learned how to create HTML files for program aesthetics and how to handle all types of errors. We have conducted several API surveys to request data in JSON format and implemented serialization and deserialization of this data. The biomedical engineer is responsible for facilitating the work of the healthcare and scientific sectors, and in this exercise, this has served to provide a rapid query for different types of diseases and targets for clinical study and diagnosis.



---

    ```