function submitForm(event) {
    event.preventDefault();
    var data = new FormData(form);
    data.append("img_id", img_id);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sortgarbage");
    xhr.send(data);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            let text = xhr.responseText;
            console.log(text)
            if (text == "Incorrect") {
                alert("Incorrect");
            } else if (text == "Correct") {
                alert("Correct");
            }
            window.location.href = "/sortgarbage";
        }
    };
}

const form = document.getElementById('sortform');
form.addEventListener('submit', submitForm);