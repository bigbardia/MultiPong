const socketio = io("/room",{"transports" : ['websocket']});

const game = () => {

}

document.addEventListener("DOMContentLoaded", ()=>{
    document.getElementById("url").innerText = window.location.hostname + document.getElementById("room_url").value;
    let start_button = document.getElementById("start");
    start_button.addEventListener("click" , ()=>{
        socketio.emit("start_game");
    })
})


function copyToClipBoard(){
    let url = document.getElementById("url").innerText;
    navigator.clipboard.writeText(url).then(()=>{
        alert("copied!")
    });
}


socketio.on("player_data", (data) => {

    for (user of data){
        let username = user["username"];
        let player = user["player"];

        document.getElementById(player[player.length-1]).innerText = `${player} : ${username}`;
    }
})



socketio.on("player1_left_before_start" , ()=>{
    window.location.replace("/");
})



socketio.on("player2_left_before_start" , ()=>{
    document.getElementById("2").innerText ="";
})


socketio.on("start_game" , ()=>{
    game();
})


socketio.on("game_ended" , ()=>{

})

socketio.on("player_left" , () => {

})