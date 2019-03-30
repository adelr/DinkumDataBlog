---
date : 2018-10-05
slug : unicode_intro
mathjax : ture
title : Unicode strings in Python
author : Adel
categories: 
  - Python
  - blogging
tags: 
  - python
  - unicode
summary : An introduction to Unicode in Python 3
thumbnailImagePosition : left
thumbnailImage : ./static/img/avatar-icon.png
---

# 1. Unicode: an introduction.

Computers only understand one thing: <b>binary</b> code. For instance, when you type the letter "A" the computer
must represent this as a sequence of 0s and 1s.

Therefore we need a rule (code) for converting between characters and sequences of 0s and 1s. A basic way to do this is 
provided by the [ASCII code](http://www.ascii-code.com/).

The ASCII code uses 1 byte (8 bits) to encode 256 possible characters, corresponding to a binary number between 0 and $255 = 2^7+2^6+2^5+2^4+2^3+2^2+2^1+2^0$.

These can be split into 3 groups (see the link above). The usual characters used in English are those whose ASCII codes are between
32 and 127.

For instance the letter "A" corresponds to the number 65 which is treated by the computer as the binary sequence $1000001$.

In Python, the ASCII code of a given letter can be obtained using the <code>ord</code> function. It can be converted to binary using <code>bin</code>, and to hexadecimal (base 16) code using <code>hex</code>.

Conversely, the character corresponding to a given ASCII code can be obtained using the <code>chr</code> function. 


```python
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


print("Character: A")
print("ASCII code:", ord('A'))
print("Binary code:", bin(ord('A')))
print("Hexadecimal code:", hex(ord('A')))
print("chr(65):", chr(65))
```

<style>.container { width:100% !important; }</style>


    Character: A
    ASCII code: 65
    Binary code: 0b1000001
    Hexadecimal code: 0x41
    chr(65): A


The result above tells us that the __binary__ code for A (starting with `0b`) corresponds to the decimal number $2^6+2^0=64+1=65$.

Similarly, the __hexadecimal__ code (starting with `0x`) tells us that A corresponds to $4\times 16^1+1\times 16^0=64+1=65$ in old money (base 10).


Let's have a look at all the characters whose ASCII code is between 32 and 127


```python
print([chr(i) for i in range(32, 127)])
```

    [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']


<p>Because the ASCII code is using (at most) 1 byte, it cannot represent more than 256 characters. This is sufficient to writing English text but it's not enough to code other symbols such as non-English alphabet, accented characters, as well as more esoteric characters... Hence, another type of character encoding is needed.</p>
<p>Modern character encoding  is built on <b>Unicode</b> which contains (at this time) more than <a href="http://www.babelstone.co.uk/Unicode/HowMany.html">130,000 characters</a>. Note that not all web browsers/fonts are able to display all these characters. In Unicode each character is represented by a code point. When stored/processed by a computer the character is encoded on 1 or more bytes. </p>

<div style="background-color:#FBEFFB;"><p style="font-size:20px;color:#FF0080">&#9888; Beware!</p> <!--- Warning --->

<p><b>We mustn't confuse the code point and the byte encoding associated with any given character</b>.</p> 
<p>Think of the code point as an identification number for a character (kind of like your social security number). This code point is distinct from the binary representation of said character in terms of 1s and 0s. <p>How do we connect the two?</p> <p>That's what <b>encodings</b>  are for. An encoding provides a convention for passing from code point to bytes.</p>


<p>There are several encodings of Unicode characters. The main one for our purpose is called UTF-8. It uses a variable length encoding (1, 2, 3 or 4 bytes).</p>

<p>Unicode has the advantage of being a superset of ASCII. In other words, all the ASCII codes are also valid <a href="http://unicode-table.com/en/">Unicode codes</a>.</p>

<p>Here's an example. The <a href="http://www.fileformat.info/info/unicode/char/20aC/index.htm">euro sign</a>  &#8364; has code <code>U+20AC</code>.
The <code>U+</code> tells us it's a unicode code point and the <code>20AC</code> is a hexadecimal number (base 16) which corresponds to 8364 in base 10.</p>

<p>In Python 3 <b>strings are by default unicode</b>, so the type <code>str</code> holds for any valid unicode character, <em>not just those that can be encoded using ASCII</em>.</p>

<p>We can represent code points in Python using a special string starting with <code>\u</code>.</p>

</div>


```python
euro = '\u20AC'
print("Character:", euro)
print("Decimal code point:", ord(euro))
print("Hexadecimal code point:", hex(ord(euro)))
print("Binary code point:", bin(ord(euro)))
print("Type:", type(euro)) 
print("Character length:", len(euro))
```

    Character: €
    Decimal code point: 8364
    Hexadecimal code point: 0x20ac
    Binary code point: 0b10000010101100
    Type: <class 'str'>
    Character length: 1


<p>Notice that we have an string of type <code>str</code> and its length is 1 character. 
</p>
<p>Notice also that, in this case, the Unicode code point used by Python is actually based on the hexadecimal code associated with the character.</p>

<p>The hexadecimal value <code>20ac</code> corresponds to the decimal value $2\times 16^3+0\times 16^2+10\times 16^1+12\times 16^0=8192+160+12=8364$.</p>

<p>If we encode the string (character really) using UTF-8, we get its byte representation, which <b>has type <code>bytes</code> and is encoded over 3 bytes</b>.</p>


```python
euroUTF8 = euro.encode('utf-8')
print("UTF-8 encoded character:", euroUTF8)
print("UTF-8 encoded type:", type(euroUTF8)) 
print("UTF-8 encoded character length:", len(euroUTF8))
```

    UTF-8 encoded character: b'\xe2\x82\xac'
    UTF-8 encoded type: <class 'bytes'>
    UTF-8 encoded character length: 3


Contrast this with:


```python
A_UTF8 = 'A'.encode('utf-8')
print("UTF-8 encoded character:", A_UTF8)
print("UTF-8 encoded type:", type(A_UTF8)) 
print("UTF-8 encoded character length:", len(A_UTF8))
```

    UTF-8 encoded character: b'A'
    UTF-8 encoded type: <class 'bytes'>
    UTF-8 encoded character length: 1


__As long as we don't confuse unicode and bytes, and get our encodings right, we and Python strings will live happily for ever after.__

__One way to think about this is that we encode a string to pass it to the computer, and we decode it to show it to a human.__


```python
print("Unicode character:", euro)
print("UTF-8 encoded character:", euroUTF8)
print("Decoded bytes:", euroUTF8.decode('utf-8'))
```

    Unicode character: €
    UTF-8 encoded character: b'\xe2\x82\xac'
    Decoded bytes: €


Note that the default encoding on many systems (at least in the English speaking world) used to be ASCII, but UTF-8 has become the norm.

(There are some additional things happening with the `print` function, but we won't get into it here.)

Note that <code>ord</code> and <code>chr</code> work with Unicode.


```python
ord('€')
```

    8364




```python
chr(8364)
```

    '€'



You can also refer to unicode characters using their name in Python using the special <code>'\N{NAME}'</code> syntax.


```python
'\N{EURO SIGN}'
```

    '€'



Most of the agonising pain associated with Unicode in Python has to do with not specifying (or knowing) whether we're dealing with unicode or bytes.
    
Once that's clear, your Python code can handle non-ASCII characters. Let's start with something easy.

<h4> German</h4>


```python
s = 'Straße'
sUTF8 = s.encode('utf-8')
s, sUTF8
```

    ('Straße', b'Stra\xc3\x9fe')




```python
print("Length of s :", len(s))
print("Length of encoded s:", len(sUTF8))
```

    Length of s : 6
    Length of encoded s: 7



```python
print("Unicode :", [c for c in s])
```

    Unicode : ['S', 't', 'r', 'a', 'ß', 'e']



```python
print("UTF-8   :",[c for c in sUTF8])
```

    UTF-8   : [83, 116, 114, 97, 195, 159, 101]


<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
<p>Notice how the character ß is represented by the 2 bytes <code>\xc3\x9f</code> however, 223 is the code point for the German <em>Eszett</em>, so is there a problem? </p>    
</div>



```python
chr(223)
```

    'ß'



In base 16 (hexadecimal), <code>df</code> corresponds to the number 223.


```python
int('df', 16)
```

    223



We can specify a hexadecimal code in a string using the <code>\x</code> prefix.


```python
'\xdf'
```

    'ß'



So if <code>'\xdf'</code> represents our unicode character, what does <code>"\xc3\x9f"</code> represents?

It represents the encoding of our unicode character over 2 bytes using UTF-8.

We can decode the corresponding byte string and get the unicode character to print to the notebook.


```python
b"\xc3\x9f".decode('utf-8')
```

    'ß'



In a different encoding (e.g. `latin-1`), the same letter would be encoded as `\xdf`.


```python
s.encode('latin-1')
```

    b'Stra\xdfe'



#### French


```python
s = u"Les cons, ça ose tout. C'est même à ça qu'on les reconnaît."
sUTF8 = s.encode('utf-8')
print(s)
print(sUTF8)
```

    Les cons, ça ose tout. C'est même à ça qu'on les reconnaît.
    b"Les cons, \xc3\xa7a ose tout. C'est m\xc3\xaame \xc3\xa0 \xc3\xa7a qu'on les reconna\xc3\xaet."



```python
sLATIN1 = s.encode('latin-1')
print(s) 
print(sLATIN1)
```

    Les cons, ça ose tout. C'est même à ça qu'on les reconnaît.
    b"Les cons, \xe7a ose tout. C'est m\xeame \xe0 \xe7a qu'on les reconna\xeet."



```python
print("Length of s :", len(s), "\t",  
      "Length of UTF-8 encoded s:", len(sUTF8), "\t",  
      "Length of LATIN-1 encoded s:", len(sLATIN1),
      "\n")

print("Unicode :", [c for c in s], "\n")

print("UTF-8   :",[c for c in sUTF8], "\n")

print("Latin-1 :",[c for c in sLATIN1], "\n")
```

    Length of s : 59 	 Length of UTF-8 encoded s: 64 	 Length of LATIN-1 encoded s: 59 
    
    Unicode : ['L', 'e', 's', ' ', 'c', 'o', 'n', 's', ',', ' ', 'ç', 'a', ' ', 'o', 's', 'e', ' ', 't', 'o', 'u', 't', '.', ' ', 'C', "'", 'e', 's', 't', ' ', 'm', 'ê', 'm', 'e', ' ', 'à', ' ', 'ç', 'a', ' ', 'q', 'u', "'", 'o', 'n', ' ', 'l', 'e', 's', ' ', 'r', 'e', 'c', 'o', 'n', 'n', 'a', 'î', 't', '.'] 
    
    UTF-8   : [76, 101, 115, 32, 99, 111, 110, 115, 44, 32, 195, 167, 97, 32, 111, 115, 101, 32, 116, 111, 117, 116, 46, 32, 67, 39, 101, 115, 116, 32, 109, 195, 170, 109, 101, 32, 195, 160, 32, 195, 167, 97, 32, 113, 117, 39, 111, 110, 32, 108, 101, 115, 32, 114, 101, 99, 111, 110, 110, 97, 195, 174, 116, 46] 
    
    Latin-1 : [76, 101, 115, 32, 99, 111, 110, 115, 44, 32, 231, 97, 32, 111, 115, 101, 32, 116, 111, 117, 116, 46, 32, 67, 39, 101, 115, 116, 32, 109, 234, 109, 101, 32, 224, 32, 231, 97, 32, 113, 117, 39, 111, 110, 32, 108, 101, 115, 32, 114, 101, 99, 111, 110, 110, 97, 238, 116, 46] 
    


This is fine but these languages are using the usual latin alphabet with the exception of a few special characters such as accents.

What about languages that use a completely different alphabet? Let's find out.

#### Greek 
(source: http://sacred-texts.com/cla/homer/greek/ili01.htm)



```python
# unicode string
iliad =  "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
print(iliad)
print(type(iliad))
print(len(iliad))
```

    μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος
    <class 'str'>
    34



```python
# byte string
iliad = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος".encode('utf-8')
print(iliad)
print(type(iliad))
print(len(iliad))
```

    b'\xce\xbc\xe1\xbf\x86\xce\xbd\xce\xb9\xce\xbd \xe1\xbc\x84\xce\xb5\xce\xb9\xce\xb4\xce\xb5 \xce\xb8\xce\xb5\xe1\xbd\xb0 \xce\xa0\xce\xb7\xce\xbb\xce\xb7\xce\xb9\xcc\x88\xe1\xbd\xb1\xce\xb4\xce\xb5\xcf\x89 \xe1\xbc\x88\xcf\x87\xce\xb9\xce\xbb\xe1\xbf\x86\xce\xbf\xcf\x82'
    <class 'bytes'>
    70


<br>
<div style="background-color:#FBEFFB;"><p style="font-size:20px;color:#FF0080">&#9888; Stop and think!</p> <!--- Warning --->
So how many characters are there in the string? 70 or 34? 
How would you list the individual characters within the string?
</div>
<br>

The answer is 34. These are the actual characters that compose the string.

The encoded version will have a different number of bytes depending on the encoding.


```python
# unicode string
iliad =  "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"

L = [c for c in iliad]
for i, c in enumerate(L):
    print(i+1, "\t", c)
```

    1 	 μ
    2 	 ῆ
    3 	 ν
    4 	 ι
    5 	 ν
    6 	  
    7 	 ἄ
    8 	 ε
    9 	 ι
    10 	 δ
    11 	 ε
    12 	  
    13 	 θ
    14 	 ε
    15 	 ὰ
    16 	  
    17 	 Π
    18 	 η
    19 	 λ
    20 	 η
    21 	 ι
    22 	 ̈
    23 	 ά
    24 	 δ
    25 	 ε
    26 	 ω
    27 	  
    28 	 Ἀ
    29 	 χ
    30 	 ι
    31 	 λ
    32 	 ῆ
    33 	 ο
    34 	 ς



```python
# byte string
iliad_encoded =  "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος".encode('utf-8')

L = [c for c in iliad_encoded]
for i, c in enumerate(L):
    print(i+1, "\t", c)
```

    1 	 206
    2 	 188
    3 	 225
    4 	 191
    5 	 134
    6 	 206
    7 	 189
    8 	 206
    9 	 185
    10 	 206
    11 	 189
    12 	 32
    13 	 225
    14 	 188
    15 	 132
    16 	 206
    17 	 181
    18 	 206
    19 	 185
    20 	 206
    21 	 180
    22 	 206
    23 	 181
    24 	 32
    25 	 206
    26 	 184
    27 	 206
    28 	 181
    29 	 225
    30 	 189
    31 	 176
    32 	 32
    33 	 206
    34 	 160
    35 	 206
    36 	 183
    37 	 206
    38 	 187
    39 	 206
    40 	 183
    41 	 206
    42 	 185
    43 	 204
    44 	 136
    45 	 225
    46 	 189
    47 	 177
    48 	 206
    49 	 180
    50 	 206
    51 	 181
    52 	 207
    53 	 137
    54 	 32
    55 	 225
    56 	 188
    57 	 136
    58 	 207
    59 	 135
    60 	 206
    61 	 185
    62 	 206
    63 	 187
    64 	 225
    65 	 191
    66 	 134
    67 	 206
    68 	 191
    69 	 207
    70 	 130


#### What's going on?
We have a __sequence of bytes__ and we are outputing each individual byte value. 

Python has no way of knowing what characters these bytes represent, hence we see a bunch of numbers.

The same applies to any other language.
#### Hebrew 
(source: http://sacred-texts.com/bib/tan/gen001.htm)


```python
# unicode string
gen1 = "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ"
print(gen1) 
print(type(gen1))
print(len(gen1))
```

    בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ
    <class 'str'>
    64



```python
# byte string
gen1_UTF8 = "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ".encode('utf-8')
print(gen1_UTF8) 
print(type(gen1_UTF8))
print(len(gen1_UTF8))
```

    b'\xd7\x91\xd6\xbc\xd6\xb0\xd7\xa8\xd6\xb5\xd7\x90\xd7\xa9\xd7\x81\xd6\xb4\xd6\x96\xd7\x99\xd7\xaa \xd7\x91\xd6\xbc\xd6\xb8\xd7\xa8\xd6\xb8\xd6\xa3\xd7\x90 \xd7\x90\xd6\xb1\xd7\x9c\xd6\xb9\xd7\x94\xd6\xb4\xd6\x91\xd7\x99\xd7\x9d \xd7\x90\xd6\xb5\xd6\xa5\xd7\xaa \xd7\x94\xd6\xb7\xd7\xa9\xd7\x81\xd6\xbc\xd6\xb8\xd7\x9e\xd6\xb7\xd6\x96\xd7\x99\xd6\xb4\xd7\x9d \xd7\x95\xd6\xb0\xd7\x90\xd6\xb5\xd6\xa5\xd7\xaa \xd7\x94\xd6\xb8\xd7\x90\xd6\xb8\xd6\xbd\xd7\xa8\xd6\xb6\xd7\xa5'
    <class 'bytes'>
    122


#### Chinese 
(source: http://ctext.org/art-of-war)


```python
# unicode string
sun = "孫子曰：兵者，國之大事，死生之地，存亡之道，不可不察也"
print(sun) 
print(type(sun))
print(len(sun))
```

    孫子曰：兵者，國之大事，死生之地，存亡之道，不可不察也
    <class 'str'>
    27



```python
# byte string
sun_UTF8 = u"孫子曰：兵者，國之大事，死生之地，存亡之道，不可不察也".encode('utf-8')
print(sun_UTF8) 
print(type(sun_UTF8))
print(len(sun_UTF8))
```

    b'\xe5\xad\xab\xe5\xad\x90\xe6\x9b\xb0\xef\xbc\x9a\xe5\x85\xb5\xe8\x80\x85\xef\xbc\x8c\xe5\x9c\x8b\xe4\xb9\x8b\xe5\xa4\xa7\xe4\xba\x8b\xef\xbc\x8c\xe6\xad\xbb\xe7\x94\x9f\xe4\xb9\x8b\xe5\x9c\xb0\xef\xbc\x8c\xe5\xad\x98\xe4\xba\xa1\xe4\xb9\x8b\xe9\x81\x93\xef\xbc\x8c\xe4\xb8\x8d\xe5\x8f\xaf\xe4\xb8\x8d\xe5\xaf\x9f\xe4\xb9\x9f'
    <class 'bytes'>
    81


#### Other characters

Unicode is not restricted to what we may traditionally think as human languages. It also includes many other characters.

Let's create a helper function to print a large number of unicode characters in a nice way.


```python
def print_unicode(start, stop, width=30):
    for code in range(start, stop):
        end = '\n' if (code-start)%width==0 else ' '
        print(chr(code), end=end)
```

```python
print_unicode(128000, 128300)
```

    🐀
    🐁 🐂 🐃 🐄 🐅 🐆 🐇 🐈 🐉 🐊 🐋 🐌 🐍 🐎 🐏 🐐 🐑 🐒 🐓 🐔 🐕 🐖 🐗 🐘 🐙 🐚 🐛 🐜 🐝 🐞
    🐟 🐠 🐡 🐢 🐣 🐤 🐥 🐦 🐧 🐨 🐩 🐪 🐫 🐬 🐭 🐮 🐯 🐰 🐱 🐲 🐳 🐴 🐵 🐶 🐷 🐸 🐹 🐺 🐻 🐼
    🐽 🐾 🐿 👀 👁 👂 👃 👄 👅 👆 👇 👈 👉 👊 👋 👌 👍 👎 👏 👐 👑 👒 👓 👔 👕 👖 👗 👘 👙 👚
    👛 👜 👝 👞 👟 👠 👡 👢 👣 👤 👥 👦 👧 👨 👩 👪 👫 👬 👭 👮 👯 👰 👱 👲 👳 👴 👵 👶 👷 👸
    👹 👺 👻 👼 👽 👾 👿 💀 💁 💂 💃 💄 💅 💆 💇 💈 💉 💊 💋 💌 💍 💎 💏 💐 💑 💒 💓 💔 💕 💖
    💗 💘 💙 💚 💛 💜 💝 💞 💟 💠 💡 💢 💣 💤 💥 💦 💧 💨 💩 💪 💫 💬 💭 💮 💯 💰 💱 💲 💳 💴
    💵 💶 💷 💸 💹 💺 💻 💼 💽 💾 💿 📀 📁 📂 📃 📄 📅 📆 📇 📈 📉 📊 📋 📌 📍 📎 📏 📐 📑 📒
    📓 📔 📕 📖 📗 📘 📙 📚 📛 📜 📝 📞 📟 📠 📡 📢 📣 📤 📥 📦 📧 📨 📩 📪 📫 📬 📭 📮 📯 📰
    📱 📲 📳 📴 📵 📶 📷 📸 📹 📺 📻 📼 📽 📾 📿 🔀 🔁 🔂 🔃 🔄 🔅 🔆 🔇 🔈 🔉 🔊 🔋 🔌 🔍 🔎
    🔏 🔐 🔑 🔒 🔓 🔔 🔕 🔖 🔗 🔘 🔙 🔚 🔛 🔜 🔝 🔞 🔟 🔠 🔡 🔢 🔣 🔤 🔥 🔦 🔧 🔨 🔩 🔪 🔫 

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
These are characters, not images. You can write them to a file on your computer's hard drive, and read them back in.
</div>


```python
# UTF-8 is used by default on my machine
with open('unicode.txt', 'w') as f:
    for code in range(128000, 128300):
        f.write(chr(code))
```

```python
!cat unicode.txt
```

    🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿👀👁👂👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖💗💘💙💚💛💜💝💞💟💠💡💢💣💤💥💦💧💨💩💪💫💬💭💮💯💰💱💲💳💴💵💶💷💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋📌📍📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾📿🔀🔁🔂🔃🔄🔅🔆🔇🔈🔉🔊🔋🔌🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫

<div style="background-color:#F7F2E0;">
<h3> <font color=MediumVioletRed>Remark:</font> </h3>
We can also get Python to print out the names of the characters.
</div>


```python
import unicodedata
for c in range(128000, 128100):
    print(chr(c), unicodedata.name(chr(c)))
```

    🐀 RAT
    🐁 MOUSE
    🐂 OX
    🐃 WATER BUFFALO
    🐄 COW
    🐅 TIGER
    🐆 LEOPARD
    🐇 RABBIT
    🐈 CAT
    🐉 DRAGON
    🐊 CROCODILE
    🐋 WHALE
    🐌 SNAIL
    🐍 SNAKE
    🐎 HORSE
    🐏 RAM
    🐐 GOAT
    🐑 SHEEP
    🐒 MONKEY
    🐓 ROOSTER
    🐔 CHICKEN
    🐕 DOG
    🐖 PIG
    🐗 BOAR
    🐘 ELEPHANT
    🐙 OCTOPUS
    🐚 SPIRAL SHELL
    🐛 BUG
    🐜 ANT
    🐝 HONEYBEE
    🐞 LADY BEETLE
    🐟 FISH
    🐠 TROPICAL FISH
    🐡 BLOWFISH
    🐢 TURTLE
    🐣 HATCHING CHICK
    🐤 BABY CHICK
    🐥 FRONT-FACING BABY CHICK
    🐦 BIRD
    🐧 PENGUIN
    🐨 KOALA
    🐩 POODLE
    🐪 DROMEDARY CAMEL
    🐫 BACTRIAN CAMEL
    🐬 DOLPHIN
    🐭 MOUSE FACE
    🐮 COW FACE
    🐯 TIGER FACE
    🐰 RABBIT FACE
    🐱 CAT FACE
    🐲 DRAGON FACE
    🐳 SPOUTING WHALE
    🐴 HORSE FACE
    🐵 MONKEY FACE
    🐶 DOG FACE
    🐷 PIG FACE
    🐸 FROG FACE
    🐹 HAMSTER FACE
    🐺 WOLF FACE
    🐻 BEAR FACE
    🐼 PANDA FACE
    🐽 PIG NOSE
    🐾 PAW PRINTS
    🐿 CHIPMUNK
    👀 EYES
    👁 EYE
    👂 EAR
    👃 NOSE
    👄 MOUTH
    👅 TONGUE
    👆 WHITE UP POINTING BACKHAND INDEX
    👇 WHITE DOWN POINTING BACKHAND INDEX
    👈 WHITE LEFT POINTING BACKHAND INDEX
    👉 WHITE RIGHT POINTING BACKHAND INDEX
    👊 FISTED HAND SIGN
    👋 WAVING HAND SIGN
    👌 OK HAND SIGN
    👍 THUMBS UP SIGN
    👎 THUMBS DOWN SIGN
    👏 CLAPPING HANDS SIGN
    👐 OPEN HANDS SIGN
    👑 CROWN
    👒 WOMANS HAT
    👓 EYEGLASSES
    👔 NECKTIE
    👕 T-SHIRT
    👖 JEANS
    👗 DRESS
    👘 KIMONO
    👙 BIKINI
    👚 WOMANS CLOTHES
    👛 PURSE
    👜 HANDBAG
    👝 POUCH
    👞 MANS SHOE
    👟 ATHLETIC SHOE
    👠 HIGH-HEELED SHOE
    👡 WOMANS SANDAL
    👢 WOMANS BOOTS
    👣 FOOTPRINTS


Similarly, we can find out the names of the characters we used previously.


```python
for c in iliad:
    print(c, unicodedata.name(c))
```

    μ GREEK SMALL LETTER MU
    ῆ GREEK SMALL LETTER ETA WITH PERISPOMENI
    ν GREEK SMALL LETTER NU
    ι GREEK SMALL LETTER IOTA
    ν GREEK SMALL LETTER NU
      SPACE
    ἄ GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
    ε GREEK SMALL LETTER EPSILON
    ι GREEK SMALL LETTER IOTA
    δ GREEK SMALL LETTER DELTA
    ε GREEK SMALL LETTER EPSILON
      SPACE
    θ GREEK SMALL LETTER THETA
    ε GREEK SMALL LETTER EPSILON
    ὰ GREEK SMALL LETTER ALPHA WITH VARIA
      SPACE
    Π GREEK CAPITAL LETTER PI
    η GREEK SMALL LETTER ETA
    λ GREEK SMALL LETTER LAMDA
    η GREEK SMALL LETTER ETA
    ι GREEK SMALL LETTER IOTA
    ̈ COMBINING DIAERESIS
    ά GREEK SMALL LETTER ALPHA WITH OXIA
    δ GREEK SMALL LETTER DELTA
    ε GREEK SMALL LETTER EPSILON
    ω GREEK SMALL LETTER OMEGA
      SPACE
    Ἀ GREEK CAPITAL LETTER ALPHA WITH PSILI
    χ GREEK SMALL LETTER CHI
    ι GREEK SMALL LETTER IOTA
    λ GREEK SMALL LETTER LAMDA
    ῆ GREEK SMALL LETTER ETA WITH PERISPOMENI
    ο GREEK SMALL LETTER OMICRON
    ς GREEK SMALL LETTER FINAL SIGMA



```python
for c in gen1:
    print(c, unicodedata.name(c))
```

    ב HEBREW LETTER BET
    ּ HEBREW POINT DAGESH OR MAPIQ
    ְ HEBREW POINT SHEVA
    ר HEBREW LETTER RESH
    ֵ HEBREW POINT TSERE
    א HEBREW LETTER ALEF
    ש HEBREW LETTER SHIN
    ׁ HEBREW POINT SHIN DOT
    ִ HEBREW POINT HIRIQ
    ֖ HEBREW ACCENT TIPEHA
    י HEBREW LETTER YOD
    ת HEBREW LETTER TAV
      SPACE
    ב HEBREW LETTER BET
    ּ HEBREW POINT DAGESH OR MAPIQ
    ָ HEBREW POINT QAMATS
    ר HEBREW LETTER RESH
    ָ HEBREW POINT QAMATS
    ֣ HEBREW ACCENT MUNAH
    א HEBREW LETTER ALEF
      SPACE
    א HEBREW LETTER ALEF
    ֱ HEBREW POINT HATAF SEGOL
    ל HEBREW LETTER LAMED
    ֹ HEBREW POINT HOLAM
    ה HEBREW LETTER HE
    ִ HEBREW POINT HIRIQ
    ֑ HEBREW ACCENT ETNAHTA
    י HEBREW LETTER YOD
    ם HEBREW LETTER FINAL MEM
      SPACE
    א HEBREW LETTER ALEF
    ֵ HEBREW POINT TSERE
    ֥ HEBREW ACCENT MERKHA
    ת HEBREW LETTER TAV
      SPACE
    ה HEBREW LETTER HE
    ַ HEBREW POINT PATAH
    ש HEBREW LETTER SHIN
    ׁ HEBREW POINT SHIN DOT
    ּ HEBREW POINT DAGESH OR MAPIQ
    ָ HEBREW POINT QAMATS
    מ HEBREW LETTER MEM
    ַ HEBREW POINT PATAH
    ֖ HEBREW ACCENT TIPEHA
    י HEBREW LETTER YOD
    ִ HEBREW POINT HIRIQ
    ם HEBREW LETTER FINAL MEM
      SPACE
    ו HEBREW LETTER VAV
    ְ HEBREW POINT SHEVA
    א HEBREW LETTER ALEF
    ֵ HEBREW POINT TSERE
    ֥ HEBREW ACCENT MERKHA
    ת HEBREW LETTER TAV
      SPACE
    ה HEBREW LETTER HE
    ָ HEBREW POINT QAMATS
    א HEBREW LETTER ALEF
    ָ HEBREW POINT QAMATS
    ֽ HEBREW POINT METEG
    ר HEBREW LETTER RESH
    ֶ HEBREW POINT SEGOL
    ץ HEBREW LETTER FINAL TSADI



```python
for c in sun:
    print(c, unicodedata.name(c))
```

    孫 CJK UNIFIED IDEOGRAPH-5B6B
    子 CJK UNIFIED IDEOGRAPH-5B50
    曰 CJK UNIFIED IDEOGRAPH-66F0
    ： FULLWIDTH COLON
    兵 CJK UNIFIED IDEOGRAPH-5175
    者 CJK UNIFIED IDEOGRAPH-8005
    ， FULLWIDTH COMMA
    國 CJK UNIFIED IDEOGRAPH-570B
    之 CJK UNIFIED IDEOGRAPH-4E4B
    大 CJK UNIFIED IDEOGRAPH-5927
    事 CJK UNIFIED IDEOGRAPH-4E8B
    ， FULLWIDTH COMMA
    死 CJK UNIFIED IDEOGRAPH-6B7B
    生 CJK UNIFIED IDEOGRAPH-751F
    之 CJK UNIFIED IDEOGRAPH-4E4B
    地 CJK UNIFIED IDEOGRAPH-5730
    ， FULLWIDTH COMMA
    存 CJK UNIFIED IDEOGRAPH-5B58
    亡 CJK UNIFIED IDEOGRAPH-4EA1
    之 CJK UNIFIED IDEOGRAPH-4E4B
    道 CJK UNIFIED IDEOGRAPH-9053
    ， FULLWIDTH COMMA
    不 CJK UNIFIED IDEOGRAPH-4E0D
    可 CJK UNIFIED IDEOGRAPH-53EF
    不 CJK UNIFIED IDEOGRAPH-4E0D
    察 CJK UNIFIED IDEOGRAPH-5BDF
    也 CJK UNIFIED IDEOGRAPH-4E5F


The End.
