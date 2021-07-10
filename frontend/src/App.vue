<template>
  <div class="bg-light">
    <NavBarComponent />
    <ProfileModal />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import NavBarComponent from "./components/Navbar.vue";
import ProfileModal from "./components/ProfileModal.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "Home",
  components: {
    NavBarComponent,
    ProfileModal,
    Footer
  },
};
</script>
<style>
svg {
  cursor: pointer;
}
</style>