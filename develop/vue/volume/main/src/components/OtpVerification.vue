<template>
  <div class="otp-container">
    <form class="otp" @submit.prevent="verifyCode">
      <p class="heading">Verificar</p>
      <div class="check">
        <svg class="check" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="60px" height="60px" viewBox="0 0 60 60" xml:space="preserve">  <image id="image0" width="60" height="60" x="0" y="0" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAQAAACQ9RH5AAAABGdBTUEAALGPC/xhBQAAACBjSFJN
          AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZ
          cwAACxMAAAsTAQCanBgAAAAHdElNRQfnAg0NDzN/r+StAAACR0lEQVRYw+3Yy2sTURTH8W+bNgVf
          aGhFaxNiAoJou3FVEUQE1yL031BEROjCnf4PLlxILZSGYncuiiC48AEKxghaNGiliAojiBWZNnNd
          xDza3pl77jyCyPzO8ubcT85wmUkG0qT539In+MwgoxQoUqDAKDn2kSNLlp3AGi4uDt9xWOUTK3xg
          hVU2wsIZSkxwnHHGKZOxHKfBe6rUqFGlTkPaVmKGn6iYao1ZyhK2zJfY0FZ9ldBzsbMKxZwZjn/e
          5szGw6UsD5I0W6T+hBhjUjiF7bNInjz37Ruj3igGABjbtpIo3GIh30u4ww5wr3fwfJvNcFeznhBs
          YgXw70TYX2bY/ulkZhWfzfBbTdtrzjPFsvFI+T/L35jhp5q2owDs51VIVvHYDM9sa/LY8XdtKy1l
          FXfM8FVN2/X2ajctZxVXzPA5TZvHpfb6CFXxkerUWTOcY11LX9w0tc20inX2mmF4qG3upnNWrOKB
          hIXLPu3dF1x+kRWq6ysHpkjDl+7eQjatYoOCDIZF3006U0unVSxIWTgTsI3HNP3soSJkFaflMDwL
          3OoHrph9YsPCJJ5466DyOGUHY3Epg2rWloUxnMjsNw7aw3AhMjwVhgW4HYm9FZaFQZ/bp6QeMRQe
          hhHehWKXGY7CAuSpW7MfKUZlAUqWdJ3DcbAAB3guZl9yKC4WYLfmT4muFtgVJwvQx7T2t0mnXK6J
          XlGGyAQvfNkaJ5JBmxnipubJ5HKDbJJsM0eY38QucSx5tJWTVHBwqDDZOzRNmn87fwDoyM4J2hRz
          NgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMy0wMi0xM1QxMzoxNTo1MCswMDowMKC8JaoAAAAldEVY
          dGRhdGU6bW9kaWZ5ADIwMjMtMDItMTNUMTM6MTU6NTArMDA6MDDR4Z0WAAAAKHRFWHRkYXRlOnRp
          bWVzdGFtcAAyMDIzLTAyLTEzVDEzOjE1OjUxKzAwOjAwIIO3fQAAAABJRU5ErkJggg=="></image></svg>
      </div>
      <div class="box">
        <input class="input" type="password" maxlength="1" v-model="otp[0]" @input="focusNext($event, 'input2')" ref="input1">
        <input class="input" type="password" maxlength="1" v-model="otp[1]" @input="focusNext($event, 'input3')" ref="input2">
        <input class="input" type="password" maxlength="1" v-model="otp[2]" @input="focusNext($event, 'input4')" ref="input3">
        <input class="input" type="password" maxlength="1" v-model="otp[3]" ref="input4">
      </div>
      <a v-on:click="log">No has recibido el mensaje?</a> <!--Meterle algo guay-->
      <button class="btn1">Enviar</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      otp: ['', '', '', '']
    };
  },
  methods: {
  verifyCode() {
    const otpCode = this.otp.join('');
    console.log('Verificando código:', otpCode);
    if (otpCode)
      this.$router.push("/dashboard")
  },
  focusNext(event, nextInputRef) {
    if(event.target.value.length === 1 && this.$refs[nextInputRef]) {
     this.$refs[nextInputRef].focus();
  }

},
log() {
    console.log("No se ha recibido el mensaje");
  }
}
};
</script>

<style scoped>
.otp-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.otp {
  width: 300px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 15px;
  background-color: white;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.heading {
  margin-bottom: 20px;
  font-weight: bold;
}

.check {
  margin-bottom: 20px;
}

.box {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 20px;
}

.input {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  border: 1px solid #ddd;
  text-align: center;
}

.btn1, .btn2 {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border-radius: 5px;
  border: none;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
}

.btn1:hover, .btn2:hover {
  background-color: #45a049;
}
</style>
