<template>

  <DefaultNavbar></DefaultNavbar>

  <PopUpError v-if="popupTriggers.responseTrigger" :error-message="errorMessage" @close="popupTriggers.responseTrigger = false"></PopUpError>
  
  <div class="register-container">
    <div class="register-form">
      <h2>Registro</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="credentials.username">
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="credentials.email">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="credentials.password">
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña:</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword">
        </div>
        <button type="submit" :disabled="!isFormValid">Registrarse</button>
      </form>
       <!-- Boton Register Intra 42 -->
      <div>
      <button class="button_intra" @click="redirectToIntra">Registrarse con Intra 42</button>
      </div>
      <GoogleLogin buttonText="Register with Google"></GoogleLogin>
    </div>
  </div>

</template>
  
<script>

import GoogleLogin from '@/components/GoogleLogin.vue';
import DefaultNavbar from '@/components/DefaultNavbar.vue';
import PopUpError from '../components/PopUpError.vue';
import { ref, computed } from 'vue';
import { register } from '@/methods/api/login.js';
import { handleIntraRedirect } from '@/methods/api/login.js';

  export default {
  name: 'RegisterView',
  components: { DefaultNavbar, PopUpError, GoogleLogin},
  setup() {
    const errorMessage = ref('');
    const popupTriggers = ref({
      responseTrigger: false,
      timmedTrigger: false
    });
    const credentials = ref({
      username: '',
      email: '',
      password: ''
    });
    const confirmPassword = ref('');

    const isFormValid = computed(() => {
      return credentials.value.password === confirmPassword.value && credentials.value.email;
    });
    return { errorMessage, popupTriggers, credentials, confirmPassword, isFormValid };
  },
  methods: {
      async handleRegister () {
      const { success, error } = await register(this.credentials);
      if (!success) {
        this.errorMessage = error;
        this.popupTriggers.responseTrigger = true;
      } else {
        this.$router.push('/lobby');
      }
    },
    async redirectToIntra () {
      handleIntraRedirect();

    }
  }
};
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; 
    margin-top: 40px;
  }
  
  .register-form {
    width: 30%; 
    padding: 20px;
    background: white; 
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"], input[type="email"], input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: default;
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
  