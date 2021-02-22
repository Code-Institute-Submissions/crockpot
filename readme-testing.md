# Crockpot

## Table of Contents

- [Testing During Development](#testing-during-development)
    - [Bug Fixes](#bug-fixes)
- [Code Validation](#code-validation)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript and JQuery](#javascript-and-jquery)
    - [Python](#python)
    - [Responsiveness](#responsiveness)
    - [Accessibility](#accessibility)
    - [Performance](#performance)
- [Testing User Stories](#testing-user-stories)

Click **[here](readme.md)** to view the complete testing process.

## Testing During Development
### Bug fixes
- Bug #1: getting ingredients to display correctly on viewRecipe.html
- Bug #2: Slicing error on search page for recipes > 9
- Bug #3: Search specificity, incorrect ingredients/instructions on editRecipe
- Changing search function from or to and

## Code Validation

### HTML
W3C Markup Validation Service - following errors:
- I used HTML of deployed website inside the validator, so that I can bypass the Jinja templating syntax.
- ID duplicates on profile page
- Empty labels on add and edit recipe
- No divs inside of ols - add and edit recipe
- Missing IDs/fors on add and edit recipe
- White spaces in ingredients ids on search recipes
- Sections lacking heading

### CSS
W3C CSS Validation Service - following errors:
/* ul.ks-cboxtags li input[type="checkbox"] {
	display: absolute;
} */

### JavaScript and JQuery
JSHint - following errors:
- missing semicolons
- hadn't declared variables at the beginning of app.js

### Python
Pep8 - following errors:
no issues

### Responsiveness
Amiresponsive, google developers, human testing - following errors:

### Accessibility
Lighthouse
- contrast error between red and white - no time to fix, will test at beginning of next project

### Performance
Lighthouse

## Testing User Stories
Screenshots
