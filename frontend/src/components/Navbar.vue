<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white shadow">
    <div class="container-md">
      <router-link
        :to="{ name: 'Home' }"
        class="navbar-brand"
        style="color: #ff6e6e"
        ><img src="../assets/img/logo.png" width="32" />AS Service Portal
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link :to="{ name: 'Home' }">
              <a class="nav-link" href="#">
                <div class="nav-icon-container">
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-house-door" viewBox="0 0 16 16">
                    <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5z"/>
                  </svg>
                </div>
                Home
              </a>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'Clubs' }">
              <a class="nav-link" href="#">
                <div class="nav-icon-container">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="30"
                    height="30"
                    fill="currentColor"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M8 16.016a7.5 7.5 0 0 0 1.962-14.74A1 1 0 0 0 9 0H7a1 1 0 0 0-.962 1.276A7.5 7.5 0 0 0 8 16.016zm6.5-7.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"
                    />
                    <path
                      d="m6.94 7.44 4.95-2.83-2.83 4.95-4.949 2.83 2.828-4.95z"
                    />
                  </svg>
                </div>
                Explore Clubs
              </a>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'Dashboard' }">
              <a class="nav-link" href="#">
                <div class="nav-icon-container">
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M6 1v3H1V1h5zM1 0a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V1a1 1 0 0 0-1-1H1zm14 12v3h-5v-3h5zm-5-1a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-5zM6 8v7H1V8h5zM1 7a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1H1zm14-6v7h-5V1h5zm-5-1a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V1a1 1 0 0 0-1-1h-5z"/>
                  </svg>
                </div>
                Dashboard
              </a>
            </router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link" href="#" data-bs-toggle="dropdown">
              <div class="nav-icon-container">
                <svg
                  class="nav-icons"
                  xmlns="http://www.w3.org/2000/svg"
                  width="30"
                  height="30"
                  fill="currentColor"
                  viewBox="0 0 16 16"
                >
                  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                  <path
                    fill-rule="evenodd"
                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
                  />
                </svg> 
              </div>
              Profile
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  data-bs-toggle="modal"
                  data-bs-target="#profileModal"
                  @click="openProfile"
                  >Edit Profile</a
                >
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <a class="dropdown-item" href="/accounts/logout/">Logout</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBarComponent",
};
</script>

<style scoped>
.navbar-brand {
  font-family: "Pattaya", sans-serif;
  font-size: 20px;
}

.nav-icon-container{
  text-align: center;
}

.nav-link{
  font-size: 12px;
}

li a{
  text-decoration:none;
}

@media (max-width: 991px) {
  .nav-icon-container{
    display: inline;
    width: 30px;
  }
  .nav-link{
    font-size: 14px;
  }
}

</style>
