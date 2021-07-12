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
  <div v-else class="container-xl p-5">
    <h1 class="text-secondary mb-3">Welcome, {{ userData.firstName }}!</h1>
    <div class="row pt-2">
      <div class="col-sm-6 mb-3">
        <div class="border rounded bg-white p-4">
          <h4 class="mb-3">Upcoming Events</h4>
          <h6 v-if="upcomingEvents.length==0" class='text-muted'>No upcoming events found.</h6>
          <ul v-else class="list-group list-container">
            <li v-for="event in upcomingEvents.slice(0,10)" :key="event.id" :set="club = findClubData(event.club)" class="d-flex list-group-item">
              <img v-if="club.logo!=null" class="thumbnail rounded float-start me-3 mt-1" :src="club.logo">
              <div v-else class="thumbnail-generic" :style="{ color: club.color_secondary, backgroundColor: club.color_primary }">
                <p class="thumbnail-generic-text">
                  {{ club.name.substring(0,1) }}
                </p> 
              </div>
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
          <h4 class="mb-3">Recent Activity</h4>
          <h6 v-if="userRecords.length==0" class='text-muted'>No recent activities found.</h6>
          <ul v-else class="list-group list-container">
            <li v-for="record in userRecords" :key="record.id" :set="club = findClubData(record.club)" class="d-flex list-group-item">

              <img v-if="club.logo!=null" class="thumbnail rounded float-start me-3 mt-1" :src="club.logo">
              <div v-else class="thumbnail-generic" :style="{ color: club.color_secondary, backgroundColor: club.color_primary }">
                <p class="thumbnail-generic-text">
                  {{ club.name.substring(0,1) }}
                </p>
              </div>
              <div>
                <p class="mb-0 text-dark" v-if="record.event!=null">Checked into <span class="fw-bold">{{ record.event.name }}</span></p>
                <p class="mb-0 fw-bold text-dark" v-else>Individual Task</p>
                <p class='text-muted sub-text'>
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" class="mb-1" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1h8zm-7.978-1A.261.261 0 0 1 7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002a.274.274 0 0 1-.014.002H7.022zM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM6.936 9.28a5.88 5.88 0 0 0-1.23-.247A7.35 7.35 0 0 0 5 9c-4 0-5 3-5 4 0 .667.333 1 1 1h4.216A2.238 2.238 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816zM4.92 10A5.493 5.493 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275zM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0zm3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>
                  </svg>
                  {{ club.name }}
                </p>
                <p class='text-muted sub-text'>
                  <svg width="14" height="14" class="mb-1" fill="currentColor"  viewBox="0 0 16 16">
                    <path d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5zm2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702c0 .7-.478 1.235-1.011 1.491A3.5 3.5 0 0 0 4.5 13v1h7v-1a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351v-.702c0-.7.478-1.235 1.011-1.491A3.5 3.5 0 0 0 11.5 3V2h-7z"/>
                  </svg>
                  {{ record.hours }} hours
                </p>
                <p class='text-muted sub-text'>
                  <svg width="14" height="14" class="mb-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.25,2.375c-4.212,0-7.625,3.413-7.625,7.625s3.413,7.625,7.625,7.625s7.625-3.413,7.625-7.625S14.462,2.375,10.25,2.375M10.651,16.811v-0.403c0-0.221-0.181-0.401-0.401-0.401s-0.401,0.181-0.401,0.401v0.403c-3.443-0.201-6.208-2.966-6.409-6.409h0.404c0.22,0,0.401-0.181,0.401-0.401S4.063,9.599,3.843,9.599H3.439C3.64,6.155,6.405,3.391,9.849,3.19v0.403c0,0.22,0.181,0.401,0.401,0.401s0.401-0.181,0.401-0.401V3.19c3.443,0.201,6.208,2.965,6.409,6.409h-0.404c-0.22,0-0.4,0.181-0.4,0.401s0.181,0.401,0.4,0.401h0.404C16.859,13.845,14.095,16.609,10.651,16.811 M12.662,12.412c-0.156,0.156-0.409,0.159-0.568,0l-2.127-2.129C9.986,10.302,9.849,10.192,9.849,10V5.184c0-0.221,0.181-0.401,0.401-0.401s0.401,0.181,0.401,0.401v4.651l2.011,2.008C12.818,12.001,12.818,12.256,12.662,12.412"></path>
                  </svg>
                  {{ record.checkInDate }}
                </p>
              </div>
            </li>
          </ul>
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
                <h4 class="m-0">Your Hours</h4>
              </div>
            </template>
            <template #empty>No clubs found.</template>
            <Column field="name" header="Club" :sortable="true">
            </Column>
            <Column header="Status">
                <template #body="{ data }">
                    <span v-if="data.isOfficer" :class="'badge bg-info'">
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
        <div class='border rounded bg-white text-center p-3'>
          <h4 class="py-2">Fact of the Day</h4>
          <h5 class="fw-light">{{fact}}</h5>
          <hr class="my-4 mx-5">
          <p class='text-muted'>source: {{source}}</p>
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
        records: [],
        hours: {}
      },
      upcomingEvents: [],
      fact:"",
      source:"",
      loading:false,
    };
  },
  computed: {
    userRecords: function () {
      return this.userData.records.slice(0,10).filter((obj) => {
        var found = false;
        for(var i = 0; i < this.userData.memberClubs.length; i++) {
            if (this.userData.memberClubs[i].id == obj.club) {
                found = true;
                break;
            }
        }
        return found;
      });
    },
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
        this.populateUpcomingEvents();
        console.log("DDDDDD");
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
    setFact(){
      let endpoint = "https://uselessfacts.jsph.pl/today.json?language=en"

      fetch(endpoint)
        .then(response => response.json())
        .then(data => {
          this.source = data.source;
          this.fact = data.text;
        });
    },
    findClubData(id){
      return this.userData.memberClubs.find(obj => {
          return obj.id === id
        })
    }
  },
  mounted() {
    this.getUserData();
    this.setFact();
  },
};
</script>

<style scoped>
.sub-text{
  font-size: 12px;
  margin-bottom: 0px;
}

.thumbnail{
  max-height:65px;
  max-width:65px;
  height:auto;
  width:auto;
}

.list-container{
  max-height: 300px;
  overflow-y: auto;
}

.thumbnail-generic{
  width: 20%;
  max-width: 50px;
  min-width: 30px;
  height: 0;
  padding-bottom: max(30px, min(50px, 20%));
  border: 1px solid black;
  border-radius: 10%;
  position: relative;
  margin-right: 18px;
}

.thumbnail-generic-text{
  transform: translate(-50%, -50%);
  position: absolute;
  top: 50%;
  left: 50%;
  font-size: 38px;
}
</style>