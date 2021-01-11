# Shopify Image Repo
<h2>Table of Contents</h2>
<ol>
<li>[Instructions for running the program from repo](#instructions)</li>
<li>Quick instructions on using the application</li>
<li>Different sections of application</li>
<li>AWS S3 and Google Vision API</li>
</ol>

<a name="instructions"></a>
<h2>Instructions for running the program from repo:</h2>
<u>Starting using the bash script:</u>
<ol>
<li>Download/clone repo (can download as ZIP)</li>
<li>In your terminal enter the main directory of the folder “shopify_image_repo”</li>
<li>Run 'chmod u+x start.sh'</li>
<li>Run './start.sh' or 'bash start.sh'</li>
<li>In your browser go to http://127.0.0.1:8000</li>
</ol>

<u>Manual start:</u>
<ol>
<li>Download/clone repo (can download as ZIP)</li>
<li>In your terminal enter the main directory of the folder “shopify_image_repo”</li>
<li>Run 'pip3 install -r requirements.txt —user'</li>
<li>Run 'python3 image_repo/manage.py makemigrations'</li>
<li>Run 'python3 image_repo/manage.py migrate'</li>
<li>Run 'python3 image_repo/manage.py runserver'</li>
<li>In your browser go to http://127.0.0.1:8000</li>
</ol>
<br>
<h2>Short instructions for first time using application</h2>

<h2>Home Page</h2>
<img src='./readme_img/home.jpg'/>
When first entering the site, the home page shows the image submission form at the top and the images that have been uploaded in the bottom half. When trying to submit an image without logging in, it will redirect the user to the log in page. The login page can also be accessed by clicking the 'Login' option in the top right corner. 

To register a new user click 

