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
  <div v-else>
    <div class="container-xl p-md-5 p-4">
      <h1 class="text-info mb-3">Welcome{{ userData.firstName ? ", " + userData.firstName : " to the SAS Service Portal" }}!</h1>
      <div class="row pt-2">
        <div class="col-sm-6 mb-3">
          <div class="border rounded bg-white p-4">
            <h4 class="mb-3 text-info">Upcoming Events</h4>
            <h6 v-if="upcomingEvents.length==0" class='text-muted'>No upcoming events found.</h6>
            <ul v-else class="list-group list-container">
              <li v-for="event in upcomingEvents.slice(0,10)" :key="event.id" :set="club = findClubData(event.club)" class="d-flex list-group-item">
                <div>
                  <p class="mb-0 fw-bold text-dark">{{ event.name }}</p>
                  <p class='text-muted sub-text'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" class="mb-1" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1h8zm-7.978-1A.261.261 0 0 1 7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002a.274.274 0 0 1-.014.002H7.022zM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM6.936 9.28a5.88 5.88 0 0 0-1.23-.247A7.35 7.35 0 0 0 5 9c-4 0-5 3-5 4 0 .667.333 1 1 1h4.216A2.238 2.238 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816zM4.92 10A5.493 5.493 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275zM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0zm3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>
                    </svg>
                    {{ club.name }}
                  </p>
                  <p class='text-muted sub-text'>
                    <svg width="14" height="14" class="mb-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10,1.375c-3.17,0-5.75,2.548-5.75,5.682c0,6.685,5.259,11.276,5.483,11.469c0.152,0.132,0.382,0.132,0.534,0c0.224-0.193,5.481-4.784,5.483-11.469C15.75,3.923,13.171,1.375,10,1.375 M10,17.653c-1.064-1.024-4.929-5.127-4.929-10.596c0-2.68,2.212-4.861,4.929-4.861s4.929,2.181,4.929,4.861C14.927,12.518,11.063,16.627,10,17.653 M10,3.839c-1.815,0-3.286,1.47-3.286,3.286s1.47,3.286,3.286,3.286s3.286-1.47,3.286-3.286S11.815,3.839,10,3.839 M10,9.589c-1.359,0-2.464-1.105-2.464-2.464S8.641,4.661,10,4.661s2.464,1.105,2.464,2.464S11.359,9.589,10,9.589"></path>
                    </svg>
                    {{ event.location }}
                  </p>
                  <p class='text-muted sub-text'>
                    <svg width="14" height="14" class="mb-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10.25,2.375c-4.212,0-7.625,3.413-7.625,7.625s3.413,7.625,7.625,7.625s7.625-3.413,7.625-7.625S14.462,2.375,10.25,2.375M10.651,16.811v-0.403c0-0.221-0.181-0.401-0.401-0.401s-0.401,0.181-0.401,0.401v0.403c-3.443-0.201-6.208-2.966-6.409-6.409h0.404c0.22,0,0.401-0.181,0.401-0.401S4.063,9.599,3.843,9.599H3.439C3.64,6.155,6.405,3.391,9.849,3.19v0.403c0,0.22,0.181,0.401,0.401,0.401s0.401-0.181,0.401-0.401V3.19c3.443,0.201,6.208,2.965,6.409,6.409h-0.404c-0.22,0-0.4,0.181-0.4,0.401s0.181,0.401,0.4,0.401h0.404C16.859,13.845,14.095,16.609,10.651,16.811 M12.662,12.412c-0.156,0.156-0.409,0.159-0.568,0l-2.127-2.129C9.986,10.302,9.849,10.192,9.849,10V5.184c0-0.221,0.181-0.401,0.401-0.401s0.401,0.181,0.401,0.401v4.651l2.011,2.008C12.818,12.001,12.818,12.256,12.662,12.412"></path>
                    </svg>
                    {{ convertDate(event.startTime.split(" ")[0]) + " at " + event.startTime.split(" ")[1] }}
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <div class="col-sm-6 mb-3">
          <div class="border rounded bg-white p-4">
            <h4 class="mb-3 text-info">Quick Links</h4>
            <div class="list-group">
              <a v-for="link in filteredLinks" :key="link.id" :href="link.url" target="_blank" class="list-group-item list-group-item-action">
                <p class="mb-0 text-dark fw-bold">{{ link.name }}</p>
                <p class='text-muted sub-text'>
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-link-45deg" viewBox="0 0 16 16">
                    <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z"/>
                    <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243L6.586 4.672z"/>
                  </svg>
                  {{ link.url.substring(link.url.indexOf("//")+2) }}
                </p>
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="row pt-2">
        <div class="col-md-8">
          <div class="border rounded bg-white p-3">
            <DataTable
              :value="hours_array"
              :rowHover="true"
              responsiveLayout="scroll"
            >
              <template #header>
                <div class="d-flex align-items-center">
                  <h4 class="m-0 text-info">Your Hours</h4>
                </div>
              </template>
              <template #empty>No clubs found.</template>
              <Column field="name" header="Club" :sortable="true">
              </Column>
              <Column header="Status">
                  <template #body="{ data }">
                      <span v-if="data.isOfficer" :class="'badge bg-primary'">
                          Officer
                      </span>
                      <span v-else :class="'badge bg-secondary'">Member</span>
                  </template>
              </Column>
              <Column field="hours" header="Hours" :sortable="true">
              </Column>
            </DataTable>
          </div>
        </div>
        <div class="col-sm-4 d-none d-lg-block">
          <div class='border rounded bg-white p-3'>
            <h4 class="py-2 text-info">Stay Updated</h4>
            <h5>
              <a href="https://www.instagram.com/sas.servicecouncil" class="link-dark" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
                </svg>
                Instagram
              </a>
            </h5>
            <h5>
              <a href="https://www.facebook.com/sashsservco/" class="link-dark" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
                </svg>
                Facebook
              </a>
            </h5>
            <h5>
              <a href="https://www.youtube.com/channel/UCeTGs0-ltQk0BOAQ_PQJ8ww" class="link-dark" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                  <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
                </svg>
                YouTube
              </a>
            </h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api_service";
import DataTable from "primevue/datatable";
import Column from "primevue/column";

export default {
  name: "Home",
  components: {
    DataTable,
    Column,
  },
  data() {
    return {
      userData: {
        firstName: "",
        hours: {}
      },
      upcomingEvents: [],
      loading:false,
      links: []
    };
  },
  computed: {
    hours_array: function() {
      let hours_array = [];
      for (var key in this.userData.hours) {
        let hours_info = {};
        hours_info.name = key;
        hours_info.hours = this.userData.hours[key];
        hours_info.isOfficer = this.userData.officerClubs.includes(key);
        hours_array.push(hours_info);
      }
      return hours_array;
    },
    filteredLinks: function() {
      return this.links.filter((item) => {
          return item.category=="quick-links"
      });
    }
  },
  methods: {
    convertDate(dateString) {
      let dateTokens = dateString.split("-");
      return (
        dateTokens[2] +
        "/" +
        dateTokens[1] +
        "/" +
        dateTokens[0]
      );
    },
    getUserData() {
      this.loading=true;
      let endpoint = "/api/user/";
      apiService(endpoint).then((data) => {
        this.userData = data;
        if(data != "") this.populateUpcomingEvents();
        this.loading=false;
      });
    },
    populateUpcomingEvents() {
      let today = new Date();
      this.upcomingEvents = [];
      for (var club in this.userData.memberClubs) {
        let events = this.userData.memberClubs[club].events.filter((obj) => {
          return new Date(obj.startTime) >= today;
        });
        this.upcomingEvents.push(...events);
      }
      this.upcomingEvents.sort((a, b) =>
        new Date(a.startTime) > new Date(b.startTime)
          ? 1
          : new Date(b.startTime) > new Date(a.startTime)
          ? -1
          : 0
      );
    },
    findClubData(id){
      return this.userData.memberClubs.find(obj => {
          return obj.id === id
        })
    },
    getLinks(){
        let endpoint = "/api/link/";
        apiService(endpoint).then((data) => {
            this.links = [];
            this.links.push(...data);
        });
    }
  },
  mounted() {
    this.getUserData();
    this.getLinks();
  }
};
</script>

<style scoped>

h1, h4{
  font-family: 'Poppins', sans-serif;
}

.link-dark{
  text-decoration: none;
}

.link-dark:hover{
  color: rgb(100, 100, 100);
}

.sub-text{
  font-size: 12px;
  margin-bottom: 0px;
}

.list-container{
  max-height: 300px;
  overflow-y: auto;
}
</style>