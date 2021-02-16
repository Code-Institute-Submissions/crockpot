// Credit to https://github.com/Manojlovic1998/Milestone_Project_3/blob/master/static/js/addRecipe.js
// Add/remove additional ingredients to add recipe form
$("document").ready(function(){
    ingredientNum = $('.ingredients-input').length;

    $("#add-ingredient").click(function(){
        ingredientNum++;

        if($("#delete-ingredient").hasClass("hidden")){ 
            $("#delete-ingredient").removeClass("hidden");
        }

        ingredientInputCopy = $("#ingredients-input-template").clone().contents();
        ingredientInputCopy.addClass("ingredients-input" + ingredientNum);

        ingredientInputCopy.find("#ingredient_name_template").attr('id', 'ingredient_name' + ingredientNum);
        ingredientInputCopy.find("#ingredient_name_template_label").attr('for', 'ingredient_name' + ingredientNum);
        ingredientInputCopy.find("#ingredient_name_template_label").removeAttr('id');

        ingredientInputCopy.find("#ingredient_quantity_template").attr('id', 'ingredient_quantity' + ingredientNum);
        ingredientInputCopy.find("#ingredient_quantity_template_label").attr('for', 'ingredient_quantity' + ingredientNum);
        ingredientInputCopy.find("#ingredient_quantity_template_label").removeAttr('id');

        ingredientInputCopy.find("#ingredient_unit_template").attr('id', 'ingredient_unit' + ingredientNum);
        ingredientInputCopy.find("#ingredient_unit_template_label").attr('for', 'ingredient_unit' + ingredientNum);
        ingredientInputCopy.find("#ingredient_unit_template_label").removeAttr('id');

        $("#add-ingredients-hr-skinny").before(ingredientInputCopy);
    })

    $("#delete-ingredient").click(function(){
        ingredientInputCopyClass = ".ingredients-input" + ingredientNum;
        $(ingredientInputCopyClass).remove();

        ingredientNum--;

        if(ingredientNum == 1){
            $("#delete-ingredient").addClass("hidden");
        }
    })
})

// Add/remove additional instructions to add recipe form
$("document").ready(function(){
    instructionNum = $('.instructions-input').length;

    $("#add-instruction").click(function(){
        instructionNum++;

        if($("#delete-instruction").hasClass("hidden")){ 
            $("#delete-instruction").removeClass("hidden");
        }

        instructionInputCopy = $("#instructions-input-template").clone().contents();
        instructionInputCopy.addClass("instructions-input" + instructionNum);

        instructionInputCopy.find("#instructions_template").attr('id', 'instructions' + instructionNum);
        instructionInputCopy.find("#instructions_template_label").attr('for', 'instructions' + instructionNum);
        instructionInputCopy.find("#instructions_template_label").removeAttr('id');

        $("#add-instructions-hr-skinny").before(instructionInputCopy);
    })

    $("#delete-instruction").click(function(){
        instructionInputCopyClass = ".instructions-input" + instructionNum;
        $(instructionInputCopyClass).remove();

        instructionNum--;

        if(instructionNum == 1){
            $("#delete-instruction").addClass("hidden");
        }
    })
})