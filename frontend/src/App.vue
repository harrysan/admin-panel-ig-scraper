<template>
  <the-header></the-header>
  <router-view v-slot="{ Component }">
    <transition name="route" mode="out-in"
      ><keep-alive> <component :is="Component" /> </keep-alive
    ></transition>
  </router-view>
  <the-footer></the-footer>
</template>

<script>
import TheHeader from "./components/layout/TheHeader.vue";
import TheFooter from "./components/layout/TheFooter.vue";

export default {
  components: {
    TheHeader,
    TheFooter,
  },
};
</script>

<style>
* {
  box-sizing: border-box;
  font-family: "Open Sans";
}

html,
body {
  /* font-family: "Open Sans"; */
  background-color: #f7fafc;
}

body {
  margin: 0;
  /* overflow: hidden; */
  position: relative;
  min-height: 100vh;
  padding-bottom: 5rem;
}

/*-----FONT-----*/
.font-light {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-weight: 300;
  font-style: normal;
}
.font-normal {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}
.font-medium {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
}
.font-semibold {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-weight: 600;
  font-style: normal;
}
.font-bold {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-weight: 700;
  font-style: normal;
}

/*-----COLOR-----*/
/* 
  Text : FFFFFF 
  Background : 1A202C
  Icon : 38B2AC
  Content : F7FAFC
  Grey : E9EAEC
  Grey Strip : 3B414B
  */
.background-bold {
  background-color: #1a202c;
}
.background-light {
  background-color: #f7fafc;
}
.background-icon {
  background-color: #38b2ac;
}
.background-white {
  background-color: #ffffff;
}
.background-grey {
  background-color: #e9eaec;
}
.text-white {
  color: #ffffff;
}
.text-icon {
  color: #38b2ac;
}
.color-grey {
  color: #e9eaec;
}
.color-grey-dark {
  color: #3b414b;
}

.profile-img {
  /* width: 100%; */
  height: 100px;
}

.route-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.route-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.route-enter-active {
  transition: all 0.3s ease-out;
}

.route-leave-active {
  transition: all 0.3s ease-in;
}

.route-enter-to,
.route-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
