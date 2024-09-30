<template>
  <button v-if="!link" class="btn btn-class" type="submit">
    <slot></slot>
  </button>
  <router-link class="btn btn-class" v-else :to="to">
    <slot></slot>
  </router-link>
</template>

<script>
export default {
  props: {
    mode: {
      type: String,
      required: false,
      default: null,
    },
    link: {
      type: Boolean,
      required: false,
      default: false,
    },
    to: {
      type: String,
      required: false,
      default: "/",
    },
  },
  setup() {
    return {};
  },
};
</script>

<style scoped>
/* small screen */
@media (max-width: 575.98px) {
  .btn-class {
    background-color: #38b2ac;
    color: #f9fafb;
  }
}

.btn-class {
  background-color: #38b2ac;
  color: #f9fafb;
}
</style>
