<template>
  <button class="rounded-button">
    <slot></slot>
  </button>
</template>

<script>
export default {
  setup() {
    return {};
  },
};
</script>

<style scoped>
.rounded-button {
  /* background-color: #37afa9; */
  color: white;
  border: none;
  border-radius: 25px; /* Half of the height to make it fully rounded */
  padding: 3px 15px;
  font-size: 14px;
  cursor: pointer;
  display: inline-block;
  text-align: center;
}

.rounded-button:hover {
  background-color: #2b8c85; /* Darker shade for hover effect */
}
</style>
