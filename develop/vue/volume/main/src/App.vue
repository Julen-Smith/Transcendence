<template>
  <!DOCTYPE html>
  <html lang="es">
  <head>
    <meta charset="UTF-8">
    <link href="https://cdn.lineicons.com/4.0/lineicons.css" rel="stylesheet" />
  </head>
<body>
  <div id="app">
    <router-view></router-view>
  </div>
</body>
  </html>
</template>

<script>

export default {

  name: 'App'
};

</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000000;
}

</style>