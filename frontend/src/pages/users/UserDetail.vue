<template>
  <h5 class="mt-3 px-3 py-3 background-grey">User Detail</h5>
  <div v-if="isLoading">
    <base-spinner></base-spinner>
  </div>
  <div v-else-if="hasUsers" class="px-1 py-1">
    <div class="mx-3 d-md-flex align-content-start gap-5 lh-lg mb-3">
      <div class="d-flex flex-column">
        <ul class="list-group list-group-flush">
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Username</div>
              {{ detail_user.data.username }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Fullname</div>
              {{ detail_user.data.full_name }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Is Private</div>
              {{ detail_user.data.is_private }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Profile Pic</div>
              <img
                :src="fetchUserImage(detail_user.data.profile_pic_url)"
                alt="profile_pic_url_hd"
                class="img-thumbnail rounded mx-auto d-block profile-img"
              />
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Profile Pic HD</div>
              <img
                :src="fetchUserImage(detail_user.data.profile_pic_url_hd)"
                alt="profile_pic_url_hd"
                class="img-thumbnail rounded mx-auto d-block profile-img"
              />
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Is Verified</div>
              {{ detail_user.data.is_verified }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Media</div>
              {{ detail_user.data.media_count }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Follower</div>
              {{ detail_user.data.follower_count }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Following</div>
              {{ detail_user.data.following_count }}
            </div>
          </li>
        </ul>
      </div>
      <div class="d-flex flex-column">
        <ul class="list-group list-group-flush">
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Biography</div>
              {{ detail_user.data.biography }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Account Type</div>
              {{ detail_user.data.account_type }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Is Bussiness</div>
              {{ detail_user.data.is_business }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Public Email</div>
              {{ detail_user.data.public_email }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Phone Country Code</div>
              {{ detail_user.data.public_phone_country_code }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Phone Number</div>
              {{ detail_user.data.public_phone_number }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Business Category Name</div>
              {{ detail_user.data.business_category_name }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Category Name</div>
              {{ detail_user.data.category_name }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Category</div>
              {{ detail_user.data.category }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">City</div>
              {{ detail_user.data.city_name }}
            </div>
          </li>
          <li
            class="list-group-item d-flex justify-content-between align-items-start"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">Zip</div>
              {{ detail_user.data.zip }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from "vue";

export default {
  props: ["id"],
  mounted() {
    this.fetchData();
  },
  computed: {
    hasUsers() {
      return !this.isLoading && this.detail_user.data.id != "";
    },
  },
  setup(props) {
    const detail_user = reactive({});
    const pk = ref("");
    const imageUser = ref(null);
    const isLoading = ref(true);

    async function fetchData() {
      this.isLoading = true;
      const url = `http://127.0.0.1:9000/users/${props.id}`;

      try {
        this.detail_user.data = await fetch(url)
          .then((response) => response.json())
          .then((data) => (detail_user.data = data));
      } catch (err) {
        this.error = err.toString();
      } finally {
        this.isLoading = false;
        this.pk = this.detail_user.pk;
      }
    }

    function fetchUserImage(param) {
      try {
        var response = `http://127.0.0.1:9000/profile_img/${param}`;

        return response;
      } catch (err) {
        this.error = err.toString();
      }
    }

    return {
      fetchData,
      detail_user,
      pk,
      fetchUserImage,
      imageUser,
      isLoading,
    };
  },
};
</script>
