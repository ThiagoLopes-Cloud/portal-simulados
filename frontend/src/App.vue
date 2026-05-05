<template>
  <!-- router-view é o componente do Vue Router -->
  <!-- Ele renderiza a página correspondente à URL atual -->
  <!-- Ex: se a URL for /login, renderiza o LoginPage.vue -->
  <router-view />
</template>

<script setup>
// App.vue é o componente raiz — ele só precisa do router-view
// Toda a lógica fica nas páginas individuais
</script>

<style>
*, *::before, *::after {
  box-sizing: border-box;
}

html {
  overflow-x: hidden;
  -webkit-text-size-adjust: 100%;
  touch-action: manipulation;
}
</style>