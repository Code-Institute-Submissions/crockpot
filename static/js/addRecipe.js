// Credit to https://github.com/Manojlovic1998/Milestone_Project_3/blob/master/static/js/addRecipe.js
// Add additional ingredients add recipe form
$("document").ready(function(){
    ingredientNum = 1;

    $("#add-ingredient").click(function(){
        ingredientNum++;

        if($("#delete-ingredient").hasClass("hidden")){ 
            $("#delete-ingredient").removeClass("hidden");
        }

        ingredientInputCopy = $("#ingredients-input-template").clone().contents();
        ingredientInputCopy.addClass("ingredients-input" + ingredientNum);
        $("#icon-row-add-ingredients").before(ingredientInputCopy);
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

// Add additional instructions add recipe form
$("document").ready(function(){
    instructionNum = 1;

    $("#add-instruction").click(function(){
        instructionNum++;

        if($("#delete-instruction").hasClass("hidden")){ 
            $("#delete-instruction").removeClass("hidden");
        }

        instructionInputCopy = $("#instructions-input-template").clone().contents();
        instructionInputCopy.addClass("instructions-input" + instructionNum);
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