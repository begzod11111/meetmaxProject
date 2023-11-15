
let singInForm = document.getElementById('sing-in-form')
let sentMailForm = document.getElementById('send-mail-form')

function openMailForm(num) {
    if (num) {
        singInForm.classList.remove('active-form')
        sentMailForm.classList.add('active-form')
    }
    else {
        singInForm.classList.add('active-form')
        sentMailForm.classList.remove('active-form')
    }
}