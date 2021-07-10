<template>
  <div>
    <h1>You just left {{ name }}</h1>
    <h2>Now redirecting you to the home page...</h2>
  </div>
</template>

<script>
import { apiService } from "../common/api_service";

export default {
  name: "Leave",
  props: {
    id: {
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
      let endpoint = `/api/clubs/${this.id}`;
      apiService(endpoint).then((data) => {
        this.name = data.name;
      });
    },
    leave() {
      let endpoint = `/api/clubs/${this.id}/membership`;
      apiService(endpoint, "DELETE");
      setTimeout(() => {
        this.$router.push({ name: "Home" });
      }, 3000);
    },
  },
  created() {
    this.getClubData();
    this.leave();
  },
};
</script>
