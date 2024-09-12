function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if(parts.length == 2)
        return parts.pop().split(';').shift();
}

function like(id, whoYouLiked) {
    const btn = document.getElementById(`${id}`);

    btn.classList.remove('red-btn')

    if(whoYouLiked.indexOf(id) >= 0){
        var liked = true;
    } else {
        var liked = false;
    }

    if(liked === true){
        fetch(`/unlike/${id}`)
        .then(response => response.json)
        .then(result => {
            location.reload();
        })
    } else {
        fetch(`/like/${id}`)
        .then(response => response.json)
        .then(result => {
            location.reload();
        })
    }

    liked = !liked
}

function edit(id) {
    // Get elements we're working with
    post_content = document.getElementById(`content_${id}`)
    edit_button = document.getElementById(`edit_button_${id}`)
    edit_box = document.getElementById(`edit_${id}`)

    // Show/Hide elements    
    post_content.style.display = "none"
    edit_button.style.display = "none"
    edit_box.style.display = "block"
}

function discard_edit(id) {
    // Get elements we're working with
    post_content = document.getElementById(`content_${id}`)
    edit_button = document.getElementById(`edit_button_${id}`)
    edit_box = document.getElementById(`edit_${id}`)
    
    // Show/Hide elements  
    edit_box.style.display = "none"
    post_content.style.display = "block"
    edit_button.style.display = "block"
}

function save_edit(id) {
    // Get elements we're working with
    post_content = document.getElementById(`content_${id}`)
    edit_button = document.getElementById(`edit_button_${id}`)
    edit_box = document.getElementById(`edit_${id}`)
    edit_ta = document.getElementById(`edit_content_${id}`)
    
    // Get edited post text
    content = edit_ta.value

    // Set post new text
    post_content.innerHTML = content

    // Send edit post request
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: content
        })
    })

    // Show/Hide elements
    edit_box.style.display = "none"
    post_content.style.display = "block"
    edit_button.style.display = "block"
}

function show_post() {
    document.getElementById(`post-box`).style.display = 'flex'
    document.getElementById(`new-post-btn`).style.display = 'none'
}