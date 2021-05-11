document.addEventListener('DOMContentLoaded', () => {

    const postForm = document.querySelector('#postForm');
    const contentContainer = document.querySelector('.post_content');

    var socket = io();

    socket.on('display_posts', (data)=>{
        contentContainer.innerHTML = "";

        if (data.length != 0){
            data.reverse().forEach(post => {
                const postContain = document.createElement('div');
                const postTime = moment().diff(moment(post.createdAt, 'YYYY-MM-DD'), 'hours') >= 24 ? `posted on ${moment(post.createdAt, 'YYYY-MM-DD')}` : moment().diff(moment(post.createdAt, 'YYYY-MM-DD'), 'hours') <= 1 ? `posted ${moment().diff(moment(post.createdAt, 'YYYY-MM-DD'), 'minutes')} minutes ago`: `posted ${moment().diff(moment(post.createdAt, 'YYYY-MM-DD'), 'hours')} hours ago`;
                const innerContent = `<div class="top-content"><p class="text">${post.content}</p></div><div class="bottom-content"><span class="like">&#128077;<small>0</small></span><span class="time"><small>${postTime}</small></span></div>`;
                postContain.setAttribute('class', 'post-item');
                postContain.innerHTML = innerContent;
                contentContainer.appendChild(postContain);
            });
        }else{
            console.log('no posts yet');
        }
    })

    postForm.onsubmit = e =>{
        e.preventDefault()
        data = document.querySelector('#formContent').value;
        if (data != ""){
            document.querySelector('#formContent').value = "";
            socket.emit('store_posts', data)
        }
    }

});