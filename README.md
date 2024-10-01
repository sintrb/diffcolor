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

![](https://temp-static-qn.inruan.com/sin-imgs/WX20241001-214247.png)

By default, diffcolor compare each character in each frame of the data. You can use the "-s" parameter to specify the delimiter, such as the space. This "-s" parameter can be used multiple times. 
For example, the following command will compare the data frame using the space.

```bash
echo "Hello World\nHello Worll" | python -m diffcolor -s " "
```

It will output the following, the last word "Worll" is different:

![](https://temp-static-qn.inruan.com/sin-imgs/WX20241001-214354.png)

By default, it splits data frames using line breaks(\n). But sometimes, we need a front end and a frame end to segment. We can use the "-b" parameter to specify the frame header and the "-e" parameter to specify the frame footer.

For example, the following command will splits the data frame begin with "[" and end with "]\n".

```bash
echo "[Hello World,\nI am Tom]\nThis is not a frame.\n[Hello Worll,\nI am Tim]" | python -m diffcolor -b="[" -e="]\n" -s=" "
```

It will output the following, the color of "This is not a frame." is gray, because it is not a frame:

![](https://temp-static-qn.inruan.com/sin-imgs/WX20241001-214500.png)

We can use the "-i" option to ignore the none frame data.

```bash
echo "[Hello World,\nI am Tom]\nThis is not a frame.\n[Hello Worll,\nI am Tim]" | python -m diffcolor -b="[" -e="]\n" -s=" " -i
```

It will output the following:

![](https://temp-static-qn.inruan.com/sin-imgs/WX20241001-214542.png)

We can use the "-f" option to handled output appended data as the file grows. This option is like "tail -f", often used to handle growing log files.

The colors define you can use "-v" option to show.

```bash
python -m diffcolor -v
```

![](https://temp-static-qn.inruan.com/sin-imgs/WX20241001-214628.png)

[Click to view more information!](https://github.com/sintrb/diffcolor)