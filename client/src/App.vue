<template>
  <div id="app" class="bg-dark">
    <router-view />
    <Toast />
  </div>
</template>

<script>
import Toast from "@/components/Toast.vue";

export default {
  name: "App",
  components: {
    Toast,
  },
};
</script>

<style>
#app {
  font-family: "Montserrat", sans-serif, Helvetica, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
}
</style>
