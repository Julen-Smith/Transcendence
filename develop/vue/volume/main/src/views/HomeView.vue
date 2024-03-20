<template>

  <DefaultNavbar></DefaultNavbar>
  
  <div v-if="!videoLoaded" class="loading-screen">
    <LoadingScreen></LoadingScreen>
  </div>

  <div v-else class="onLoaded">

    <div class="video-background">
      <div class="video-background" :class="{ 'video-loaded': videoLoaded }"></div>
      <video preload="auto" autoplay loop muted playsinline @loadstart="videoLoaded = true">
        <source src="" type="video/webm">
        Tu navegador no soporta videos.
     </video>
    </div>

    <div class="content">
      <h1>Transcendence</h1>
      <p>Prueba deploy Bienvenido a la página de inicio del proyecto Transcendence</p>
      <div class="button-container">
        <button class="btn btn-primary" @click="redirect_login">Login</button>
        <button class="btn btn-primary" @click="redirect_register">Registrarse</button>
      </div>
    </div>

  </div> 

</template>
  
<script>

import DefaultNavbar from '@/components/DefaultNavbar.vue';
import LoadingScreen from '@/components/LoadingScreen.vue';

  export default 
  {
    name: 'HomeView',
    data()
    {
      return {
        videoLoaded: false
    };
  },
  
  mounted()
  {
    setTimeout(() => 
    {
      this.videoLoaded = true;
    }, 500);
    },
    
    methods: 
    {
        redirect_login()
        {
            this.$router.push('/login');
        },
        redirect_register()
        {
            this.$router.push('/register');
        }
    },
  components: { DefaultNavbar, LoadingScreen }
}

</script>
  

<style scoped>

@font-face
{
  font-family: Squid;
  src: url('~@/assets/Fonts/Game Of Squids.ttf');
}

.navbar
{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 2;
}

.navbar li
{
  margin-left: 50px;
}

.video-background
{
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -1;
}

.video-background video
{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
}

.video-background::before
{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7); 
  z-index: 1; 
}
.content 
{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1; 
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.content h1 
{
  font-size: 10.5em;
  color : white;
  font-family: Squid;
}

.content p 
{
  color : white;
}


.button-container 
{
  display: flex;
  justify-content: center; 
  gap: 10px;
}

</style>
  
  