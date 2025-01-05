<template>
  <v-app>
    <Navbar1/>
      <!-- <POS/> -->
      <!-- <component v-bind:is="page" class="mx-4 md-4  main-div" ></component> -->
      <v-main class="pt-0" style="background: #F4F4F4;">
      <v-container fluid>
        <POS/>

      </v-container>

    </v-main>
  
   
  </v-app>
  </template>
  
  <script>
  import { ref } from 'vue';
  import Navbar1 from './components/Navbar1.vue';
  import POS from './components/zaraPos/Home.vue';

  
  export default {
    name: 'MyComponent',
    components: {
        Navbar1,
        POS
  },
    setup() {
      // Reactive data using ref
      // const message = ref('Hello from Vue 3!');
      // const counter = ref(0);
      const page = ref('POS');

  
      // Functions for handling actions
      const incrementCounter = () => {
        counter.value++;
      };
  
      const resetCounter = () => {
        counter.value = 0;
      };
  
      // Return data and methods to the template
      return {
        // message,
        // counter,
        // incrementCounter,
        // resetCounter,
      };
    },
  };
  </script>
  
  <style >
  .border-16{
  border-radius: 16px!important;
}
  </style>
  
  