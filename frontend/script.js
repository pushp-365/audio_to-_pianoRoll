const input =
document.getElementById("audioFile");


const player =
document.getElementById("mainPlayer");


input.onchange = () => {


    let file =
    input.files[0];


    if(file)
    {

        let url =
        URL.createObjectURL(file);


        player.src = url;

    }

}