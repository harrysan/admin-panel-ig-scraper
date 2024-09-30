<template>
  <div class="container-fluid mt-4">
    <div class="shadow mb-2 bg-body rounded py-1 mb-4">
      <div class="d-flex p-3 gap-3">
        <base-button link :to="userDetailLink">Detail</base-button>
        <base-button link :to="userPostLink">Posts</base-button>
        <base-button link :to="userStoryLink">Story</base-button>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  props: ["id"],
  computed: {
    userPostLink() {
      return "/users/" + this.id + "/posts";
    },
    userStoryLink() {
      return "/users/" + this.id + "/story";
    },
    userDetailLink() {
      return "/users/" + this.id + "/detail";
    },
  },
};
</script>
