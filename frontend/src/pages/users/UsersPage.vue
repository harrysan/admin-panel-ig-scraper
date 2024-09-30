<template>
  <div class="container-lg mt-4">
    <div class="container shadow p-3 mb-5 bg-body rounded px-2 py-1">
      <h2 class="font-bold text-dark mt-2 mb-2 p-3">Users</h2>
      <div class="row mb-3">
        <div class="col-md-6 mb-2">
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            placeholder="Search..."
          />
        </div>
        <div class="col-md-3 mb-2">
          <select v-model="selectedPrivate" class="form-control">
            <option value="">Filter by Private</option>
            <option v-for="pvt in uniquePrivates" :key="pvt" :value="pvt">
              {{ pvt }}
            </option>
          </select>
        </div>
        <div class="col-md-3 text-right">
          <base-button @click="exportToCSV">Export to CSV</base-button>
        </div>
      </div>
      <div class="table-responsive mt-3">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th scope="col" @click="sortTable('username')">Username</th>
              <th scope="col" @click="sortTable('fullname')">Fullname</th>
              <th scope="col">Private</th>
              <th scope="col">Description</th>
              <th scope="col">Follower</th>
              <th scope="col">Following</th>
              <th scope="col">Detail</th>
            </tr>
          </thead>
          <div v-if="isLoading">
            <base-spinner></base-spinner>
          </div>
          <tbody v-else-if="hasUsers">
            <tr v-for="(item, index) in paginatedData" :key="index">
              <td>{{ item.username }}</td>
              <td>{{ item.full_name }}</td>
              <td>
                <base-option
                  :style="{
                    backgroundColor:
                      item.is_private == '1' ? '#38b2ac' : 'black',
                    // color: item.private ? 'white' : 'black',
                  }"
                  >{{ item.is_private }}</base-option
                >
              </td>
              <td>{{ item.biography }}</td>
              <td>{{ item.follower_count }}</td>
              <td>{{ item.following_count }}</td>
              <td>
                <base-button link :to="'/users/' + item.id">Detail</base-button>
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
  </div>
</template>

<script>
import { reactive, ref } from "vue";

export default {
  created() {
    this.fetchData();
  },
  computed: {
    uniquePrivates() {
      // Mengambil daftar unik dari semua kota yang tersedia
      var privateitem;
      if (this.users.data?.length) {
        privateitem = this.users.data.map((item) => item.is_private);
      }

      return [...new Set(privateitem)];
    },
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

      // Filter berdasarkan kota yang dipilih dari dropdown
      if (this.selectedPrivate === false) {
        data = data.filter((item) => item.is_private === this.selectedPrivate);
      } else if (this.selectedPrivate === true) {
        data = data.filter((item) => item.is_private === this.selectedPrivate);
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
    exportToCSV() {
      const data = this.sortedData.map((item) => ({
        Username: item.username,
        Fullname: item.full_name,
        Private: item.is_private,
        // Description: item.biography,
        Follower: item.follower_count,
        Following: item.following_count,
      }));
      const csvContent = [
        Object.keys(data[0]).join(","), // Header
        ...data.map((row) => Object.values(row).join(",")), // Data rows
      ].join("\n");
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const link = document.createElement("a");
      const url = URL.createObjectURL(blob);

      link.setAttribute("href", url);
      link.setAttribute("download", "data.csv");
      link.style.visibility = "hidden";

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  },
  watch: {
    searchQuery() {
      this.currentPage = 1; // Reset ke halaman 1 ketika melakukan pencarian
    },
    selectedCity() {
      this.currentPage = 1; // Reset ke halaman 1 ketika memilih filter kota
    },
  },
  setup() {
    const searchQuery = ref("");
    const selectedPrivate = ref("");
    const sortKey = ref("name");
    const sortOrder = ref(1);
    const currentPage = ref(1);
    const itemsPerPage = 7;
    const users = reactive({});
    const selectedUser = reactive({});
    const isLoading = ref(true);
    const error = ref("");

    async function fetchData() {
      this.isLoading = true;

      try {
        this.users.data = await fetch("http://127.0.0.1:9000/users")
          .then((response) => response.json())
          .then((data) => (users.data = data));
      } catch (err) {
        this.error = err.toString();
      } finally {
        this.isLoading = false;
      }
    }

    return {
      searchQuery,
      selectedPrivate,
      sortKey,
      sortOrder,
      currentPage,
      itemsPerPage,
      users,
      selectedUser,
      isLoading,
      error,
      fetchData,
    };
  },
};
</script>

<style scoped>
.form-control:focus {
  border-color: #38b2ac;
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}
.buttoncss {
  border: none;
  cursor: pointer;
  appearance: none;
  background-color: inherit;
}
.modal-backdrop.show {
  background-color: grey;
  opacity: 0.3;
}
</style>
