let account_btn = document.getElementById("account-btn");
let form = document.getElementById("account-form");
let change_btn = document.getElementById("change-btn");
let mode = "signup"
let submit_btn = document.getElementById("submit-btn");
let error_div  = document.getElementById("errors");
let csrf_token = document.getElementById("csrf-token").value;


form.style.display = "none";
account_btn.addEventListener("click" , ()=>{
        
    if (form.style.display === "none"){
        form.style.display = "";
    }
    else{
        form.style.display = "none";
        
    }
})

change_btn.addEventListener("click" , ()=>{
    if (mode === "signup"){
        clear_errors();
        mode = "login";
        document.getElementById("auth-action").innerText = "login";
        document.getElementById("change-btn").innerText = "signup"
        let rep_pwd = document.getElementById("repeat-password");
        rep_pwd.remove();
    }else if (mode === "login"){
        clear_errors();
        mode = "signup";
        document.getElementById("auth-action").innerText = "signup";
        document.getElementById("change-btn").innerText = "login";
        var div = document.getElementById("repeat-pwd");
        var input = document.createElement("input");
        input.placeholder = "repeat password";
        input.type = "password";
        input.name = "password2";
        input.id = "repeat-password";
        div.appendChild(input);

    }
})


function clear_errors(){
    
    error_div.innerHTML = "";
}

submit_btn.addEventListener("click", ()=>{
    if (mode === "signup"){
        let username = document.getElementsByName("username")[0].value;
        let password = document.getElementsByName("password")[0].value;
        let password2 = document.getElementsByName("password2")[0].value;

        
        fetch("/signup",{
            method : "post",
            headers : {
                "X-CSRFToken" : csrf_token,
            },
            body : JSON.stringify({
                "username" : username,
                "password" : password,
                "password2" : password2
            }),
        }).then(resp => {
            if (resp.redirected){
                window.location.href = "/";
            }else{
                resp.json().then( data =>{
                    clear_errors();

                    for (let error of data){
                        let p = document.createElement("p");
                        p.innerText = error;
                        p.classList.add("error");
                        error_div.appendChild(p);
                    }
                })
            }
        }).catch(()=>{
            clear_errors();
            let p = document.createElement("p");
            p.innerText = "something went wrong";
            p.classList.add("error");
            error_div.appendChild(p);
        })



    }else if (mode === "login"){
        let username = document.getElementsByName("username")[0].value;
        let password = document.getElementsByName("password")[0].value;

        fetch("/login" , {
            method : "post",
            headers : {
                "X-CSRFToken" : csrf_token,
            },
            body : JSON.stringify({
                "username" : username,
                "password" : password
            })
        }).then(resp => {
            if (resp.redirected){
                window.location.href = "/";
            }
            else{
                resp.json().then(data => {
                    clear_errors();
                    var error = data["error"];
                    let p = document.createElement("p");
                    p.innerText = error;
                    p.classList.add("error");
                    error_div.appendChild(p);  
                })
            }
        }).catch(()=>{

        })

    }
})
