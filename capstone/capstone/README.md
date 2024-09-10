# Song List Web Application:
## CS50 Web Final Project: 
For my final CS50 web project I created an application that stores the names and artists of several songs, each user has their own list of songs.

## Distinctiveness and Complexity: 
I believe that this project is complex enough because I have spent several days and hours working on it, have cried several tears and completed this in less than two weeks because of my college's requirements. If I had more time I could have incorporated more features that would probably make the project pass on all of the requirements that you, as Harvard have given me. 
However I do believe that this project has a large scalability potential on which I will keep working even after submitting it.

## Basic idea behind the web app:
The idea came to me for this when I realized that the way I have been making lists of all the songs I would like to have was probably not the most effective and could be improved on. Therefor this app helps me keep track of all of the songs that I like and want keep the names of, whether I have them as a CD, on my Spotify© playlist or not. We as humans are not as reliable as we would like to believe and to think that we will remember all the names of the songs, who sings the song, etc. is hopeful at best. Our memory cracks down with age. Everything actually but that is irrelevant to this topic. 

## My Goal:
My goal behind this project was to create an app that remembers song names and who sings them for me. And for anyone else who would like to use this app in the future once I have made it publicly available and found a hosting site that is inexpensive enough, preferably free, lol. 
Music is very important to me and without it I would not be here today.

## The Code:

### HTML:
I have eight (8) HTML templates. The 'base.html' is the layout page for most of the project from which six (6) of the webpages expand from. The 'homepage.html' does not expand from this however because it is rarely used or opened by the user. The pages are in two (2) folders, namely the 'registration' folder which contains the login, logout and register pages where the user either logs in, logs out, or where a new user registers to use the app, and the 'songs' folder which contains the homepage, the 'song_confirm_delete.html' where the user is asked whether they are sure if they want to delete the song entry from their list, the 'song_form.html' where the adding of information for a new song entry happens, and the 'song_list.html' where all of the user's songs are displayed. 

#### base.html:
This is the html file that determines the layout of most of the web pages in my project. The following pages are the extensions of this page:
- login.html
- logout.html
- register.html
- song_confirm_delete.html
- song_form.html
- song_list.html

#### login.html:
This is the web page where the user is redirected when selecting to login on the homepage. It uses a form from forms.py to access a user already in the database. 

#### logout.html:
This is the web page where the user is redirected when they log out of their account. It simply displays that the user is logged out and gives the option to log in again. 

#### register.html:
This is the web page where a new user is added to the database. It uses the 'UserRegisterForm' class created in the 'forms.py' file. On this web page there is also the option to log in if the user already has an account.

#### homepage.html:
This web page is the only other html file that is fully written out, as it is not an extension of the 'base.html' page. When the user first opens the website this page will be displayed giving the user the options to login or to register a new account. If the user is logged in they can also view their list of songs or log out.

#### song_confirm_delete.html:
When the user chooses to delete a song entry from their list the user is directed to this page. The user is then presented with the options to either delete the entry or to cancel the delete and return to the web page where the other entries of songs are. This page is to ensure that the user does not accidentally choose to delete an entry which they wanted to keep. 

#### song_form.html:
When the user selects to add a new song entry to their list they are taken to this web page. Here the user fills in a form created in 'forms.py' named 'SongForm'. When creating the entry the user must fill two fields, one for the 'title' of the song, and another for the 'artist' of the song. The date on which the user adds the song is also displayed in the 'song_list.html'. 

#### song_list.html:
This is where all of the magic happens. On this page the user's song entries are displayed in a table format, which is the title of the song, the artist or artists and the date on which the song was added. There are also two 'buttons' next to each entry where the user has the option to edit the song information or delete the entry completely. When the user clicks on the delete button, the user is redirected to the 'song_confirm_delete.html' page. When the user clicks to edit the entry, the web page gets redirected to the 'song_form.html' page to change the data already filled in. On this page at the top left of the table there is another button which the user can click to add another song to the list. When the user selects to either add another song to the web page, they will be redirected to the 'song_form.html' page.

### Static: 
For the static of the web app I used CSS to style the web page but the JavaScript does not function because of a lack of time and I am too scared that the program will break again so close to due date. So my deepest apologies. 

### The App Itself: 
The app is called 'songs' and is written using Django. I use models and forms to help me manage the data that I receive from the users. 

#### models.py:
In models.py I created one model. The model stores all of the songs created by each user via only the title and artist fields. 
I created a 'Song' class where four (4) fields or variables are used. The 'user' variable is used to determine who has which songs and which songs need to be displayed where. The 'title' variable is used to determine what the title of the song is that they want to add. The 'artist' variable is used to determine who the artist is whom made the song that the user wants to add to the database. The 'date_added' variable is used to show the user when they added the song entry to their list, this variable cannot be edited by the user and is not part of the form which they fill in.

#### forms.py:
In forms.py I created two (2) forms. The 'SongForm' form is used to send the data to the 'Song' model. There are only two (2) input fields, the 'title' and the 'artist' fields. 
The UserRegisterForm receives help from a Django library that I imported to help me create users. It takes the UserCreationForm from django.contrib.auth.forms and sends the data to a pre-existing Django model, 'User', from the django.contrib.auth.models library to create the users for me. 

#### views.py:
In views.py I have created several functions to help me with this project. Most of which require the user to be logged in. 
The 'song_list' function filters the song models created and filters them according to users and then renders the filtered songs to the 'song_list.html' web page. 
The 'song_add' function uses a post method of request to create a song entry for a specific user and then redirects the user back to the 'song_list.html' web page after the save was completed. 
The 'song_edit' function uses the 'song_id' to retrieve the information of a specific song which the user wants to edit and resubmits the edited song via the post method. The user is then once again redirected to the 'song_list.html' web page. 
The 'song_delete' function uses the 'song_id' to retrieve the song and remove the song from the database. I feel like this one is pretty obvious but okay. 
The 'register' function uses the 'UserRegisterForm' to create a new user and add them to the database. If the registration was successful the user will be redirected to their 'song_list.html' web page, if not the user will stay on the 'register.html' page until the registration works or the user chooses another page manually. 
The 'homepage' function merely takes the user to the homepage when arriving on the website. 

## Contributors and Help:
I received a lot of help for my project. I used ChatGPT, Claude.ai and Microsoft Co-Pilot. Although Co-Pilot was useless in diagnosing and solving the problem I must include it. 
However my biggest debt and most help received is from a fellow class mate of mine and good friend, Luke Melaia. He helped me to fix my urls and get the app running so that I could continue my work to finish this project. He deserves the most admiration and words will not cover it. I LOVE YOU HAM.

## Requirements:
This project has no requirements when it comes to things that need to be installed beforehand or such, I only used the Django libraries so just make sure that your Django is up to date. 