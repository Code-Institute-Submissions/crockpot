// Modal controls
function openModalView() {
    idNumModal = document.getElementById("modal-delete");
    $(idNumModal).removeClass("hidden");
}

function closeModalView() {
    idNumModal = document.getElementById("modal-delete");
    $(idNumModal).addClass("hidden");
}

// Non-profile
function openModal() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete" + idNum);

    // console.log(id);
    // console.log(idNum);
    // console.log(id.match(/\d+/)[0]);
    $(idNumModal).removeClass("hidden");
}

function closeModal() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete" + idNum);

    $(idNumModal).addClass("hidden");
}

// Profile
function openModalMy() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-my-recipe" + idNum);

    $(idNumModal).removeClass("hidden");
}

function closeModalMy() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-my-recipe" + idNum);

    $(idNumModal).addClass("hidden");
}

function openModalMyMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-my-recipe-md" + idNum);

    $(idNumModal).removeClass("hidden");
    $(".icon").addClass("hidden");
}

function closeModalMyMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-my-recipe-md" + idNum);

    $(idNumModal).addClass("hidden");
    $(".icon").removeClass("hidden");
}

function openModalFav() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-fav-recipe" + idNum);

    $(idNumModal).removeClass("hidden");
}

function closeModalFav() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-fav-recipe" + idNum);

    $(idNumModal).addClass("hidden");
}

function openModalFavMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-fav-recipe-md" + idNum);

    $(idNumModal).removeClass("hidden");
    $(".icon").addClass("hidden");
}

function closeModalFavMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-fav-recipe-md" + idNum);

    $(idNumModal).addClass("hidden");
    $(".icon").removeClass("hidden");
}

// Show serving slider value
var sliderServes = document.getElementById("serves");
var outputServes = document.getElementById("serves-value");
outputServes.innerHTML = sliderServes.value;

sliderServes.oninput = function() {
  outputServes.innerHTML = this.value;
}

// Show cooking time slider value
var sliderCookTime = document.getElementById("cooktime");
var outputCookTime = document.getElementById("cooktime-value");
outputCookTime.innerHTML = sliderCookTime.value;

sliderCookTime.oninput = function() {
  outputCookTime.innerHTML = this.value;
}