<template>
  <div>
    <h5 class="mt-3 px-3 py-3 background-grey">User Posts</h5>
    <div class="table-responsive mt-5 px-3">
      <table class="table table-hover">
        <thead class="table-light">
          <tr class="align-top">
            <th scope="col">Pk</th>
            <th scope="col">Id</th>
            <th scope="col">Code</th>
            <th scope="col">Taken At</th>
            <th scope="col">Media Type</th>
            <th scope="col">Thumbnail</th>
            <th scope="col">Comment</th>
            <th scope="col">Like</th>
            <th scope="col">Caption</th>
            <th scope="col">Video</th>
            <th scope="col">Viewers</th>
            <th scope="col">Duration</th>
            <th scope="col">Tags</th>
          </tr>
        </thead>
        <div v-if="isLoading">
          <base-spinner></base-spinner>
        </div>
        <tbody v-else-if="hasUsers">
          <tr v-for="item in paginatedData" :key="item.id">
            <td>{{ item.pk }}</td>
            <td>{{ item.id }}</td>
            <td>{{ item.code }}</td>
            <td>{{ item.taken_at }}</td>
            <td>{{ mediaType(item.media_type, item.product_type) }}</td>
            <td>
              <img
                v-if="item.thumbnail_url"
                :src="fetchUserImage(item.thumbnail_url)"
                alt="thumbnail_url"
                class="img-thumbnail rounded mx-auto d-block profile-img"
              />
            </td>
            <td>{{ item.comment_count }}</td>
            <td>{{ item.like_count }}</td>
            <td class="text-wrap" style="">
              {{ item.caption_text }}
            </td>
            <td>
              <video v-if="item.video_url" controls width="320" height="240">
                <source
                  :src="fetchUserImage(item.video_url)"
                  type="video/mp4"
                />
                Your browser does not support the video tag.
              </video>
            </td>
            <td>{{ item.view_count }}</td>
            <td>{{ item.video_duration }}</td>
            <td>
              <!-- Tampilkan loading icon jika sedang memuat tags -->
              <span v-if="loadingTags[item.id]"
                ><base-spinner></base-spinner
              ></span>
              <!-- Tampilkan tags jika sudah diambil -->
              <span v-else>{{ postTags[item.id] || "" }}</span>
              <!-- Tombol untuk mengambil tags -->
              <base-button
                v-if="
                  typeof postTags[item.id] !== 'string' && !loadingTags[item.id]
                "
                @click="fetchPostTags(item.id)"
                >Tags</base-button
              >
            </td>
          </tr>
        </tbody>
      </table>
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage--"
              >Previous</a
            >
          </li>
          <li
            class="page-item"
            v-for="page in totalPages"
            :key="page"
            :class="{ active: currentPage === page }"
          >
            <a class="page-link" href="#" @click.prevent="goToPage(page)">{{
              page
            }}</a>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
            <a class="page-link" href="#" @click.prevent="currentPage++"
              >Next</a
            >
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";

export default {
  props: ["id"],
  mounted() {
    this.fetchData();
    console.log(this.postTags);
    // console.log("mounted");
  },
  computed: {
    filteredData() {
      let data = this.users.data;

      // Filter berdasarkan query pencarian
      if (this.searchQuery) {
        data = data.filter((item) => {
          return Object.keys(item).some((key) => {
            return String(item[key])
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase());
          });
        });
      }

      return data;
    },
    sortedData() {
      var sortedData;
      if (this.filteredData?.length) {
        sortedData = this.filteredData.slice().sort((a, b) => {
          return (a[this.sortKey] > b[this.sortKey] ? 1 : -1) * this.sortOrder;
        });
      }
      return sortedData;
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      var paginatedData;
      if (this.sortedData?.length) {
        paginatedData = this.sortedData.slice(start, end);
      }
      return paginatedData;
    },
    totalPages() {
      var totalPages = 0;
      if (this.filteredData?.length) {
        totalPages = Math.ceil(this.filteredData.length / this.itemsPerPage);
      }
      return totalPages;
    },
    hasUsers() {
      return !this.isLoading && this.users.data.length > 0;
    },
  },
  methods: {
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortOrder = -this.sortOrder;
      } else {
        this.sortKey = key;
        this.sortOrder = 1;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
  },
  setup(props) {
    const searchQuery = ref("");
    const sortKey = ref("name");
    const sortOrder = ref(1);
    const currentPage = ref(1);
    const itemsPerPage = 7;
    const users = reactive({});
    const isLoading = ref(true);
    const error = ref("");
    const postTags = ref({}); // Menyimpan tags berdasarkan post id
    const loadingTags = ref({}); // Menyimpan status loading untuk tiap post

    async function fetchData() {
      this.isLoading = true;

      try {
        // Get User Pk
        const response = await fetch(`http://127.0.0.1:9000/users/${props.id}`);
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        const json = await response.json();

        // Get Posts
        this.users.data = fetch(
          `http://127.0.0.1:9000/posts/by_user_pk/${json.pk}`
        )
          .then((response) => response.json())
          .then((data) => (users.data = data));
      } catch (err) {
        this.error = err.toString();
      } finally {
        this.isLoading = false;
      }
    }

    function fetchUserImage(param) {
      try {
        var response = `http://127.0.0.1:9000/post_img/${param}`;

        return response;
      } catch (err) {
        this.error = err.toString();
      }
    }

    function mediaType(media, type) {
      var media_type = "";
      if (media == 1) {
        media_type = "Photo";
      } else if (media == 2 && type == "feed") {
        media_type = "Video";
      } else if (media == 2 && type == "igtv") {
        media_type = "IGTV";
      } else if (media == 2 && type == "clips") {
        media_type = "Reel";
      } else if (media == 8) {
        media_type = "Album";
      }

      return media_type;
    }

    async function fetchPostTags(post_id) {
      var tags = "";
      // Set status loading untuk post ini
      this.loadingTags[post_id] = true;

      try {
        const response = await fetch(
          `http://127.0.0.1:9000/post_tags/by_post_id/${post_id}`
        ).then((response) => response.json());

        for (let i = 0; i < response.length; i++) {
          let obj = response[i];
          tags += obj.username + ",";
        }
        const post_tags = tags.slice(0, -1);

        // Menyimpan hasil tags untuk post ini
        this.postTags[post_id] = post_tags;
      } catch (error) {
        console.error(`Error fetching tags for post ${post_id}:`, error);
      } finally {
        // Hapus status loading setelah API call selesai
        this.loadingTags[post_id] = false;
      }
    }

    return {
      searchQuery,
      sortKey,
      sortOrder,
      currentPage,
      itemsPerPage,
      users,
      isLoading,
      error,
      fetchData,
      fetchUserImage,
      mediaType,
      fetchPostTags,
      postTags,
      loadingTags,
    };
  },
};
</script>
