setTimeout(function () {
    let messages = document.getElementById('msg');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);

setTimeout(function () {
let messages = document.querySelectorAll('.error-msg');

messages.forEach(error1 => {
    error1.remove();
});
}, 5000);