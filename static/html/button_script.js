function onRegisterButtonClick() {
    const url = "http://localhost:8000/";

    let user_name = ''
    if (document.getElementById('type_of_1').checked){
        user_name = document.getElementById('type_of_1').value;
    }
    else if (document.getElementById('type_of_2').checked){
        user_name = document.getElementById('type_of_2').value;
    }
    else if (document.getElementById('type_of_3').checked){
        user_name = document.getElementById('type_of_3').value;
    }
    let n_of_chunks = document.getElementById("n_of_chunks").value;
    let chunks_length = document.getElementById("chunks").value;
    let height = document.getElementById("height").value;

    console.log(user_name, n_of_chunks, chunks_length, height)
    fetch(url, {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
                'type_of_generation': user_name,
                "chunks": n_of_chunks,
                "length": chunks_length,
                'height': height
        }
    })
    .then(window.location.replace("http://localhost:8000/generated"));
}