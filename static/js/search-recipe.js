// Adds values of checked ingredients checkboxes to query string for search function
function searchIngredients() {
    var ingredientsList = document.getElementById("ingredients-list");
    var ingredientsCheckbox = ingredientsList.getElementsByTagName("input");
    var ingredientsStringChecked = "";

    for (var i = 0; i < ingredientsCheckbox.length; ++i) {
        ingredientsString = ingredientsCheckbox[i].value.replace(/\s/g, '');

        if (ingredientsCheckbox[i].checked) {
            ingredientsStringChecked = ingredientsStringChecked.concat(ingredientsString + " ");
        }
    }

    var query = document.getElementById('query');
    query.value += "&";
    query.value += ingredientsStringChecked;
}