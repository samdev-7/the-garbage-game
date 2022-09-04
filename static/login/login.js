function submitForm(event) {
    event.preventDefault();
    var data = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login");
    xhr.send(data);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            let text = xhr.responseText;
            console.log(text)
            if (text == "Incorrect credentials") {
                alert("Incorrect credentials");
            } else if (text == "No account exists") {
                alert("No account exists, please sign up");
            } else if (text == "Success") {
                window.location.href = "/";
            }
        }
    };
}

const form = document.getElementById('loginform');
form.addEventListener('submit', submitForm);