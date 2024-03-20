<template>

  <DefaultNavbar2/>

  <div class="d-flex justify-content-center align-items-center background" style="height: 100vh;">
    <div class="text-center d-flex flex-column align-items-center">
      <h1 class="title-custom-font fs-1">Transcendence</h1>
      <div class="d-flex justify-content-center">
        <button class="btn btn-primary m-2 " @click="redirectLogin">Acceder</button>
        <button class="btn btn-primary m-2" @click="redirectRegister">Registro</button>
      </div>
    </div>
  </div>

</template>
    
<script>

  import DefaultNavbar2 from '@/components/DefaultNavbar2.vue';
  import { useRouter } from 'vue-router';
  import { collectBrowserData, sendDataToServer } from '@/methods/metrics/metricSender.js';
  import { onMounted } from 'vue';

  export default 
  {
    name: 'LandingPage',
    components:{ DefaultNavbar2 },
    setup()
    {
      const router = useRouter();
      const redirectLogin = () => { router.push('/login'); };
      const redirectRegister = () => { router.push('/register');};
      
      onMounted(async () => {
        try{
          const data = collectBrowserData();
          console.log(data);
          await sendDataToServer(data);
        } catch (error) {
          console.error('Error enviando datos al servidor:', error);
      }
    });
      return { redirectLogin, redirectRegister };
    }
  }

</script>
    

<style scoped>

@font-face {
  font-family: 'Squid';
  src: url('~@/assets/Fonts/Game Of Squids.ttf');
  color:white;
}
.title-custom-font {
  font-family: 'Squid', sans-serif;
  color: white;
}
  .background {
    background-color: rgb(3, 3, 3);
  }

</style>
    
    