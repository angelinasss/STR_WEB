document.getElementById("toggleSettings").addEventListener("change", function () {
    const customizationOptions = document.getElementById("customizationOptions");
    if (this.checked) {
        customizationOptions.style.display = "block";
    } else {
        customizationOptions.style.display = "none";
    }
});

document.getElementById("fontSize").addEventListener("input", function () {
    document.getElementById("text_content").style.fontSize = this.value + "px";
});

document.getElementById("textColor").addEventListener("input", function () {
    document.getElementById("text_content").style.color = this.value;
});

document.getElementById("bgColor").addEventListener("input", function () {
    document.body.style.backgroundColor = this.value;
});