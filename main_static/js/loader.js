
document.addEventListener('DOMContentLoaded', (event) => {
    const media = document.querySelectorAll('img')
    let i = media.length
    Array.from(media).forEach((file) => {
        file.onload = () => {
            i--
            if (i === 0) {
                let preloader = document.getElementById('preloader');
                preloader.classList.add('preloader-hidden')
            }
        }
    })

})