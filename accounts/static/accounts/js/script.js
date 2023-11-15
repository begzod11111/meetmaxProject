
function modalOpen(num) {
    let modal = document.getElementById("m" + String(num))
    if (modal.classList[1] === 'open-modal') {
        modal.classList.remove('open-modal')
    }
    else {
        modal.classList.add('open-modal')
    }
}



function tabs(num) {
    let tabsBt = document.querySelectorAll('.tabs')
    let tabsCt = document.querySelectorAll(".tabs-ct")
    let activeTab = document.getElementById('active-tab')
    for (let i = 0; i < tabsCt.length; i++){
        if (i === num) {
            tabsCt[i].style.display = 'block';
            let flag = true;
            for (let j = 0; j < tabsBt[i].children.length; j++){
                if (tabsBt[0].children[j] === activeTab){
                    flag = false
                }
            }
            if (flag === true){
                tabsBt[i].appendChild(activeTab)
            }

        }
        else {
            for (let j = 0; j < tabsBt[i].children.length; j++){
                if (tabsBt[0].children[j] === activeTab){
                    tabsBt[0].children[j].remove()
                }
            }
            tabsCt[i].style.display = 'none'
        }

    }

}