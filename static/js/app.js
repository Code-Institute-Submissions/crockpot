// Slider value display
var sliderServes = document.getElementById("serves");
var outputServes = document.getElementById("serves-value");

var sliderCookingTime = document.getElementById("cooking_time");
var outputCookingTime = document.getElementById("cooking_time-value");

outputServes.innerHTML = sliderServes.value;
outputCookingTime.innerHTML = sliderCookingTime.value;

sliderServes.oninput = function() {
  outputServes.innerHTML = this.value;
}
sliderCookingTime.oninput = function() {
  outputCookingTime.innerHTML = this.value;
}