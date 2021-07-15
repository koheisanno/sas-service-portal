<template>
  <div>
    <h1 class="py-3">Welcome! You just joined {{ name }}</h1>
    <h2 class="py-3">Now redirecting you to the home page...</h2>
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
      apiService(endpoint, "POST");
      setTimeout(() => {
        this.$router.push({ name: "Home" });
      }, 3000);
    },
  },
  created() {
    this.getClubData();
    this.join();
  },
};
</script>
