# Crockpot - Testing

## Table of Contents

- [Testing During Development](#testing-during-development)
- [Code Validation](#code-validation)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript and JQuery](#javascript-and-jquery)
    - [Python](#python)
    - [Responsiveness](#responsiveness)
    - [Accessibility](#accessibility)
    - [Performance](#performance)
- [Testing User Stories](#testing-user-stories)

Click **[here](readme.md)** to return to the main document.

## Testing During Development
My main methods of testing my code throughout the development process was using the ```console.log()``` function for my JavaScript and the ```print()``` function for my Python to check what variables my functions were actually producing and to identify any unpredictable behaviour. This helped to fix the following bugs:
- __0d22362__ _Bug fix #1: Ingredients display correctly on viewRecipe.html_ - I initially struggled to get the ingredients to display properly on my View Recipe page. Instead of displaying as the values for name, quantity and unit, they rendered as one long array. I resolved this by zipping the three lists together in my run.py file:
```
ingredients = zip(ingredient_names_reformat,
                          recipe["ingredient_quantity"],
                          recipe["ingredient_unit"])
```
and iterating through this new matrix using Jinja in the HTML:
```
<ul class="text-left mb-0">
    {% for ingredient in ingredients %}
    <li><span class="capital">{{ingredient[0]}}</span> x
        {{ingredient[1]}}{{ingredient[2]}}
    </li>
    {% endfor %}
</ul>
```
- __84dcb29__ _Bug fix #2: Slicing issue on searchRecipe.html resolved_ - I noticed during my first round of testing that when the user had more than 9 recipes on their Profile, Search or Menu pages, the "Menu", "Edit" and "Delete" icons wouldn't work properly. I had written a function in JavaScript to open and close the modals for each recipe - the HTML id attribute for each recipe had a ```{{loop.index}}``` after it to assign it a unique number and the JavaScript function used the code ```var idNum = id.slice(-1)``` to get this number and open the corresponding modal. However, when the assigned number got into double digits this code stopped the function from working (eg. if the number was 10, idNum would be 0). I replaced this code with ```var idNum = id.match(/\d+/)[0]``` instead to identify any number (single digit or double digits) in the string which resolved the issue.
- __8d05205__ _Bug fix #3: Split editRecipe function into two to render and save form input correctly_ - I also noticed in my first round of testing that my edit function didn't work properly. When the user tried to edit a recipe, the changes that they saved would overwrite the old data instead of adding to it (eg. if a user added an extra instruction to the recipe, this would remove all of the original instructions and just save the new one). I resolved this by splitting my edit function into two parts - one that inserted the old data into the edit form and another that saved all of the data, old and new, when the user submitted their changes.
- __ea60bed__ _Bug fix #4: Resolve image display issue on mobile devices_ - When a user adds a recipe without an image, a placeholder image of the _Crockpot_ logo is added instead. I was initially rendering this using Jinja in my HTML, but my tutor advised me to assign this in my Python code instead. While fixing this issue, I accidentally deleted part of the HTML which controls the size of the recipe images. I used previous versions of my code on Github to identify the error and rectify it.

## Code Validation

### HTML
I used the W3C Markup Validation Service to test the validity of my HTML. I copied the source code for each page at each breakpoint and input it directly into the validator to bypass the Jinja template syntax. It flagged the following errors:
- There were id attribute duplicates on profile.html
- There were empty labels for options on the dropdown select menu for ingredient unit and missing for attributes on add-recipe.html and edit-recipe.html
- I had div elements inside an ordered list on add-recipe.html and edit-recipe.html
- The id attributes on the ingredients on search-recipe.html were rendering with white spaces

I have resolved all of these issues. The one warning that remains is that some of the sections on some of the pages don't have h1 headings - these always feature in the first section at the top of each page so I didn't feel the need to fix this.

### CSS
I used the W3C CSS Validation Service to test the validity of my CSS. It flagged that the code
```
ul.ks-cboxtags li input[type="checkbox"] {
	display: absolute;
}
```
that I had gotten from https://codepen.io/quinlo/pen/ReMRXz for my ingredients checkboxes was incorrect, as ```display: absolute``` isn't a proper ruleset. I deleted the class which didn't impact the functionality of the site, thereby resolving the issue.

### JavaScript and JQuery
I used JSHint to test the validity of my JavaScript and JQuery functions. It flagged the following errors:
- There were a few missing semicolons at various points in my code
- I hadn't declared my variables at the start of app.js

I have resolved all of these issues.

### Python
I used PEP8Online to check the compliance of my run.py file and it didn't flag any errors.

### Responsiveness
I used Google Developer tools to test the layout of my site on multiple device sizes during development, and Amiresponsive to finetune the site when I finished the bulk of the code. Amiresponsive flagged a spacing error on the Log In and Sign Up pages on really small mobile devices. To resolve this I added specific CSS media query targeting devices that are ```(max-height: 480px) and (max-width: 320px)``` to make elements on these pages smaller so everything fits in. I also shared the site with 20 of my friends and family who tested it on their various devices - no-one flagged any issues aside from what had already been highlighted by Amiresponsive.

### Accessibility
I used the Lighthouse tool on the Google Developer platform to test the accessibility of my site. The main issue that it flagged was that the contrast of the small white text against the red background in the navbar and the footer was too low and it would be hard for those with visual impairments to read. Poor contrast was an issue that had been flagged in my MS1 project as well - I didn't have time to redo the colour scheme across the site but I will prioritise it at the start of my MS4 to make sure it is not an issue there. Another issue was that some of the button elements didn't have any descriptive text attached to them so I added descriptions with an "sr-only" class.

At the end of testing my accessibility score across the site was above 90 - I was satisfied by this for the scope of the project, but it could be improved in future iterations by fixing the contrast issue and using more semantic elements.

### Performance
I used the Lighthouse tool on the Google Developer platform to test the performance of my site. It flagged that a lot of the images were increasing the "time to interactive" value for my site, so I compressed all of the images saved in my "static" folder which improved my overall score. However, I couldn't compress the images for the individual recipes as they are sourced from URLs, not static content, so I couldn't improve my score as much as I would have liked through this method.

At the end of testing my performance score across the site was above 83 - I was satisfied by this for the scope of the project, but it could be improved in future iterations by fixing the using lazy loading functionality on some of the images, delivering critical JS/CSS inline and deferring all non-critical JS/styles to allow the page to load faster.

## Testing User Stories
To quantify how well _Crockpot_ fulfils the criteria outlined in my User Stories, I shared the site with 20 of my friends and family and asked them to score it out of 10 for "UX experience", "Easy to use", "Functionality" and for various functions across the site.

_**Developer**_
1. _As the developer, I want to create an online platform where users can add, edit, delete and search for recipes to complete the third_ Code Institute _Milestone Project._
    - I have developed a platform where users can add, edit, delete and search for recipes.
2. _As the developer, I want the website to be aesthetically pleasing and easy to use to demonstrate my ability to code in HTML and CSS and to create a positive UX experience for the site users._
    - The consistent styling, colour scheme, CSS effects and page layout create a positive UX experience for the user. There are clear instructions on the relevant pages about how to use the site, and the consistent colour scheme and iconography associated with the interactive elements create an intuitive and easy-to-use interface. Out of the 20 people surveyed, it scored 9.5 for "UX experience" and 9.8 for "Easy to use".
3. _As the developer, I want the website to function well to demonstrate my ability to code in JavaScript and Python and to create a positive UX experience for the site users._
    - The JavaScript, JQuery and Python code is bug free and the different functions interact with each other without issue, indicating that the site functions well. Out of the 20 people surveyed, it scored 9.3 for "Functionality".

_**Site owner**_
1. _As the site owner, I want the site users to have a positive UX experience while using the website so that the_ Crockpot _community grows._
    - See 2 in Testing User Stories - Developer.
2. _As the site owner, I want the site users to have a positive UX experience while adding, editing and deleting recipes to increase the number of communal recipes that are shared with the website._
    - See 2 in Testing User Stories - Developer.

_**Site users**_
1. _As a new user, I want to be able to easily create my own profile so I can start using the website quickly._
    - The first thing a new user sees on the _Crockpot_ site is a link to sign up or log in. The sign up link is larger to draw the eye to it first. The Sign Up page is also accessible through the navbar. Once they are on the Sign Up page, the username and password inputs are in the centre and clearly labelled. If their username is already taken they are notified by flashed message; if the syntax of their username or password is incompatible they are notified by pop-up. Out of the 20 users surveyed, no-one reported an issue with creating a profile.
2. _As a new user, I want clear instructions on how to use the website so I can start using the website quickly._
    - Once the user has created their profile, the first thing they see on the Profile, Search and Menu pages is instructions on how to use each page. Consistent iconography is used next to the instructional text to reinforce the message. Of the 20 people surveyed, the site scored 9.8 for "Easy to use".
3. _As a returning user, I want to be able to easily log in to my profile so I can start using the website quickly._
    - The first thing a returning user sees on the _Crockpot_ site is a link to sign up or log in. The Log In page is also accessible through the navbar. Once they are on the Log In page, the username and password inputs are in the centre and clearly labelled. If their username and password combination is already taken they are notified by flashed message; if the syntax of their username or password is incompatible they are notified by pop-up. Out of the 20 users surveyed, no-one reported an issue with logging in. Two people mentioned that it would be useful to include a feature that would remind the user of their log in credentials if they forgot them - this would be a good feature to include in future iterations of the project.
4. _As a site user, I want to be able to add my own recipes so all of my recipes are saved in one place._
    - Users are informed on how to add recipes on their Profile page when they first join the site. Users can access the Add Recipe form from their profile or the navbar. The form inputs are clearly labelled with placeholders or separate text, and the toggles, sliders and dropdown menus are intuitive to use. If the user tries to save the recipe and has entered something incorrectly they will be notified via pop-up. Out of the 20 users surveyed, no-one reported an issue with adding a recipe.
5. _As a site user, I want to be able to edit my own recipes if they need updating._
    - Users are informed on how to edit recipes on their Profile page when they first join the site. Users can access the Edit Recipe form for their own recipes from the "Edit" icon on the recipe tile or when viewing the full recipe. The Edit Recipe form is consistent with the Add Recipe form to create a good UX experience. If the user tries to save the recipe and has entered something incorrectly they will be notified via pop-up. Out of the 20 users surveyed, no-one reported an issue with editing a recipe.
6. _As a site user, I want to be able to delete my own recipes if I don't want to use them anymore._
    - Users are informed on how to delete recipes on their Profile page when they first join the site. Users can access the delete recipe function for their own recipes from the "Delete" icon on the recipe tile or when viewing the full recipe. When the user clicks on the "Delete" icon this opens a modal checking if they definitely want to delete it. Out of the 20 users surveyed, no-one reported an issue with deleting a recipe.
7. _As a site user, I want feedback from the website when I add, edit and delete my recipes to show that my input has been successful._
    - Users are informed if they have successfully added, edited and deleted their recipes via flashed message.
8. _As a site user, I want to be able to browse the recipes I have added when I am deciding what to cook._
    - Users can browse all of the recipes they have added from their Profile page. After logging in they can access their Profile page by clicking the _Crockpot_ logo in the top left of the navbar, or through the navbar link.
9. _As a site user, I want to be able to browse the recipes that other users have added when I am deciding what to cook._
    - Users can browse all of the recipes on the database on the Search page. They can access the Search page through their Profile page, or through the navbar link.
10. _As a site user, I want clear, well-presented information about the recipe including name, cooking time, ingredients and instructions so I know how to cook the recipe._
    - Users can access the recipe by clicking on the recipe tile - the tiles grow in size when the user hovers over them indicating that they can be clicked. The recipe information is clearly displayed in a grid system. The icons that allow users to add the recipe to their menu, edit, delete or favourite it are all at the top to make them easily accessible. If the user hasn't added a recipe image there will be a _Crockpot_ logo as a placeholder to make it more aesthetically pleasing. If the user hasn't added any "Top Tips" or "Source" these won't render on the page. The ingredients and instructions are in dropdown menus if the user wants to minimise the content on the page. Out of the 20 users surveyed, no-one reported an issue with viewing a recipe.
11. _As a site user, I want to be able to save my favourite recipes so they are easier to look up when I next want to cook them._
    - Users are informed on how to favourite recipes on their Profile page when they first join the site. Users can access the favourite function when adding or editing a recipe, or while viewing the recipe. They are informed via flashed message if they have successfully added/removed a recipe from their favourites. They can then view their favourited recipes on their Profile page. Out of the 20 users surveyed, no-one reported an issue with favouriting a recipe.
12. _As a site user, I want to be able to search the communal database for recipes based on various criteria if I am looking for a specific recipe._
    - The layout of the Search page is in keeping with common design practices, and is therefore intuitive to use. Users receive additional instructions on how to use the search function if they search for something with no results. The ingredients are ordered alphabetically to make it easier to find specific ingredients. Users can input a recipe name, some ingredients or both depending on their query. Out of the 20 users surveyed, no-one reported an issue with searching for a recipe.
13. _As a site user, I want to be able to access the website from both mobile and desktop browsers so I can access the website from any of my devices._
    - The site is fully responsive (see Code Validation - Responsiveness).
14. _As a site user, I want to be able to log out of the site when I am finished using it._
    - Users can log out of the site using the link in the navbar. It is in the same position as the sign up and log in links before the user logs in to the site, so the user should intuively know where to find the link.
15. _As a site user (me), I want to be able to search the communal database for recipes based on what ingredients I have._
    - Users can search for recipes based on ingredients using the dropdown ingredients menu on the search page which contains all the unique ingredients listed on the database.
16. _As a site user (me), I want to be able to generate a shopping list from the recipes I have selected._
    - Users are informed on how to add recipes to their "Menu" on the Menu page when they first join the site. The "Shopping List" displays all of the unique ingredients and sums the quantities of the duplicate ingredients. Users can add/remove recipes from their "Menu" using the "Menu" icon on the recipe tile or when viewing the full recipe; they are informed via flashed message if they have successfully done this. They can access the menu page from their profile or from the link in the navbar. Out of the 20 users surveyed, no-one reported an issue with adding a recipe to their menu.

Having reviewed my user stories I believe I have fulfilled all of the requirements I laid out for myself in my Strategy Plane. I have also included all of the "must-have" features outlined in my Scope Plane and one of the "nice-to-haves" (_"The site could generate a shopping list based on what recipes the user has selected."_)