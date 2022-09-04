function submitForm(event) {
    event.preventDefault();
    var data = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/signup/");
    xhr.send(data);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            let text = xhr.responseText;
            console.log(text)
            if (text == "Account already exists") {
                alert("Account already exists, please log in");
            } else if (text == "Success") {
                window.location.href = "/";
            }
        }
    };
}

const form = document.getElementById('loginform');
form.addEventListener('submit', submitForm);