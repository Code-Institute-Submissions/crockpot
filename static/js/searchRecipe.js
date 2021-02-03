function searchIngredients() {
    var ingredientsList = document.getElementById("ingredients-list");
    var ingredientsCheckbox = ingredientsList.getElementsByTagName("input");
    var ingredientsString = "";
    var ingredientsStringChecked = "";

    for (var i = 0; i < ingredientsCheckbox.length; ++i) {
        ingredientsString2 = ingredientsCheckbox[i].value

        if (ingredientsCheckbox[i].checked) {
            ingredientsStringChecked = ingredientsStringChecked.concat(ingredientsString2 + " ");
        }
        else {
            ingredientsString = ingredientsString.concat(ingredientsString2 + " ");
        }
    }

    console.log("Non checked boxes: " + ingredientsString);
    console.log("Checked boxes: " + ingredientsStringChecked);
}