const socketio = io();
let USERNAME = ""
fetch("/get_username").then(resp=>{
    resp.text().then(data=>{
        USERNAME += data;
    })
})


let chatbox = document.getElementById("chat-box");

const addAnouncement = (msg) =>{

    let chat_area = document.getElementById("chat-area");
    let chat_div = document.createElement("div");
    chat_div.classList.add("chat");
    let announcement = document.createElement("p");
    announcement.classList.add("announcement");
    announcement.innerText = msg;
    chat_div.appendChild(announcement);
    chat_area.appendChild(chat_div);
}

socketio.on("user_joined_chat" , msg =>{
    addAnouncement(msg);
});




socketio.on("user_left_chat", msg =>{
    console.log(1);
    addAnouncement(msg);
})


socketio.on("public_chat", data => {
    let username = data.username;
    let text = data.text;
    let chat_area = document.getElementById("chat-area");
    let chat_div = document.createElement("div");

    chat_div.classList.add("chat");
    let p = document.createElement("p");
    let b = document.createElement("b");
    b.innerText = username + " : "

    if (username === USERNAME){
        b.style.color = "red";
    }
    
    p.appendChild(b);
    p.append(text);
    chat_div.appendChild(p);

    chat_area.appendChild(chat_div);

    let chat_container = document.getElementById("chat-container");
    chat_container.scrollTop = chat_container.scrollHeight;

})





chatbox.addEventListener("keydown" , k => {
    if (k.key == "Enter"){
        let msg = chatbox.value;
        socketio.emit("public_chat" , msg);
        chatbox.value = "";
    }
})