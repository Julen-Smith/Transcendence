<template>
	<div class="container">
        <div class="nav-bar">
            <a>Chat</a>
            <div class="min">
                <div class="minimize"></div>
            </div>
          <div class="close">
               <div class="line one"></div>
               <div class="line two"></div>
          </div>
        </div>
        <div class="messages-area">
          
          <div class="message one"></div>
          <div class="message two"></div>
          <div class="message three"></div>
          <div class="message four"></div>
          <div class="message five"></div>
          <div class="message six"></div>
        </div>
        <div class="sender-area">
          <div class="input-place">
              <input placeholder="Send a message." class="send-input" type="text">
              <div class="send">
                  <svg class="send-icon" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve"><g><g><path fill="#6B6C7B" d="M481.508,210.336L68.414,38.926c-17.403-7.222-37.064-4.045-51.309,8.287C2.86,59.547-3.098,78.551,1.558,96.808 L38.327,241h180.026c8.284,0,15.001,6.716,15.001,15.001c0,8.284-6.716,15.001-15.001,15.001H38.327L1.558,415.193 c-4.656,18.258,1.301,37.262,15.547,49.595c14.274,12.357,33.937,15.495,51.31,8.287l413.094-171.409 C500.317,293.862,512,276.364,512,256.001C512,235.638,500.317,218.139,481.508,210.336z"></path></g></g></svg>
              </div>
            </div>
        </div>
      <div></div></div>
  </template>
  
  <script>
  export default {
    name: 'ChatBox'
  };
  </script>
  
  <style scoped>
  .container {
    width: 300px;
    height: 320px;
    background-color: #343541;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    color: white;
    position: fixed;
    bottom: 0;
    right: 0;
  }
  
  .nav-bar {
    width: 100%;
    height: 40px;
    background-color: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .nav-bar a {
    color: #6B6C7B;
    white-space: nowrap;
    margin-left: 10px;
    user-select: none;
  }
  
  .close {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    cursor: pointer;
  }
  
  .line {
    position: absolute;
    width: 20px;
    height: 3px;
    background-color: #6B6C7B;
    border-radius: 30px;
  }
  
  .line.one {
    transform: rotate(45deg)
  }
  
  .line.two {
    transform: rotate(135deg)
  }

  .min {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    cursor: pointer;
  }
  .minimize {
    margin-left:175px;
    margin-top:10px;
    position: absolute;
    width: 20px;
    height: 3px;
    background-color: #6B6C7B;
    border-radius: 30px;
  }
  
  
  .messages-area {
    background-color: green;
    width: 100%;
    height: 210px;
  }
  
  .sender-area {
    background-color: #343541;
    width: 100%;
    height: 70px;
    display: flex;
    border-radius: 8px;
  }
  
  .message {
    width: 100%;
    height: 40px;
  }
  
  .message.one,
  .message.three,
  .message.five {
    background-color: #2E2F3A;
  }
  
  .message.two,
  .message.four,
  .message.six {
    background-color: #343541;
  }
  
  .send-img {
    width: 30px;
  }
  
  .send-input {
    outline: none;
    display: flex;
    border: none;
    background: none;
    height: 40px;
    width: 230px;
    border-radius: 7px;
    background: none;
    color: white;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    margin-left: 5px;
  }
  
  .send-input::placeholder {
    color: #828E9E;
  }
  
  .input-place {
    display: flex;
    flex-direction: row;
    margin-top: 15px;
    margin-left: 10px;
    align-items: center;
    background-color: #40414F;
    border-radius: 7px;
    height: 40px;
    width: 280px;
    gap: 5px;
    border: 1px solid #2E2F3A;
  }
  
  .send {
    width: 30px;
    height: 30px;
    background-color: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  
  .send-icon {
    width: 17px;
  }
  </style>
  