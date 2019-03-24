---
date : 2018-11-15
slug : pandas_groupby
mathjax : ture
title : Pandas (Blood)groupby
author : Adel Rahmani
categories: 
  - Python
  - blogging
tags: 
  - python
  - pandas
  - groupby
  - data wrangling
summary : An introduction to groupby operations in pandas
thumbnailImagePosition : left
thumbnailImage : ./static/img/avatar-icon.png
---


```python
from math import *
import numpy as np
import pandas as pd
from pathlib import Path

%matplotlib inline
import matplotlib.pyplot as plt

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
```

<style>.container { width:100% !important; }</style>


## 1. Pandas GroupBy

To illustrate how the pandas <code>groupby</code> operation works let's use some fake data. With `numpy` it's trivial to generate random numerical data, however, it's usually a lot more tedious to generate random people data that looks realistic.

A very useful tool for this is the [Fake Name Generator](http://www.fakenamegenerator.com/). That's what I used to generate 
this dataset. 

Let's load the dataset into a dataframe.


```python
input_path = Path('data/people.csv')

data = pd.read_csv(input_path, encoding='utf-8')
```

```python
data.head()
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
      <th>GivenName</th>
      <th>Surname</th>
      <th>Gender</th>
      <th>StreetAddress</th>
      <th>City</th>
      <th>Country</th>
      <th>Birthday</th>
      <th>BloodType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stepanida</td>
      <td>Sukhorukova</td>
      <td>female</td>
      <td>62 Ockham Road</td>
      <td>EASTER WHYNTIE</td>
      <td>United Kingdom</td>
      <td>8/25/1968</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Hiệu</td>
      <td>Lương</td>
      <td>male</td>
      <td>4 Iolaire Road</td>
      <td>NEW CROSS</td>
      <td>United Kingdom</td>
      <td>1/31/1962</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Petra</td>
      <td>Neudorf</td>
      <td>female</td>
      <td>56 Victoria Road</td>
      <td>LISTON</td>
      <td>United Kingdom</td>
      <td>1/10/1964</td>
      <td>B+</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Eho</td>
      <td>Amano</td>
      <td>female</td>
      <td>83 Stroud Rd</td>
      <td>OGMORE</td>
      <td>United Kingdom</td>
      <td>4/12/1933</td>
      <td>O-</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Noah</td>
      <td>Niland</td>
      <td>male</td>
      <td>61 Wrexham Rd</td>
      <td>FACEBY</td>
      <td>United Kingdom</td>
      <td>11/20/1946</td>
      <td>A+</td>
    </tr>
  </tbody>
</table>
</div>



The data contains information about fictitious people.


```python
data.count()
```

    GivenName        5000
    Surname          5000
    Gender           5000
    StreetAddress    5000
    City             5000
    Country          5000
    Birthday         5000
    BloodType        5000
    dtype: int64



<div style="background-color:#F7F2E0;">
<h4> <font color=MediumVioletRed>Remark:</font> </h4>
<p>We've got different types of variables here. For instance, <code>Gender</code> is a categorical variable, so are <code>BloodType</code> and <code>Country</code>. </p>
<p><code>Birthday</code> can be thought of as an interval variable, although we'll convert it to an <code>Age</code> variable, which is more convenient for our purpose, and will be treated as a continuous numeric variable. </p>
<p>Notice, however, that by default pandas will identify non-numeric data as a generic object, which is not the most efficient way of handling categorical data. Let's fix that.</p>
</div>


```python
data.dtypes
```

    GivenName        object
    Surname          object
    Gender           object
    StreetAddress    object
    City             object
    Country          object
    Birthday         object
    BloodType        object
    dtype: object




```python
data['Gender']  = data['Gender'].astype('category')
data['Country'] = data['Country'].astype('category')
data['BloodType']  = data['BloodType'].astype('category')
data.dtypes
```

    GivenName          object
    Surname            object
    Gender           category
    StreetAddress      object
    City               object
    Country          category
    Birthday           object
    BloodType        category
    dtype: object



<h3> <center><font color=MediumVioletRed>A. Dealing with dates.</font></center></h3>

<h4>Method 1 - <code>datetime</code> module.</h4>

One of the features (columns) in our dataset is <code>Birthday</code>. While this information may be useful if you wanted to
find out, for instance, how many people share a birthday, most of the time we mainly care about their age.

One way to convert the <code>Birthday</code> into an <code>Age</code> feature would be to extract the year and compute the current year minus
the birthday year. The <code>split</code> method of string objects could be used for that, however, there's a more elegant, and general
way of handling dates in Python using the <a href="https://pymotw.com/3/datetime/"><code>datetime.strptime</code> function</a>.


<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>This isn't necessarily the fastest, or best way to handle date and time objects in <code>pandas</code>. </p>
</div>


```python
from datetime import datetime

t1 = datetime.strptime("21/01/2019", "%d/%m/%Y")
print(t1.year)
print(datetime.today()-t1)
```

    2019
    62 days, 20:14:58.495945


The `datetime` module allows you to manipulate date objects and perform basic __operations on dates__. It also allows you to 
format dates in a consistent way.

We can apply this to our `Birthday` feature.


```python
data.Birthday[0], data.Birthday[1]
```

    ('8/25/1968', '1/31/1962')




```python
datetime.strptime(data.Birthday[0],"%m/%d/%Y")
```

    datetime.datetime(1968, 8, 25, 0, 0)




```python
datetime.strptime(data.Birthday[1],"%m/%d/%Y")
```

    datetime.datetime(1962, 1, 31, 0, 0)



#### Let's use the Pandas `apply` method to format the dates in a consistent way


```python
data.Birthday = data.apply(lambda row: datetime.strptime(row['Birthday'], "%m/%d/%Y"), axis='columns')
```

```python
data.Birthday.head()
```

    0   1968-08-25
    1   1962-01-31
    2   1964-01-10
    3   1933-04-12
    4   1946-11-20
    Name: Birthday, dtype: datetime64[ns]



<h4>Method 2 - using the <code>to_datetime</code> method of pandas.</h4>


```python
original_data = pd.read_csv(input_path, encoding='utf-8')
original_data.Birthday = pd.to_datetime(original_data.Birthday)
original_data.Birthday.head()
```

    0   1968-08-25
    1   1962-01-31
    2   1964-01-10
    3   1933-04-12
    4   1946-11-20
    Name: Birthday, dtype: datetime64[ns]



<h4>Method 3 - convert at reading time.</h4>


```python
original_data = pd.read_csv(input_path, encoding='utf-8', parse_dates=['Birthday'])
original_data.Birthday.head()
```

    0   1968-08-25
    1   1962-01-31
    2   1964-01-10
    3   1933-04-12
    4   1946-11-20
    Name: Birthday, dtype: datetime64[ns]



<h4>We can now define an <code>Age</code> feature by subtracting the year of birth from the current year.</h4> 

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>Because we are not hard-coding (typing by hand) the current date, if we come back to this code in a year's time and run it again,
    the <code>Age</code> will be updated automatically. </p>
</div>

#### We could compute the age using <code>apply</code> to iterate through the rows of the dataframe...


```python
data.apply(lambda row: datetime.now().year - row['Birthday'].year, axis='columns').head()
```

    0    51
    1    57
    2    55
    3    86
    4    73
    dtype: int64



<h4>However, it is usually faster to operate on the whole dataframe at one.</h4>

<p>Datetime methods on a pandas series (such as a column of a dataframe), can be accessed via the <code>dt</code> method.</p>



```python
(datetime.now().year - data.Birthday.dt.year).head()
```

    0    51
    1    57
    2    55
    3    86
    4    73
    Name: Birthday, dtype: int64




```python
data['Age'] = datetime.now().year - data.Birthday.dt.year
```

```python
data.head()
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
      <th>GivenName</th>
      <th>Surname</th>
      <th>Gender</th>
      <th>StreetAddress</th>
      <th>City</th>
      <th>Country</th>
      <th>Birthday</th>
      <th>BloodType</th>
      <th>Age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stepanida</td>
      <td>Sukhorukova</td>
      <td>female</td>
      <td>62 Ockham Road</td>
      <td>EASTER WHYNTIE</td>
      <td>United Kingdom</td>
      <td>1968-08-25</td>
      <td>A+</td>
      <td>51</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Hiệu</td>
      <td>Lương</td>
      <td>male</td>
      <td>4 Iolaire Road</td>
      <td>NEW CROSS</td>
      <td>United Kingdom</td>
      <td>1962-01-31</td>
      <td>A+</td>
      <td>57</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Petra</td>
      <td>Neudorf</td>
      <td>female</td>
      <td>56 Victoria Road</td>
      <td>LISTON</td>
      <td>United Kingdom</td>
      <td>1964-01-10</td>
      <td>B+</td>
      <td>55</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Eho</td>
      <td>Amano</td>
      <td>female</td>
      <td>83 Stroud Rd</td>
      <td>OGMORE</td>
      <td>United Kingdom</td>
      <td>1933-04-12</td>
      <td>O-</td>
      <td>86</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Noah</td>
      <td>Niland</td>
      <td>male</td>
      <td>61 Wrexham Rd</td>
      <td>FACEBY</td>
      <td>United Kingdom</td>
      <td>1946-11-20</td>
      <td>A+</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>



<h3> <center><font color=MediumVioletRed>B. GroupBy feature.</font></center></h3>

Given the data, common questions to answer would be how certain features are distributed in each
country, or for each gender. 

These could be as simple as __What is the average age in each country?__
to much more complex questions such as __How many people of each blood type are there in each country, for 
each gender, for a given age group?__

Fortunately, Pandas' `GroupBy` method allows us to organise the data in ways only limited by our sagacity.


<h4> Let's look at the country distribution first.  </h4>


```python
data.Country.value_counts()
```

    Australia         1800
    Italy              800
    United States      700
    United Kingdom     500
    New Zealand        500
    France             500
    Iceland            200
    Name: Country, dtype: int64




```python
data.Country.value_counts(ascending=True).plot(kind='barh', color='g', alpha=0.5);
```

![png](output_31_0.png)


#### The `groupby` method creates a `GroupBy` object.
The `groupby` object is a recipe for how to perform operation on the data.

To use a `groupby` object, we need to perform some operation on it.


```python
grouped_by_country = data.groupby('Country')
grouped_by_country
```

    <pandas.core.groupby.generic.DataFrameGroupBy object at 0x106ca5710>




```python
grouped_by_country.size()
```

    Country
    Australia         1800
    France             500
    Iceland            200
    Italy              800
    New Zealand        500
    United Kingdom     500
    United States      700
    dtype: int64




```python
grouped_by_country.ngroups
```

    7




```python
for group in grouped_by_country.groups:
    print(group)
```

    Australia
    France
    Iceland
    Italy
    New Zealand
    United Kingdom
    United States



```python
grouped_by_country['Age'].mean()
```

    Country
    Australia         57.817778
    France            57.944000
    Iceland           57.660000
    Italy             56.607500
    New Zealand       56.630000
    United Kingdom    57.740000
    United States     57.415714
    Name: Age, dtype: float64



<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>Recall that the <code>apply</code> method allows you to apply an <b>arbitrary function</b> to all the rows in your dataframe. Therefore, as long as you can express your operations as a function (lambda or otherwise), you can include it in the <code>apply</code>, <b>even if your function returns multiple values</b>, provided you wrap them in a tuple.</p>
</div>


```python
grouped_by_country['Age'].apply(lambda x: (np.min(x), 
                                           f'{x.mean():0.2f}', 
                                           np.max(x), 
                                           f'{x.std():0.2f}')
                                )
```

    Country
    Australia         (24, 57.82, 91, 19.49)
    France            (24, 57.94, 91, 19.54)
    Iceland           (24, 57.66, 91, 19.46)
    Italy             (24, 56.61, 91, 18.98)
    New Zealand       (24, 56.63, 91, 19.05)
    United Kingdom    (24, 57.74, 91, 19.53)
    United States     (24, 57.42, 91, 19.29)
    Name: Age, dtype: object



#### A different and nicer output can be obtained using the `agg` method on a groupby object.


```python
grouped_by_country['Age'].agg(['min','mean','max','std'])
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
      <th>min</th>
      <th>mean</th>
      <th>max</th>
      <th>std</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <td>24</td>
      <td>57.817778</td>
      <td>91</td>
      <td>19.488031</td>
    </tr>
    <tr>
      <th>France</th>
      <td>24</td>
      <td>57.944000</td>
      <td>91</td>
      <td>19.541869</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>24</td>
      <td>57.660000</td>
      <td>91</td>
      <td>19.461194</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>24</td>
      <td>56.607500</td>
      <td>91</td>
      <td>18.981275</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>24</td>
      <td>56.630000</td>
      <td>91</td>
      <td>19.049905</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>24</td>
      <td>57.740000</td>
      <td>91</td>
      <td>19.527905</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>24</td>
      <td>57.415714</td>
      <td>91</td>
      <td>19.285003</td>
    </tr>
  </tbody>
</table>
</div>



#### For categorical variables, such as `BloodType`, basic information can be extracted using the `describe` method.


```python
grouped_by_country['BloodType'].describe()
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
      <th>count</th>
      <th>unique</th>
      <th>top</th>
      <th>freq</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <td>1800</td>
      <td>8</td>
      <td>O+</td>
      <td>648</td>
    </tr>
    <tr>
      <th>France</th>
      <td>500</td>
      <td>8</td>
      <td>O+</td>
      <td>184</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>200</td>
      <td>7</td>
      <td>O+</td>
      <td>86</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>800</td>
      <td>8</td>
      <td>O+</td>
      <td>299</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>500</td>
      <td>8</td>
      <td>O+</td>
      <td>185</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>500</td>
      <td>8</td>
      <td>O+</td>
      <td>188</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>700</td>
      <td>8</td>
      <td>O+</td>
      <td>273</td>
    </tr>
  </tbody>
</table>
</div>




```python
grouped_by_country['GivenName'].describe()
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
      <th>count</th>
      <th>unique</th>
      <th>top</th>
      <th>freq</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <td>1800</td>
      <td>1368</td>
      <td>Michael</td>
      <td>9</td>
    </tr>
    <tr>
      <th>France</th>
      <td>500</td>
      <td>444</td>
      <td>Anna</td>
      <td>4</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>200</td>
      <td>193</td>
      <td>Dieter</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>800</td>
      <td>677</td>
      <td>Jennifer</td>
      <td>6</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>500</td>
      <td>447</td>
      <td>James</td>
      <td>4</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>500</td>
      <td>450</td>
      <td>Ellis</td>
      <td>3</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>700</td>
      <td>620</td>
      <td>Lily</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



`describe` only tells us about the most frequent blood type. To get a count of the boodtypes let us use a `Counter` object.

<div style="background-color:#FBEFFB;">
<h4>Which item appears most frequently?</h4>

Counting the number of objects of a given type is such a common operation that Python has a very useful <code>Counter</code> object
from the <code>collections</code> module. 

What a <code>Counter</code> object does to a sequence of items is group the elements of the sequence into bins according to their value, and count how many element each bin has. A <code>Counter</code> object also had several useful properties, for instance, to determine the most common object in the sequence.
</div>


```python
from collections import Counter

L = ['a', 'b', 'c', 'a', 'a', 'c', 'b', 'b', 'b', 'b']
c = Counter(L)
c
```

    Counter({'a': 3, 'b': 5, 'c': 2})




```python
print(c.most_common())
print(c.most_common(2))
print(c.most_common(1))
```

    [('b', 5), ('a', 3), ('c', 2)]
    [('b', 5), ('a', 3)]
    [('b', 5)]



```python
grouped_by_country['BloodType'].apply(Counter)
```

    Country            
    Australia       A+     468.0
                    A-      59.0
                    AB+    100.0
                    AB-      8.0
                    B+     419.0
                    B-      24.0
                    O+     648.0
                    O-      74.0
    France          A+     145.0
                    A-      17.0
                    AB+     19.0
                    AB-      1.0
                    B+     106.0
                    B-       4.0
                    O+     184.0
                    O-      24.0
    Iceland         A+      45.0
                    A-       6.0
                    AB+      5.0
                    B+      44.0
                    B-       5.0
                    O+      86.0
                    O-       9.0
    Italy           A+     207.0
                    A-      31.0
                    AB+     37.0
                    AB-      5.0
                    B+     185.0
                    B-       4.0
                    O+     299.0
                    O-      32.0
    New Zealand     A+     154.0
                    A-       9.0
                    AB+     21.0
                    AB-      5.0
                    B+     100.0
                    B-       5.0
                    O+     185.0
                    O-      21.0
    United Kingdom  A+     132.0
                    A-      23.0
                    AB+     25.0
                    AB-      4.0
                    B+     102.0
                    B-       7.0
                    O+     188.0
                    O-      19.0
    United States   A+     157.0
                    A-      25.0
                    AB+     35.0
                    AB-      4.0
                    B+     157.0
                    B-      15.0
                    O+     273.0
                    O-      34.0
    Name: BloodType, dtype: float64



<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>Note how the result is one long column of information. This result is actually a Pandas <code>Series</code> object (recall that a <code>Series</code> object is essentially an array with an index).</p>

<p>It may look a bit like a dataframe, but remember that in a dataframe each column corresponds to a <b>unique</b> feature. Here, what looks like the second column is actually a second level for the index. We'll talk about multi-index shortly.  </p>
<p>The result as it stands may not be the easiest to read. It would be better if we could transform it back into a dataframe so
that we could compare the results for two countries more easily. In Pandas, you can do that with one command: <code>unstack</code>.
</p>
</div>


```python
grouped_by_country['BloodType'].apply(Counter).unstack()
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
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>468.0</td>
      <td>59.0</td>
      <td>100.0</td>
      <td>8.0</td>
      <td>419.0</td>
      <td>24.0</td>
      <td>648.0</td>
      <td>74.0</td>
    </tr>
    <tr>
      <th>France</th>
      <td>145.0</td>
      <td>17.0</td>
      <td>19.0</td>
      <td>1.0</td>
      <td>106.0</td>
      <td>4.0</td>
      <td>184.0</td>
      <td>24.0</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>45.0</td>
      <td>6.0</td>
      <td>5.0</td>
      <td>NaN</td>
      <td>44.0</td>
      <td>5.0</td>
      <td>86.0</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>207.0</td>
      <td>31.0</td>
      <td>37.0</td>
      <td>5.0</td>
      <td>185.0</td>
      <td>4.0</td>
      <td>299.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>154.0</td>
      <td>9.0</td>
      <td>21.0</td>
      <td>5.0</td>
      <td>100.0</td>
      <td>5.0</td>
      <td>185.0</td>
      <td>21.0</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>132.0</td>
      <td>23.0</td>
      <td>25.0</td>
      <td>4.0</td>
      <td>102.0</td>
      <td>7.0</td>
      <td>188.0</td>
      <td>19.0</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>157.0</td>
      <td>25.0</td>
      <td>35.0</td>
      <td>4.0</td>
      <td>157.0</td>
      <td>15.0</td>
      <td>273.0</td>
      <td>34.0</td>
    </tr>
  </tbody>
</table>
</div>



If we want to switch the index and the columns around, we need to specify the `level` parameter in  `unstack()` which, by default, is -1, that is the last (innermost) level of the index.


```python
grouped_by_country['BloodType'].apply(Counter).unstack(level=0)
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
      <th>Country</th>
      <th>Australia</th>
      <th>France</th>
      <th>Iceland</th>
      <th>Italy</th>
      <th>New Zealand</th>
      <th>United Kingdom</th>
      <th>United States</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A+</th>
      <td>468.0</td>
      <td>145.0</td>
      <td>45.0</td>
      <td>207.0</td>
      <td>154.0</td>
      <td>132.0</td>
      <td>157.0</td>
    </tr>
    <tr>
      <th>A-</th>
      <td>59.0</td>
      <td>17.0</td>
      <td>6.0</td>
      <td>31.0</td>
      <td>9.0</td>
      <td>23.0</td>
      <td>25.0</td>
    </tr>
    <tr>
      <th>AB+</th>
      <td>100.0</td>
      <td>19.0</td>
      <td>5.0</td>
      <td>37.0</td>
      <td>21.0</td>
      <td>25.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>AB-</th>
      <td>8.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>B+</th>
      <td>419.0</td>
      <td>106.0</td>
      <td>44.0</td>
      <td>185.0</td>
      <td>100.0</td>
      <td>102.0</td>
      <td>157.0</td>
    </tr>
    <tr>
      <th>B-</th>
      <td>24.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>7.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>O+</th>
      <td>648.0</td>
      <td>184.0</td>
      <td>86.0</td>
      <td>299.0</td>
      <td>185.0</td>
      <td>188.0</td>
      <td>273.0</td>
    </tr>
    <tr>
      <th>O-</th>
      <td>74.0</td>
      <td>24.0</td>
      <td>9.0</td>
      <td>32.0</td>
      <td>21.0</td>
      <td>19.0</td>
      <td>34.0</td>
    </tr>
  </tbody>
</table>
</div>



#### The level can also be specified by name


```python
grouped_by_country['BloodType'].apply(Counter).unstack(level='Country')
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
      <th>Country</th>
      <th>Australia</th>
      <th>France</th>
      <th>Iceland</th>
      <th>Italy</th>
      <th>New Zealand</th>
      <th>United Kingdom</th>
      <th>United States</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A+</th>
      <td>468.0</td>
      <td>145.0</td>
      <td>45.0</td>
      <td>207.0</td>
      <td>154.0</td>
      <td>132.0</td>
      <td>157.0</td>
    </tr>
    <tr>
      <th>A-</th>
      <td>59.0</td>
      <td>17.0</td>
      <td>6.0</td>
      <td>31.0</td>
      <td>9.0</td>
      <td>23.0</td>
      <td>25.0</td>
    </tr>
    <tr>
      <th>AB+</th>
      <td>100.0</td>
      <td>19.0</td>
      <td>5.0</td>
      <td>37.0</td>
      <td>21.0</td>
      <td>25.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>AB-</th>
      <td>8.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>B+</th>
      <td>419.0</td>
      <td>106.0</td>
      <td>44.0</td>
      <td>185.0</td>
      <td>100.0</td>
      <td>102.0</td>
      <td>157.0</td>
    </tr>
    <tr>
      <th>B-</th>
      <td>24.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>7.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>O+</th>
      <td>648.0</td>
      <td>184.0</td>
      <td>86.0</td>
      <td>299.0</td>
      <td>185.0</td>
      <td>188.0</td>
      <td>273.0</td>
    </tr>
    <tr>
      <th>O-</th>
      <td>74.0</td>
      <td>24.0</td>
      <td>9.0</td>
      <td>32.0</td>
      <td>21.0</td>
      <td>19.0</td>
      <td>34.0</td>
    </tr>
  </tbody>
</table>
</div>



Note that we have a  bunch of `NaN` in our dataframe. This indicates that no one from Iceland has blood type `AB+` in our dataset.

Since there was no such data in our dataset, it appears as a __missing value__.

However, here, a value of 0 would be more appropriate. We can tell the dataframe to
replace its missing values by 0 using the `fillna` method.

Since we're dealing with count data, it's also a good idea to convert the type to <code>int</code>.


```python
grouped_by_country['BloodType'].apply(Counter).unstack().fillna(0).astype(int)
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
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>468</td>
      <td>59</td>
      <td>100</td>
      <td>8</td>
      <td>419</td>
      <td>24</td>
      <td>648</td>
      <td>74</td>
    </tr>
    <tr>
      <th>France</th>
      <td>145</td>
      <td>17</td>
      <td>19</td>
      <td>1</td>
      <td>106</td>
      <td>4</td>
      <td>184</td>
      <td>24</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>45</td>
      <td>6</td>
      <td>5</td>
      <td>0</td>
      <td>44</td>
      <td>5</td>
      <td>86</td>
      <td>9</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>207</td>
      <td>31</td>
      <td>37</td>
      <td>5</td>
      <td>185</td>
      <td>4</td>
      <td>299</td>
      <td>32</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>154</td>
      <td>9</td>
      <td>21</td>
      <td>5</td>
      <td>100</td>
      <td>5</td>
      <td>185</td>
      <td>21</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>132</td>
      <td>23</td>
      <td>25</td>
      <td>4</td>
      <td>102</td>
      <td>7</td>
      <td>188</td>
      <td>19</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>157</td>
      <td>25</td>
      <td>35</td>
      <td>4</td>
      <td>157</td>
      <td>15</td>
      <td>273</td>
      <td>34</td>
    </tr>
  </tbody>
</table>
</div>



<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>We are using <b>fake data</b> so don't give too much credence to these results. </p>

<p>This being said,  blood type frequencies do vary
across countries and you can read more about it <a href="http://en.wikipedia.org/wiki/Blood_type_distribution_by_country">here</a>.
</p>
</div>

<h3> <center><font color=MediumVioletRed>C. GroupBy on multiple features.</font></center></h3>

Of, course, <code>GroupBy</code> operations aren't limited to single features.

If we want to see the data grouped by country <b>and</b> blood type , we just need to specify both features in constructing the <code>GroupBy</code> object.
<h4>Note that with a <code>groupby</code> on multiple features we can obtain the previous result in a different way.</h4>


```python
data.groupby(['Country','BloodType']).count().iloc[:, 0].unstack().fillna(0).astype(int)
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>468</td>
      <td>59</td>
      <td>100</td>
      <td>8</td>
      <td>419</td>
      <td>24</td>
      <td>648</td>
      <td>74</td>
    </tr>
    <tr>
      <th>France</th>
      <td>145</td>
      <td>17</td>
      <td>19</td>
      <td>1</td>
      <td>106</td>
      <td>4</td>
      <td>184</td>
      <td>24</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>45</td>
      <td>6</td>
      <td>5</td>
      <td>0</td>
      <td>44</td>
      <td>5</td>
      <td>86</td>
      <td>9</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>207</td>
      <td>31</td>
      <td>37</td>
      <td>5</td>
      <td>185</td>
      <td>4</td>
      <td>299</td>
      <td>32</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>154</td>
      <td>9</td>
      <td>21</td>
      <td>5</td>
      <td>100</td>
      <td>5</td>
      <td>185</td>
      <td>21</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>132</td>
      <td>23</td>
      <td>25</td>
      <td>4</td>
      <td>102</td>
      <td>7</td>
      <td>188</td>
      <td>19</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>157</td>
      <td>25</td>
      <td>35</td>
      <td>4</td>
      <td>157</td>
      <td>15</td>
      <td>273</td>
      <td>34</td>
    </tr>
  </tbody>
</table>
</div>



#### Let's group our data based on country and gender.


```python
grouped_by_country_and_gender = data.groupby(['Country', 'Gender'])

grouped_by_country_and_gender['BloodType'].apply(Counter).unstack()
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
      <th></th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>229.0</td>
      <td>29.0</td>
      <td>54.0</td>
      <td>4.0</td>
      <td>205.0</td>
      <td>13.0</td>
      <td>328.0</td>
      <td>41.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>239.0</td>
      <td>30.0</td>
      <td>46.0</td>
      <td>4.0</td>
      <td>214.0</td>
      <td>11.0</td>
      <td>320.0</td>
      <td>33.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>76.0</td>
      <td>11.0</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>47.0</td>
      <td>2.0</td>
      <td>79.0</td>
      <td>16.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69.0</td>
      <td>6.0</td>
      <td>9.0</td>
      <td>1.0</td>
      <td>59.0</td>
      <td>2.0</td>
      <td>105.0</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>22.0</td>
      <td>5.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>17.0</td>
      <td>4.0</td>
      <td>34.0</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>23.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>NaN</td>
      <td>27.0</td>
      <td>1.0</td>
      <td>52.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>102.0</td>
      <td>14.0</td>
      <td>22.0</td>
      <td>1.0</td>
      <td>89.0</td>
      <td>1.0</td>
      <td>160.0</td>
      <td>17.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>105.0</td>
      <td>17.0</td>
      <td>15.0</td>
      <td>4.0</td>
      <td>96.0</td>
      <td>3.0</td>
      <td>139.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>75.0</td>
      <td>5.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>53.0</td>
      <td>2.0</td>
      <td>91.0</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>79.0</td>
      <td>4.0</td>
      <td>13.0</td>
      <td>4.0</td>
      <td>47.0</td>
      <td>3.0</td>
      <td>94.0</td>
      <td>12.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>65.0</td>
      <td>6.0</td>
      <td>14.0</td>
      <td>1.0</td>
      <td>55.0</td>
      <td>4.0</td>
      <td>99.0</td>
      <td>13.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>67.0</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>3.0</td>
      <td>47.0</td>
      <td>3.0</td>
      <td>89.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>89.0</td>
      <td>13.0</td>
      <td>18.0</td>
      <td>3.0</td>
      <td>77.0</td>
      <td>7.0</td>
      <td>138.0</td>
      <td>12.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>68.0</td>
      <td>12.0</td>
      <td>17.0</td>
      <td>1.0</td>
      <td>80.0</td>
      <td>8.0</td>
      <td>135.0</td>
      <td>22.0</td>
    </tr>
  </tbody>
</table>
</div>



Once again let's replace missing values by 0.


```python
grouped_by_country_and_gender['BloodType'].apply(Counter).unstack().fillna(0).astype(int)
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
      <th></th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>229</td>
      <td>29</td>
      <td>54</td>
      <td>4</td>
      <td>205</td>
      <td>13</td>
      <td>328</td>
      <td>41</td>
    </tr>
    <tr>
      <th>male</th>
      <td>239</td>
      <td>30</td>
      <td>46</td>
      <td>4</td>
      <td>214</td>
      <td>11</td>
      <td>320</td>
      <td>33</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>76</td>
      <td>11</td>
      <td>10</td>
      <td>0</td>
      <td>47</td>
      <td>2</td>
      <td>79</td>
      <td>16</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69</td>
      <td>6</td>
      <td>9</td>
      <td>1</td>
      <td>59</td>
      <td>2</td>
      <td>105</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>22</td>
      <td>5</td>
      <td>2</td>
      <td>0</td>
      <td>17</td>
      <td>4</td>
      <td>34</td>
      <td>8</td>
    </tr>
    <tr>
      <th>male</th>
      <td>23</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>27</td>
      <td>1</td>
      <td>52</td>
      <td>1</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>102</td>
      <td>14</td>
      <td>22</td>
      <td>1</td>
      <td>89</td>
      <td>1</td>
      <td>160</td>
      <td>17</td>
    </tr>
    <tr>
      <th>male</th>
      <td>105</td>
      <td>17</td>
      <td>15</td>
      <td>4</td>
      <td>96</td>
      <td>3</td>
      <td>139</td>
      <td>15</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>75</td>
      <td>5</td>
      <td>8</td>
      <td>1</td>
      <td>53</td>
      <td>2</td>
      <td>91</td>
      <td>9</td>
    </tr>
    <tr>
      <th>male</th>
      <td>79</td>
      <td>4</td>
      <td>13</td>
      <td>4</td>
      <td>47</td>
      <td>3</td>
      <td>94</td>
      <td>12</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>65</td>
      <td>6</td>
      <td>14</td>
      <td>1</td>
      <td>55</td>
      <td>4</td>
      <td>99</td>
      <td>13</td>
    </tr>
    <tr>
      <th>male</th>
      <td>67</td>
      <td>17</td>
      <td>11</td>
      <td>3</td>
      <td>47</td>
      <td>3</td>
      <td>89</td>
      <td>6</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>89</td>
      <td>13</td>
      <td>18</td>
      <td>3</td>
      <td>77</td>
      <td>7</td>
      <td>138</td>
      <td>12</td>
    </tr>
    <tr>
      <th>male</th>
      <td>68</td>
      <td>12</td>
      <td>17</td>
      <td>1</td>
      <td>80</td>
      <td>8</td>
      <td>135</td>
      <td>22</td>
    </tr>
  </tbody>
</table>
</div>




```python
grouped_by_country_and_gender.mean()
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
      <th></th>
      <th>Age</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>58.101883</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.531773</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>59.207469</td>
    </tr>
    <tr>
      <th>male</th>
      <td>56.768340</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>57.315217</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.953704</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>57.300493</td>
    </tr>
    <tr>
      <th>male</th>
      <td>55.893401</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>55.823770</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.398438</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>57.284047</td>
    </tr>
    <tr>
      <th>male</th>
      <td>58.222222</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>57.299720</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.536443</td>
    </tr>
  </tbody>
</table>
</div>



Notice how we didn't specify the `Age` feature. Pandas automatically outputs results for which the `mean` function makes sense. Here only Age fits the bill.


Like with any dataframe, you can also use `apply` to map a function to the grouped data, however, for anything more complex, like applying multiple functions at once, the `agg` method is more convenient.


```python
grouped_by_country_and_gender['Age'].agg(['min','max','mean','std'])
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
      <th></th>
      <th>min</th>
      <th>max</th>
      <th>mean</th>
      <th>std</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>58.101883</td>
      <td>19.587278</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>57.531773</td>
      <td>19.394326</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>25</td>
      <td>91</td>
      <td>59.207469</td>
      <td>19.041143</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>56.768340</td>
      <td>19.961407</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>57.315217</td>
      <td>19.527343</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>57.953704</td>
      <td>19.490896</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>57.300493</td>
      <td>19.116494</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>90</td>
      <td>55.893401</td>
      <td>18.838508</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>55.823770</td>
      <td>19.546233</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>57.398438</td>
      <td>18.570202</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>57.284047</td>
      <td>20.168651</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>58.222222</td>
      <td>18.856132</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>24</td>
      <td>91</td>
      <td>57.299720</td>
      <td>19.167134</td>
    </tr>
    <tr>
      <th>male</th>
      <td>24</td>
      <td>91</td>
      <td>57.536443</td>
      <td>19.434197</td>
    </tr>
  </tbody>
</table>
</div>



<h4> For descriptive statistics of numerical data, the <code>quantile</code> function is also useful.</h4>
<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>The 0.5 quantile is the <b>median</b> of our data.</p>
</div>


```python
grouped_by_country_and_gender['Age'].quantile((0.10, 0.25, 0.5, 0.75, 0.90)).unstack()
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
      <th></th>
      <th>0.1</th>
      <th>0.25</th>
      <th>0.5</th>
      <th>0.75</th>
      <th>0.9</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>31.0</td>
      <td>41.00</td>
      <td>58.0</td>
      <td>75.00</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>30.0</td>
      <td>41.00</td>
      <td>58.0</td>
      <td>74.00</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>31.0</td>
      <td>44.00</td>
      <td>61.0</td>
      <td>76.00</td>
      <td>84.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>30.0</td>
      <td>37.00</td>
      <td>57.0</td>
      <td>75.00</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>32.1</td>
      <td>40.75</td>
      <td>59.0</td>
      <td>74.00</td>
      <td>83.9</td>
    </tr>
    <tr>
      <th>male</th>
      <td>32.0</td>
      <td>42.00</td>
      <td>56.5</td>
      <td>74.00</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>31.0</td>
      <td>41.00</td>
      <td>57.0</td>
      <td>73.00</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>31.0</td>
      <td>39.00</td>
      <td>55.0</td>
      <td>71.00</td>
      <td>84.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>29.3</td>
      <td>39.00</td>
      <td>54.0</td>
      <td>72.25</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>32.0</td>
      <td>41.00</td>
      <td>58.0</td>
      <td>72.00</td>
      <td>83.5</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>29.6</td>
      <td>39.00</td>
      <td>57.0</td>
      <td>75.00</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>30.2</td>
      <td>43.00</td>
      <td>59.0</td>
      <td>73.00</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>31.0</td>
      <td>41.00</td>
      <td>57.0</td>
      <td>74.00</td>
      <td>84.0</td>
    </tr>
    <tr>
      <th>male</th>
      <td>30.0</td>
      <td>40.50</td>
      <td>58.0</td>
      <td>74.00</td>
      <td>83.0</td>
    </tr>
  </tbody>
</table>
</div>



<p>How can we use the <code>grouped_by_country_and_gender</code> object to output the number of people who were born
on a given month (numbered 1 to 12), for each country, and for each gender?</p>

<p><b>Hint:</b>
This can be done in one line using <code>apply</code> and <code>value_counts</code>, but you need to make sure you keep track of the type of object you are dealing with at each stage of the pipeline.</p>


```python
# Method 1 - one liner 
(grouped_by_country_and_gender['Birthday']
            .apply(lambda x: x.dt.month.value_counts())
            .unstack()
            .fillna(0))
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
      <th></th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>83</td>
      <td>75</td>
      <td>70</td>
      <td>66</td>
      <td>71</td>
      <td>78</td>
      <td>90</td>
      <td>77</td>
      <td>70</td>
      <td>65</td>
      <td>73</td>
      <td>85</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69</td>
      <td>64</td>
      <td>74</td>
      <td>71</td>
      <td>74</td>
      <td>57</td>
      <td>77</td>
      <td>91</td>
      <td>80</td>
      <td>81</td>
      <td>81</td>
      <td>78</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>26</td>
      <td>15</td>
      <td>18</td>
      <td>13</td>
      <td>30</td>
      <td>22</td>
      <td>22</td>
      <td>19</td>
      <td>11</td>
      <td>21</td>
      <td>21</td>
      <td>23</td>
    </tr>
    <tr>
      <th>male</th>
      <td>22</td>
      <td>15</td>
      <td>22</td>
      <td>28</td>
      <td>19</td>
      <td>22</td>
      <td>26</td>
      <td>23</td>
      <td>26</td>
      <td>22</td>
      <td>16</td>
      <td>18</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>7</td>
      <td>11</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>10</td>
      <td>10</td>
      <td>12</td>
      <td>9</td>
      <td>4</td>
      <td>7</td>
      <td>8</td>
    </tr>
    <tr>
      <th>male</th>
      <td>7</td>
      <td>11</td>
      <td>15</td>
      <td>2</td>
      <td>8</td>
      <td>9</td>
      <td>11</td>
      <td>6</td>
      <td>12</td>
      <td>10</td>
      <td>9</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>31</td>
      <td>34</td>
      <td>39</td>
      <td>33</td>
      <td>36</td>
      <td>28</td>
      <td>33</td>
      <td>36</td>
      <td>36</td>
      <td>37</td>
      <td>34</td>
      <td>29</td>
    </tr>
    <tr>
      <th>male</th>
      <td>31</td>
      <td>28</td>
      <td>35</td>
      <td>41</td>
      <td>27</td>
      <td>28</td>
      <td>37</td>
      <td>33</td>
      <td>29</td>
      <td>33</td>
      <td>33</td>
      <td>39</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>18</td>
      <td>20</td>
      <td>19</td>
      <td>21</td>
      <td>22</td>
      <td>26</td>
      <td>26</td>
      <td>15</td>
      <td>14</td>
      <td>23</td>
      <td>23</td>
      <td>17</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>22</td>
      <td>16</td>
      <td>22</td>
      <td>30</td>
      <td>19</td>
      <td>16</td>
      <td>25</td>
      <td>18</td>
      <td>25</td>
      <td>23</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>22</td>
      <td>14</td>
      <td>20</td>
      <td>31</td>
      <td>22</td>
      <td>19</td>
      <td>24</td>
      <td>34</td>
      <td>14</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>16</td>
      <td>22</td>
      <td>26</td>
      <td>20</td>
      <td>21</td>
      <td>23</td>
      <td>18</td>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>38</td>
      <td>32</td>
      <td>35</td>
      <td>24</td>
      <td>37</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>32</td>
      <td>31</td>
      <td>21</td>
      <td>32</td>
    </tr>
    <tr>
      <th>male</th>
      <td>44</td>
      <td>30</td>
      <td>23</td>
      <td>25</td>
      <td>23</td>
      <td>29</td>
      <td>31</td>
      <td>29</td>
      <td>26</td>
      <td>28</td>
      <td>26</td>
      <td>29</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Method 2 - Starting from the original data
# create a month series first and use it to perform groupby

months = data.Birthday.dt.month
(data
   .groupby(['Country', 'Gender', months])['Age']
   .count()
   .unstack()
   .fillna(0))
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
      <th>Birthday</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>83</td>
      <td>75</td>
      <td>70</td>
      <td>66</td>
      <td>71</td>
      <td>78</td>
      <td>90</td>
      <td>77</td>
      <td>70</td>
      <td>65</td>
      <td>73</td>
      <td>85</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69</td>
      <td>64</td>
      <td>74</td>
      <td>71</td>
      <td>74</td>
      <td>57</td>
      <td>77</td>
      <td>91</td>
      <td>80</td>
      <td>81</td>
      <td>81</td>
      <td>78</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>26</td>
      <td>15</td>
      <td>18</td>
      <td>13</td>
      <td>30</td>
      <td>22</td>
      <td>22</td>
      <td>19</td>
      <td>11</td>
      <td>21</td>
      <td>21</td>
      <td>23</td>
    </tr>
    <tr>
      <th>male</th>
      <td>22</td>
      <td>15</td>
      <td>22</td>
      <td>28</td>
      <td>19</td>
      <td>22</td>
      <td>26</td>
      <td>23</td>
      <td>26</td>
      <td>22</td>
      <td>16</td>
      <td>18</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>7</td>
      <td>11</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>10</td>
      <td>10</td>
      <td>12</td>
      <td>9</td>
      <td>4</td>
      <td>7</td>
      <td>8</td>
    </tr>
    <tr>
      <th>male</th>
      <td>7</td>
      <td>11</td>
      <td>15</td>
      <td>2</td>
      <td>8</td>
      <td>9</td>
      <td>11</td>
      <td>6</td>
      <td>12</td>
      <td>10</td>
      <td>9</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>31</td>
      <td>34</td>
      <td>39</td>
      <td>33</td>
      <td>36</td>
      <td>28</td>
      <td>33</td>
      <td>36</td>
      <td>36</td>
      <td>37</td>
      <td>34</td>
      <td>29</td>
    </tr>
    <tr>
      <th>male</th>
      <td>31</td>
      <td>28</td>
      <td>35</td>
      <td>41</td>
      <td>27</td>
      <td>28</td>
      <td>37</td>
      <td>33</td>
      <td>29</td>
      <td>33</td>
      <td>33</td>
      <td>39</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>18</td>
      <td>20</td>
      <td>19</td>
      <td>21</td>
      <td>22</td>
      <td>26</td>
      <td>26</td>
      <td>15</td>
      <td>14</td>
      <td>23</td>
      <td>23</td>
      <td>17</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>22</td>
      <td>16</td>
      <td>22</td>
      <td>30</td>
      <td>19</td>
      <td>16</td>
      <td>25</td>
      <td>18</td>
      <td>25</td>
      <td>23</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>22</td>
      <td>14</td>
      <td>20</td>
      <td>31</td>
      <td>22</td>
      <td>19</td>
      <td>24</td>
      <td>34</td>
      <td>14</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>16</td>
      <td>22</td>
      <td>26</td>
      <td>20</td>
      <td>21</td>
      <td>23</td>
      <td>18</td>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>38</td>
      <td>32</td>
      <td>35</td>
      <td>24</td>
      <td>37</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>32</td>
      <td>31</td>
      <td>21</td>
      <td>32</td>
    </tr>
    <tr>
      <th>male</th>
      <td>44</td>
      <td>30</td>
      <td>23</td>
      <td>25</td>
      <td>23</td>
      <td>29</td>
      <td>31</td>
      <td>29</td>
      <td>26</td>
      <td>28</td>
      <td>26</td>
      <td>29</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Note that although we've used 'Age' here, any feature would have done. 
# Do you see why?

# Method 3 - Starting from the original data and assign a new month column
(data
   .assign(month=data.Birthday.dt.month)
   .groupby(['Country', 'Gender', 'month'])['Age']
   .count()
   .unstack()
   .fillna(0))
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
      <th>month</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>83</td>
      <td>75</td>
      <td>70</td>
      <td>66</td>
      <td>71</td>
      <td>78</td>
      <td>90</td>
      <td>77</td>
      <td>70</td>
      <td>65</td>
      <td>73</td>
      <td>85</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69</td>
      <td>64</td>
      <td>74</td>
      <td>71</td>
      <td>74</td>
      <td>57</td>
      <td>77</td>
      <td>91</td>
      <td>80</td>
      <td>81</td>
      <td>81</td>
      <td>78</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>26</td>
      <td>15</td>
      <td>18</td>
      <td>13</td>
      <td>30</td>
      <td>22</td>
      <td>22</td>
      <td>19</td>
      <td>11</td>
      <td>21</td>
      <td>21</td>
      <td>23</td>
    </tr>
    <tr>
      <th>male</th>
      <td>22</td>
      <td>15</td>
      <td>22</td>
      <td>28</td>
      <td>19</td>
      <td>22</td>
      <td>26</td>
      <td>23</td>
      <td>26</td>
      <td>22</td>
      <td>16</td>
      <td>18</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>7</td>
      <td>11</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>10</td>
      <td>10</td>
      <td>12</td>
      <td>9</td>
      <td>4</td>
      <td>7</td>
      <td>8</td>
    </tr>
    <tr>
      <th>male</th>
      <td>7</td>
      <td>11</td>
      <td>15</td>
      <td>2</td>
      <td>8</td>
      <td>9</td>
      <td>11</td>
      <td>6</td>
      <td>12</td>
      <td>10</td>
      <td>9</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>31</td>
      <td>34</td>
      <td>39</td>
      <td>33</td>
      <td>36</td>
      <td>28</td>
      <td>33</td>
      <td>36</td>
      <td>36</td>
      <td>37</td>
      <td>34</td>
      <td>29</td>
    </tr>
    <tr>
      <th>male</th>
      <td>31</td>
      <td>28</td>
      <td>35</td>
      <td>41</td>
      <td>27</td>
      <td>28</td>
      <td>37</td>
      <td>33</td>
      <td>29</td>
      <td>33</td>
      <td>33</td>
      <td>39</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>18</td>
      <td>20</td>
      <td>19</td>
      <td>21</td>
      <td>22</td>
      <td>26</td>
      <td>26</td>
      <td>15</td>
      <td>14</td>
      <td>23</td>
      <td>23</td>
      <td>17</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>22</td>
      <td>16</td>
      <td>22</td>
      <td>30</td>
      <td>19</td>
      <td>16</td>
      <td>25</td>
      <td>18</td>
      <td>25</td>
      <td>23</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>22</td>
      <td>14</td>
      <td>20</td>
      <td>31</td>
      <td>22</td>
      <td>19</td>
      <td>24</td>
      <td>34</td>
      <td>14</td>
    </tr>
    <tr>
      <th>male</th>
      <td>21</td>
      <td>16</td>
      <td>22</td>
      <td>26</td>
      <td>20</td>
      <td>21</td>
      <td>23</td>
      <td>18</td>
      <td>17</td>
      <td>21</td>
      <td>19</td>
      <td>19</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>38</td>
      <td>32</td>
      <td>35</td>
      <td>24</td>
      <td>37</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>32</td>
      <td>31</td>
      <td>21</td>
      <td>32</td>
    </tr>
    <tr>
      <th>male</th>
      <td>44</td>
      <td>30</td>
      <td>23</td>
      <td>25</td>
      <td>23</td>
      <td>29</td>
      <td>31</td>
      <td>29</td>
      <td>26</td>
      <td>28</td>
      <td>26</td>
      <td>29</td>
    </tr>
  </tbody>
</table>
</div>



<h3> <center><font color=MediumVioletRed>D. MultiIndex.</font></center></h3>

<h4> We can of course group the data by more than 2 features.</h4>
However, results might get a bit harder to take in.


```python
s = data.groupby(['Country','Gender','BloodType'])['Age'].mean().round(2)
s
```

    Country         Gender  BloodType
    Australia       female  A+           59.36
                            A-           59.90
                            AB+          53.13
                            AB-          61.50
                            B+           56.62
                            B-           66.00
                            O+           58.46
                            O-           58.02
                    male    A+           57.67
                            A-           51.70
                            AB+          59.98
                            AB-          62.00
                            B+           58.79
                            B-           44.73
                            O+           56.94
                            O-           59.76
    France          female  A+           58.54
                            A-           53.09
                            AB+          63.40
                            B+           58.47
                            B-           61.50
                            O+           60.18
                            O-           61.06
                    male    A+           60.81
                            A-           56.00
                            AB+          62.78
                            AB-          41.00
                            B+           55.03
                            B-           67.00
                            O+           53.90
                                         ...  
    United Kingdom  female  AB+          49.79
                            AB-          63.00
                            B+           55.33
                            B-           65.50
                            O+           57.16
                            O-           63.23
                    male    A+           57.39
                            A-           60.41
                            AB+          53.91
                            AB-          65.33
                            B+           59.68
                            B-           32.67
                            O+           58.37
                            O-           64.83
    United States   female  A+           57.46
                            A-           71.54
                            AB+          58.44
                            AB-          53.67
                            B+           55.75
                            B-           65.57
                            O+           57.57
                            O-           41.83
                    male    A+           55.07
                            A-           47.08
                            AB+          55.12
                            AB-          66.00
                            B+           54.34
                            B-           71.25
                            O+           61.33
                            O-           55.73
    Name: Age, Length: 109, dtype: float64



<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p><code>s</code> is a Pandas <code>Series</code> object with a <code>MultiIndex</code> object as its index.
</p>
</div>


```python
s.index
```

    MultiIndex(levels=[['Australia', 'France', 'Iceland', 'Italy', 'New Zealand', 'United Kingdom', 'United States'], ['female', 'male'], ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']],
               codes=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 4, 5, 6, 7, 0, 1, 2, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]],
               names=['Country', 'Gender', 'BloodType'])



We can convert the MultiIndexed series to a MultiIndexed dataframe using unstack.


```python
df = s.unstack().fillna(0)
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>59.36</td>
      <td>59.90</td>
      <td>53.13</td>
      <td>61.50</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.67</td>
      <td>51.70</td>
      <td>59.98</td>
      <td>62.00</td>
      <td>58.79</td>
      <td>44.73</td>
      <td>56.94</td>
      <td>59.76</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>58.54</td>
      <td>53.09</td>
      <td>63.40</td>
      <td>0.00</td>
      <td>58.47</td>
      <td>61.50</td>
      <td>60.18</td>
      <td>61.06</td>
    </tr>
    <tr>
      <th>male</th>
      <td>60.81</td>
      <td>56.00</td>
      <td>62.78</td>
      <td>41.00</td>
      <td>55.03</td>
      <td>67.00</td>
      <td>53.90</td>
      <td>65.62</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>56.95</td>
      <td>63.40</td>
      <td>63.00</td>
      <td>0.00</td>
      <td>60.06</td>
      <td>67.25</td>
      <td>53.15</td>
      <td>60.00</td>
    </tr>
    <tr>
      <th>male</th>
      <td>62.09</td>
      <td>35.00</td>
      <td>57.00</td>
      <td>0.00</td>
      <td>59.37</td>
      <td>74.00</td>
      <td>55.13</td>
      <td>81.00</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>55.68</td>
      <td>55.36</td>
      <td>68.50</td>
      <td>46.00</td>
      <td>56.07</td>
      <td>57.00</td>
      <td>57.96</td>
      <td>55.12</td>
    </tr>
    <tr>
      <th>male</th>
      <td>54.45</td>
      <td>54.47</td>
      <td>62.60</td>
      <td>44.75</td>
      <td>54.82</td>
      <td>66.00</td>
      <td>57.32</td>
      <td>55.47</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>57.49</td>
      <td>59.20</td>
      <td>50.50</td>
      <td>67.00</td>
      <td>58.19</td>
      <td>45.00</td>
      <td>53.22</td>
      <td>58.33</td>
    </tr>
    <tr>
      <th>male</th>
      <td>60.39</td>
      <td>74.75</td>
      <td>65.08</td>
      <td>64.00</td>
      <td>53.96</td>
      <td>52.33</td>
      <td>54.68</td>
      <td>57.42</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>58.42</td>
      <td>63.17</td>
      <td>49.79</td>
      <td>63.00</td>
      <td>55.33</td>
      <td>65.50</td>
      <td>57.16</td>
      <td>63.23</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.39</td>
      <td>60.41</td>
      <td>53.91</td>
      <td>65.33</td>
      <td>59.68</td>
      <td>32.67</td>
      <td>58.37</td>
      <td>64.83</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>57.46</td>
      <td>71.54</td>
      <td>58.44</td>
      <td>53.67</td>
      <td>55.75</td>
      <td>65.57</td>
      <td>57.57</td>
      <td>41.83</td>
    </tr>
    <tr>
      <th>male</th>
      <td>55.07</td>
      <td>47.08</td>
      <td>55.12</td>
      <td>66.00</td>
      <td>54.34</td>
      <td>71.25</td>
      <td>61.33</td>
      <td>55.73</td>
    </tr>
  </tbody>
</table>
</div>



To access specific data using the MultiIndex for a __Series__, you can use the `xs` method and specify the level at which you are extracting the data, if you are not using the top level.

To access specific data using the MultiIndex for a __DataFrame__, you can use the `loc` method, but specifying the level is a bit more involved.

#### Top level selection


```python
s['Australia']
```

    Gender  BloodType
    female  A+           59.36
            A-           59.90
            AB+          53.13
            AB-          61.50
            B+           56.62
            B-           66.00
            O+           58.46
            O-           58.02
    male    A+           57.67
            A-           51.70
            AB+          59.98
            AB-          62.00
            B+           58.79
            B-           44.73
            O+           56.94
            O-           59.76
    Name: Age, dtype: float64




```python
df.loc['Australia', :]
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
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
      <th>female</th>
      <td>59.36</td>
      <td>59.9</td>
      <td>53.13</td>
      <td>61.5</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.67</td>
      <td>51.7</td>
      <td>59.98</td>
      <td>62.0</td>
      <td>58.79</td>
      <td>44.73</td>
      <td>56.94</td>
      <td>59.76</td>
    </tr>
  </tbody>
</table>
</div>



This is equivalent to:


```python
s['Australia'].unstack()
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
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
      <th>female</th>
      <td>59.36</td>
      <td>59.9</td>
      <td>53.13</td>
      <td>61.5</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.67</td>
      <td>51.7</td>
      <td>59.98</td>
      <td>62.0</td>
      <td>58.79</td>
      <td>44.73</td>
      <td>56.94</td>
      <td>59.76</td>
    </tr>
  </tbody>
</table>
</div>



The levels can be exchanged either by unstacking the right level, or by transposing the resulting dataframe.


```python
s['Australia'].unstack(level='Gender')
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
      <th>Gender</th>
      <th>female</th>
      <th>male</th>
    </tr>
    <tr>
      <th>BloodType</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A+</th>
      <td>59.36</td>
      <td>57.67</td>
    </tr>
    <tr>
      <th>A-</th>
      <td>59.90</td>
      <td>51.70</td>
    </tr>
    <tr>
      <th>AB+</th>
      <td>53.13</td>
      <td>59.98</td>
    </tr>
    <tr>
      <th>AB-</th>
      <td>61.50</td>
      <td>62.00</td>
    </tr>
    <tr>
      <th>B+</th>
      <td>56.62</td>
      <td>58.79</td>
    </tr>
    <tr>
      <th>B-</th>
      <td>66.00</td>
      <td>44.73</td>
    </tr>
    <tr>
      <th>O+</th>
      <td>58.46</td>
      <td>56.94</td>
    </tr>
    <tr>
      <th>O-</th>
      <td>58.02</td>
      <td>59.76</td>
    </tr>
  </tbody>
</table>
</div>




```python
s['Australia'].unstack().T
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
      <th>Gender</th>
      <th>female</th>
      <th>male</th>
    </tr>
    <tr>
      <th>BloodType</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A+</th>
      <td>59.36</td>
      <td>57.67</td>
    </tr>
    <tr>
      <th>A-</th>
      <td>59.90</td>
      <td>51.70</td>
    </tr>
    <tr>
      <th>AB+</th>
      <td>53.13</td>
      <td>59.98</td>
    </tr>
    <tr>
      <th>AB-</th>
      <td>61.50</td>
      <td>62.00</td>
    </tr>
    <tr>
      <th>B+</th>
      <td>56.62</td>
      <td>58.79</td>
    </tr>
    <tr>
      <th>B-</th>
      <td>66.00</td>
      <td>44.73</td>
    </tr>
    <tr>
      <th>O+</th>
      <td>58.46</td>
      <td>56.94</td>
    </tr>
    <tr>
      <th>O-</th>
      <td>58.02</td>
      <td>59.76</td>
    </tr>
  </tbody>
</table>
</div>



#### To select data at a deeper level of the multiindex, you need to  specify the level.
#### Here's an example with Gender.
Notice the different syntax using `xs`.


```python
s.xs('female', level='Gender').unstack()
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>59.36</td>
      <td>59.90</td>
      <td>53.13</td>
      <td>61.50</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>France</th>
      <td>58.54</td>
      <td>53.09</td>
      <td>63.40</td>
      <td>NaN</td>
      <td>58.47</td>
      <td>61.50</td>
      <td>60.18</td>
      <td>61.06</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>56.95</td>
      <td>63.40</td>
      <td>63.00</td>
      <td>NaN</td>
      <td>60.06</td>
      <td>67.25</td>
      <td>53.15</td>
      <td>60.00</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>55.68</td>
      <td>55.36</td>
      <td>68.50</td>
      <td>46.00</td>
      <td>56.07</td>
      <td>57.00</td>
      <td>57.96</td>
      <td>55.12</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>57.49</td>
      <td>59.20</td>
      <td>50.50</td>
      <td>67.00</td>
      <td>58.19</td>
      <td>45.00</td>
      <td>53.22</td>
      <td>58.33</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>58.42</td>
      <td>63.17</td>
      <td>49.79</td>
      <td>63.00</td>
      <td>55.33</td>
      <td>65.50</td>
      <td>57.16</td>
      <td>63.23</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>57.46</td>
      <td>71.54</td>
      <td>58.44</td>
      <td>53.67</td>
      <td>55.75</td>
      <td>65.57</td>
      <td>57.57</td>
      <td>41.83</td>
    </tr>
  </tbody>
</table>
</div>





#### Selecting the data from a deeper level is trickier with a dataframe.

#### We need to specify an index `slice`.




```python
df.loc[(slice(None), 'female'), :].droplevel('Gender')
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>59.36</td>
      <td>59.90</td>
      <td>53.13</td>
      <td>61.50</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>France</th>
      <td>58.54</td>
      <td>53.09</td>
      <td>63.40</td>
      <td>0.00</td>
      <td>58.47</td>
      <td>61.50</td>
      <td>60.18</td>
      <td>61.06</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>56.95</td>
      <td>63.40</td>
      <td>63.00</td>
      <td>0.00</td>
      <td>60.06</td>
      <td>67.25</td>
      <td>53.15</td>
      <td>60.00</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>55.68</td>
      <td>55.36</td>
      <td>68.50</td>
      <td>46.00</td>
      <td>56.07</td>
      <td>57.00</td>
      <td>57.96</td>
      <td>55.12</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>57.49</td>
      <td>59.20</td>
      <td>50.50</td>
      <td>67.00</td>
      <td>58.19</td>
      <td>45.00</td>
      <td>53.22</td>
      <td>58.33</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>58.42</td>
      <td>63.17</td>
      <td>49.79</td>
      <td>63.00</td>
      <td>55.33</td>
      <td>65.50</td>
      <td>57.16</td>
      <td>63.23</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>57.46</td>
      <td>71.54</td>
      <td>58.44</td>
      <td>53.67</td>
      <td>55.75</td>
      <td>65.57</td>
      <td>57.57</td>
      <td>41.83</td>
    </tr>
  </tbody>
</table>
</div>



or alternatively, using a pandas <code>IndexSlice</code> object.


```python
idx = pd.IndexSlice
```

```python
df.loc[idx[:, 'female'], :].droplevel('Gender')
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
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
      <th>Australia</th>
      <td>59.36</td>
      <td>59.90</td>
      <td>53.13</td>
      <td>61.50</td>
      <td>56.62</td>
      <td>66.00</td>
      <td>58.46</td>
      <td>58.02</td>
    </tr>
    <tr>
      <th>France</th>
      <td>58.54</td>
      <td>53.09</td>
      <td>63.40</td>
      <td>0.00</td>
      <td>58.47</td>
      <td>61.50</td>
      <td>60.18</td>
      <td>61.06</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>56.95</td>
      <td>63.40</td>
      <td>63.00</td>
      <td>0.00</td>
      <td>60.06</td>
      <td>67.25</td>
      <td>53.15</td>
      <td>60.00</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>55.68</td>
      <td>55.36</td>
      <td>68.50</td>
      <td>46.00</td>
      <td>56.07</td>
      <td>57.00</td>
      <td>57.96</td>
      <td>55.12</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>57.49</td>
      <td>59.20</td>
      <td>50.50</td>
      <td>67.00</td>
      <td>58.19</td>
      <td>45.00</td>
      <td>53.22</td>
      <td>58.33</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>58.42</td>
      <td>63.17</td>
      <td>49.79</td>
      <td>63.00</td>
      <td>55.33</td>
      <td>65.50</td>
      <td>57.16</td>
      <td>63.23</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>57.46</td>
      <td>71.54</td>
      <td>58.44</td>
      <td>53.67</td>
      <td>55.75</td>
      <td>65.57</td>
      <td>57.57</td>
      <td>41.83</td>
    </tr>
  </tbody>
</table>
</div>



#### Same if you want to select `BloodType` as the level.


```python
s.xs('O+', level='BloodType').unstack().fillna(0)
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
      <th>Gender</th>
      <th>female</th>
      <th>male</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <td>58.46</td>
      <td>56.94</td>
    </tr>
    <tr>
      <th>France</th>
      <td>60.18</td>
      <td>53.90</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>53.15</td>
      <td>55.13</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>57.96</td>
      <td>57.32</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>53.22</td>
      <td>54.68</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>57.16</td>
      <td>58.37</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>57.57</td>
      <td>61.33</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.loc[:, ['O+']].unstack().droplevel('BloodType', axis='columns')
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
      <th>Gender</th>
      <th>female</th>
      <th>male</th>
    </tr>
    <tr>
      <th>Country</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <td>58.46</td>
      <td>56.94</td>
    </tr>
    <tr>
      <th>France</th>
      <td>60.18</td>
      <td>53.90</td>
    </tr>
    <tr>
      <th>Iceland</th>
      <td>53.15</td>
      <td>55.13</td>
    </tr>
    <tr>
      <th>Italy</th>
      <td>57.96</td>
      <td>57.32</td>
    </tr>
    <tr>
      <th>New Zealand</th>
      <td>53.22</td>
      <td>54.68</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>57.16</td>
      <td>58.37</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>57.57</td>
      <td>61.33</td>
    </tr>
  </tbody>
</table>
</div>



#### Multiple levels can be specified at once


```python
s.xs(('Australia','female'), level=['Country','Gender'])
```

    BloodType
    A+     59.36
    A-     59.90
    AB+    53.13
    AB-    61.50
    B+     56.62
    B-     66.00
    O+     58.46
    O-     58.02
    Name: Age, dtype: float64




```python
df.loc[('Australia', 'female'), :]
```

    BloodType
    A+     59.36
    A-     59.90
    AB+    53.13
    AB-    61.50
    B+     56.62
    B-     66.00
    O+     58.46
    O-     58.02
    Name: (Australia, female), dtype: float64




```python
s.xs(('Australia','O+'), level=['Country','BloodType'])
```

    Gender
    female    58.46
    male      56.94
    Name: Age, dtype: float64




```python
df.loc['Australia', 'O+']
```

    Gender
    female    58.46
    male      56.94
    Name: O+, dtype: float64



### Let's visualise some of these results


```python
# colormap from matplotlib
from matplotlib import cm

# Also see this stackoverflow post for the legend placement: 
# http://stackoverflow.com/questions/23556153/how-to-put-legend-outside-the-plot-with-pandas
```

```python
ax = (s.xs('female', level='Gender')
       .unstack()
       .fillna(0)
       .plot(kind='bar', 
             figsize=(15,5), 
             width=0.8, 
             alpha=0.8, 
             ec='k',
             rot=0,
             colormap=cm.Paired_r)
     )
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()
```

![png](output_105_0.png)


#### Notice the difference between the previous plot and the one below.


```python
ax = (s.xs('female', level='Gender')
       .unstack('Country')
       .fillna(0)
       .plot(kind='bar', 
             figsize=(15,5), 
             width=0.8, 
             alpha=0.8, 
             ec='k',
             rot=0,
             colormap=cm.Paired_r)
     )
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()
```

![png](output_107_0.png)


<h3> <center><font color=MediumVioletRed>E. Fine Tuning.</font></center></h3>

So far we've applied an operation on a <b>single feature</b> of a GroupBy object. 

For instance, we've computed the mean for the <code>Age</code> feature, and then, <b>in a separate computation</b> we've computed 
a count of the blood types.

You can actually do everything at once by specifying <b>a different operation for each feature</b> using a dictionary,
and use the <code>agg</code> method to aggregate the data across the dataframe.


```python
group = data.groupby(['Country', 'Gender'])

def data_count(x):
    return Counter(x).items()

method = {'Age': [np.mean, np.std], 'BloodType': data_count}

group.agg(method).rename({'data_count':'group_counts'}, axis=1)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead tr th {
        text-align: left;
    }
    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="2" halign="left">Age</th>
      <th>BloodType</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
      <th>std</th>
      <th>group_counts</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>58.101883</td>
      <td>19.587278</td>
      <td>((B+, 205), (O-, 41), (AB+, 54), (O+, 328), (A...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.531773</td>
      <td>19.394326</td>
      <td>((B+, 214), (AB+, 46), (A+, 239), (O+, 320), (...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>59.207469</td>
      <td>19.041143</td>
      <td>((A-, 11), (B+, 47), (A+, 76), (O+, 79), (O-, ...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>56.768340</td>
      <td>19.961407</td>
      <td>((B+, 59), (A+, 69), (AB+, 9), (O+, 105), (O-,...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>57.315217</td>
      <td>19.527343</td>
      <td>((O+, 34), (A+, 22), (B-, 4), (B+, 17), (A-, 5...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.953704</td>
      <td>19.490896</td>
      <td>((O+, 52), (A+, 23), (AB+, 3), (B+, 27), (O-, ...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>57.300493</td>
      <td>19.116494</td>
      <td>((A+, 102), (O+, 160), (B+, 89), (O-, 17), (AB...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>55.893401</td>
      <td>18.838508</td>
      <td>((A+, 105), (O+, 139), (B+, 96), (AB-, 4), (B-...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>55.823770</td>
      <td>19.546233</td>
      <td>((O-, 9), (O+, 91), (A+, 75), (AB+, 8), (B+, 5...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.398438</td>
      <td>18.570202</td>
      <td>((A+, 79), (O+, 94), (AB+, 13), (B+, 47), (O-,...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>57.284047</td>
      <td>20.168651</td>
      <td>((A+, 65), (B+, 55), (O-, 13), (O+, 99), (AB+,...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>58.222222</td>
      <td>18.856132</td>
      <td>((A+, 67), (B+, 47), (O-, 6), (A-, 17), (O+, 8...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>57.299720</td>
      <td>19.167134</td>
      <td>((A+, 89), (B+, 77), (O+, 138), (AB+, 18), (A-...</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.536443</td>
      <td>19.434197</td>
      <td>((A+, 68), (O+, 135), (B+, 80), (A-, 12), (AB+...</td>
    </tr>
  </tbody>
</table>
</div>



#### Accessing a particular portion of the result is just a matter of navigating the multilevel structure of the index and the columns.


```python
group.agg(method).loc[[('Australia', 'male')]]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead tr th {
        text-align: left;
    }
    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="2" halign="left">Age</th>
      <th>BloodType</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
      <th>std</th>
      <th>data_count</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <th>male</th>
      <td>57.531773</td>
      <td>19.394326</td>
      <td>((B+, 214), (AB+, 46), (A+, 239), (O+, 320), (...</td>
    </tr>
  </tbody>
</table>
</div>



This is equivalent to


```python
group.agg(method).xs(('Australia', 'male'), level=['Country', 'Gender'])
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead tr th {
        text-align: left;
    }
    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="2" halign="left">Age</th>
      <th>BloodType</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
      <th>std</th>
      <th>data_count</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Australia</th>
      <th>male</th>
      <td>57.531773</td>
      <td>19.394326</td>
      <td>((B+, 214), (AB+, 46), (A+, 239), (O+, 320), (...</td>
    </tr>
  </tbody>
</table>
</div>



#### Notice the difference with


```python
group.agg(method).xs(('Australia', 'male'))
```

    Age        mean                                                    57.5318
               std                                                     19.3943
    BloodType  data_count    ((B+, 214), (AB+, 46), (A+, 239), (O+, 320), (...
    Name: (Australia, male), dtype: object



#### We can select data using levels of the columns.


```python
group.agg(method).loc[:,[('Age', 'mean')]]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead tr th {
        text-align: left;
    }
    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th>Age</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>58.101883</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.531773</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>59.207469</td>
    </tr>
    <tr>
      <th>male</th>
      <td>56.768340</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>57.315217</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.953704</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>57.300493</td>
    </tr>
    <tr>
      <th>male</th>
      <td>55.893401</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>55.823770</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.398438</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>57.284047</td>
    </tr>
    <tr>
      <th>male</th>
      <td>58.222222</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>57.299720</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.536443</td>
    </tr>
  </tbody>
</table>
</div>



This is equivalent to


```python
group.agg(method).xs([('Age', 'mean')], axis=1)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead tr th {
        text-align: left;
    }
    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th>Age</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>58.101883</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.531773</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>59.207469</td>
    </tr>
    <tr>
      <th>male</th>
      <td>56.768340</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>57.315217</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.953704</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>57.300493</td>
    </tr>
    <tr>
      <th>male</th>
      <td>55.893401</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>55.823770</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.398438</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>57.284047</td>
    </tr>
    <tr>
      <th>male</th>
      <td>58.222222</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>57.299720</td>
    </tr>
    <tr>
      <th>male</th>
      <td>57.536443</td>
    </tr>
  </tbody>
</table>
</div>



#### You can go as "deep" as you need.


```python
group.agg(method).loc['Australia', 'female']['Age']['mean']
```

    58.10188261351052



This is equivalent to


```python
group.agg(method).xs(('Australia', 'female'))['Age']['mean']
```

    58.10188261351052



#### To extract just the values (without the index), use the `values` attribute.


```python
group.agg(method).loc['Australia', 'female']['BloodType'].values
```

    array([dict_items([('B+', 205), ('O-', 41), ('AB+', 54), ('O+', 328), ('A+', 229), ('A-', 29), ('B-', 13), ('AB-', 4)])],
          dtype=object)



#### Cross-tabulation is an effective way to have a quick look at how the data is distributed across categories.


```python
pd.crosstab(data.Gender, data.BloodType, margins=True)
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
      <th>All</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
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
      <th>female</th>
      <td>658</td>
      <td>83</td>
      <td>128</td>
      <td>10</td>
      <td>543</td>
      <td>33</td>
      <td>929</td>
      <td>116</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>male</th>
      <td>650</td>
      <td>87</td>
      <td>114</td>
      <td>17</td>
      <td>570</td>
      <td>31</td>
      <td>934</td>
      <td>97</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>All</th>
      <td>1308</td>
      <td>170</td>
      <td>242</td>
      <td>27</td>
      <td>1113</td>
      <td>64</td>
      <td>1863</td>
      <td>213</td>
      <td>5000</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.crosstab([data.Country, data.Gender], data.BloodType, margins=True)
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
      <th>All</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
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
      <th rowspan="2" valign="top">Australia</th>
      <th>female</th>
      <td>229</td>
      <td>29</td>
      <td>54</td>
      <td>4</td>
      <td>205</td>
      <td>13</td>
      <td>328</td>
      <td>41</td>
      <td>903</td>
    </tr>
    <tr>
      <th>male</th>
      <td>239</td>
      <td>30</td>
      <td>46</td>
      <td>4</td>
      <td>214</td>
      <td>11</td>
      <td>320</td>
      <td>33</td>
      <td>897</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">France</th>
      <th>female</th>
      <td>76</td>
      <td>11</td>
      <td>10</td>
      <td>0</td>
      <td>47</td>
      <td>2</td>
      <td>79</td>
      <td>16</td>
      <td>241</td>
    </tr>
    <tr>
      <th>male</th>
      <td>69</td>
      <td>6</td>
      <td>9</td>
      <td>1</td>
      <td>59</td>
      <td>2</td>
      <td>105</td>
      <td>8</td>
      <td>259</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Iceland</th>
      <th>female</th>
      <td>22</td>
      <td>5</td>
      <td>2</td>
      <td>0</td>
      <td>17</td>
      <td>4</td>
      <td>34</td>
      <td>8</td>
      <td>92</td>
    </tr>
    <tr>
      <th>male</th>
      <td>23</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>27</td>
      <td>1</td>
      <td>52</td>
      <td>1</td>
      <td>108</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Italy</th>
      <th>female</th>
      <td>102</td>
      <td>14</td>
      <td>22</td>
      <td>1</td>
      <td>89</td>
      <td>1</td>
      <td>160</td>
      <td>17</td>
      <td>406</td>
    </tr>
    <tr>
      <th>male</th>
      <td>105</td>
      <td>17</td>
      <td>15</td>
      <td>4</td>
      <td>96</td>
      <td>3</td>
      <td>139</td>
      <td>15</td>
      <td>394</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">New Zealand</th>
      <th>female</th>
      <td>75</td>
      <td>5</td>
      <td>8</td>
      <td>1</td>
      <td>53</td>
      <td>2</td>
      <td>91</td>
      <td>9</td>
      <td>244</td>
    </tr>
    <tr>
      <th>male</th>
      <td>79</td>
      <td>4</td>
      <td>13</td>
      <td>4</td>
      <td>47</td>
      <td>3</td>
      <td>94</td>
      <td>12</td>
      <td>256</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United Kingdom</th>
      <th>female</th>
      <td>65</td>
      <td>6</td>
      <td>14</td>
      <td>1</td>
      <td>55</td>
      <td>4</td>
      <td>99</td>
      <td>13</td>
      <td>257</td>
    </tr>
    <tr>
      <th>male</th>
      <td>67</td>
      <td>17</td>
      <td>11</td>
      <td>3</td>
      <td>47</td>
      <td>3</td>
      <td>89</td>
      <td>6</td>
      <td>243</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">United States</th>
      <th>female</th>
      <td>89</td>
      <td>13</td>
      <td>18</td>
      <td>3</td>
      <td>77</td>
      <td>7</td>
      <td>138</td>
      <td>12</td>
      <td>357</td>
    </tr>
    <tr>
      <th>male</th>
      <td>68</td>
      <td>12</td>
      <td>17</td>
      <td>1</td>
      <td>80</td>
      <td>8</td>
      <td>135</td>
      <td>22</td>
      <td>343</td>
    </tr>
    <tr>
      <th>All</th>
      <th></th>
      <td>1308</td>
      <td>170</td>
      <td>242</td>
      <td>27</td>
      <td>1113</td>
      <td>64</td>
      <td>1863</td>
      <td>213</td>
      <td>5000</td>
    </tr>
  </tbody>
</table>
</div>



<h3> <center><font color=MediumVioletRed>F. GroupBy on continuous features.</font></center></h3>

We've seen how we can group the data according to the features that are in the original dataset. 

For instance, grouping the data by country is trivial. Same for the blood type because these are <b>categorical</b> data.

But what about <code>Age</code>? If we do a <code>groupby</code> without thinking too much about it we get something rather useless.


```python
g = data.groupby('Age')
g['BloodType'].describe().unstack()
```

           Age
    count  24     37
           25     72
           26     73
           27     86
           28     69
           29     81
           30     71
           31     86
           32     73
           33     78
           34     54
           35     79
           36     70
           37     88
           38     70
           39     81
           40     62
           41     75
           42     66
           43     70
           44     67
           45     80
           46     85
           47     65
           48     77
           49     88
           50     77
           51     75
           52     83
           53     86
                  ..
    freq   62     28
           63     41
           64     26
           65     26
           66     38
           67     28
           68     35
           69     36
           70     25
           71     25
           72     39
           73     21
           74     32
           75     39
           76     21
           77     20
           78     33
           79     32
           80     30
           81     21
           82     34
           83     27
           84     25
           85     25
           86     28
           87     32
           88     23
           89     30
           90     24
           91     18
    Length: 272, dtype: object



We get one entry for each year of `Age` which isn't what we want. 

Ideally, we'd want to split the data into age groups and use that to group the data. Pandas has a `cut` function that allows us to do that.


```python
data.Age.describe()
```

    count    5000.000000
    mean       57.447600
    std        19.339422
    min        24.000000
    25%        41.000000
    50%        57.000000
    75%        74.000000
    max        91.000000
    Name: Age, dtype: float64




```python
bins = np.arange(20, 100, 10)
bins
```

    array([20, 30, 40, 50, 60, 70, 80, 90])




```python
labels = pd.cut(data.Age, bins)
labels[:5]
```

    0    (50, 60]
    1    (50, 60]
    2    (50, 60]
    3    (80, 90]
    4    (70, 80]
    Name: Age, dtype: category
    Categories (7, interval[int64]): [(20, 30] < (30, 40] < (40, 50] < (50, 60] < (60, 70] < (70, 80] < (80, 90]]




```python
data.Age.head()
```

    0    51
    1    57
    2    55
    3    86
    4    73
    Name: Age, dtype: int64



#### We can use the newly created label to partition the Age variable into intervals.


```python
grouped = data.groupby(['Country', labels])

grouped.size().unstack().fillna(0)
```

    Age             (20, 30]  (30, 40]  (40, 50]  (50, 60]  (60, 70]  (70, 80]  \
    Country                                                                      
    Australia            177       254       269       275       257       280   
    France                48        76        68        71        75        76   
    Iceland               16        32        36        24        30        26   
    Italy                 74       131       120       134       128        96   
    New Zealand           49        76        81        70        93        57   
    United Kingdom        54        69        77        64        72        91   
    United States         71       103        99       111       102       115   
    
    Age             (80, 90]  
    Country                   
    Australia            272  
    France                82  
    Iceland               34  
    Italy                111  
    New Zealand           71  
    United Kingdom        69  
    United States         94  



If we want the `Age` groups to be our index we can use `unstack(0)` or much the more explicit and therefore better, `unstack('Country')` .


```python
grouped.size().unstack('Country').fillna(0)
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
      <th>Country</th>
      <th>Australia</th>
      <th>France</th>
      <th>Iceland</th>
      <th>Italy</th>
      <th>New Zealand</th>
      <th>United Kingdom</th>
      <th>United States</th>
    </tr>
    <tr>
      <th>Age</th>
      <th></th>
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
      <th>(20, 30]</th>
      <td>177</td>
      <td>48</td>
      <td>16</td>
      <td>74</td>
      <td>49</td>
      <td>54</td>
      <td>71</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>254</td>
      <td>76</td>
      <td>32</td>
      <td>131</td>
      <td>76</td>
      <td>69</td>
      <td>103</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>269</td>
      <td>68</td>
      <td>36</td>
      <td>120</td>
      <td>81</td>
      <td>77</td>
      <td>99</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>275</td>
      <td>71</td>
      <td>24</td>
      <td>134</td>
      <td>70</td>
      <td>64</td>
      <td>111</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>257</td>
      <td>75</td>
      <td>30</td>
      <td>128</td>
      <td>93</td>
      <td>72</td>
      <td>102</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>280</td>
      <td>76</td>
      <td>26</td>
      <td>96</td>
      <td>57</td>
      <td>91</td>
      <td>115</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>272</td>
      <td>82</td>
      <td>34</td>
      <td>111</td>
      <td>71</td>
      <td>69</td>
      <td>94</td>
    </tr>
  </tbody>
</table>
</div>



#### Just like before, we can pass more features to the `groupby` method.


```python
grouped = data.groupby(['Country', 'BloodType', labels])
grouped.size().unstack('BloodType').fillna(0)
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
      <th>BloodType</th>
      <th>A+</th>
      <th>A-</th>
      <th>AB+</th>
      <th>AB-</th>
      <th>B+</th>
      <th>B-</th>
      <th>O+</th>
      <th>O-</th>
    </tr>
    <tr>
      <th>Country</th>
      <th>Age</th>
      <th></th>
      <th></th>
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
      <th rowspan="7" valign="top">Australia</th>
      <th>(20, 30]</th>
      <td>41.0</td>
      <td>11.0</td>
      <td>13.0</td>
      <td>0.0</td>
      <td>49.0</td>
      <td>3.0</td>
      <td>53.0</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>63.0</td>
      <td>8.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>57.0</td>
      <td>4.0</td>
      <td>97.0</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>73.0</td>
      <td>9.0</td>
      <td>16.0</td>
      <td>2.0</td>
      <td>56.0</td>
      <td>2.0</td>
      <td>100.0</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>74.0</td>
      <td>5.0</td>
      <td>16.0</td>
      <td>0.0</td>
      <td>67.0</td>
      <td>2.0</td>
      <td>100.0</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>60.0</td>
      <td>7.0</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>55.0</td>
      <td>8.0</td>
      <td>106.0</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>85.0</td>
      <td>7.0</td>
      <td>15.0</td>
      <td>1.0</td>
      <td>57.0</td>
      <td>4.0</td>
      <td>101.0</td>
      <td>10.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>65.0</td>
      <td>11.0</td>
      <td>16.0</td>
      <td>3.0</td>
      <td>77.0</td>
      <td>1.0</td>
      <td>84.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">France</th>
      <th>(20, 30]</th>
      <td>17.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>19.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>17.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>22.0</td>
      <td>0.0</td>
      <td>28.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>17.0</td>
      <td>3.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>12.0</td>
      <td>0.0</td>
      <td>27.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>18.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>32.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>23.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>18.0</td>
      <td>1.0</td>
      <td>25.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>22.0</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>0.0</td>
      <td>26.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>30.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>17.0</td>
      <td>1.0</td>
      <td>24.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">Iceland</th>
      <th>(20, 30]</th>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>7.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>15.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>5.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>17.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>8.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>5.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>12.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>7.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>6.0</td>
      <td>3.0</td>
      <td>9.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>9.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>10.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">Italy</th>
      <th>(20, 30]</th>
      <td>19.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>23.0</td>
      <td>0.0</td>
      <td>22.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>39.0</td>
      <td>8.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>29.0</td>
      <td>0.0</td>
      <td>45.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>36.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>27.0</td>
      <td>1.0</td>
      <td>40.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>27.0</td>
      <td>2.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>32.0</td>
      <td>1.0</td>
      <td>62.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>33.0</td>
      <td>2.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>27.0</td>
      <td>1.0</td>
      <td>52.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>33.0</td>
      <td>4.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>22.0</td>
      <td>0.0</td>
      <td>29.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>19.0</td>
      <td>5.0</td>
      <td>8.0</td>
      <td>0.0</td>
      <td>25.0</td>
      <td>1.0</td>
      <td>47.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">New Zealand</th>
      <th>(20, 30]</th>
      <td>13.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>1.0</td>
      <td>22.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>19.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>17.0</td>
      <td>1.0</td>
      <td>29.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>17.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>18.0</td>
      <td>1.0</td>
      <td>39.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>24.0</td>
      <td>2.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>29.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>33.0</td>
      <td>3.0</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>21.0</td>
      <td>0.0</td>
      <td>26.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>24.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>1.0</td>
      <td>17.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>23.0</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>15.0</td>
      <td>0.0</td>
      <td>21.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">United Kingdom</th>
      <th>(20, 30]</th>
      <td>12.0</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>1.0</td>
      <td>21.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>21.0</td>
      <td>2.0</td>
      <td>7.0</td>
      <td>0.0</td>
      <td>13.0</td>
      <td>3.0</td>
      <td>23.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>22.0</td>
      <td>2.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>0.0</td>
      <td>31.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>14.0</td>
      <td>3.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>14.0</td>
      <td>1.0</td>
      <td>24.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>15.0</td>
      <td>7.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>31.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>28.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>24.0</td>
      <td>1.0</td>
      <td>28.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>19.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>1.0</td>
      <td>29.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">United States</th>
      <th>(20, 30]</th>
      <td>21.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>16.0</td>
      <td>1.0</td>
      <td>21.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>(30, 40]</th>
      <td>21.0</td>
      <td>1.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>26.0</td>
      <td>1.0</td>
      <td>41.0</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>(40, 50]</th>
      <td>23.0</td>
      <td>3.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>30.0</td>
      <td>1.0</td>
      <td>31.0</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>(50, 60]</th>
      <td>27.0</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>25.0</td>
      <td>1.0</td>
      <td>40.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(60, 70]</th>
      <td>17.0</td>
      <td>6.0</td>
      <td>5.0</td>
      <td>2.0</td>
      <td>26.0</td>
      <td>2.0</td>
      <td>39.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>(70, 80]</th>
      <td>22.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>18.0</td>
      <td>5.0</td>
      <td>61.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>(80, 90]</th>
      <td>24.0</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>15.0</td>
      <td>3.0</td>
      <td>39.0</td>
      <td>2.0</td>
    </tr>
  </tbody>
</table>
</div>



The End...
