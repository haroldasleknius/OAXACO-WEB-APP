function copyToClipboard() {
    var copyText = document.getElementById("contactinfo");
    navigator.clipboard.writeText(copyText.value);
}