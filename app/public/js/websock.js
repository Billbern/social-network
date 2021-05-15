document.addEventListener('DOMContentLoaded', () => {

    const timeChange = document.querySelectorAll('.time small');

    [...timeChange].forEach(item => {
        item.textContent = DateToNumbers(item.nextElementSibling.value);
    })

})

function menuDisplay(e){
    const menuBox = e.parentNode.parentNode.lastElementChild;
    if (menuBox.classList.contains('close-menu')){
        menuBox.classList.remove('close-menu');
    }else{
        menuBox.classList.add('close-menu');
    }
}

function DateToNumbers(dateTime) {
    const postedOn = moment(dateTime);
    const immDate = moment(Date.now());
    let result;
    if (immDate.diff(postedOn, 'seconds') <= 60) {
        if (immDate.diff(postedOn, 'seconds') <= 1) {
            result = `${immDate.diff(postedOn, 'seconds')} second ago`;
        } else {
            result = `${immDate.diff(postedOn, 'seconds')} seconds ago`;
        }
    } else if (immDate.diff(postedOn, 'minutes') <= 60) {
        if (immDate.diff(postedOn, 'minutes') <= 1) {
            result = `${immDate.diff(postedOn, 'minutes')} minute ago`;
        } else {
            result = `${immDate.diff(postedOn, 'minutes')} minutes ago`;
        }
    } else if (immDate.diff(postedOn, 'hours') <= 24) {
        if (immDate.diff(postedOn, 'hours') <= 1) {
            result = `${immDate.diff(postedOn, 'hours')} hour ago`;
        } else {
            result = `${immDate.diff(postedOn, 'hours')} hours ago`;
        }
    } else {
        if (immDate.diff(postedOn, 'days') <= 1) {
            result = `${immDate.diff(postedOn, 'days')} day ago`;
        } else {
            result = `${immDate.diff(postedOn, 'days')} days ago`;
        }
    }

    return result;
}

