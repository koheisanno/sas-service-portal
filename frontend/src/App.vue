<template>
  <div class="bg-light">
    <NavBarComponent :is_auth="is_auth"/>
    <ProfileModal />
    <router-view :is_auth="is_auth"/>
    <Footer />
  </div>
</template>

<script>
import NavBarComponent from "./components/Navbar.vue";
import ProfileModal from "./components/ProfileModal.vue";
import Footer from "./components/Footer.vue";
import { apiService } from "./common/api_service";

export default {
  name: "Home",
  components: {
    NavBarComponent,
    ProfileModal,
    Footer
  },
  data() {
    return {
        is_auth: false,
    };
  },
  methods: {
    getIsAuthenticated(){
      let endpoint = "/api/user-isauth/";
        apiService(endpoint).then((data) => {
          this.is_auth = data;
        });
    }
  },
  mounted(){
    this.getIsAuthenticated();
  },
};
</script>
<style>
svg {
  cursor: pointer;
}

* {
  font-family: 'Open Sans', sans-serif;
}
</style>