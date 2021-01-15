// Add additional ingredients add recipe form
$("document").ready(function(){
    ingredientNum = 1;

    console.log(ingredientNum);

    $("#add-ingredient").click(function(){
        if($("#delete-ingredient").hasClass("hidden")){
            $("#delete-ingredient").removeClass("hidden");
        }
        ingredientNum++;
        console.log(ingredientNum);
    })

    $("#delete-ingredient").click(function(){
        ingredientNum--;
        if(ingredientNum == 1){
            $("#delete-ingredient").addClass("hidden");
        }
        console.log(ingredientNum);
    })
})

// Add additional instructions add recipe form
$("document").ready(function(){
    instructionNum = 1;

    console.log(instructionNum);

    $("#add-instruction").click(function(){
        if($("#delete-instruction").hasClass("hidden")){
            $("#delete-instruction").removeClass("hidden");
        }
        instructionNum++;
        console.log(instructionNum);
    })

    $("#delete-instruction").click(function(){
        instructionNum--;
        if(instructionNum == 1){
            $("#delete-instruction").addClass("hidden");
        }
        console.log(instructionNum);
    })
})