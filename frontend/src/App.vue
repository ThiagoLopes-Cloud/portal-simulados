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
/* Estilos globais da aplicação */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}
</style>