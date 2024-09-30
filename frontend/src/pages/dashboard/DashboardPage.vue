<template>
  <div>
    <div class="container-lg py-3 mt-3">
      <div class="container p-3 mb-3 px-2 py-1">
        <div class="d-flex row-flex">
          <div class="p-4 border rounded background-icon text-white shadow">
            <div class="d-flex gap-5 row-flex-item">
              <div>
                <h5 class="font-light">Total Users</h5>
                <h4>{{ count_users }}</h4>
              </div>
              <img
                src="../../assets/icon/users.png"
                class="img-fluid"
                width="72"
                height="72"
                alt="Users Logo"
              />
            </div>
          </div>
          <div class="p-4 border rounded background-icon text-white shadow">
            <div class="d-flex gap-5 row-flex-item">
              <div>
                <h5 class="font-light">Total Posts</h5>
                <h4>{{ count_posts }}</h4>
              </div>
              <img
                src="../../assets/icon/posts.png"
                class="img-fluid"
                width="72"
                height="72"
                alt="Users Logo"
              />
            </div>
          </div>
          <div class="p-4 border rounded background-icon text-white shadow">
            <div class="d-flex gap-5 row-flex-item">
              <div>
                <h5 class="font-light">Total Story</h5>
                <h4>{{ count_stories }}</h4>
              </div>
              <img
                src="../../assets/icon/stories.png"
                class="img-fluid"
                width="72"
                height="72"
                alt="Users Logo"
              />
            </div>
          </div>
        </div>
        <div class="mt-5" v-if="isLoading">
          <base-spinner></base-spinner>
        </div>
        <div
          v-else
          class="container shadow p-3 mb-5 bg-body rounded px-2 py-1 mt-5"
        >
          <h3 class="font-semibold text-dark mt-2 mb-2 p-3">Scrap User</h3>
          <div class="row p-3 background-grey">
            <div class="col">Please fill field below.</div>
          </div>
          <form class="p-3" @submit.prevent="sendScrap">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="username"
                placeholder="Username to Scrap"
              />
            </div>
            <base-button>Send</base-button>
          </form>
          <div class="mt-1 p-3" v-if="isDone">
            Successfully Scrap. Please check on users page :) !
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dateFormat from "dateformat";
import { ref } from "vue";

export default {
  created() {
    this.countDatas("count_users");
    this.countDatas("count_posts");
    this.countDatas("count_stories");
  },
  setup() {
    const now = new Date();
    const datetoday = dateFormat(now, "dddd, mmmm dS, yyyy, h:MM:ss TT");
    const count_users = ref(0);
    const count_posts = ref(0);
    const count_stories = ref(0);
    const isLoading = ref(true);
    const username = ref("");
    const isDone = ref(false);

    async function countDatas(param) {
      this.isLoading = true;

      try {
        var response = await fetch(`http://127.0.0.1:9000/api/${param}`)
          .then((response) => response.json())
          .then((data) => (response = data));
      } catch (err) {
        this.error = err.toString();
      } finally {
        this.isLoading = false;

        if (param == "count_users") {
          this.count_users = response.user_count;
        } else if (param == "count_posts") {
          this.count_posts = response.post_count;
        } else if (param == "count_stories") {
          this.count_stories = response.story_count;
        }
      }
    }

    async function sendScrap() {
      this.isLoading = true;
      this.isDone = false;

      var data = {
        username: username.value,
      };

      try {
        await fetch(`http://127.0.0.1:9000/scrap`, {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });

        username.value = "";
      } catch (error) {
        console.log(error);
      } finally {
        this.isLoading = false;
        this.isDone = true;
      }
    }

    return {
      datetoday,
      isLoading,
      count_users,
      count_posts,
      count_stories,
      countDatas,
      username,
      isDone,
      sendScrap,
    };
  },
};
</script>

<style scoped>
.row-flex {
  gap: 30px;
}

/* Media Queries */
@media (max-width: 768px) {
  .gap-icon-dashboard {
    gap: 3px;
  }
  .row-flex {
    flex-direction: column;
    gap: 10px;
  }
  .row-flex-item {
    justify-content: space-between;
  }
}
</style>
