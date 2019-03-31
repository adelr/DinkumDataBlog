---
date : 2019-03-28
slug : polyglot_wrangling
mathjax : ture
title : Polyglot Data Wrangling
author : Adel Rahmani
categories: 
  - Python
  - blogging
tags: 
  - python
  - sql
  - r
  - data wrangling
summary : SQL vs Python vs R - Un pour tous, tous pour un!
thumbnailImagePosition : left
thumbnailImage : ./static/img/avatar-icon.png
---

# SQL vs Python vs R

In this post we will look a how basic data wrangling operations can be performed in 3 languages
commonly used in data science: 

 - Structured Query Language (SQL)
 - Python
 - R
        
Note that while Python and R have obvious similarities in their approach to data wrangling, SQL is designed to work with relational data, where most of the time consuming operations are (ideally) performed on the database side rather than
in the client's memory. Both Python and R can process data in chunks, or even work with huge, distributed data sets through libraries like [Dask](https://docs.dask.org/en/latest/) (Python only) or [Apache Spark](https://spark.apache.org/) (Python, R, Scala, Java).
However, we're mostly interested in illustrating some basic data wrangling pipelines in all three languages, so we'll be using a small database that can easily fit in memory.

The [Jupyter notebook](https://jupyter.org/) allows us to run all our examples in one place.
We'll run an IPython kernel as our base platform and use an [IPython magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html) to run our R code within the same environment, and we'll use [sqlalchemy](https://www.sqlalchemy.org/) to run queries on a postgreSQL data base.

We won't be covering the basics of each language in this post. There are many excellent resources online.
For data wrangling the [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) is an outstanding book. For R it's hard to get past the wonderful [R for Data Science](https://r4ds.had.co.nz/) by Garrett Grolemund and Hadley Wickham. For SQL there are more resources than we can mention, especially once we factor in the various vendor-specific flavours of SQL. One of my personal favourites is [SQL Fundamentals for BI](https://www.packtpub.com/application-development/sql-fundamentals-business-intelligence-video) by Jeffrey James. 
Our SQL examples are based on some of the contents of that course.

We start by loading the Python required libraries (we'll do all our data wrangling using the awesome [pandas](https://pandas.pydata.org/) module) and create a connection to the PostgreSQL database using sqlalchemy.
For our examples we'll be using the well-known [dvdrental database](http://www.postgresqltutorial.com/postgresql-sample-database/) which contains 15 tables representing various aspects of a DVD rental business.


```python
# Connect to a SQL (PostgreSQL) database
from sqlalchemy import create_engine
db = 'postgres:///dvdrental'
con = create_engine(db, echo=False)

# Import pandas for data wrangling in python
import pandas as pd
import warnings
warnings.simplefilter('ignore')

# use ipython magic command to load R into our environment.
%load_ext rpy2.ipython

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
```

<style>.container { width:100% !important; }</style>


All our R code will be preceded by `%%R` command to run it on the R interpreter from within our Jupyter notebook.
We start by loading the [tidyverse](https://www.tidyverse.org/) library (which is in fact a collection of libraries),
and setting an option to make controlling how some outputs are rendered.


```r
%%R
library(tidyverse)
options(crayon.enabled = FALSE)
```

Because we're running on top of an ipython kernel, we'll write our SQL queries as strings and use pandas to run them on our database via sqlalchemy. 

----

## The data

First, let's see what tables are in our DVD rental database.


```python
q = '''
SELECT * FROM pg_catalog.pg_tables;
'''
```

```python
df = pd.read_sql_query(q, con)
tables = df[~(df.tablename.str.startswith('pg_')|df.tablename.str.startswith('sql_'))].tablename.values
print(tables)
```

    ['category' 'country' 'film_category' 'language' 'inventory' 'actor'
     'staff' 'payment' 'rental' 'store' 'city' 'film' 'address' 'film_actor'
     'customer']


For convenience, let's create a python dictionary with all the tables as dataframes. 

Obviously, this means that we're loading all the tables into memory, __which is not what one would typically want to do with a SQL database__, however, since our database is small, and we're only interested in comparing the wrangling syntax across different languages, this is fine for our purpose.


```python
tbl = {table: pd.read_sql_query(f'SELECT * FROM {table};', 
                                con, parse_dates=['payment_date']) 
       for table in tables}
```

Let's look at a few rows of the payment table.


```python
payment = tbl['payment']
payment.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>payment_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>17503</td>
      <td>341</td>
      <td>2</td>
      <td>1520</td>
      <td>7.99</td>
      <td>2007-02-15 22:25:46.996577</td>
    </tr>
    <tr>
      <th>1</th>
      <td>17504</td>
      <td>341</td>
      <td>1</td>
      <td>1778</td>
      <td>1.99</td>
      <td>2007-02-16 17:23:14.996577</td>
    </tr>
    <tr>
      <th>2</th>
      <td>17505</td>
      <td>341</td>
      <td>1</td>
      <td>1849</td>
      <td>7.99</td>
      <td>2007-02-16 22:41:45.996577</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17506</td>
      <td>341</td>
      <td>2</td>
      <td>2829</td>
      <td>2.99</td>
      <td>2007-02-19 19:39:56.996577</td>
    </tr>
    <tr>
      <th>4</th>
      <td>17507</td>
      <td>341</td>
      <td>2</td>
      <td>3130</td>
      <td>7.99</td>
      <td>2007-02-20 17:31:48.996577</td>
    </tr>
  </tbody>
</table>
</div>



We can "pass" the `payment` dataframe to R in the following way:


```r
%%R -i payment
head(payment)
```

      payment_id customer_id staff_id rental_id amount        payment_date
    0      17503         341        2      1520   7.99 2007-02-15 22:25:46
    1      17504         341        1      1778   1.99 2007-02-16 17:23:14
    2      17505         341        1      1849   7.99 2007-02-16 22:41:45
    3      17506         341        2      2829   2.99 2007-02-19 19:39:56
    4      17507         341        2      3130   7.99 2007-02-20 17:31:48
    5      17508         341        1      3382   5.99 2007-02-21 12:33:49



Now that we've got all the tables loaded, let's run a few queries. 

Let's start with something simple.

----

### Which movie rentals were below a dollar for customers with an id above 500?


#### ▶ SQL

The query is nothing fancy here. We're selecting a few features (columns) from the `payment` table,
filtering on the dollar amount and customer id before ordering the rows.


```python
q = '''
SELECT 
    p.payment_id, p.customer_id, p.amount 
FROM 
    payment p
WHERE 
    p.amount < 1 AND p.customer_id > 500
ORDER BY 1 ASC, 2 DESC, 3 ASC;
'''
df_sql = pd.read_sql_query(q, con)     # run the query on the database
print(df_sql.shape)                    # output the shape of the resulting table
df_sql.head()                          # display the first few rows
```

    (413, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18121</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18122</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18125</td>
      <td>503</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18134</td>
      <td>506</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18144</td>
      <td>510</td>
      <td>0.99</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python

Pandas allow us to chain methods on a dataframe, however, writing everything on a single line is cumbersome for long pipelines. 

We can write each step of the pipeline on its own line by wrapping the pipeline in brackets.


```python
df = (payment[(payment.amount < 1) & (payment.customer_id > 500)]  # select rows based on conditions
         .loc[:, ['payment_id','customer_id','amount']]            # select 3 columns
         .sort_values(by=['payment_id', 'customer_id', 'amount'],  # sort the rows according to the values  
                      ascending=[True, False, True])               #      in the columns
         .reset_index(drop=True)                                   # not really required but looks nicer
        )
print(df.shape)
df.head()
```

    (413, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18121</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18122</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18125</td>
      <td>503</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18134</td>
      <td>506</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18144</td>
      <td>510</td>
      <td>0.99</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R

For this simple query the R code is similar to the Python one. The pipe symbol `%>%` is equivalent to the dot symbol in pandas which allows us to chain methods together. 

The `%%R -o df_r` part of the code is a way to transfer the R dataframe back to our Python interpreter.


```r
%%R -o df_r   
df_r = payment %>% 
        filter(amount < 1, customer_id > 500) %>% 
        select(payment_id, customer_id, amount) %>% 
        arrange(payment_id, desc(customer_id), amount)
```

```python
df_r.shape
df_r.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18121</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18122</td>
      <td>502</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18125</td>
      <td>503</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18134</td>
      <td>506</td>
      <td>0.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18144</td>
      <td>510</td>
      <td>0.99</td>
    </tr>
  </tbody>
</table>
</div>



#### Sanity check
Just to make sure that we've run our query correctly, we can compare the result from the SQL query with the results of the Python and R pipelines. Because of the fact that R indexing starts at 1 instead of 0, we need to reset the index of the R dataframe after we export it to Python.


```python
all(df==df_sql), all(df_r==df_sql)
```

    (True, True)



Any other trivial query could be handled in a similar way... 

Let's look at a query where we need to extract a feature that doesn't appear explicitly in the original data.

---

### Which transactions occured in the month of March only (irrespective of the year)?

The `payment` table has a `payment_date` feature from which we will need to extract the month.

#### ▶  SQL

We can extract the month value out of the `payment_date` column using the `EXTRACT` function.


```python
q = '''
SELECT 
    p.payment_id, p.customer_id cust_id, p.amount, p.payment_date
FROM 
    payment p
WHERE 
    EXTRACT(month FROM p.payment_date) = 3
    AND p.amount < 1
ORDER BY 
    cust_id DESC, 3 ASC;
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql.head()
```

    (1021, 4)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>cust_id</th>
      <th>amount</th>
      <th>payment_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>22611</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-02 15:51:25.996577</td>
    </tr>
    <tr>
      <th>1</th>
      <td>22613</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-21 07:09:41.996577</td>
    </tr>
    <tr>
      <th>2</th>
      <td>22606</td>
      <td>597</td>
      <td>0.99</td>
      <td>2007-03-19 05:51:32.996577</td>
    </tr>
    <tr>
      <th>3</th>
      <td>22589</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-01 20:50:37.996577</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22598</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-22 21:49:07.996577</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python

When we loaded the payment table from the database using sqlalchemy, the `payment_date` feature was correctly
parsed as a datetime object. 

This allows us to use the pandas `dt` accessor to extract a variety of date and time related features, including the month.


```python
df = (payment[(payment.amount < 1) & (payment.payment_date.dt.month==3)]
       .rename({'customer_id': 'cust_id'}, axis=1)
       .reindex(['payment_id','cust_id','amount','payment_date'], axis=1)
       .sort_values(['cust_id', 'amount'], ascending=[False, True])
       .reset_index(drop=True)
     )
      
print(df.shape)
df.head()
```

    (1021, 4)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>cust_id</th>
      <th>amount</th>
      <th>payment_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>22611</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-02 15:51:25.996577</td>
    </tr>
    <tr>
      <th>1</th>
      <td>22613</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-21 07:09:41.996577</td>
    </tr>
    <tr>
      <th>2</th>
      <td>22606</td>
      <td>597</td>
      <td>0.99</td>
      <td>2007-03-19 05:51:32.996577</td>
    </tr>
    <tr>
      <th>3</th>
      <td>22589</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-01 20:50:37.996577</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22592</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-17 15:08:26.996577</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R

A great way to handle datetime objects in R is via the [lubridate](https://lubridate.tidyverse.org/) library. 
To make it clear when we're using a lubridate object, we won't load the library, but we call its functions using
the `lubridate::` prefix.


```r
%%R -o df_r
df_r = payment %>% 
        filter(amount < 1, lubridate::month(payment$payment_date)==3) %>% 
        rename(cust_id=customer_id) %>% 
        select(-rental_id, -staff_id) %>% 
        arrange(desc(cust_id), amount)
```

```python
print(df_r.shape)
df_r.head()
```

    (1021, 4)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>cust_id</th>
      <th>amount</th>
      <th>payment_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>22611</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-02 15:51:25+11:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>22613</td>
      <td>598</td>
      <td>0.99</td>
      <td>2007-03-21 07:09:41+11:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>22606</td>
      <td>597</td>
      <td>0.99</td>
      <td>2007-03-19 05:51:32+11:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>22589</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-01 20:50:37+11:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22592</td>
      <td>596</td>
      <td>0.99</td>
      <td>2007-03-17 15:08:26+11:00</td>
    </tr>
  </tbody>
</table>
</div>



Here we get an glimpse into the infinite joy of working with datetime objects. 

During the transfer from Python to R and back to Python, our `payment_date` format has changed slightly.

Instead of worrying about fixing this we'll just exclude that column when comparing the R result with the SQL/Python ones.

Henceforth, we won't be worrying about this issue. We'll simply check that the dataframes shape match and
the first few rows are consistent.


```python
all(df==df_sql), all(df.iloc[:, :-1]==df_r.reset_index(drop=True).iloc[:, :-1])
```

    (True, True)



----

### Which day saw the most business (largest number of transactions)?

This is a common operation. We need to group our payments by date, count how many transactions occured on that date
and order the results accordingly.

#### ▶ SQL


```python
q = '''
SELECT 
    p.payment_date::date, COUNT(*)
FROM 
    payment p
GROUP BY 1
ORDER BY 2 DESC
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (32, 2)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_date</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-04-30</td>
      <td>1311</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-01</td>
      <td>676</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-21</td>
      <td>673</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-04-27</td>
      <td>643</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-04-29</td>
      <td>640</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-19</td>
      <td>631</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-04-28</td>
      <td>627</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-18</td>
      <td>624</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-22</td>
      <td>621</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-20</td>
      <td>611</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-02</td>
      <td>595</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-17</td>
      <td>584</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-23</td>
      <td>557</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-04-08</td>
      <td>516</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-04-09</td>
      <td>514</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-04-06</td>
      <td>486</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-04-10</td>
      <td>482</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-04-07</td>
      <td>472</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-04-11</td>
      <td>468</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-04-12</td>
      <td>452</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-02-19</td>
      <td>310</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-02-15</td>
      <td>308</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-02-18</td>
      <td>302</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-02-20</td>
      <td>291</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-02-17</td>
      <td>283</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-02-16</td>
      <td>282</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-02-21</td>
      <td>213</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-05-14</td>
      <td>182</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-04-26</td>
      <td>79</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-16</td>
      <td>72</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-04-05</td>
      <td>64</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2007-02-14</td>
      <td>27</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶  Python

The Python pipeline mimics the SQL query rather closely.


```python
df = (payment
       .groupby(payment.payment_date.dt.date)['amount']
       .count().rename('count')
       .sort_values(ascending=False)
       .reset_index()
     )
df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_date</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-04-30</td>
      <td>1311</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-01</td>
      <td>676</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-21</td>
      <td>673</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-04-27</td>
      <td>643</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-04-29</td>
      <td>640</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-19</td>
      <td>631</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-04-28</td>
      <td>627</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-18</td>
      <td>624</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-22</td>
      <td>621</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-20</td>
      <td>611</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-02</td>
      <td>595</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-17</td>
      <td>584</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-23</td>
      <td>557</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-04-08</td>
      <td>516</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-04-09</td>
      <td>514</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-04-06</td>
      <td>486</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-04-10</td>
      <td>482</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-04-07</td>
      <td>472</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-04-11</td>
      <td>468</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-04-12</td>
      <td>452</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-02-19</td>
      <td>310</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-02-15</td>
      <td>308</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-02-18</td>
      <td>302</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-02-20</td>
      <td>291</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-02-17</td>
      <td>283</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-02-16</td>
      <td>282</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-02-21</td>
      <td>213</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-05-14</td>
      <td>182</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-04-26</td>
      <td>79</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-16</td>
      <td>72</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-04-05</td>
      <td>64</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2007-02-14</td>
      <td>27</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶  R

We follow the same pattern for our R code. The conversion to a dataframe at the end (using `as.data.frame`) is
simply to get a nicer formatting of the output.


```r
%%R 
df_r = payment %>% 
        group_by(payment_date=lubridate::date(payment$payment_date)) %>% 
        summarise(n = n()) %>% 
        arrange(desc(n)) %>%
        as.data.frame()
df_r
```

       payment_date    n
    1    2007-04-30 1311
    2    2007-03-01  676
    3    2007-03-21  673
    4    2007-04-27  643
    5    2007-04-29  640
    6    2007-03-19  631
    7    2007-04-28  627
    8    2007-03-18  624
    9    2007-03-22  621
    10   2007-03-20  611
    11   2007-03-02  595
    12   2007-03-17  584
    13   2007-03-23  557
    14   2007-04-08  516
    15   2007-04-09  514
    16   2007-04-06  486
    17   2007-04-10  482
    18   2007-04-07  472
    19   2007-04-11  468
    20   2007-04-12  452
    21   2007-02-19  310
    22   2007-02-15  308
    23   2007-02-18  302
    24   2007-02-20  291
    25   2007-02-17  283
    26   2007-02-16  282
    27   2007-02-21  213
    28   2007-05-14  182
    29   2007-04-26   79
    30   2007-03-16   72
    31   2007-04-05   64
    32   2007-02-14   27



---

### How much did each customer spend and when?

There are a number of ways to answer this question. To look at a different way of aggregating the data we will return the collection of transaction dates for each customer. In SQL we can do that with an array.

#### ▶ SQL


```python
q = '''
SELECT 
    p.customer_id, 
    SUM(p.amount) total, 
    ARRAY_AGG(p.payment_date::date) dates
FROM 
    payment p
GROUP BY 1
ORDER BY 2 DESC
'''

df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql.head()
```

    (599, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>total</th>
      <th>dates</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>148</td>
      <td>211.55</td>
      <td>[2007-02-15, 2007-02-15, 2007-02-19, 2007-02-1...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>526</td>
      <td>208.58</td>
      <td>[2007-02-15, 2007-02-16, 2007-02-17, 2007-02-1...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>178</td>
      <td>194.61</td>
      <td>[2007-02-15, 2007-02-15, 2007-02-16, 2007-02-1...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>137</td>
      <td>191.62</td>
      <td>[2007-02-18, 2007-02-19, 2007-02-20, 2007-02-2...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>144</td>
      <td>189.60</td>
      <td>[2007-02-16, 2007-02-17, 2007-02-19, 2007-02-2...</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶  Python

In Python we'll gather the transaction dates for each customer as a list. 

We can build that list using a `lambda` (anonymous) function during the aggregation step.


```python
df = (payment
       .groupby('customer_id')[['amount', 'payment_date']]
       .agg({
               'amount':'sum',
               'payment_date': lambda x: list(x.dt.date)
            })
       .rename(columns={'amount':'total', 'payment_date': 'date'})
       .sort_values('total', ascending=False)
       .reset_index()
      )
print(df.shape)
df.head()
```

    (599, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>total</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>148</td>
      <td>211.55</td>
      <td>[2007-02-15, 2007-02-15, 2007-02-19, 2007-02-1...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>526</td>
      <td>208.58</td>
      <td>[2007-02-15, 2007-02-16, 2007-02-17, 2007-02-1...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>178</td>
      <td>194.61</td>
      <td>[2007-02-15, 2007-02-15, 2007-02-16, 2007-02-1...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>137</td>
      <td>191.62</td>
      <td>[2007-02-18, 2007-02-19, 2007-02-20, 2007-02-2...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>144</td>
      <td>189.60</td>
      <td>[2007-02-16, 2007-02-17, 2007-02-19, 2007-02-2...</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R

For this query the R code is similar to the Python one (syntactic idiosyncrasies aside).


```r
%%R 
df_r = payment %>% 
      mutate(payment_date = as.Date(payment_date)) %>% 
      group_by(customer_id) %>% 
      summarise(total=sum(amount), dates=list(payment_date)) %>% 
      arrange(desc(total))

print(dim(df_r))
print(head(df_r, 5))
```

    [1] 599   3
    # A tibble: 5 x 3
      customer_id total dates      
            <int> <dbl> <list>     
    1         148  212. <date [45]>
    2         526  209. <date [42]>
    3         178  195. <date [39]>
    4         137  192. <date [38]>
    5         144  190. <date [40]>



At first glance it looks like the results are different from the SQL/Python, but this is purely cosmetic. The R data structure (a `tibble` actually) rounds up the floating point values and shrinks the lists when displaying the results. We could convert the `tibble` to a R dataframe but the output would be unwieldy.
Instead, we can unpack the first row to show that the data has been parsed correctly.


```r
%%R
print(df_r$total[1]) 
print(df_r$dates[1])
```

    [1] 211.55
    [[1]]
     [1] "2007-02-15" "2007-02-15" "2007-02-19" "2007-02-19" "2007-02-19"
     [6] "2007-03-01" "2007-03-02" "2007-03-17" "2007-03-17" "2007-03-18"
    [11] "2007-03-18" "2007-03-18" "2007-03-20" "2007-03-20" "2007-03-20"
    [16] "2007-03-21" "2007-03-21" "2007-03-21" "2007-03-21" "2007-03-22"
    [21] "2007-03-22" "2007-03-22" "2007-03-22" "2007-04-05" "2007-04-06"
    [26] "2007-04-08" "2007-04-08" "2007-04-08" "2007-04-09" "2007-04-10"
    [31] "2007-04-11" "2007-04-12" "2007-04-27" "2007-04-27" "2007-04-27"
    [36] "2007-04-28" "2007-04-28" "2007-04-28" "2007-04-29" "2007-04-29"
    [41] "2007-04-29" "2007-04-29" "2007-04-30" "2007-04-29" "2007-04-30"
    



---

### Which  days of March 2007 recorded no sale?

This may seem like the sort of query we've already looked at, however there is a catch.
The database only records transactions that have occurred (it seems obvious when said like that!).
This means that dates with no sales aren't in the database. 
Therefore we need to generate a series of dates (with a daily frequency) and join our payment data on it to find the days with no sales.

In PostgreSQL we can use `generate_series` to do that. Note that we select from it as if it were a table (which
we name `gs`). By joining on it we can "expand" our payment data to include the dates for which no transaction took place. These would of course contain `NULL` values for the transaction data. By identifying where those `NULL` rows are we can answer the original question.

#### ▶  SQL


```python
q = '''
SELECT 
    gs::date, p.*
FROM 
    generate_series('2007-03-01', '2007-03-31', INTERVAL '1 Day') gs
LEFT JOIN 
    payment p 
ON 
    p.payment_date::date = gs::date
WHERE 
    payment_date is NULL
'''
```

```python
df_sql = pd.read_sql_query(q, con).fillna('')['gs']
print(df_sql.shape)
df_sql
```

    (21,)
    0     2007-03-03
    1     2007-03-04
    2     2007-03-05
    3     2007-03-06
    4     2007-03-07
    5     2007-03-08
    6     2007-03-09
    7     2007-03-10
    8     2007-03-11
    9     2007-03-12
    10    2007-03-13
    11    2007-03-14
    12    2007-03-15
    13    2007-03-24
    14    2007-03-25
    15    2007-03-26
    16    2007-03-27
    17    2007-03-28
    18    2007-03-29
    19    2007-03-30
    20    2007-03-31
    Name: gs, dtype: object



#### ▶ Python
We could do something similar in Python, however let's try a more pythonic approach and use set operations to extract the dates we want. We simply construct the set of all dates in March 2007 and take the difference with the dates that are already in the database. The moral of the story here is that whereas the Python (and R) syntax can often look _SQLish_, this is not always the most concise or even suitable way to get to the answer.


```python
gs = pd.date_range(start='20070301', end='20070331', freq='D')
df = pd.DataFrame(index = set(gs.date) - set(payment.payment_date.dt.date.values))
print(df.shape)
df
```

    (21, 0)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2007-03-28</th>
    </tr>
    <tr>
      <th>2007-03-30</th>
    </tr>
    <tr>
      <th>2007-03-26</th>
    </tr>
    <tr>
      <th>2007-03-13</th>
    </tr>
    <tr>
      <th>2007-03-10</th>
    </tr>
    <tr>
      <th>2007-03-15</th>
    </tr>
    <tr>
      <th>2007-03-08</th>
    </tr>
    <tr>
      <th>2007-03-09</th>
    </tr>
    <tr>
      <th>2007-03-24</th>
    </tr>
    <tr>
      <th>2007-03-03</th>
    </tr>
    <tr>
      <th>2007-03-12</th>
    </tr>
    <tr>
      <th>2007-03-05</th>
    </tr>
    <tr>
      <th>2007-03-27</th>
    </tr>
    <tr>
      <th>2007-03-25</th>
    </tr>
    <tr>
      <th>2007-03-29</th>
    </tr>
    <tr>
      <th>2007-03-31</th>
    </tr>
    <tr>
      <th>2007-03-06</th>
    </tr>
    <tr>
      <th>2007-03-07</th>
    </tr>
    <tr>
      <th>2007-03-11</th>
    </tr>
    <tr>
      <th>2007-03-04</th>
    </tr>
    <tr>
      <th>2007-03-14</th>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R
Set operations also work in R. The output is a bit strange. We have a list of lists with a single element.
We could flatten the nested list but it would only obfuscate the code so we'll leave it like that.


```r
%%R
gs = seq(lubridate::ymd('2007-03-01'), lubridate::ymd('2007-03-31'), by = '1 day')
lapply(setdiff(gs, lubridate::date(payment$payment_date)), as.Date, origin='1970-01-01')
```

    [[1]]
    [1] "2007-03-03"
    
    [[2]]
    [1] "2007-03-04"
    
    [[3]]
    [1] "2007-03-05"
    
    [[4]]
    [1] "2007-03-06"
    
    [[5]]
    [1] "2007-03-07"
    
    [[6]]
    [1] "2007-03-08"
    
    [[7]]
    [1] "2007-03-09"
    
    [[8]]
    [1] "2007-03-10"
    
    [[9]]
    [1] "2007-03-11"
    
    [[10]]
    [1] "2007-03-12"
    
    [[11]]
    [1] "2007-03-13"
    
    [[12]]
    [1] "2007-03-14"
    
    [[13]]
    [1] "2007-03-15"
    
    [[14]]
    [1] "2007-03-24"
    
    [[15]]
    [1] "2007-03-25"
    
    [[16]]
    [1] "2007-03-26"
    
    [[17]]
    [1] "2007-03-27"
    
    [[18]]
    [1] "2007-03-28"
    
    [[19]]
    [1] "2007-03-29"
    
    [[20]]
    [1] "2007-03-30"
    
    [[21]]
    [1] "2007-03-31"
    



---

### How many transactions were there for each day of March 2007?

This is a simple question, we just need to keep in mind that some days had no transaction. We should still ouput those with a count of zero. The basic idea is similar to the previous example. We create a time series to "pad out" the missing days in the `payment_date` feature. 

#### ▶ SQL


```python
q = '''
SELECT 
    gs::date date, 
    COUNT(p.*) number_of_transactions
FROM 
    generate_series('2007-03-01', '2007-03-31', INTERVAL '1 Day') gs
LEFT JOIN 
    payment p 
ON 
    p.payment_date::date = gs::date 
GROUP BY 
    gs::date 
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (31, 2)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>number_of_transactions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-03-01</td>
      <td>676</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-02</td>
      <td>595</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-03</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-03-04</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-03-05</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-06</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-03-07</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-08</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-09</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-11</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-12</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-03-14</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-03-15</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-03-16</td>
      <td>72</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-03-17</td>
      <td>584</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-03-18</td>
      <td>624</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-03-19</td>
      <td>631</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-03-20</td>
      <td>611</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-03-21</td>
      <td>673</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-03-22</td>
      <td>621</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-03-23</td>
      <td>557</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-03-24</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-03-25</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-03-26</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-03-27</td>
      <td>0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-03-28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-03-29</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-03-31</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python

Similarly, in Python we can create the series of dates for March 2007 using the `date_range` object from `pandas`.


```python
gs = pd.date_range(start='20070301', end='20070331', freq='D')
df = (payment
       .assign(payment_date=pd.to_datetime(payment.payment_date).dt.date)
       .groupby('payment_date')
       .agg({'amount':'count'})
       .reindex(gs, fill_value=0)
       .reset_index()
       .rename(columns={'index':'date','amount':'number_of_transactions'})
)

print(df.shape)
df
```

    (31, 2)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>number_of_transactions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-03-01</td>
      <td>676</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-02</td>
      <td>595</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-03</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-03-04</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-03-05</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-06</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-03-07</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-08</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-09</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-11</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-12</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-03-14</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-03-15</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-03-16</td>
      <td>72</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-03-17</td>
      <td>584</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-03-18</td>
      <td>624</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-03-19</td>
      <td>631</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-03-20</td>
      <td>611</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-03-21</td>
      <td>673</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-03-22</td>
      <td>621</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-03-23</td>
      <td>557</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-03-24</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-03-25</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-03-26</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-03-27</td>
      <td>0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-03-28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-03-29</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-03-31</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶  R

Once again, the pattern for R follows the same principles.


```r
%%R -o df_r
gs = data_frame(payment_date=seq(lubridate::ymd('2007-03-01'), 
                                 lubridate::ymd('2007-03-31'), 
                                 by = '1 day'))

df_r = payment %>% 
      mutate(payment_date=lubridate::date(payment_date)) %>% 
      group_by(payment_date) %>% 
      summarise(number_of_transactions=n()) %>% 
      right_join(gs, by='payment_date') %>%
      replace_na(list(number_of_transactions=0))

as.data.frame(df_r)
```

       payment_date number_of_transactions
    1    2007-03-01                    676
    2    2007-03-02                    595
    3    2007-03-03                      0
    4    2007-03-04                      0
    5    2007-03-05                      0
    6    2007-03-06                      0
    7    2007-03-07                      0
    8    2007-03-08                      0
    9    2007-03-09                      0
    10   2007-03-10                      0
    11   2007-03-11                      0
    12   2007-03-12                      0
    13   2007-03-13                      0
    14   2007-03-14                      0
    15   2007-03-15                      0
    16   2007-03-16                     72
    17   2007-03-17                    584
    18   2007-03-18                    624
    19   2007-03-19                    631
    20   2007-03-20                    611
    21   2007-03-21                    673
    22   2007-03-22                    621
    23   2007-03-23                    557
    24   2007-03-24                      0
    25   2007-03-25                      0
    26   2007-03-26                      0
    27   2007-03-27                      0
    28   2007-03-28                      0
    29   2007-03-29                      0
    30   2007-03-30                      0
    31   2007-03-31                      0



---

### Days with no transactions in March 2007 - Alternate version

Let's revisit the problem we dealt with previous using set operations in Python and R and illustrate how we could answer the question using a more SQLish pipeline.
We can reuse the code from the previous example. We just need to add a filtering step.

#### ▶ SQL


```python
q = '''
SELECT 
    gs::date date, COUNT(p.*) number_of_transactions
FROM 
    generate_series('2007-03-01', '2007-03-31', INTERVAL '1 Day') gs
LEFT JOIN 
    payment p 
ON 
    p.payment_date::date = gs::date 
GROUP BY 
    gs::date 
HAVING 
    COUNT(p.*) = 0
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (21, 2)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>number_of_transactions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-03-03</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-04</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-05</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-03-06</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-03-07</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-08</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-03-09</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-11</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-12</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-14</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-15</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-03-24</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-03-25</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-03-26</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-03-27</td>
      <td>0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-03-28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-03-29</td>
      <td>0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-03-30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-03-31</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python


```python
gs = pd.date_range(start='20070301', end='20070331', freq='D')
df = (payment
       .assign(payment_date=pd.to_datetime(payment.payment_date).dt.date)
       .groupby('payment_date')
       .agg({'amount':'count'})
       .rename(columns={'amount':'number_of_transactions'})
       .reindex(gs, fill_value=0)
       .query('number_of_transactions == 0')  
)

print(df.shape)
df
```

    (21, 1)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>number_of_transactions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2007-03-03</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-04</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-05</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-06</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-07</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-08</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-09</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-10</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-11</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-12</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-13</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-14</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-15</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-24</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-25</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-26</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-27</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-28</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-29</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-30</th>
      <td>0</td>
    </tr>
    <tr>
      <th>2007-03-31</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R


```r
%%R
gs = data_frame(payment_date=seq(lubridate::ymd('2007-03-01'), 
                                 lubridate::ymd('2007-03-31'), 
                                 by = '1 day'))

df_r = payment %>% 
      mutate(payment_date=lubridate::date(payment_date)) %>% 
      group_by(payment_date) %>% 
      summarise(number_of_transactions=n()) %>% 
      right_join(gs, by="payment_date") %>%
      replace_na(list(number_of_transactions=0)) %>%
      subset(number_of_transactions==0)

print(dim(df_r))
as.data.frame(df_r)
```

    [1] 21  2
       payment_date number_of_transactions
    1    2007-03-03                      0
    2    2007-03-04                      0
    3    2007-03-05                      0
    4    2007-03-06                      0
    5    2007-03-07                      0
    6    2007-03-08                      0
    7    2007-03-09                      0
    8    2007-03-10                      0
    9    2007-03-11                      0
    10   2007-03-12                      0
    11   2007-03-13                      0
    12   2007-03-14                      0
    13   2007-03-15                      0
    14   2007-03-24                      0
    15   2007-03-25                      0
    16   2007-03-26                      0
    17   2007-03-27                      0
    18   2007-03-28                      0
    19   2007-03-29                      0
    20   2007-03-30                      0
    21   2007-03-31                      0



---

### Which movies have never been rented?

So far we've only worked with a single table out of the 15 contained in the database. To match movies to rental transactions we will need
to use 3 new tables. The film one contains information about the movies, the inventory one links the movies to an inventory id, which is used in the rental table to connect movies to actual rentals.

Let's have a look at the structures of these tables.


```python
for t in ['inventory', 'payment', 'rental', 'film']:
    q = f'''
SELECT * FROM {t}
LIMIT 1
'''
    df = pd.read_sql_query(q, con)
    print(t)
    display(df)
```

    inventory



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>inventory_id</th>
      <th>film_id</th>
      <th>store_id</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2006-02-15 10:09:17</td>
    </tr>
  </tbody>
</table>
</div>


    payment



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>payment_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>17503</td>
      <td>341</td>
      <td>2</td>
      <td>1520</td>
      <td>7.99</td>
      <td>2007-02-15 22:25:46.996577</td>
    </tr>
  </tbody>
</table>
</div>


    rental



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rental_id</th>
      <th>rental_date</th>
      <th>inventory_id</th>
      <th>customer_id</th>
      <th>return_date</th>
      <th>staff_id</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>2005-05-24 22:54:33</td>
      <td>1525</td>
      <td>459</td>
      <td>2005-05-28 19:40:33</td>
      <td>1</td>
      <td>2006-02-16 02:30:53</td>
    </tr>
  </tbody>
</table>
</div>


    film



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>description</th>
      <th>release_year</th>
      <th>language_id</th>
      <th>rental_duration</th>
      <th>rental_rate</th>
      <th>length</th>
      <th>replacement_cost</th>
      <th>rating</th>
      <th>last_update</th>
      <th>special_features</th>
      <th>fulltext</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>133</td>
      <td>Chamber Italian</td>
      <td>A Fateful Reflection of a Moose And a Husband ...</td>
      <td>2006</td>
      <td>1</td>
      <td>7</td>
      <td>4.99</td>
      <td>117</td>
      <td>14.99</td>
      <td>NC-17</td>
      <td>2013-05-26 14:50:58.951</td>
      <td>[Trailers]</td>
      <td>'chamber':1 'fate':4 'husband':11 'italian':2 ...</td>
    </tr>
  </tbody>
</table>
</div>


#### ▶ SQL

Let's join the tables, count how many times each movie has been rented and select those for which the count is zero.


```python
q = '''
SELECT 
    t.film_id, t.title, t.rentals 
FROM 
    (SELECT 
        f.film_id, f.title, 
        COUNT(distinct r.rental_id) as rentals
    FROM film f
        LEFT JOIN inventory i ON i.film_id = f.film_id
        LEFT JOIN rental r ON r.inventory_id = i.inventory_id
    GROUP BY 1,2
    HAVING 
        COUNT(distinct r.rental_id) = 0
        ) t
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (42, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>rentals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>14</td>
      <td>Alice Fantasia</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>33</td>
      <td>Apollo Teen</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>36</td>
      <td>Argonauts Town</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>38</td>
      <td>Ark Ridgemont</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>41</td>
      <td>Arsenic Independence</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>87</td>
      <td>Boondock Ballroom</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>108</td>
      <td>Butch Panther</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>128</td>
      <td>Catch Amistad</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>144</td>
      <td>Chinatown Gladiator</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>148</td>
      <td>Chocolate Duck</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>171</td>
      <td>Commandments Express</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>192</td>
      <td>Crossing Divorce</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>195</td>
      <td>Crowds Telemark</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>198</td>
      <td>Crystal Breaking</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>217</td>
      <td>Dazed Punk</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>221</td>
      <td>Deliverance Mulholland</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>318</td>
      <td>Firehouse Vietnam</td>
      <td>0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>325</td>
      <td>Floats Garden</td>
      <td>0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>332</td>
      <td>Frankenstein Stranger</td>
      <td>0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>359</td>
      <td>Gladiator Westward</td>
      <td>0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>386</td>
      <td>Gump Date</td>
      <td>0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>404</td>
      <td>Hate Handicap</td>
      <td>0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>419</td>
      <td>Hocus Frida</td>
      <td>0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>495</td>
      <td>Kentuckian Giant</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>497</td>
      <td>Kill Brotherhood</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>607</td>
      <td>Muppet Mile</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>642</td>
      <td>Order Betrayed</td>
      <td>0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>669</td>
      <td>Pearl Destiny</td>
      <td>0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>671</td>
      <td>Perdition Fargo</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>701</td>
      <td>Psycho Shrunk</td>
      <td>0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>712</td>
      <td>Raiders Antitrust</td>
      <td>0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>713</td>
      <td>Rainbow Shock</td>
      <td>0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>742</td>
      <td>Roof Champion</td>
      <td>0</td>
    </tr>
    <tr>
      <th>33</th>
      <td>801</td>
      <td>Sister Freddy</td>
      <td>0</td>
    </tr>
    <tr>
      <th>34</th>
      <td>802</td>
      <td>Sky Miracle</td>
      <td>0</td>
    </tr>
    <tr>
      <th>35</th>
      <td>860</td>
      <td>Suicides Silence</td>
      <td>0</td>
    </tr>
    <tr>
      <th>36</th>
      <td>874</td>
      <td>Tadpole Park</td>
      <td>0</td>
    </tr>
    <tr>
      <th>37</th>
      <td>909</td>
      <td>Treasure Command</td>
      <td>0</td>
    </tr>
    <tr>
      <th>38</th>
      <td>943</td>
      <td>Villain Desperate</td>
      <td>0</td>
    </tr>
    <tr>
      <th>39</th>
      <td>950</td>
      <td>Volume House</td>
      <td>0</td>
    </tr>
    <tr>
      <th>40</th>
      <td>954</td>
      <td>Wake Jaws</td>
      <td>0</td>
    </tr>
    <tr>
      <th>41</th>
      <td>955</td>
      <td>Walls Artist</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python
The go to approach for join operations in pandas is the `merge` method. The type of join can be specified as an optional parameter. 


```python
film, inventory, rental = tbl['film'], tbl['inventory'], tbl['rental']

df = (film
        .merge(inventory, on='film_id', how='left')
        .merge(rental, on='inventory_id', how='left')
        .groupby(['film_id','title'])[['rental_id']]
        .count()
        .rename(columns={'rental_id':'rentals'})
        .query('rentals == 0')
        .reset_index()
     )
print(df.shape)
df
```

    (42, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>rentals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>14</td>
      <td>Alice Fantasia</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>33</td>
      <td>Apollo Teen</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>36</td>
      <td>Argonauts Town</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>38</td>
      <td>Ark Ridgemont</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>41</td>
      <td>Arsenic Independence</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>87</td>
      <td>Boondock Ballroom</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>108</td>
      <td>Butch Panther</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>128</td>
      <td>Catch Amistad</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>144</td>
      <td>Chinatown Gladiator</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>148</td>
      <td>Chocolate Duck</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>171</td>
      <td>Commandments Express</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>192</td>
      <td>Crossing Divorce</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>195</td>
      <td>Crowds Telemark</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>198</td>
      <td>Crystal Breaking</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>217</td>
      <td>Dazed Punk</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>221</td>
      <td>Deliverance Mulholland</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>318</td>
      <td>Firehouse Vietnam</td>
      <td>0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>325</td>
      <td>Floats Garden</td>
      <td>0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>332</td>
      <td>Frankenstein Stranger</td>
      <td>0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>359</td>
      <td>Gladiator Westward</td>
      <td>0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>386</td>
      <td>Gump Date</td>
      <td>0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>404</td>
      <td>Hate Handicap</td>
      <td>0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>419</td>
      <td>Hocus Frida</td>
      <td>0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>495</td>
      <td>Kentuckian Giant</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>497</td>
      <td>Kill Brotherhood</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>607</td>
      <td>Muppet Mile</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>642</td>
      <td>Order Betrayed</td>
      <td>0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>669</td>
      <td>Pearl Destiny</td>
      <td>0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>671</td>
      <td>Perdition Fargo</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>701</td>
      <td>Psycho Shrunk</td>
      <td>0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>712</td>
      <td>Raiders Antitrust</td>
      <td>0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>713</td>
      <td>Rainbow Shock</td>
      <td>0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>742</td>
      <td>Roof Champion</td>
      <td>0</td>
    </tr>
    <tr>
      <th>33</th>
      <td>801</td>
      <td>Sister Freddy</td>
      <td>0</td>
    </tr>
    <tr>
      <th>34</th>
      <td>802</td>
      <td>Sky Miracle</td>
      <td>0</td>
    </tr>
    <tr>
      <th>35</th>
      <td>860</td>
      <td>Suicides Silence</td>
      <td>0</td>
    </tr>
    <tr>
      <th>36</th>
      <td>874</td>
      <td>Tadpole Park</td>
      <td>0</td>
    </tr>
    <tr>
      <th>37</th>
      <td>909</td>
      <td>Treasure Command</td>
      <td>0</td>
    </tr>
    <tr>
      <th>38</th>
      <td>943</td>
      <td>Villain Desperate</td>
      <td>0</td>
    </tr>
    <tr>
      <th>39</th>
      <td>950</td>
      <td>Volume House</td>
      <td>0</td>
    </tr>
    <tr>
      <th>40</th>
      <td>954</td>
      <td>Wake Jaws</td>
      <td>0</td>
    </tr>
    <tr>
      <th>41</th>
      <td>955</td>
      <td>Walls Artist</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R
We start by "transfering" the new dataframes to R. The rest of the pipeline is very much like the one used in Python.


```r
%%R -i rental -i inventory -i film -o df_r
df_r = film %>% 
        left_join(inventory, by="film_id") %>% 
        left_join(rental, by="inventory_id") %>% 
        group_by(film_id, title) %>% 
        summarise(rentals=n_distinct(rental_id, na.rm=TRUE)) %>% 
        filter(rentals==0) %>%
        as.data.frame()

df_r
```

       film_id                  title rentals
    1       14         Alice Fantasia       0
    2       33            Apollo Teen       0
    3       36         Argonauts Town       0
    4       38          Ark Ridgemont       0
    5       41   Arsenic Independence       0
    6       87      Boondock Ballroom       0
    7      108          Butch Panther       0
    8      128          Catch Amistad       0
    9      144    Chinatown Gladiator       0
    10     148         Chocolate Duck       0
    11     171   Commandments Express       0
    12     192       Crossing Divorce       0
    13     195        Crowds Telemark       0
    14     198       Crystal Breaking       0
    15     217             Dazed Punk       0
    16     221 Deliverance Mulholland       0
    17     318      Firehouse Vietnam       0
    18     325          Floats Garden       0
    19     332  Frankenstein Stranger       0
    20     359     Gladiator Westward       0
    21     386              Gump Date       0
    22     404          Hate Handicap       0
    23     419            Hocus Frida       0
    24     495       Kentuckian Giant       0
    25     497       Kill Brotherhood       0
    26     607            Muppet Mile       0
    27     642         Order Betrayed       0
    28     669          Pearl Destiny       0
    29     671        Perdition Fargo       0
    30     701          Psycho Shrunk       0
    31     712      Raiders Antitrust       0
    32     713          Rainbow Shock       0
    33     742          Roof Champion       0
    34     801          Sister Freddy       0
    35     802            Sky Miracle       0
    36     860       Suicides Silence       0
    37     874           Tadpole Park       0
    38     909       Treasure Command       0
    39     943      Villain Desperate       0
    40     950           Volume House       0
    41     954              Wake Jaws       0
    42     955           Walls Artist       0




```python
all(df==df_sql), all(df==df_r)
```

    (True, True)



---

### Find each customer's first order. 

To solve the problem in SQL we need to use a [__correlated subquery__](https://en.wikipedia.org/wiki/Correlated_subquery) whereby the inner query gets executed for every row of the outer query. 

In our case, the inner query gets executed for every row of the outer query because `min(rental_id)` will change with each customer. 

#### ▶ SQL


```python
q = '''
SELECT 
    r.customer_id, 
    min(r.rental_id) first_order_id, 
    (    
        SELECT r2.rental_date::date FROM rental r2 
        WHERE r2.rental_id = min(r.rental_id)
    ) first_order_date
FROM 
    rental r
GROUP BY 1
ORDER BY 1
'''

df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
display(df_sql.head())
```

    (599, 3)



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>first_order_id</th>
      <th>first_order_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>76</td>
      <td>2005-05-25</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>320</td>
      <td>2005-05-27</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>435</td>
      <td>2005-05-27</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1297</td>
      <td>2005-06-15</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>731</td>
      <td>2005-05-29</td>
    </tr>
  </tbody>
</table>
</div>


#### ▶ Python
In this case the Python syntax is a bit simpler. We group by the `customer_id` and pick the smallest `rental_id`.


```python
df = (rental
        .assign(rental_date=rental.rental_date.dt.date)
        .groupby(['customer_id' ])['rental_id','rental_date']
        .min()
        .reset_index()
        .rename(columns={'rental_id':'first_order_id', 'rental_date':'first_order_date'})
      )

print(df.shape)
display(df.head())
```

    (599, 3)



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>first_order_id</th>
      <th>first_order_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>76</td>
      <td>2005-05-25</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>320</td>
      <td>2005-05-27</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>435</td>
      <td>2005-05-27</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1297</td>
      <td>2005-06-15</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>731</td>
      <td>2005-05-29</td>
    </tr>
  </tbody>
</table>
</div>



```python
all(df==df_sql)
```

    True



#### ▶ R
The R version of the code is similar to the Python one.


```r
%%R 

df_r = rental %>% 
        mutate(rental_date=lubridate::date(rental_date)) %>% 
        group_by(customer_id) %>% 
        summarise_at(vars(rental_id, rental_date), funs(min)) %>%
        as.data.frame()

print(dim(df_r))
print(head(df_r, 5))
```

    [1] 599   3
      customer_id rental_id rental_date
    1           1        76  2005-05-25
    2           2       320  2005-05-27
    3           3       435  2005-05-27
    4           4      1297  2005-06-15
    5           5       731  2005-05-29



---

### Handling multiple conditions.

Let's look at a more complex query. We'd like to return all the rental transactions conducted by the staff with id 1, for which the rental id is larger than 15000, and the payment occured between 3am and 4am or 11pm and midnight in March 2007.

#### ▶ SQL
Although more complex than our previous examples, this query can be built from the pieces we've used before.
To keep things somewhat simple, we'll assume that between 3am and 4am means between 3:00 and 3:59. This will allow use to only concern ourselves with the hour number when filtering our data. Same with the second time period.


```python
q = '''
WITH base_table AS (
    SELECT gs::date AS date,  p.*
    FROM 
        generate_series('2007-03-01', '2007-03-31', INTERVAL '1 day') as gs
    LEFT JOIN payment p ON p.payment_date::date=gs::date AND p.staff_id = 1
    ORDER BY 1 NULLS FIRST
) 
SELECT 
    bt.date, bt.payment_id, bt.customer_id, bt.staff_id, bt.rental_id, bt.amount, 
    EXTRACT(hour FROM bt.payment_date)::int AS hour
FROM 
    base_table bt
WHERE 
    bt.rental_id > 15000 
    AND         
    EXTRACT(hour FROM bt.payment_date) IN (4,23)
ORDER BY bt.payment_date, bt.rental_id
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (36, 7)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-03-22</td>
      <td>23134</td>
      <td>46</td>
      <td>1</td>
      <td>15438</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-22</td>
      <td>23958</td>
      <td>136</td>
      <td>1</td>
      <td>15439</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-22</td>
      <td>23095</td>
      <td>42</td>
      <td>1</td>
      <td>15442</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-03-22</td>
      <td>22615</td>
      <td>598</td>
      <td>1</td>
      <td>15443</td>
      <td>7.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-03-22</td>
      <td>22960</td>
      <td>28</td>
      <td>1</td>
      <td>15445</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-22</td>
      <td>20574</td>
      <td>379</td>
      <td>1</td>
      <td>15446</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-03-22</td>
      <td>21651</td>
      <td>490</td>
      <td>1</td>
      <td>15448</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-22</td>
      <td>20027</td>
      <td>322</td>
      <td>1</td>
      <td>15450</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-22</td>
      <td>21866</td>
      <td>514</td>
      <td>1</td>
      <td>15451</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-22</td>
      <td>20370</td>
      <td>359</td>
      <td>1</td>
      <td>15453</td>
      <td>1.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-22</td>
      <td>24882</td>
      <td>238</td>
      <td>1</td>
      <td>15455</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-22</td>
      <td>25113</td>
      <td>262</td>
      <td>1</td>
      <td>15456</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-22</td>
      <td>19906</td>
      <td>306</td>
      <td>1</td>
      <td>15457</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-03-22</td>
      <td>22876</td>
      <td>20</td>
      <td>1</td>
      <td>15460</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-03-22</td>
      <td>23646</td>
      <td>103</td>
      <td>1</td>
      <td>15461</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-03-22</td>
      <td>20675</td>
      <td>389</td>
      <td>1</td>
      <td>15462</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-03-22</td>
      <td>23869</td>
      <td>127</td>
      <td>1</td>
      <td>15463</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-03-22</td>
      <td>23283</td>
      <td>62</td>
      <td>1</td>
      <td>15464</td>
      <td>6.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-03-22</td>
      <td>21921</td>
      <td>520</td>
      <td>1</td>
      <td>15465</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-03-22</td>
      <td>20970</td>
      <td>418</td>
      <td>1</td>
      <td>15466</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-03-22</td>
      <td>23647</td>
      <td>103</td>
      <td>1</td>
      <td>15467</td>
      <td>3.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-03-22</td>
      <td>20768</td>
      <td>399</td>
      <td>1</td>
      <td>15468</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-03-22</td>
      <td>22610</td>
      <td>597</td>
      <td>1</td>
      <td>15469</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-03-23</td>
      <td>24692</td>
      <td>215</td>
      <td>1</td>
      <td>15583</td>
      <td>2.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-03-23</td>
      <td>21731</td>
      <td>500</td>
      <td>1</td>
      <td>15584</td>
      <td>2.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-03-23</td>
      <td>22149</td>
      <td>545</td>
      <td>1</td>
      <td>15585</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-03-23</td>
      <td>21723</td>
      <td>499</td>
      <td>1</td>
      <td>15587</td>
      <td>7.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-03-23</td>
      <td>21764</td>
      <td>503</td>
      <td>1</td>
      <td>15588</td>
      <td>3.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-03-23</td>
      <td>22901</td>
      <td>22</td>
      <td>1</td>
      <td>15589</td>
      <td>6.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-23</td>
      <td>23284</td>
      <td>62</td>
      <td>1</td>
      <td>15591</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-03-23</td>
      <td>24163</td>
      <td>153</td>
      <td>1</td>
      <td>15593</td>
      <td>1.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2007-03-23</td>
      <td>25135</td>
      <td>264</td>
      <td>1</td>
      <td>15595</td>
      <td>4.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2007-03-23</td>
      <td>24478</td>
      <td>186</td>
      <td>1</td>
      <td>15596</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2007-03-23</td>
      <td>23323</td>
      <td>66</td>
      <td>1</td>
      <td>15598</td>
      <td>8.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>34</th>
      <td>2007-03-23</td>
      <td>23648</td>
      <td>103</td>
      <td>1</td>
      <td>15599</td>
      <td>5.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>35</th>
      <td>2007-03-23</td>
      <td>23729</td>
      <td>113</td>
      <td>1</td>
      <td>15600</td>
      <td>1.99</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python
Just for some variety we use the `between` method of pandas series to select the March 2007 data.
We pass pandas `Timestamp` objects to mark the first and last day of the month.
The rest of the pipeline should be self-explanatory. The last line is added for convenience.
We order the columns of the pandas dataframe to match the ordering of the columns in our SQL result.


```python
df = (payment
  .assign(date=payment.payment_date.dt.date)
  .loc[payment.payment_date.between(
              pd.Timestamp(year=2007, month=3, day=1), 
              pd.Timestamp(year=2007, month=3, day=31))
      ]
  .assign(hour=payment.payment_date.dt.hour)
  .query('(hour in (4, 23)) & (rental_id > 15000) & (staff_id == 1)')
  .sort_values('payment_date')
  .reset_index()
  .loc[:, df_sql.columns]
) 

print(df.shape)
df
```

    (36, 7)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2007-03-22</td>
      <td>23134</td>
      <td>46</td>
      <td>1</td>
      <td>15438</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007-03-22</td>
      <td>23958</td>
      <td>136</td>
      <td>1</td>
      <td>15439</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2007-03-22</td>
      <td>23095</td>
      <td>42</td>
      <td>1</td>
      <td>15442</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2007-03-22</td>
      <td>22615</td>
      <td>598</td>
      <td>1</td>
      <td>15443</td>
      <td>7.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2007-03-22</td>
      <td>22960</td>
      <td>28</td>
      <td>1</td>
      <td>15445</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2007-03-22</td>
      <td>20574</td>
      <td>379</td>
      <td>1</td>
      <td>15446</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2007-03-22</td>
      <td>21651</td>
      <td>490</td>
      <td>1</td>
      <td>15448</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2007-03-22</td>
      <td>20027</td>
      <td>322</td>
      <td>1</td>
      <td>15450</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2007-03-22</td>
      <td>21866</td>
      <td>514</td>
      <td>1</td>
      <td>15451</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2007-03-22</td>
      <td>20370</td>
      <td>359</td>
      <td>1</td>
      <td>15453</td>
      <td>1.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2007-03-22</td>
      <td>24882</td>
      <td>238</td>
      <td>1</td>
      <td>15455</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2007-03-22</td>
      <td>25113</td>
      <td>262</td>
      <td>1</td>
      <td>15456</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2007-03-22</td>
      <td>19906</td>
      <td>306</td>
      <td>1</td>
      <td>15457</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2007-03-22</td>
      <td>22876</td>
      <td>20</td>
      <td>1</td>
      <td>15460</td>
      <td>2.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2007-03-22</td>
      <td>23646</td>
      <td>103</td>
      <td>1</td>
      <td>15461</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2007-03-22</td>
      <td>20675</td>
      <td>389</td>
      <td>1</td>
      <td>15462</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2007-03-22</td>
      <td>23869</td>
      <td>127</td>
      <td>1</td>
      <td>15463</td>
      <td>5.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-03-22</td>
      <td>23283</td>
      <td>62</td>
      <td>1</td>
      <td>15464</td>
      <td>6.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2007-03-22</td>
      <td>21921</td>
      <td>520</td>
      <td>1</td>
      <td>15465</td>
      <td>0.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2007-03-22</td>
      <td>20970</td>
      <td>418</td>
      <td>1</td>
      <td>15466</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2007-03-22</td>
      <td>23647</td>
      <td>103</td>
      <td>1</td>
      <td>15467</td>
      <td>3.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-03-22</td>
      <td>20768</td>
      <td>399</td>
      <td>1</td>
      <td>15468</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2007-03-22</td>
      <td>22610</td>
      <td>597</td>
      <td>1</td>
      <td>15469</td>
      <td>4.99</td>
      <td>23</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2007-03-23</td>
      <td>24692</td>
      <td>215</td>
      <td>1</td>
      <td>15583</td>
      <td>2.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2007-03-23</td>
      <td>21731</td>
      <td>500</td>
      <td>1</td>
      <td>15584</td>
      <td>2.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2007-03-23</td>
      <td>22149</td>
      <td>545</td>
      <td>1</td>
      <td>15585</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2007-03-23</td>
      <td>21723</td>
      <td>499</td>
      <td>1</td>
      <td>15587</td>
      <td>7.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2007-03-23</td>
      <td>21764</td>
      <td>503</td>
      <td>1</td>
      <td>15588</td>
      <td>3.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2007-03-23</td>
      <td>22901</td>
      <td>22</td>
      <td>1</td>
      <td>15589</td>
      <td>6.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2007-03-23</td>
      <td>23284</td>
      <td>62</td>
      <td>1</td>
      <td>15591</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2007-03-23</td>
      <td>24163</td>
      <td>153</td>
      <td>1</td>
      <td>15593</td>
      <td>1.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2007-03-23</td>
      <td>25135</td>
      <td>264</td>
      <td>1</td>
      <td>15595</td>
      <td>4.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2007-03-23</td>
      <td>24478</td>
      <td>186</td>
      <td>1</td>
      <td>15596</td>
      <td>0.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2007-03-23</td>
      <td>23323</td>
      <td>66</td>
      <td>1</td>
      <td>15598</td>
      <td>8.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>34</th>
      <td>2007-03-23</td>
      <td>23648</td>
      <td>103</td>
      <td>1</td>
      <td>15599</td>
      <td>5.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>35</th>
      <td>2007-03-23</td>
      <td>23729</td>
      <td>113</td>
      <td>1</td>
      <td>15600</td>
      <td>1.99</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>




```python
all(df==df_sql)
```

    True



#### ▶ R
Once again a similar pipeline can be build in R.


```r
%%R -o df_r

df_r = payment %>% 
  mutate(date=lubridate::date(payment_date)) %>% 
  filter(date >= as.Date('2007-03-01') &  date <= as.Date('2007-03-31')) %>% 
  mutate(hour=lubridate::hour(payment_date)) %>% 
  filter(hour %in% c(4, 23) & rental_id > 15000 & staff_id == 1) %>% 
  arrange(payment_date) %>% 
  select(date, payment_id, customer_id, staff_id, rental_id, amount, hour) %>% 
  as.data.frame()

print(dim(df_r))
df_r
```

    [1] 36  7
             date payment_id customer_id staff_id rental_id amount hour
    1  2007-03-22      23134          46        1     15438   2.99   23
    2  2007-03-22      23958         136        1     15439   4.99   23
    3  2007-03-22      23095          42        1     15442   2.99   23
    4  2007-03-22      22615         598        1     15443   7.99   23
    5  2007-03-22      22960          28        1     15445   4.99   23
    6  2007-03-22      20574         379        1     15446   4.99   23
    7  2007-03-22      21651         490        1     15448   2.99   23
    8  2007-03-22      20027         322        1     15450   0.99   23
    9  2007-03-22      21866         514        1     15451   2.99   23
    10 2007-03-22      20370         359        1     15453   1.99   23
    11 2007-03-22      24882         238        1     15455   0.99   23
    12 2007-03-22      25113         262        1     15456   0.99   23
    13 2007-03-22      19906         306        1     15457   2.99   23
    14 2007-03-22      22876          20        1     15460   2.99   23
    15 2007-03-22      23646         103        1     15461   5.99   23
    16 2007-03-22      20675         389        1     15462   5.99   23
    17 2007-03-22      23869         127        1     15463   5.99   23
    18 2007-03-22      23283          62        1     15464   6.99   23
    19 2007-03-22      21921         520        1     15465   0.99   23
    20 2007-03-22      20970         418        1     15466   4.99   23
    21 2007-03-22      23647         103        1     15467   3.99   23
    22 2007-03-22      20768         399        1     15468   4.99   23
    23 2007-03-22      22610         597        1     15469   4.99   23
    24 2007-03-23      24692         215        1     15583   2.99    4
    25 2007-03-23      21731         500        1     15584   2.99    4
    26 2007-03-23      22149         545        1     15585   0.99    4
    27 2007-03-23      21723         499        1     15587   7.99    4
    28 2007-03-23      21764         503        1     15588   3.99    4
    29 2007-03-23      22901          22        1     15589   6.99    4
    30 2007-03-23      23284          62        1     15591   0.99    4
    31 2007-03-23      24163         153        1     15593   1.99    4
    32 2007-03-23      25135         264        1     15595   4.99    4
    33 2007-03-23      24478         186        1     15596   0.99    4
    34 2007-03-23      23323          66        1     15598   8.99    4
    35 2007-03-23      23648         103        1     15599   5.99    4
    36 2007-03-23      23729         113        1     15600   1.99    4



---

###  Customer lifetime value
Which customers made their first order on a weekend, paid more than \\$5, and have a customer lifetime value (total amount spent) which exceeds \\$100?

#### ▶ SQL
For this query we need to extract the day of the week for each transaction. This can be done using `dow`.

Note that in PostgreSQL Sunday is coded as 0, and Saturday as 6.


```python
q = '''
SELECT t.* FROM (
    SELECT 
        p.*, 
        EXTRACT(dow FROM p.payment_date)::int  dow,
        (
            SELECT SUM(p3.amount) 
            FROM payment p3
            WHERE p3.customer_id = p.customer_id   
        ) as CLV
    FROM 
        payment p
    WHERE 
        p.payment_id = (
            SELECT MIN(p2.payment_id)
            FROM payment p2
            WHERE p.customer_id = p2.customer_id
        ) 
        AND 
            EXTRACT(dow FROM p.payment_date) IN (0, 6)
        AND 
            p.amount > 5     

    GROUP BY 1
)t WHERE t.CLV > 100
ORDER BY t.CLV DESC
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql
```

    (17, 8)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>payment_date</th>
      <th>dow</th>
      <th>clv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>19029</td>
      <td>137</td>
      <td>1</td>
      <td>2469</td>
      <td>6.99</td>
      <td>2007-02-18 18:52:49.996577</td>
      <td>0</td>
      <td>191.62</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18572</td>
      <td>21</td>
      <td>2</td>
      <td>2235</td>
      <td>7.99</td>
      <td>2007-02-18 02:37:16.996577</td>
      <td>0</td>
      <td>146.68</td>
    </tr>
    <tr>
      <th>2</th>
      <td>17526</td>
      <td>346</td>
      <td>1</td>
      <td>1994</td>
      <td>5.99</td>
      <td>2007-02-17 09:35:32.996577</td>
      <td>6</td>
      <td>145.70</td>
    </tr>
    <tr>
      <th>3</th>
      <td>19502</td>
      <td>265</td>
      <td>2</td>
      <td>2027</td>
      <td>7.99</td>
      <td>2007-02-17 11:35:22.996577</td>
      <td>6</td>
      <td>132.72</td>
    </tr>
    <tr>
      <th>4</th>
      <td>17509</td>
      <td>342</td>
      <td>2</td>
      <td>2190</td>
      <td>5.99</td>
      <td>2007-02-17 23:58:17.996577</td>
      <td>6</td>
      <td>130.68</td>
    </tr>
    <tr>
      <th>5</th>
      <td>17866</td>
      <td>436</td>
      <td>1</td>
      <td>2291</td>
      <td>9.99</td>
      <td>2007-02-18 06:05:12.996577</td>
      <td>0</td>
      <td>126.73</td>
    </tr>
    <tr>
      <th>6</th>
      <td>18099</td>
      <td>497</td>
      <td>2</td>
      <td>2180</td>
      <td>8.99</td>
      <td>2007-02-17 23:16:09.996577</td>
      <td>6</td>
      <td>121.73</td>
    </tr>
    <tr>
      <th>7</th>
      <td>18995</td>
      <td>128</td>
      <td>2</td>
      <td>2519</td>
      <td>7.99</td>
      <td>2007-02-18 22:47:47.996577</td>
      <td>0</td>
      <td>118.70</td>
    </tr>
    <tr>
      <th>8</th>
      <td>19496</td>
      <td>263</td>
      <td>2</td>
      <td>2126</td>
      <td>8.99</td>
      <td>2007-02-17 19:23:02.996577</td>
      <td>6</td>
      <td>116.73</td>
    </tr>
    <tr>
      <th>9</th>
      <td>18636</td>
      <td>32</td>
      <td>2</td>
      <td>1887</td>
      <td>6.99</td>
      <td>2007-02-17 02:21:44.996577</td>
      <td>6</td>
      <td>112.74</td>
    </tr>
    <tr>
      <th>10</th>
      <td>19345</td>
      <td>225</td>
      <td>2</td>
      <td>2226</td>
      <td>7.99</td>
      <td>2007-02-18 02:08:22.996577</td>
      <td>0</td>
      <td>111.76</td>
    </tr>
    <tr>
      <th>11</th>
      <td>18395</td>
      <td>579</td>
      <td>2</td>
      <td>2425</td>
      <td>5.99</td>
      <td>2007-02-18 16:06:11.996577</td>
      <td>0</td>
      <td>111.73</td>
    </tr>
    <tr>
      <th>12</th>
      <td>18554</td>
      <td>16</td>
      <td>2</td>
      <td>1934</td>
      <td>6.99</td>
      <td>2007-02-17 05:33:23.996577</td>
      <td>6</td>
      <td>109.75</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18666</td>
      <td>40</td>
      <td>2</td>
      <td>2470</td>
      <td>7.99</td>
      <td>2007-02-18 18:56:57.996577</td>
      <td>0</td>
      <td>105.74</td>
    </tr>
    <tr>
      <th>14</th>
      <td>18446</td>
      <td>593</td>
      <td>2</td>
      <td>2055</td>
      <td>5.99</td>
      <td>2007-02-17 13:55:29.996577</td>
      <td>6</td>
      <td>101.76</td>
    </tr>
    <tr>
      <th>15</th>
      <td>18367</td>
      <td>572</td>
      <td>2</td>
      <td>1889</td>
      <td>10.99</td>
      <td>2007-02-17 02:33:38.996577</td>
      <td>6</td>
      <td>100.76</td>
    </tr>
    <tr>
      <th>16</th>
      <td>19441</td>
      <td>251</td>
      <td>1</td>
      <td>2238</td>
      <td>6.99</td>
      <td>2007-02-18 02:50:32.996577</td>
      <td>0</td>
      <td>100.75</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python
Let's break the pipeline in two parts.
First we compute the subset of customers who placed their first order on a week-end.

Note that unlike PostgreSQL, pandas codes Saturday as 5 and Sunday as 6.


```python
subset_fo = (payment
               .assign(dow=lambda x: x.payment_date.dt.weekday) # extract the day of the week as an integer
               .groupby('customer_id')[['payment_date', 'payment_id', 'amount', 'rental_id', 'staff_id', 'dow']]
               .first()                                         # pick the first row for each group
               .query('(amount > 5) & (dow in [5, 6])')
             )
subset_fo.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_date</th>
      <th>payment_id</th>
      <th>amount</th>
      <th>rental_id</th>
      <th>staff_id</th>
      <th>dow</th>
    </tr>
    <tr>
      <th>customer_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>16</th>
      <td>2007-02-17 05:33:23.996577</td>
      <td>18554</td>
      <td>6.99</td>
      <td>1934</td>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2007-02-17 22:46:24.996577</td>
      <td>18558</td>
      <td>5.99</td>
      <td>2175</td>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2007-02-18 02:37:16.996577</td>
      <td>18572</td>
      <td>7.99</td>
      <td>2235</td>
      <td>2</td>
      <td>6</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2007-02-17 02:21:44.996577</td>
      <td>18636</td>
      <td>6.99</td>
      <td>1887</td>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>40</th>
      <td>2007-02-18 18:56:57.996577</td>
      <td>18666</td>
      <td>7.99</td>
      <td>2470</td>
      <td>2</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



We then join the payment table on this subset to get the information we want.


```python
df = (payment
       .loc[payment.customer_id.isin(subset_fo.index)]
       .groupby('customer_id')[['amount']].sum()
       .rename(columns={'amount':'clv'})
       .query('clv >= 100')
       .join(subset_fo, how='left')
       .sort_values('clv', ascending=False)
       .reset_index()
       .loc[:, df_sql.columns]
    )

print(df.shape)
df
```

    (17, 8)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>payment_id</th>
      <th>customer_id</th>
      <th>staff_id</th>
      <th>rental_id</th>
      <th>amount</th>
      <th>payment_date</th>
      <th>dow</th>
      <th>clv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>19029</td>
      <td>137</td>
      <td>1</td>
      <td>2469</td>
      <td>6.99</td>
      <td>2007-02-18 18:52:49.996577</td>
      <td>6</td>
      <td>191.62</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18572</td>
      <td>21</td>
      <td>2</td>
      <td>2235</td>
      <td>7.99</td>
      <td>2007-02-18 02:37:16.996577</td>
      <td>6</td>
      <td>146.68</td>
    </tr>
    <tr>
      <th>2</th>
      <td>17526</td>
      <td>346</td>
      <td>1</td>
      <td>1994</td>
      <td>5.99</td>
      <td>2007-02-17 09:35:32.996577</td>
      <td>5</td>
      <td>145.70</td>
    </tr>
    <tr>
      <th>3</th>
      <td>19502</td>
      <td>265</td>
      <td>2</td>
      <td>2027</td>
      <td>7.99</td>
      <td>2007-02-17 11:35:22.996577</td>
      <td>5</td>
      <td>132.72</td>
    </tr>
    <tr>
      <th>4</th>
      <td>17509</td>
      <td>342</td>
      <td>2</td>
      <td>2190</td>
      <td>5.99</td>
      <td>2007-02-17 23:58:17.996577</td>
      <td>5</td>
      <td>130.68</td>
    </tr>
    <tr>
      <th>5</th>
      <td>17866</td>
      <td>436</td>
      <td>1</td>
      <td>2291</td>
      <td>9.99</td>
      <td>2007-02-18 06:05:12.996577</td>
      <td>6</td>
      <td>126.73</td>
    </tr>
    <tr>
      <th>6</th>
      <td>18099</td>
      <td>497</td>
      <td>2</td>
      <td>2180</td>
      <td>8.99</td>
      <td>2007-02-17 23:16:09.996577</td>
      <td>5</td>
      <td>121.73</td>
    </tr>
    <tr>
      <th>7</th>
      <td>18995</td>
      <td>128</td>
      <td>2</td>
      <td>2519</td>
      <td>7.99</td>
      <td>2007-02-18 22:47:47.996577</td>
      <td>6</td>
      <td>118.70</td>
    </tr>
    <tr>
      <th>8</th>
      <td>19496</td>
      <td>263</td>
      <td>2</td>
      <td>2126</td>
      <td>8.99</td>
      <td>2007-02-17 19:23:02.996577</td>
      <td>5</td>
      <td>116.73</td>
    </tr>
    <tr>
      <th>9</th>
      <td>18636</td>
      <td>32</td>
      <td>2</td>
      <td>1887</td>
      <td>6.99</td>
      <td>2007-02-17 02:21:44.996577</td>
      <td>5</td>
      <td>112.74</td>
    </tr>
    <tr>
      <th>10</th>
      <td>19345</td>
      <td>225</td>
      <td>2</td>
      <td>2226</td>
      <td>7.99</td>
      <td>2007-02-18 02:08:22.996577</td>
      <td>6</td>
      <td>111.76</td>
    </tr>
    <tr>
      <th>11</th>
      <td>18395</td>
      <td>579</td>
      <td>2</td>
      <td>2425</td>
      <td>5.99</td>
      <td>2007-02-18 16:06:11.996577</td>
      <td>6</td>
      <td>111.73</td>
    </tr>
    <tr>
      <th>12</th>
      <td>18554</td>
      <td>16</td>
      <td>2</td>
      <td>1934</td>
      <td>6.99</td>
      <td>2007-02-17 05:33:23.996577</td>
      <td>5</td>
      <td>109.75</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18666</td>
      <td>40</td>
      <td>2</td>
      <td>2470</td>
      <td>7.99</td>
      <td>2007-02-18 18:56:57.996577</td>
      <td>6</td>
      <td>105.74</td>
    </tr>
    <tr>
      <th>14</th>
      <td>18446</td>
      <td>593</td>
      <td>2</td>
      <td>2055</td>
      <td>5.99</td>
      <td>2007-02-17 13:55:29.996577</td>
      <td>5</td>
      <td>101.76</td>
    </tr>
    <tr>
      <th>15</th>
      <td>18367</td>
      <td>572</td>
      <td>2</td>
      <td>1889</td>
      <td>10.99</td>
      <td>2007-02-17 02:33:38.996577</td>
      <td>5</td>
      <td>100.76</td>
    </tr>
    <tr>
      <th>16</th>
      <td>19441</td>
      <td>251</td>
      <td>1</td>
      <td>2238</td>
      <td>6.99</td>
      <td>2007-02-18 02:50:32.996577</td>
      <td>6</td>
      <td>100.75</td>
    </tr>
  </tbody>
</table>
</div>




```python
all(df==df_sql)
```

    True



#### ▶ R
Let's do the same with R. We'll drop the `payment_date` column at the end so that we can fit all the remaining columns horizontally.

Of course, R (lubridate) uses yet another encoding for the days of the week. Saturday is represented as 7 and Sunday as 1.


```r
%%R

subset_fo = payment %>% 
              group_by(customer_id) %>% 
              mutate(dow=lubridate::wday(payment_date)) %>% 
              filter(row_number()==1 & dow%in% c(1, 7) & amount>5) 

df_r = payment %>% 
        right_join(subset_fo, by="customer_id") %>% 
        group_by(customer_id) %>% 
        summarise(clv=sum(amount.x)) %>% 
        filter(clv > 100) %>% 
        left_join(subset_fo, by='customer_id') %>% 
        select(payment_id, customer_id, staff_id, rental_id, amount, payment_date, dow, clv) %>% 
        arrange(desc(clv)) %>%
        select(-payment_date)

print(dim(df_r))
as.data.frame(df_r)
```

    [1] 17  7
       payment_id customer_id staff_id rental_id amount dow    clv
    1       19029         137        1      2469   6.99   1 191.62
    2       18572          21        2      2235   7.99   1 146.68
    3       17526         346        1      1994   5.99   7 145.70
    4       19502         265        2      2027   7.99   7 132.72
    5       17509         342        2      2190   5.99   7 130.68
    6       17866         436        1      2291   9.99   1 126.73
    7       18099         497        2      2180   8.99   7 121.73
    8       18995         128        2      2519   7.99   1 118.70
    9       19496         263        2      2126   8.99   7 116.73
    10      18636          32        2      1887   6.99   7 112.74
    11      19345         225        2      2226   7.99   1 111.76
    12      18395         579        2      2425   5.99   1 111.73
    13      18554          16        2      1934   6.99   7 109.75
    14      18666          40        2      2470   7.99   1 105.74
    15      18446         593        2      2055   5.99   7 101.76
    16      18367         572        2      1889  10.99   7 100.76
    17      19441         251        1      2238   6.99   1 100.75



---

### How many movies have a replacement cost above or below the average replacement cost?

Once way to answer this is to compute how many movies have a replacement cost higher than the average, how many
have a replacement cost lower or equal to the average, and take the union of the two.

#### ▶ SQL


```python
q = '''
SELECT t.grouping, COUNT(*) FROM (
    SELECT f.*, 'above' as grouping
    FROM film f
    WHERE f.replacement_cost > (SELECT AVG(f2.replacement_cost) FROM film f2) 

    UNION 

    SELECT f.*, 'below_eq' as grouping
    FROM film f
    WHERE f.replacement_cost <= (SELECT AVG(f2.replacement_cost) FROM film f2) 
    )t 
GROUP BY 1
'''
```

```python
df_sql = pd.read_sql_query(q, con)
print(df_sql.shape)
df_sql.head()
```

    (2, 2)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>grouping</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>below_eq</td>
      <td>464</td>
    </tr>
    <tr>
      <th>1</th>
      <td>above</td>
      <td>536</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python

The Python syntax is definitely simpler here because we can create a Boolean mask telling us whether the replacement cost is above average, and then use `value_counts` to tally up the `True` and `False` counts.


```python
(film
  .assign(above=film.replacement_cost > film.replacement_cost.mean())
  .loc[:, 'above']
  .value_counts()
  .rename(index={True: 'above', False: 'below_eq'})
)
```

    above       536
    below_eq    464
    Name: above, dtype: int64



#### ▶  R
The R code is similar to the Python one.


```r
%%R
film %>% 
  mutate(above=replacement_cost>mean(film$replacement_cost)) %>% 
  count(above) %>% 
  mutate(above=if_else(above, 'above', 'below_eq'))
```

    # A tibble: 2 x 2
      above        n
      <chr>    <int>
    1 below_eq   464
    2 above      536



----

### Which movie generated the more revenue, for each viewer rating category?

#### ▶ SQL
The grouping by rating part is straightforward, however, we want the _top performing movie_ within each group.
We can use a window function (the `PARTITION BY` part) to do this.


```python
q = '''
WITH some_table AS (
    SELECT 
        f.film_id, 
        f.title, 
        f.rating, 
        SUM(p.amount),
        ROW_NUMBER() OVER(PARTITION BY f.rating ORDER BY SUM(p.amount) DESC)

    FROM film f
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON r.inventory_id = i.inventory_id
    JOIN payment p ON p.rental_id = r.rental_id
    GROUP BY 1, 2, 3
    ORDER BY 3) 
    
SELECT st.* FROM some_table st 
WHERE st.row_number = 1
ORDER BY 4 DESC
'''
```

```python
df_sql = pd.read_sql_query(q, con)
df_sql
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>rating</th>
      <th>sum</th>
      <th>row_number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>879</td>
      <td>Telegraph Voyage</td>
      <td>PG</td>
      <td>215.75</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1000</td>
      <td>Zorro Ark</td>
      <td>NC-17</td>
      <td>199.72</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>460</td>
      <td>Innocent Usual</td>
      <td>PG-13</td>
      <td>191.74</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>764</td>
      <td>Saturday Lambs</td>
      <td>G</td>
      <td>190.74</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>938</td>
      <td>Velvet Terminator</td>
      <td>R</td>
      <td>152.77</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ Python

The pattern below is a common one. We group by some features to compute an aggregate measure, and then ungroup (`reset_index`) to group the data again at a different level of granularity.


```python
df = (film
       .merge(inventory, on='film_id', how='left')    
       .merge(rental, on='inventory_id', how='left')
       .merge(payment, on='rental_id', how='left')
       .groupby(['rating','film_id'])[['amount']]
       .sum()
       .sort_values('amount', ascending=False)
       .rename(columns={'amount': 'sum'})
       .reset_index()
       .groupby('rating')
       .first()
       .merge(film, on='film_id', how='left')
       .sort_values('sum', ascending=False)
       .reset_index()
       .loc[:, ['film_id','title','rating','sum']]
      )

df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>rating</th>
      <th>sum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>879</td>
      <td>Telegraph Voyage</td>
      <td>PG</td>
      <td>215.75</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1000</td>
      <td>Zorro Ark</td>
      <td>NC-17</td>
      <td>199.72</td>
    </tr>
    <tr>
      <th>2</th>
      <td>460</td>
      <td>Innocent Usual</td>
      <td>PG-13</td>
      <td>191.74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>764</td>
      <td>Saturday Lambs</td>
      <td>G</td>
      <td>190.74</td>
    </tr>
    <tr>
      <th>4</th>
      <td>938</td>
      <td>Velvet Terminator</td>
      <td>R</td>
      <td>152.77</td>
    </tr>
  </tbody>
</table>
</div>



#### ▶ R
This the same approach as in Python.


```r
%%R
df_r = film %>% 
  left_join(inventory, by='film_id') %>% 
  left_join(rental, by='inventory_id') %>% 
  left_join(payment, by='rental_id') %>% 
  group_by(rating, film_id) %>% 
  summarise(sum=sum(amount, na.rm=TRUE)) %>% 
  ungroup() %>% 
  arrange(desc(sum)) %>% 
  group_by(rating) %>% 
  filter(row_number()==1) %>% 
  left_join(film, by='film_id') %>% 
  select(film_id, title, rating.x, sum) 

as.data.frame(df_r)
```

      film_id             title rating.x    sum
    1     879  Telegraph Voyage       PG 215.75
    2    1000         Zorro Ark    NC-17 199.72
    3     460    Innocent Usual    PG-13 191.74
    4     764    Saturday Lambs        G 190.74
    5     938 Velvet Terminator        R 152.77



To be continued...
