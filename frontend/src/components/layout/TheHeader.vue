<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand text-white" href="#">
        <img
          src="../../assets/icon/insta.png"
          class="img-fluid"
          width="28"
          height="24"
          alt="Web App Logo"
        />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link
              to="/dashboard"
              class="nav-link active text-white"
              aria-current="page"
              >Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              to="/users"
              class="nav-link active text-white"
              aria-current="page"
              >Users</router-link
            >
          </li>
          <li class="nav-item">
            <div class="nav-link color-grey-dark" aria-current="page">
              Posts
            </div>
          </li>
          <li class="nav-item">
            <div class="nav-link color-grey-dark" aria-current="page">
              Story
            </div>
          </li>
        </ul>
        <div class="d-flex">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link
                to="/feedback"
                class="nav-link active text-white"
                aria-current="page"
                >Feedback</router-link
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  setup() {
    return {};
  },
};
</script>

<style scoped>
.dropdown-menu {
  background: transparent;
}
</style>
