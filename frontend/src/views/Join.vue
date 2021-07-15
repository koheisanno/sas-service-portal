<template>
  <div v-if="loading" class="d-flex justify-content-center">
    <div
      class="spinner-border mt-5 text-secondary"
      style="width: 5rem; height: 5rem"
      role="status"
    >
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="text-center" v-else>
    <h3 class="py-3">Welcome to {{ name }}!</h3>
    <p class="text-dark py-3">Now redirecting you to the home page...</p>
  </div>
</template>

<script>
import { apiService } from "../common/api_service";

export default {
  name: "Join",
  props: {
    query: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      name: null,
    };
  },
  methods: {
    getClubData() {
      let endpoint = `/api/club/${this.query}/`;
      apiService(endpoint).then((data) => {
        this.name = data.name;
      });
    },
    join() {
      let endpoint = `/api/club/${this.query}/membership/`;
      apiService(endpoint, "POST").then(() => {
        this.loading=false;
        setTimeout(() => {
          this.$router.push({ name: "Home" });
        }, 3000);
      });
    },
  },
  created() {
    this.getClubData();
    this.join();
  },
};
</script>
