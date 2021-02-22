// Open accordions automatically on larger devices
onload = function () {
    if (window.innerWidth >= 768) {
        $(".collapse").addClass("show");
    }
};

var idNumModal = 0;

// Modal controls - profile.html
function openModalView() {
    idNumModal = document.getElementById("modal-delete");
    $(idNumModal).removeClass("hidden");
}

function closeModalView() {
    idNumModal = document.getElementById("modal-delete");
    $(idNumModal).addClass("hidden");
}

function openModal() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete" + idNum);
    
    $(idNumModal).removeClass("hidden");
}

function closeModal() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete" + idNum);

    $(idNumModal).addClass("hidden");
}

function openModalMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-md" + idNum);
    
    $(idNumModal).removeClass("hidden");
}

function closeModalMd() {
    var target = event.target || event.srcElement;
    var id = target.id;
    var idNum = id.match(/\d+/)[0];
    var idNumModal = document.getElementById("modal-delete-md" + idNum);

    $(idNumModal).addClass("hidden");
}

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