
      var getCodeButton = document.getElementById('get-code');
      var verifyButton = document.getElementById('verify');
      var codeInput = document.getElementById('code-input');
      var timerElement = document.getElementById('timer');
      const getCodeForm = document.getElementById("getcodeform");
      const verifyCode = document.getElementById("verifycode");
      console.log("check ✔️✔️✔️")
      getCodeForm.onsubmit = function (e){
            e.preventDefault();
            console.log("test")
            const phone = document.getElementById("phone-number").value;
            console.log(phone);
            const xhr = new XMLHttpRequest();
            const csrf = document.querySelectorAll('input[name="csrfmiddlewaretoken"]')[0].getAttribute('value');
            
            xhr.open("POST","{%url 'verify'%}",true);
            xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xhr.setRequestHeader("X-CSRFToken",csrf);
            const params = `phone=${phone}&type=getcode`;
            xhr.onload = function (e){
                if(this.status == 200){
                    const data = JSON.parse(this.responseText);
                    const gcoutput = document.getElementById("gcoutput");
                    gcoutput.innerHTML = data.validate;
                    gcoutput.style.color = "red";
                    console.log(data.validate);
                    if(data.valid){
                        console.log('Code retrieved');

                        getCodeButton.disabled = true;
                        //  codeInput.disabled = true;
                        verifyButton.classList.remove('disabled');
                        verifyButton.disabled = false;

                        var totalSeconds = 60;
                        var secondsRemaining = totalSeconds;

                        var countdown = setInterval(function() {
                        secondsRemaining--;
                        var minutes = Math.floor(secondsRemaining / 60);
                        var seconds = secondsRemaining % 60;
                        timerElement.textContent = ('0' + minutes).slice(-2) + ':' + ('0' + seconds).slice(-2);

                        if (secondsRemaining === 0) {
                             clearInterval(countdown);
                             console.log("Test")
                             verifyButton.disabled = false;
                             getCodeButton.disabled = false;
                             timer.innerHTML = "";

                             }
                          }, 1000);
                     };
                    
                }
               };
        
            xhr.send(params);
      };
     // getCodeButton.addEventListener('click', function() {
        // Perform code retrieval logic here
        // Replace the following line with your own logic


      //verifyButton.addEventListener('click', function() {
        // Perform code verification logic here
        // Replace the following line with your own logic
      //  console.log('Code verified');
     // });
   // });
            verifyCode.onsubmit = function (e){
            e.preventDefault();
            const code = document.getElementById("code-input").value;
            const xhr = new XMLHttpRequest();
            xhr.open("POST","{%url 'verify'%}",true);
            const csrf = document.querySelectorAll('input[name="csrfmiddlewaretoken"]')[1].getAttribute('value');
            xhr.setRequestHeader('X-CSRFToken',csrf);
            xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
            const params = `code=${code}&type=verify`;
            xhr.onload = function (e){
                if(this.status == 200){
                    const soutput = document.getElementById("soutput");
                    const data = JSON.parse(this.responseText);
                    console.log("dataaa",data);
                    if(data.action == 'redirect'){
                        console.log("inside the redirect");
                        window.location.href = data.url;
                    }
                    soutput.style.color = "red";
                    console.log("uuuuuuu...")
                    soutput.innerHTML = data.resp
                }
            };
            xhr.send(params);
            
        };