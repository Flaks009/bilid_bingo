import bs4
import pandas as pd
from io import BytesIO
import requests
import numpy

sheet = requests.get('https://docs.google.com/spreadsheets/d/1GWKa8DKPYauNm3S_RrJSolnXqZsgJ87W4LQdVWhvVCQ/export?gid=0&format=csv')
data = sheet.content
data = pd.Series(BytesIO(data))
data = data.str.decode("utf-8")
data = data.str.replace("\r\n","")
html = open('bingo_template.html')
df = pd.read_html(html)[0]

html_string = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="bingo.css" media="screen, print"/>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css" integrity="sha512-NhSC1YmyruXifcj/KFRWoC561YpHpc5Jtzgvbuzx5VozKpWvQ+4nXhPdFgmx8xqexRcpAglTj9sIBWINXa8x5w==" crossorigin="anonymous" />
    <title>Bingo</title>
</head>
<body>
    <div class ="main">
    <div class="header">
        <table class="header-table">
            <th>
                <td>B</td>
                <td>I</td>
                <td>L</td>
                <td>I</td>
                <td>D</td>
            </th>
        </table>
    </div>
    <div class="table">
    {}
    </div>
    <div id="download">
        <button onclick="download()" class="button" id="button-download">Download</button>
    </div>
    </div>
    <script>
        function download(){{
            button = document.getElementById("button-download")
            button.style.display = "none";
            window.print();
            button.style.display = "block";

        }}
    </script>
</body>
</html>
'''

#################################
row_data = data.sample(n=25)
array_split = numpy.array_split(numpy.array(row_data),5)
for row in df.itertuples():
    df[row.Index] = array_split[row.Index]

check_duplicated = df.stack().duplicated().reset_index()[0]

df.iloc[2,2] = '<img src="http://drive.google.com/uc?export=view&id=1-xh60-roPtxJzzfWrQSvQOAetypSas0s" id="img-center">'

with open('bingo_template.html', 'w') as f:
    f.write(html_string.format(df.to_html(index=False, header=False, escape=False)))