# py-quotes
A little website to gather nice quotes

The backend is made of a cherrypi minimal REST webservice, storing data into a sqlite database (`../quotes.py`). 

The frontend is implemented with AngularJS 1. It allows you to:

 - insert quotes (text + author);
 - search quotes;
 - export all quotes to a downloadable json file;
 - display random quotes.
 
 
 The idea came from the realisation that I love quotes, but never remember them. By having a simple interface to store and 
 consult them, I was finally motivated to stop my tasks and write them down when they especially touched me. 
 The fact that it is exportable in json make the quotes independant from the app: you can easily get them and use them 
 with another app/texteditor.

 
