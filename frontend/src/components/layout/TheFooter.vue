<template>
  <footer class="footercss background-bold">
    <div class="d-flex flex-column py-3 text-center">
      <div class="text-white">
        Find me on
        <a href="https://github.com/harrysan" target="_blank">github</a>
      </div>
      <div class="text-white">copyright <span>&#169;</span> {{ year }}</div>
    </div>
  </footer>
</template>

<script>
export default {
  setup() {
    const year = new Date().getFullYear();

    return { year };
  },
};
</script>

<style scoped>
.footercss {
  position: absolute;
  bottom: 0;
  width: 100%;
}

a:link,
a:visited,
a:hover,
a:active {
  text-decoration: none;
  color: #f9fafb;
}
</style>
