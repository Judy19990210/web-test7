
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Referrer-Policy': 'no-referrer',
            'Origin': 'https://localhost:5000'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {

      if (data.success==1) {
              alert("Login success");
      } 
      if (data.success==2) {
              alert("Login failure: invalid email or password.");
      } 
      if(data.success==3) {
              alert("Login failure: password is not hashed, because you used the unsafe page to register. Please use the safe web page to register.");
      }
      
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");
  
    registerForm.addEventListener("submit", function (event) {
      event.preventDefault();
  
      const email = document.getElementById("register-email").value;
      const username = document.getElementById("register-username").value;
      const password = document.getElementById("register-password").value;
      const passwordConfirm = document.getElementById("register-password-confirm").value;
  
      const payload = {
        email,
        username,
        password,
        password_confirm: passwordConfirm
      };
  
      fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Referrer-Policy': 'no-referrer',
          'Origin': 'https://localhost:5000'
        },
        body: JSON.stringify(payload),
      })
        .then((response) => response.json())
        .then((data) => {
          
          if (data.success==1) {
            alert("Registration failure: the password does not meet the format requirements.");
          } 
          if (data.success==2) {
            alert("Registration failure: the two passwords are different. Please re-enter them.");
          } 
          if(data.success==3) {
            alert("Registration failure: the email already exists.");
          }

          if (data.success==4) {
            alert("Successful registration");
          } 

        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
