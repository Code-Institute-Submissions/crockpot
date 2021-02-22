// Show serving slider value
var sliderServes = document.getElementById("serves");
var outputServes = document.getElementById("serves-value");
outputServes.innerHTML = sliderServes.value;

sliderServes.oninput = function() {
  outputServes.innerHTML = this.value;
};

// Show cooking time slider value
var sliderCookTime = document.getElementById("cooktime");
var outputCookTime = document.getElementById("cooktime-value");
outputCookTime.innerHTML = sliderCookTime.value;

sliderCookTime.oninput = function() {
  outputCookTime.innerHTML = this.value;
};