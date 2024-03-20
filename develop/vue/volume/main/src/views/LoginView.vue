<template>
 
  <DefaultNavbar></DefaultNavbar>

  <div class="login-container" v-if="!showOTPVerification">
    <div class="login-info">
    </div>
    <div class="login-form">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="credentials.username" autocomplete="username">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="credentials.password" autocomplete="current-password">
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
        <div>
          <button class="button_intra" @click="redirectToIntra">Entrar con Intra 42</button>
        </div>
      <GoogleLogin></GoogleLogin>
    </div>
  </div>

  <PopUpError v-if="popupTriggers.responseTrigger" :error-message="errorMessage" @close="popupTriggers.responseTrigger = false"></PopUpError>
  
  <OTPVerification v-if="showOTPVerification"></OTPVerification>

</template>
  
<script>

import GoogleLogin from '@/components/GoogleLogin.vue';
import DefaultNavbar from '@/components/DefaultNavbar.vue';
import OTPVerification from '@/components/OtpVerification.vue';
import PopUpError from '@/components/PopUpError.vue';
import { login } from '@/methods/api/login.js';
import { handleIntraRedirect } from '@/methods/api/login.js';
import { ref } from 'vue';


export default {
  name: 'LoginView',
  components: { GoogleLogin, DefaultNavbar, OTPVerification, PopUpError },
  setup() {
    const errorMessage = ref('');
    const popupTriggers = ref({
      responseTrigger: false,
      timmedTrigger: false
    });
    const credentials = ref({
      username: '',
      password: ''
    });
    const showOTPVerification = ref(false);
    return { credentials , popupTriggers, errorMessage, showOTPVerification };
  },
  methods: 
  {
    async handleLogin() {
      try {
      const { success, error, status } = await login(this.credentials);
      if (!success) {
        if (status == 428)
          this.showOTPVerification = true;
        else
        {
          this.errorMessage = error;
          this.popupTriggers.responseTrigger = true;
        }
      } else {

        this.$router.push('/dashboard');
      }
    } catch (error) {
    console.error('Error during login:', error);
    }
    },
    async redirectToIntra () {
      handleIntraRedirect();
    }
  }
};


</script>
  
<style scoped>

.login-container
{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
    
.login-form 
{
  width: 15%;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width:50vh;
}
  
.form-group 
{
    margin-bottom: 15px;
}
  
label 
{
  display: block;
  margin-bottom: 5px;
}
  
input[type="text"], input[type="password"] 
{
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
  
button 
{
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  margin: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

button:hover 
{
  background-color: #45a049;
}

  .button_intra{
  background-color: black;
  color: white;
  padding: 10px 15px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}
.button_intra:hover {
  background-color: black; 
}




</style>
  