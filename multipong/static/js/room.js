const socketio = io("/room",{"transports" : ['websocket']});


document.addEventListener("DOMContentLoaded", ()=>{
    document.getElementById("url").innerText = window.location.hostname + document.getElementById("room_url").value;
})

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
