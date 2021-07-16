<template>
  <div>
    <h4 class="mb-3">
        Settings and Preferences
    </h4>
    <div class="accordion" id="accordionExample">
      <!--
      <div class="accordion-item">
        <h2 class="accordion-header" id="clubLogo">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseLogo"
            aria-expanded="true"
            aria-controls="collapseLogo"
          >
            Club Logo (OPTIONAL)
          </button>
        </h2>
        <div
          id="collapseLogo"
          class="accordion-collapse collapse"
          aria-labelledby="clubLogo"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            <img height="80" :src="currentClubData.logo">
            <div class='my-3'>
              <label for="logo" class="form-label">Upload a logo (max 1MB):</label>
              <input 
                    @change="uploadLogo"
                    class="form-control" type="file"
                    id="logo" name="logo"
                    accept="image/png, image/jpeg">
              <p v-show="imageError" class='text-danger'>The image size must be under 1MB.</p>
            </div>
            <button type="button" @click='submitLogo' class="btn btn-secondary" :disabled="imageError!=false">Upload</button>
          </div>
        </div>
      </div>
      -->
      <div class="accordion-item">
        <h2 class="accordion-header" id="clubInformation">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseOne"
            aria-expanded="true"
            aria-controls="collapseOne"
          >
            Club Information
          </button>
        </h2>
        <div
          id="collapseOne"
          class="accordion-collapse collapse"
          aria-labelledby="clubInformation"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
              <div class='mb-4'>
                  <label for="instagram">Instagram Handle</label>
                  <div class="form-text">
                      Optional. Please omit the @.
                  </div>
                  <input
                      type="text"
                      v-model="instagram"
                      class="form-control"
                      maxlength="150"
                      id="instagram"
                      placeholder="@"
                  >
              </div>
              <div class='mb-4'>
                  <label for="mission">Mission Statement</label>
                  <div class="form-text">
                      Brief mission statement. Max 200 characters.
                  </div>
                  <textarea
                      v-model="mission"
                      class="form-control"
                      maxlength="200"
                      id="mission"
                      placeholder="Mission Statement"
                      style="height: 80px"
                  ></textarea>
              </div>
            <div class="mb-4">
              <label for="description">Club Description</label>
              <div class="form-text">
                Description of your club's activities. Max 1200 characters.
              </div>
              <textarea
                v-model="description"
                class="form-control"
                maxlength="1200"
                placeholder="Club Description"
                id="description"
                style="height: 120px"
              ></textarea>
            </div>
            <div class="mb-4">
              <label for="involvement">How to Get Involved</label>
              <div class="form-text">
                What should members expect once they join the club? Put any
                sign-up or application forms here. Max 400 characters.
              </div> 
              <textarea
                v-model="involvement"
                class="form-control"
                maxlength="400"
                id="involvement"
                placeholder="How to Get Involved"
                style="height: 80px"
              ></textarea>
            </div>
            <div class="mb-4">
              <label for="meeting">Meeting Times and Locations</label>
              <div class="form-text">Max 200 characters.</div>
              <textarea
                v-model="meeting"
                class="form-control"
                maxlength="200"
                id="meeting"
                placeholder="Meeting Times and Locations"
                style="height: 80px"
              ></textarea>
            </div>
            <div class="mb-4">
              <label for="welcome">Welcome Message</label>
              <div class="form-text">
                This message will be sent to users via email upon joining. Max 800 characters.
              </div>
              <textarea
                v-model="welcome"
                class="form-control"
                maxlength="800"
                placeholder="Club Description"
                id="welcome"
                style="height: 120px"
              ></textarea>
            </div>
            <div class="d-grid gap-2 col-3 ms-auto">
              <button
                type="button"
                class="btn btn-primary"
                @click="saveSettingsInfo"
              >
                Update
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="officersSponsors">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseTwo"
            aria-expanded="false"
            aria-controls="collapseTwo"
          >
            Club Officers and Sponsors
          </button>
        </h2>
        <div
          id="collapseTwo"
          class="accordion-collapse collapse"
          aria-labelledby="officersSponsors"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            <div class="row">
              <div class="col-6 px-3">
                <h3>Officers</h3>
                <Table
                  :list="officers"
                  name="officers"
                  :club="currentClubData"
                  @removeOfficerSuccess="removeOfficerSuccess"
                  @addOfficerSuccess="addOfficerSuccess"
                />
              </div>
              <div class="col-6 px-3">
                <h3>Sponsors</h3>
                <Table
                  :list="sponsors"
                  name="sponsors"
                  :club="currentClubData"
                  @removeOfficerSuccess="removeOfficerSuccess"
                  @addOfficerSuccess="addOfficerSuccess"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="primaryContact">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapsePrimaryContact"
            aria-expanded="false"
            aria-controls="collapsePrimaryContact"
          >
            Primary Contact
          </button>
        </h2>
        <div
          id="collapsePrimaryContact"
          class="accordion-collapse collapse"
          aria-labelledby="primaryContact"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            <label class="form-label">Select your officer team's primary contact.</label>
            <div class="col-lg-5">
              <select class="form-select mb-2 mt-1" v-model="primary_contact">
                <option value=null>No 'Contact Us' option</option>
                <option v-for="officer in currentClubData.officers" :key="officer.id" :value="officer.id">
                  {{ officer.firstName + " " + officer.lastName }}
                </option>
              </select>
            </div>
            <div class="form-text mb-3">
              Users may send the primary contact an email through the "Contact Us" button on your club page.
            </div>
            <button type="button" @click='updatePrimaryContact' class="btn btn-secondary">Update</button>
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="clubColors">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseThree"
            aria-expanded="false"
            aria-controls="collapseThree"
          >
            Club Colors
          </button>
        </h2>
        <div
          id="collapseThree"
          class="accordion-collapse collapse"
          aria-labelledby="clubColors"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            <div class="d-flex justify-content-center mb-3">
              <input
                class="mx-2"
                type="color"
                id="primary"
                name="primary"
                v-model="color_primary"
              />
              <label for="primary">Primary</label>
              <input
                class="mx-2"
                type="color"
                id="secondary"
                name="secondary"
                v-model="color_secondary"
              />
              <label for="secondary">Secondary</label>
            </div>
            <div class="container-sm mb-3">
              <div class="row justify-content-md-center">
                <div class="col-lg-3 col-md-2 col-sm-1"></div>
                <div class="col-lg-6 col-md-8 col-sm-10">
                  <div
                    class="clubCard card text-center mx-auto"
                    :style="{
                      backgroundColor: color_primary,
                      color: color_secondary,
                    }"
                  >
                    <div class="card-body">
                      <h3 class="card-title">{{ currentClubData.name }}</h3>
                      <p class="card-text">{{ currentClubData.mission }}</p>
                    </div>
                    <div class="card-footer">
                      {{ currentClubData.umbrella }}
                    </div>
                  </div>
                </div>
                <div class="col-lg-3 col-md-2 col-sm-1"></div>
              </div>
            </div>
            <div class="d-grid gap-2 col-3 ms-auto">
              <button
                type="button"
                class="btn btn-primary"
                @click="saveSettingsColors"
              >
                Update
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script> 
import Table from "../components/Table";
//import { apiService, apiImageService } from "../common/api_service";
import { apiService } from "../common/api_service";

export default {
  name: "SettingsTab",
  components: {
    Table,
  },
  props: {
    currentClubData: {
      type: Object,
      default: function () {
        return {
          name: "",
          id: "",
          officers: [],
        };
      },
    },
  },
  data() {
    return {
      color_primary: null,
      color_secondary: null,
      sponsors: [],
      officers: [],
      mission: "",
      description: "",
      involvement: "",
      welcome: "",
      meeting: "",
      instagram: "",
      imageError: null,
      logo:null,
      primary_contact:null,
    };
  },
  methods: {
    saveSettingsInfo() {
      let endpoint = `/api/club/${this.currentClubData.id}/`;
      let body = {
        mission: this.mission,
        description: this.description,
        involvement: this.involvement,
        welcome: this.welcome,
        meeting: this.meeting,
        instagram: this.instagram,
      };
      apiService(endpoint, "PATCH", body).then((data) => {
        if (data != false) {
            this.$emit("success-officer", "Club settings updated.");
        }
      });
    },
    saveSettingsColors() {
      let endpoint = `/api/club/${this.currentClubData.id}/`;
      let body = {
        color_primary: this.color_primary,
        color_secondary: this.color_secondary,
      };
      apiService(endpoint, "PATCH", body).then((data) => {
        if (data != false) {
            this.$emit("success-officer", "Club settings updated.");
        }
      });
    },
    setSettingsFields() {
      this.mission = this.currentClubData.mission;
      this.description = this.currentClubData.description;
      this.meeting = this.currentClubData.meeting;
      this.involvement = this.currentClubData.involvement;
      this.welcome = this.currentClubData.welcome;
      this.instagram = this.currentClubData.instagram;

      this.color_primary = this.currentClubData.color_primary;
      this.color_secondary = this.currentClubData.color_secondary;

      this.primary_contact = this.currentClubData.primary_contact;

      this.sponsors = this.currentClubData.officers.filter((obj) => {
        return obj.status === "faculty";
      });

      this.officers = this.currentClubData.officers.filter((obj) => {
        return obj.status === "student";
      });
    },
    removeOfficerSuccess(){
        this.$emit("success-officer", "Officer removed successfully.");
    },
    addOfficerSuccess(){
        this.$emit("success-officer", "Officer added successfully.");
    },

    /*
    uploadLogo(event){
      if(event.target.files[0].size > 1048576){
        this.imageError = true;
      } else{
        this.logo = event.target.files[0];
        this.imageError = false;
      }
    },
    submitLogo(){
      let endpoint = `/api/club/${this.currentClubData.id}/logo/`;
      let formData = new FormData();
      formData.append('file', this.logo);

      apiImageService(endpoint, "PUT", formData).then((data) => {
        if (data != false) {
            this.$emit("success-officer", "Club logo updated.");
        }
      });
    },
    */
    updatePrimaryContact(){
      let endpoint = `/api/club/${this.currentClubData.id}/`;
      let body = {
        "primary_contact": this.primary_contact=="null" ? "" : this.primary_contact
      }
      console.log(body)
      apiService(endpoint, "PATCH", body).then((data) => {
        if (data != false) {
            this.$emit("success-officer", "Club settings updated.");
        }
      });
    }
  },
  watch: {
    currentClubData: function () {
      this.setSettingsFields();
    }
  },
};
</script>
