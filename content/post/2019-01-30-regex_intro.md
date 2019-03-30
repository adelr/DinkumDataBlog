---
date : 2019-01-30
slug : regex_intro
mathjax : ture
title : Introduction to regular expressions
author : Adel
categories: 
  - Python
  - blogging
tags: 
  - python
  - regex
summary : Great! Now you have at least one problem!
thumbnailImagePosition : left
thumbnailImage : ./static/img/avatar-icon.png
---

<div style="background-color:#FBEFFB;">
<hr style="height:5px;border:none;color:#333;background-color:#333;" />
<h3>Jamie Zawinski:</h3>
<blockquote><b>Some people, when confronted with a problem, think <em>"I know, I'll use regular expressions".</em> <br>Now they have two problems.</b></blockquote>

<hr style="height:5px;border:none;color:#333;background-color:#333;" />
</div>

<div>
<h2> 1. Prelude:</h2>
<h4>Regular expressions are powerful...</h4>
<br>
<figure>
<img src="http://imgs.xkcd.com/comics/regular_expressions.png" width="500">
<figcaption><center>http://xkcd.com/208/</center></figcaption>
</figure>

<br />
<br />
<h4> ...but at first, they can be puzzling.</h4>
<br>
<figure>
<img src="http://imgs.xkcd.com/comics/perl_problems.png" width="600">
<figcaption><center>http://xkcd.com/1171/</center></figcaption>
</figure>
</div>


```python
from math import *
import numpy as np
import pandas as pd
from pathlib import Path

%matplotlib inline
import matplotlib.pyplot as plt

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))
```

<style>.container { width:90% !important; }</style>


<div>
<h2> 2. Introduction</h2>
<p>A regular expression (<a href="http://en.wikipedia.org/wiki/Regular_expression">regex</a>) is a sequence of literal characters, and metacharacters, which defines <b>search patterns</b>. </p>

<p>Most programming languages have some implementation of regular expressions, however, their syntax may vary.</p>

<p>One basic example is the asterisk used as a wildcard by most file systems to denote any number of characters. </p>

<p>For instance, <code>*.txt</code> 
denotes all files with a <code>.txt</code> extension.</p>

<p>The most elementary search pattern is the one that consists of the very characters you're looking for. </p>

<p>The <code>find</code> method of strings does just that.</p>
</div>


```python
s = "To be or not to be"
print(s.find('not'), s.find('question'))
```

    9 -1


__For a more general, and powerful approach to pattern searching, Python has the `re` module__


```python
import re
```

We'll use the opening paragraphs from _A Tale of Two Cities_ as an example.


```python
dickens = '''
It was the best of times, it was the worst of times, 
it was the age of wisdom, it was the age of foolishness, it was the epoch of belief,
it was the epoch of incredulity, it was the season of Light, it was the season of Darkness,
it was the spring of hope, it was the winter of despair, we had everything before us, we had
nothing before us, we were all going direct to Heaven, we were all going direct the other way -
in short, the period was so far like the present period, that some of its noisiest authorities
insisted on its being received, for good or for evil, in the superlative degree of comparison only.

There were a king with a large jaw and a queen with a plain face, on the
throne of England; there were a king with a large jaw and a queen with
a fair face, on the throne of France. In both countries it was clearer
than crystal to the lords of the State preserves of loaves and fishes,
that things in general were settled for ever.

It was the year of Our Lord one thousand seven hundred and seventy-five.
Spiritual revelations were conceded to England at that favoured period,
as at this. Mrs. Southcott had recently attained her five-and-twentieth
blessed birthday, of whom a prophetic private in the Life Guards had
heralded the sublime appearance by announcing that arrangements were
made for the swallowing up of London and Westminster. Even the Cock-lane
ghost had been laid only a round dozen of years, after rapping out its
messages, as the spirits of this very year last past (supernaturally
deficient in originality) rapped out theirs. Mere messages in the
earthly order of events had lately come to the English Crown and People,
from a congress of British subjects in America: which, strange
to relate, have proved more important to the human race than any
communications yet received through any of the chickens of the Cock-lane
brood.
'''
```

<h3> <center><font color=MediumVioletRed>A. Literals</font></center></h3>

__The <code>search</code> method of the <code>re</code> module returns a <code>_sre.SRE_Match</code> object which has some useful properties.__


```python
result = re.search('times', dickens)

print(type(result))
print(*[item for item in dir(result) if not item.startswith('_')], sep='\n')
```

    <class '_sre.SRE_Match'>
    end
    endpos
    expand
    group
    groupdict
    groups
    lastgroup
    lastindex
    pos
    re
    regs
    span
    start
    string


__The result of the search will tell us if, and where the pattern is found in the string.__


```python
print("result.span(): ", result.span())

print("result.group():", result.group())

s = result.span()

print(dickens[s[0]:s[1]])
```

    result.span():  (20, 25)
    result.group(): times
    times


__There are other useful functions for finding a pattern beside the <code>search</code> function.</h4>__

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3><br />
If a search pattern is to be reused, it is faster to <em>compile</em> it first. We'll do that henceforth.
 <br>
</div>


```python
pattern = re.compile(r'times')

# only matches the beginning of the string.
result = pattern.match(dickens)
print('match:  ', result)

# search for first match
result = pattern.search(dickens)
print('search: ', result.group())

# returns a list of all matches.
result = pattern.findall(dickens)
print('findall:', result)
```

    match:   None
    search:  times
    findall: ['times', 'times']


<div style="background-color:#F7F2E0;">
<h4> <font color=MediumVioletRed>Note:</font> </h4>
<p>What we've used above is an example of search pattern involving literals. 
<b>The pattern was the very string we were looking for.</b></p>

<p>Notice that we didn't have to worry about punctuation. The pattern is the only sub-string returned by the <code>search</code> or <code>findall</code> function, if it is found.</p>
</div>


<h3> <center><font color=MediumVioletRed>B. Character classes</font></center></h3>

Sometimes we'd like to consider variants of a string. For, instance, `"It"` and `"it"`.

This means that we need to look for __either__ an uppercase "i" or a lowercase one, followed by the letter "t".

Character classes are specified using __square brackets__.


```python
pattern = re.compile(r'[Ii]t')

result = pattern.findall(dickens)

print(result)
```

    ['It', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'it', 'It', 'it', 'it', 'it', 'it', 'it']


This is a simple example of character set. 

<code>[Ii]</code> means match <b>any one</b> of the characters between the square brackets.

Using character sets allows us to greatly simplify our syntax. 


Python has some <b>predefined character sets</b> which help us write compact code.

<table style="width:90%">
  <th>Character Class
  </th>
  <th>Matches
  </th>
  <tr>
      <td><code>[A-Z]</code></td>
      <td><b>any single</b> letter of the Latin alphabet in uppercase</td> 
  </tr>
  <tr>
      <td><code>[a-z]</code></td>
      <td><b>any single</b>  letter of the Latin alphabet in uppercase</td> 
  </tr>
  <tr>
      <td><code>[A-z]</code></td>
      <td><b>any single</b>  letter of the Latin alphabet in either lowercase or uppercase</td> 
  </tr>
  <tr>
      <td><code>[0-9]</code></td>
      <td><b>any single digit</b> between 0 and 9</td> 
  </tr>  <tr>
    <td><code>[^0-9]</code></td>
    <td><b>any character except for single digit</b> between 0 and 9</td> 
  </tr>
</table>

<p>Here's an example:</p>


```python
re.findall(r'[0-9]', "Today is the 23rd of May")
```

    ['2', '3']




```python
re.findall(r'[A-z]', "Today is the 23rd of May")
```

    ['T',
     'o',
     'd',
     'a',
     'y',
     'i',
     's',
     't',
     'h',
     'e',
     'r',
     'd',
     'o',
     'f',
     'M',
     'a',
     'y']




```python
re.findall(r'[^A-z ]', "Today is the 23rd of May")
```

    ['2', '3']




```python
re.findall(r'[^0-9]', "Today is the 23rd of May")
```

    ['T',
     'o',
     'd',
     'a',
     'y',
     ' ',
     'i',
     's',
     ' ',
     't',
     'h',
     'e',
     ' ',
     'r',
     'd',
     ' ',
     'o',
     'f',
     ' ',
     'M',
     'a',
     'y']



Back to our long string.

If we were searching for a substring made of any single uppercase letter followed by any single lower case letter
we could write:



```python
pattern = re.compile(r'[A-Z][a-z]')
result = pattern.findall(dickens)
print(result)
```

    ['It', 'Li', 'Da', 'He', 'Th', 'En', 'Fr', 'In', 'St', 'It', 'Ou', 'Lo', 'Sp', 'En', 'Mr', 'So', 'Li', 'Gu', 'Lo', 'We', 'Ev', 'Co', 'Me', 'En', 'Cr', 'Pe', 'Br', 'Am', 'Co']


<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Note:</font> </h3>
<ul>
<li>Notice that except for a couple of elements in the list, we didn't get entire words. 
</li><br>
<li>The regular expression only specifies a pattern with one uppercase letter, followed by one lower case letter.</li><br>
<li>That's usually not what you're after. You'd probably want to extract <b>whole words</b> which start with an uppercase letter, followed by any number of lowercase letters (capitalised words).  </li>
</ul>

</div>

__Maybe all we need is to add more `[a-z]` sets to our patterns? Let's try that...__


```python
pattern = re.compile(r'[A-Z][a-z][a-z]')
result = pattern.findall(dickens)
print(result)
```

    ['Lig', 'Dar', 'Hea', 'The', 'Eng', 'Fra', 'Sta', 'Our', 'Lor', 'Spi', 'Eng', 'Mrs', 'Sou', 'Lif', 'Gua', 'Lon', 'Wes', 'Eve', 'Coc', 'Mer', 'Eng', 'Cro', 'Peo', 'Bri', 'Ame', 'Coc']


__That's not really what we want.__

Sure we've now got one more lowercase letter after the first, uppercase one, but we still don't have whole words, unless our string contains capitalised, three-letter words. To top it off, we've now lost `"It"`!

In other words, unless you want to only extract capitalised words, with a __specific number of letter__, this is not the way to go. 

Actually, even in that case, this is not a smart way to do it.

If we wanted to find all the capitalised words that are, say, 10 letters long, we don't really want to have to type a pattern such as: 
```

[A-Z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]
```

We need a way to specify that we want __one or more__ lowercase letters.

For this we need more than literals or character sets, we need __metacharacters__.

<h3><center><font color=MediumVioletRed>C. Metacharacters</font></center></h3>

Literals are characters which are simply part of the pattern we are looking for. 

Metacharacters, on the other hand, act like <b>modifiers</b>. They change how the literals, or character classes are handled.

By default each literal is matched only once. By using the <code>+</code> symbol, any character or character class appearing <b>just before</b>  the metacharacter will be matched <b>one or more times</b>.

There are several modifiers that we can use.

<table style="width:60%">
  <th>Modifier
  </th>
  <th>Number of occurences
  </th>
  <tr>
      <td><code>+</code></td>
    <td><b>one</b> or more</td> 
  </tr>
  <tr>
      <td><code>*</code></td>
    <td><b>zero</b> or more</td> 
  </tr>
  <tr>
      <td><code>?</code></td>
    <td>zero or one</td> 
  </tr>
  <tr>
      <td><code>{m}</code></td>
      <td><code>m</code> times</td> 
  </tr> 
  <tr>
      <td><code>{m, n}</code></td>
      <td>between <code>m</code> and <code>n</code> times</td> 
  </tr> 
</table>


<p>For instance, if we wanted to extract a list of the words that are capitalised in a string, in the past we may have written something like this:</p>


```python
print([word for word in dickens.strip().split() if word[0].isupper() and word[1].islower()])
```

    ['It', 'Light,', 'Darkness,', 'Heaven,', 'There', 'England;', 'France.', 'In', 'State', 'It', 'Our', 'Lord', 'Spiritual', 'England', 'Mrs.', 'Southcott', 'Life', 'Guards', 'London', 'Westminster.', 'Even', 'Cock-lane', 'Mere', 'English', 'Crown', 'People,', 'British', 'America:', 'Cock-lane']


Notice, however, that some of the words have punctuation symbols attached to them.

No big deal, we know how to deal with this.


```python
import string 
print([word.strip(string.punctuation) for word in dickens.split() if word[0].isupper() and word[1].islower()])
```

    ['It', 'Light', 'Darkness', 'Heaven', 'There', 'England', 'France', 'In', 'State', 'It', 'Our', 'Lord', 'Spiritual', 'England', 'Mrs', 'Southcott', 'Life', 'Guards', 'London', 'Westminster', 'Even', 'Cock-lane', 'Mere', 'English', 'Crown', 'People', 'British', 'America', 'Cock-lane']


That worked fine, however the syntax is a bit unwieldy. 

Another version could be.


```python
import string 
print([word.strip(string.punctuation) for word in dickens.strip().split() 
 if word.istitle()])
```

    ['It', 'Light', 'Darkness', 'Heaven', 'There', 'England', 'France', 'In', 'State', 'It', 'Our', 'Lord', 'Spiritual', 'England', 'Mrs', 'Southcott', 'Life', 'Guards', 'London', 'Westminster', 'Even', 'Mere', 'English', 'Crown', 'People', 'British', 'America']


Notice, however, that we lost a word...

__Using a regular expression, we can specify character sets which match our pattern.__


```python
pattern = re.compile(r'[A-Z][a-z]+')
result = pattern.findall(dickens)
print(result)
```

    ['It', 'Light', 'Darkness', 'Heaven', 'There', 'England', 'France', 'In', 'State', 'It', 'Our', 'Lord', 'Spiritual', 'England', 'Mrs', 'Southcott', 'Life', 'Guards', 'London', 'Westminster', 'Even', 'Cock', 'Mere', 'English', 'Crown', 'People', 'British', 'America', 'Cock']


__Notice that with this pattern, hyphenated words are split and only the first part is returned. Let's handle this case.__


```python
pattern = re.compile(r'[A-Z][a-z]+-?[a-z]*')
result = pattern.findall(dickens)
print(result)
```

    ['It', 'Light', 'Darkness', 'Heaven', 'There', 'England', 'France', 'In', 'State', 'It', 'Our', 'Lord', 'Spiritual', 'England', 'Mrs', 'Southcott', 'Life', 'Guards', 'London', 'Westminster', 'Even', 'Cock-lane', 'Mere', 'English', 'Crown', 'People', 'British', 'America', 'Cock-lane']


<h3><center><font color=MediumVioletRed>D. Other built-in character classes and metacharacters</font></center></h3>

<table style="width:90%">
  <th>Class
  </th>
  <th>Matches
  </th>
  <tr>
      <td><code>.</code></td>
      <td>any character except <code>\n</code></td> 
  </tr>
  <tr>
      <td><code>\d</code></td>
    <td>Any numeric character</td> 
  </tr>
  <tr>
      <td><code>\D</code></td>
    <td>Non-numeric character</td> 
  </tr>
  <tr>
      <td><code>\w</code></td>
      <td>alphanumeric characters (same as <code>[0-9a-zA-Z_]</code>)</td> 
  </tr>
  <tr>
      <td><code>\W</code></td>
    <td>Non-alphanumeric characters</td> 
  </tr>
  <tr>
      <td><code>\b</code></td>
    <td>word boundary</td> 
  </tr> 
  <tr>
      <td><code>\s</code></td>
      <td>whitespace character (including <code>\n</code>, <code>\t</code>)</td> 
  </tr> 
  <tr>
      <td><code>\S</code></td>
    <td>Non-whitespace character </td> 
  </tr> 
  <tr>
      <td><code>^</code></td>
    <td>Start of line </td> 
  </tr> 
  <tr>
    <td><code>$</code></td>
    <td>End of line </td> 
  </tr> 
</table>

__First word of each sentence.__

We use `re.MULTILINE` to have the patterned searched across more than one line.


```python
result = re.findall(r'^\w+', dickens, re.MULTILINE)
print(result)
```

    ['It', 'it', 'it', 'it', 'nothing', 'in', 'insisted', 'There', 'throne', 'a', 'than', 'that', 'It', 'Spiritual', 'as', 'blessed', 'heralded', 'made', 'ghost', 'messages', 'deficient', 'earthly', 'from', 'to', 'communications', 'brood']


__Last word of each sentence.__

This is a bit more tricky. First note the following:


```python
result = re.findall(r'\w+$', dickens, re.MULTILINE)
print(result)
```

    ['had', 'authorities', 'the', 'with', 'clearer', 'twentieth', 'had', 'were', 'lane', 'its', 'supernaturally', 'the', 'strange', 'any', 'lane']


The problem here is that our pattern will only consider a word as being a match if it is at the end of a line if there is no other character after it.

Let's try to include the possibility of a punctuation symbol.


```python
result = re.findall(r'\w+.?$', dickens, re.MULTILINE)
print(result)
```

    ['belief,', 'Darkness,', 'had', 'authorities', 'only.', 'the', 'with', 'clearer', 'fishes,', 'ever.', 'five.', 'period,', 'twentieth', 'had', 'were', 'lane', 'its', 'supernaturally', 'the', 'People,', 'strange', 'any', 'lane', 'brood.']


That's better but we don't actually want the punctuation symbols to appear in the result. 

<h3> <center><font color=MediumVioletRed>E. Capture Groups</font></center></h3>

We can use a __capture group__ to specify which part of the pattern should be returned as a group, using parentheses.

Let's first see how this works on a simple example.

__No groups__

We get a list back.


```python
re.findall(r'\w+\s\d+\w{0,2}', "Let's meet on November 9 at 5pm, or November 12 at 11am or 4pm.")
```

    ['November 9', 'at 5pm', 'November 12', 'at 11am', 'or 4pm']



__2 capture groups__

We get a list of tuples with 2 elements.


```python
re.findall(r'(\w+)\s(\d+)\w{0,2}', "Let's meet on November 9 at 5pm, or November 12 at 11am or 4pm.")
```

    [('November', '9'), ('at', '5'), ('November', '12'), ('at', '11'), ('or', '4')]



__1 non-capture group, starting with `(?:` and 1 capture group.__


```python
re.findall(r'(?:\w+)\s(\d+)\w{0,2}', "Let's meet on November 9 at 5pm, or November 12 at 11am or 4pm.")
```

    ['9', '5', '12', '11', '4']



__Note:__

This example is a bit lame. The same result could be achieved more simply, but it illustrates how non-capture groups work.


```python
re.findall(r'\d+', "Let's meet on November 9 at 5pm, or November 12 at 11am or 4pm.")
```

    ['9', '5', '12', '11', '4']



__Back to our problem of finding the last words of each line.__


```python
result = re.findall(r'(\w+).?$', dickens, re.MULTILINE)
print(result)
```

    ['belief', 'Darkness', 'had', 'authorities', 'only', 'the', 'with', 'clearer', 'fishes', 'ever', 'five', 'period', 'twentieth', 'had', 'were', 'lane', 'its', 'supernaturally', 'the', 'People', 'strange', 'any', 'lane', 'brood']


Almost there. We just need to take care of hyphenated words and whitespaces.


```python
# You can usually write multiple regular expressions to perform a task,
# however, it's best to try and make the regular expression as discriminating as possible.

# Method 1
result = re.findall('([\w+-?]+\w+).?[\s-]*$', dickens, re.MULTILINE)
print(result)


# Method 2
result = re.findall('([\w+-?]+\w+).?\W*$', dickens, re.MULTILINE)
print(result)


# Method 3
result = re.findall('([\w-]+)\W*$', dickens, re.MULTILINE)
print(result)
```

    ['times', 'belief', 'Darkness', 'had', 'way', 'authorities', 'only', 'the', 'with', 'clearer', 'fishes', 'ever', 'seventy-five', 'period', 'five-and-twentieth', 'had', 'were', 'Cock-lane', 'its', 'supernaturally', 'the', 'People', 'strange', 'any', 'Cock-lane', 'brood']
    ['times', 'belief', 'Darkness', 'had', 'way', 'authorities', 'only', 'the', 'with', 'clearer', 'fishes', 'ever', 'seventy-five', 'period', 'five-and-twentieth', 'had', 'were', 'Cock-lane', 'its', 'supernaturally', 'the', 'People', 'strange', 'any', 'Cock-lane', 'brood']
    ['times', 'belief', 'Darkness', 'had', 'way', 'authorities', 'only', 'the', 'with', 'clearer', 'fishes', 'ever', 'seventy-five', 'period', 'five-and-twentieth', 'had', 'were', 'Cock-lane', 'its', 'supernaturally', 'the', 'People', 'strange', 'any', 'Cock-lane', 'brood']


<h2>3. Data Extraction</h2>

<p>When we're working with data you haven't generated, we usually have little control over the formatting of the data.</p>

<p>What's worse, the formatting can be inconsistent. This is where regular expression can be extremely useful.</p>

<p>Consider the data below. We'd like to extract the credit card information for each entry.<p> 

<p>Notice that the credit card numbers are not formatted in a consistent way.</p>


```python
messy_data = '''
Ms. Dixie T Patenaude 18 rue Descartes STRASBOURG Alsace 67100 FR France Dixie.Patenaude@teleworm.us Shound Cheecaey3s 03.66.62.81.38 Grondin 4/15/1958 MasterCard 5379 7969 2881 8421 958 12/2017 nan 1Z 114 58A 80 2148 893 8 Blue Safety specialist Atlas Realty 2000 Subaru Outback AnalystWatch.fr O- 191.0 86.8 5' 11" 156 dd0548bb-a8b5-438d-b181-c76ad282a9a1 48.577584 7.842637
Mr. Silvano G Romani 34 Faunce Crescent WHITE TOP NSW 2675 AU Australia Silvano-Romani@einrot.com Pock1993 AeV7ziek (02) 6166 5988 Sagese 2/25/1993 MasterCard 5253-7637-4959-3303 404 06-2018 nan 1Z 814 E43 42 9322 015 2 Green Coin vending and amusement machine servicer repairer Miller & Rhoads 1998 Honda S-MX StarJock.com.au B+ 128.3 58.3 6' 2" 189 7e310daa-46f5-407e-8dda-d975715ac4d5 -33.429793 145.234214
Mr. Felix C Fried 37 Jubilee Drive CAXTON nan CB3 5WG GB United Kingdom FelixFried@rhyta.com Derser Aisequ0haz 078 1470 0903 Eisenhauer 1/19/1933 Visa 4716046346218902 738 02 2018 SP 39 75 51 D 1Z V88 635 94 7608 112 4 Blue School psychologist Wetson's 2001 Audi Allroad MoverRelocation.co.uk O+ 188.5 85.7 5' 7" 169 95515377-74a9-4c1e-9117-44b9753dad8c 51.922175 -0.353221
'''
```

```python
credit_card_number = re.compile(r'(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})')
```

```python
credit_card_number.findall(messy_data)
```

    ['5379 7969 2881 8421', '5253-7637-4959-3303', '4716046346218902']



Let's write a regular expression called `height` to extract the height of each person in the data.


```python
height = re.compile(r'(\d)\'\s+(\d{,2})"')

height.findall(messy_data)
```

    [('5', '11'), ('6', '2'), ('5', '7')]



__For more complex patterns we can use _named_ capture groups.__

<h3> <center><font color=MediumVioletRed>A. Named Capture Groups</font></center></h3>

<p>Let's write a regular expression that will extract not just the credit card number, but also the card type, CCV number, and expiry date.</p>

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Note:</font> </h3>
<p>When you are extracting several groups that correspond to a particular type of information, it's often useful to associate a name with each group. That's what named groups allow you to do.</p>

<p>A named group has the form <code>(?P&lt;name&gt;regex)</code>.</p>
</div>


```python
credit_card_details = re.compile(r'(?P<CardType>Visa|MasterCard).*'
                                 r'(?P<CardNumber>\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})[-\s]?'
                                 r'(?P<CCV>\d{3})\s+'
                                 r'(?P<Expiry>\d{2}[- /]{1}\d{4})')
```

```python
for line in messy_data.strip().splitlines():
    print(credit_card_details.search(line).groupdict())
```

    {'CardType': 'MasterCard', 'CardNumber': '5379 7969 2881 8421', 'CCV': '958', 'Expiry': '12/2017'}
    {'CardType': 'MasterCard', 'CardNumber': '5253-7637-4959-3303', 'CCV': '404', 'Expiry': '06-2018'}
    {'CardType': 'Visa', 'CardNumber': '4716046346218902', 'CCV': '738', 'Expiry': '02 2018'}


We can get a nicer output by transforming the dictionary into a dataframe.


```python
pd.DataFrame([credit_card_details.search(line).groupdict() for line in  messy_data.strip().splitlines()])
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
      <th>CCV</th>
      <th>CardNumber</th>
      <th>CardType</th>
      <th>Expiry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>958</td>
      <td>5379 7969 2881 8421</td>
      <td>MasterCard</td>
      <td>12/2017</td>
    </tr>
    <tr>
      <th>1</th>
      <td>404</td>
      <td>5253-7637-4959-3303</td>
      <td>MasterCard</td>
      <td>06-2018</td>
    </tr>
    <tr>
      <th>2</th>
      <td>738</td>
      <td>4716046346218902</td>
      <td>Visa</td>
      <td>02 2018</td>
    </tr>
  </tbody>
</table>
</div>



Let's now write a regular expression <code>email</code> that will extract the email address from our data, and return the login and internet service provider for each entry, as two named capture groups. 


```python
email = re.compile(r'(?P<Login>[\w.-]+)@(?P<ISP>[\w.-]+)')

pd.DataFrame([email.search(line).groupdict() for line in  messy_data.strip().splitlines()])
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
      <th>ISP</th>
      <th>Login</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>teleworm.us</td>
      <td>Dixie.Patenaude</td>
    </tr>
    <tr>
      <th>1</th>
      <td>einrot.com</td>
      <td>Silvano-Romani</td>
    </tr>
    <tr>
      <th>2</th>
      <td>rhyta.com</td>
      <td>FelixFried</td>
    </tr>
  </tbody>
</table>
</div>



<h3> <center><font color=MediumVioletRed>B. Pandas &amp; Regular expressions</font></center></h3>

For more complex data sets we can of course combine the strengths of regular expressions and Pandas.

As an example, let's revisit the birthday formatting problem of a previous post.


```python
path = Path("data/people.csv")
data = pd.read_csv(path, encoding='utf-8')
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



<p>We'd like the dates to be formatted as <code>year-month-day</code>.</p>

<p>In a previous notebook we worked out a solution using the <code>datetime</code> module.</p>

<p>Let's do this using regular expressions.</p>

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>In a previous post we did more than simply change the format of the dates. We created a special datetime objects which can be used to perform <b>computations</b> on dates. Here we're merely focussing on the formatting aspect to illustrate how regular expressions can be combined with our usual Pandas workflow.</p>
</div>


```python
# Compile the regex first for increased speed.
birthday = re.compile(r'(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{2,4})')

def transform_birthday(row):
    date = birthday.search(row['Birthday']).groupdict()
    return "-".join([date['year'], date['month'], date['day']])
    
data['Birthday'] = data.apply(transform_birthday, axis=1)
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
      <td>1968-8-25</td>
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
      <td>1962-1-31</td>
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
      <td>1964-1-10</td>
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
      <td>1933-4-12</td>
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
      <td>1946-11-20</td>
      <td>A+</td>
    </tr>
  </tbody>
</table>
</div>



__By using Pandas' advanced regex syntax we can achieve the same thing in one line of code.__

Let's reload the original data.


```python
data = pd.read_csv(path, encoding='utf-8')
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



We can extract the day, month and year of birth for each person in one line of code by passing the compiled regex to the 
`str.extract` method of our Pandas Series corresponding to the `Birthday` column.


```python
data.Birthday.str.extract(birthday, expand=True).head()
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
      <th>day</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>8</td>
      <td>25</td>
      <td>1968</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>31</td>
      <td>1962</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>10</td>
      <td>1964</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>12</td>
      <td>1933</td>
    </tr>
    <tr>
      <th>4</th>
      <td>11</td>
      <td>20</td>
      <td>1946</td>
    </tr>
  </tbody>
</table>
</div>



Note that the names of the columns have been automatically extracted from the named groups of the regex `birthday`.

Using this, we can use the `apply` method to process the date in the format that we want.

For more clarity, we wrap our method chaining expression in parentheses, which allows us to write each method call on a new line.


```python
data.Birthday = (data
                     .Birthday
                     .str
                     .extract(birthday, expand=True)
                     .apply(lambda date:"-".join([date['year'], 
                                                  date['month'], 
                                                  date['day']]), 
                            axis=1)
                )
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
      <td>1968-8-25</td>
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
      <td>1962-1-31</td>
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
      <td>1964-1-10</td>
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
      <td>1933-4-12</td>
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
      <td>1946-11-20</td>
      <td>A+</td>
    </tr>
  </tbody>
</table>
</div>



__That being said, the best way to achieve our goal in pandas is to let it parse the dates automatically!__


```python
data = pd.read_csv(path, encoding='utf-8', parse_dates=['Birthday'])
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
      <td>1968-08-25</td>
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
      <td>1962-01-31</td>
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
      <td>1964-01-10</td>
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
      <td>1933-04-12</td>
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
      <td>1946-11-20</td>
      <td>A+</td>
    </tr>
  </tbody>
</table>
</div>




```python
data.dtypes
```

    GivenName                object
    Surname                  object
    Gender                   object
    StreetAddress            object
    City                     object
    Country                  object
    Birthday         datetime64[ns]
    BloodType                object
    dtype: object



The End...
