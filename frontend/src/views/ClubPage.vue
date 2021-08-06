<template>
  <div class="container p-5">
    <ConfirmDialogue ref="confirmDialogue"/>
    <div v-if="loading">
      <div class="d-flex justify-content-center" v-if="loading">
        <div
          class="spinner-border text-secondary mt-3"
          style="width: 5rem; height: 5rem"
          role="status"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
    <div v-else class="row">
      <div class="col-md-8">
        <div class="bg-white border py-3 px-4 mb-3 rounded">
          <div class="mb-3">
            <h1 class='mb-0'>
              {{ club.name }}
            </h1>
            <span
              v-for="tag in club.tags"
              :key="tag.id"
              class="badge bg-secondary mx-1"
              >{{ tag.name }}</span
            >
            <span
              class="badge rounded-pill bg-primary">
              {{ club.umbrella }}
            </span>
          </div>
        </div>
        <div class="bg-white border py-3 px-4 rounded">
          <h4>Mission</h4>
          <p style="white-space: pre-line">{{ club.mission }}</p>
          <div v-if="club.description">
            <h4>Description</h4>
            <p style="white-space: pre-line">{{ club.description }}</p>
          </div>
          <div v-if="club.involvement">
            <h4>How to Get Involved</h4>
            <p>{{ club.involvement }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="bg-white border py-3 px-4 mb-3 rounded">
          <div class="d-grid text-secondary mb-2" v-if="is_member">
            You are a member.
            <button @click="leaveClub" type="button" class="btn btn-danger">
              Leave
            </button>
          </div>
          <div class="d-grid text-secondary mb-2" v-else>
            You are not a member yet.
            <button @click="joinClub" type="button" class="btn btn-primary">
              Join
            </button>
          </div>
        </div>
        <div class="bg-white border py-3 px-4 mb-3 rounded">
          <h4>Meetings</h4>
          <p>{{ club.meeting }}</p>
        </div>
        <div v-if="primary_contact!=null" class="d-grid mb-3">
          <a :href="'mailto:' + primary_contact.email" class="btn btn-secondary" type="button">
            Contact Us
            <svg class="mb-1" width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.388,4.751H2.613c-0.213,0-0.389,0.175-0.389,0.389v9.72c0,0.216,0.175,0.389,0.389,0.389h14.775c0.214,0,0.389-0.173,0.389-0.389v-9.72C17.776,4.926,17.602,4.751,17.388,4.751 M16.448,5.53L10,11.984L3.552,5.53H16.448zM3.002,6.081l3.921,3.925l-3.921,3.925V6.081z M3.56,14.471l3.914-3.916l2.253,2.253c0.153,0.153,0.395,0.153,0.548,0l2.253-2.253l3.913,3.916H3.56z M16.999,13.931l-3.921-3.925l3.921-3.925V13.931z"></path>
            </svg>
          </a>
        </div>
        <div class="bg-white border py-3 px-4 mb-3 rounded">
          <h4>Officers and Sponsors</h4>
          <ul>
            <li v-for="officer in club.officers" :key="officer.id">
              {{
              officer.firstName + " " + officer.lastName
              }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { apiService } from "../common/api_service";
import ConfirmDialogue from "../components/ConfirmDialogue.vue"

export default {
  name: "ClubPage",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  components: {
    ConfirmDialogue,
  },
  data() {
    return {
      club: {},
      is_member: false,
      loading: false,
    };
  },
  methods: {
    getClubData() {
      this.loading = true;
      let endpoint = `/api/club/${this.id}/`;
      apiService(endpoint).then((data) => {
        if (data) {
          this.club = data;
          this.is_member = data.is_member;
        } else {
          this.club = null;
        }
        this.loading = false;
      });
    },
    toggleMembership() {
      this.is_member === false ? this.joinClub() : this.leaveClub();
    },
    joinClub() {
      let endpoint = `/api/club/${this.club.id}/membership/`;
      apiService(endpoint, "POST").then(()=>{
          this.is_member = true;
        });
    },
    async leaveClub() {
      const confirm = await this.$refs.confirmDialogue.show({
          title: "Leave Club",
          message: `Are you sure you want to leave ${this.club.name}?`,
          okButton: "Leave",
      });

      if(confirm){
        let endpoint = `/api/club/${this.club.id}/membership/`;
        apiService(endpoint, "DELETE").then(()=>{
          this.is_member = false;
        });
      }
    },
  },
  computed: {
    primary_contact: function () {
      return this.club.officers.filter((obj) => {
        return obj.id === this.club.primary_contact;
      })[0];
    },
  },
  created() {
    this.getClubData();
  },
};
</script>
