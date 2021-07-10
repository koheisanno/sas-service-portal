<template>
  <div class="container px-5 py-3">
    <div v-if="checkedin == null">
      <div v-if="loading" class="mt-2 d-flex justify-content-center">
        <div
          class="spinner-border text-secondary"
          style="width: 3rem; height: 3rem"
          role="status"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else class="row align-items-start">
        <div
          class="col-lg-6 offset-lg-3 col-md-8 offset-md-2 col-sm-10 offset-sm-1"
        >
          <div v-if="events.length > 0">
            <h3 class="text-dark mt-1 mb-3">Check-in to:</h3>
            <select v-model="selectedEvent" class="form-select mb-3">
              <option v-for="event in events" :key="event.id" :value="event.id">
                {{ event.name }}
              </option>
            </select>
            <button type="button" class="btn btn-primary" @click="checkin">
              Check-in
            </button>
          </div>
          <div v-else>
            <h3 class="text-dark text-center mt-2">No ongoing events found.</h3>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="checkedin == true">
      <h3 class="text-dark text-center mt-2">{{ success_message }}</h3>
    </div>
    <div v-else-if="checkedin == false">
      <h3 class="text-danger text-center mt-2">Check-in failed.</h3>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api_service";

export default {
  name: "Checkin",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      checkedin: null,
      name: null,
      events: [],
      selectedEvent: null,
      success_message: ""
    };
  },
  methods: {
    getClubData() {
      let endpoint = `/api/club/${this.id}/current-events/`;
      apiService(endpoint).then((data) => {
        this.name = data.name;
        this.events = data.events;
        if (this.events.length > 0) {
          this.selectedEvent = this.events[0].id;
        }
        this.loading = false;
      });
    },
    checkin() {
      let endpoint = `/api/event/${this.selectedEvent}/checkin/`;
      apiService(endpoint, "POST").then((data) => {
        if (data != false) {
          this.checkedin = true;
          this.success_message = data;
        } else {
          this.checkedin = false;
        }
      });
    },
  },
  created() {
    this.getClubData();
  },
};
</script>
