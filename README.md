
===============
Compare text and show the difference with color.


Install
===============
```
 pip install diffcolor
```

Useage
===============
show the help
```bash
python -m diffcolor
```

After that, diffcolor will read data from STDIN.

For more help, you can use the "-h" option.

So, the following test command
```bash
echo "Hello World\nHello Worll" | python -m diffcolor
```
It will output the following, the last "l" is different:

<div style="font-family:monospace; color:white; background-color:black; padding:5px; font-size:14px;">
<p>Hello World<br/>Hello Worl<span style="color:red">l</span></p>
</div>


By default, diffcolor compare each character in each frame of the data. You can use the "-s" parameter to specify the delimiter, such as the space. This "-s" parameter can be used multiple times. 
For example, the following command will compare the data frame using the space.

```bash
echo "Hello World\nHello Worll" | python -m diffcolor -s " "
```

It will output the following, the last word "Worll" is different:

<div style="font-family:monospace; color:white; background-color:black; padding:5px; font-size:14px;">
<p>Hello World<br/>Hello <span style="color:red">Worll</span></p>
</div>

By default, it splits data frames using line breaks(\n). But sometimes, we need a front end and a frame end to segment. We can use the "-b" parameter to specify the frame header and the "-e" parameter to specify the frame footer.

For example, the following command will splits the data frame begin with "[" and end with "]\n".

```bash
echo "[Hello World,\nI am Tom]\nThis is not a frame.\n[Hello Worll,\nI am Tim]" | python -m diffcolor -b="[" -e="]\n" -s=" "
```

It will output the following, the color of "This is not a frame." is gray, because it is not a frame:

<div style="font-family:monospace; color:white; background-color:black; padding:5px; font-size:14px;">
<p>[Hello World,<br/>I am Tom]<br/><span style="color:gray">This is not a frame.</span><br/>Hello <span style="color:red">Worll</span>,<br/>I am <span style="color:red">Tim]</span></p>
</div>

We can use the "-i" option to ignore the none frame data.

```bash
echo "[Hello World,\nI am Tom]\nThis is not a frame.\n[Hello Worll,\nI am Tim]" | python -m diffcolor -b="[" -e="]\n" -s=" " -i
```

It will output the following:

<div style="font-family:monospace; color:white; background-color:black; padding:5px; font-size:14px;">
<p>[Hello World,<br/>I am Tom]<br/>Hello <span style="color:red">Worll</span>,<br/>I am <span style="color:red">Tim]</span></p>
</div>

We can use the "-f" option to handled output appended data as the file grows. This option is like "tail -f", often used to handle growing log files.

The colors define you can use "-v" option to show.

```bash
python -m diffcolor -v
```

<div style="display: grid; grid-template-columns: 1fr 1fr; font-family: monospace; color: white; background: black; padding: 5px; font-size: 14px;">
    <div style="font-weight: bold;">TYPE</div>
    <div style="font-weight: bold;">COLOR</div>
    <div>NORMAL</div>
    <div>NORMAL</div>
    <div>DIFF</div>
    <div style="color: red;">DIFF</div>
    <div>IGNORE</div>
    <div style="color: gray;">DIFF</div>
    <div>MISS</div>
    <div style="color: green;">DIFF</div>
    <div>OVER</div>
    <div style="color: blue;">DIFF</div>
</div>

[Click to view more information!](https://github.com/sintrb/diffcolor)