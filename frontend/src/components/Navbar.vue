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
            <router-link :to="{ name: 'Clubs' }">
              <button type="button" class="me-2 my-1 btn btn-outline-secondary">
                <svg
                  class="nav-icons"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
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
                Explore Clubs
              </button>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'Dashboard' }">
              <button type="button" class="me-2 my-1 btn btn-outline-secondary">
                <svg
                  class="nav-icons"
                  width="24"
                  height="24"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M17.431,2.156h-3.715c-0.228,0-0.413,0.186-0.413,0.413v6.973h-2.89V6.687c0-0.229-0.186-0.413-0.413-0.413H6.285c-0.228,0-0.413,0.184-0.413,0.413v6.388H2.569c-0.227,0-0.413,0.187-0.413,0.413v3.942c0,0.228,0.186,0.413,0.413,0.413h14.862c0.228,0,0.413-0.186,0.413-0.413V2.569C17.844,2.342,17.658,2.156,17.431,2.156 M5.872,17.019h-2.89v-3.117h2.89V17.019zM9.587,17.019h-2.89V7.1h2.89V17.019z M13.303,17.019h-2.89v-6.651h2.89V17.019z M17.019,17.019h-2.891V2.982h2.891V17.019z"
                  ></path>
                </svg>
                Officer Dashboard
              </button>
            </router-link>
          </li>
          <li class="nav-item dropdown">
            <button
              type="button"
              class="me-2 my-1 btn btn-outline-primary dropdown-toggle"
              data-bs-toggle="dropdown"
            >
              <svg
                class="nav-icons"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                viewBox="0 0 16 16"
              >
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                <path
                  fill-rule="evenodd"
                  d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
                />
              </svg> 
              <span class="d-inline d-xs-inline d-sm-inline d-md-inline d-lg-none ms-2">Account</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  data-bs-toggle="modal"
                  data-bs-target="#profileModal"
                  @click="openProfile"
                  >Profile</a
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
.nav-icons {
  margin-bottom: 3px;
}
btn {
  margin-top: 8px;
}
</style>
