<template>
  <div v-if="is_auth == false">
    <h3 class="text-secondary text-center mt-5 mb-2">
      Oops...
    </h3>
    <h5 class="text-secondary text-center mb-5">
      Please login to access the officer dashboard.
    </h5>
  </div>
  <div v-else-if="clubs == null">
    <h3 class="text-secondary text-center mt-5 mb-2">
      Oops...
    </h3>
    <h5 class="text-secondary text-center mb-5">
      The officer dashboard is unavailable. Please make sure that you're registered as an officer for at least one club!
    </h5>
  </div>
  <div v-else-if="loading" class="d-flex justify-content-center">
    <div
      class="spinner-border mt-5 text-secondary"
      style="width: 5rem; height: 5rem"
      role="status"
    >
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div v-else class="container-xl pt-4">
    <Toast position="bottom-left" />
    <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
    <div class="row">
      <div class="col-2">
        <div
          class="nav flex-column nav-pills"
          id="v-pills-tab"
          role="tablist"
          aria-orientation="vertical"
          style="position: sticky; top: 90px"
        >
          <select
            class="form-select"
            v-model="currentClub"
          >
            <option v-for="club in clubs" v-bind:key="club.id" :value="club.id">
              {{ club.name }}
            </option>
          </select>
          <hr />
          <button
            class="nav-link active text-start"
            id="v-pills-members-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-members"
            type="button"
            role="tab"
            aria-controls="v-pills-members"
            aria-selected="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              class="mb-1"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"
              />
            </svg>
            Members
          </button>
          <button
            class="nav-link text-start"
            id="v-pills-events-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-events"
            type="button"
            role="tab"
            aria-controls="v-pills-events"
            aria-selected="false"
          >
            <svg class="mb-1" xmlns="http://www.w3.org/2000/svg" height="18" width="18" fill="currentColor" viewBox="0 0 20 20">
							<path d="M16.254,3.399h-0.695V3.052c0-0.576-0.467-1.042-1.041-1.042c-0.576,0-1.043,0.467-1.043,1.042v0.347H6.526V3.052c0-0.576-0.467-1.042-1.042-1.042S4.441,2.476,4.441,3.052v0.347H3.747c-0.768,0-1.39,0.622-1.39,1.39v11.813c0,0.768,0.622,1.39,1.39,1.39h12.507c0.768,0,1.391-0.622,1.391-1.39V4.789C17.645,4.021,17.021,3.399,16.254,3.399z M14.17,3.052c0-0.192,0.154-0.348,0.348-0.348c0.191,0,0.348,0.156,0.348,0.348v0.347H14.17V3.052z M5.136,3.052c0-0.192,0.156-0.348,0.348-0.348S5.831,2.86,5.831,3.052v0.347H5.136V3.052z M16.949,16.602c0,0.384-0.311,0.694-0.695,0.694H3.747c-0.384,0-0.695-0.311-0.695-0.694V7.568h13.897V16.602z M16.949,6.874H3.052V4.789c0-0.383,0.311-0.695,0.695-0.695h12.507c0.385,0,0.695,0.312,0.695,0.695V6.874z M5.484,11.737c0.576,0,1.042-0.467,1.042-1.042c0-0.576-0.467-1.043-1.042-1.043s-1.042,0.467-1.042,1.043C4.441,11.271,4.908,11.737,5.484,11.737z M5.484,10.348c0.192,0,0.347,0.155,0.347,0.348c0,0.191-0.155,0.348-0.347,0.348s-0.348-0.156-0.348-0.348C5.136,10.503,5.292,10.348,5.484,10.348z M14.518,11.737c0.574,0,1.041-0.467,1.041-1.042c0-0.576-0.467-1.043-1.041-1.043c-0.576,0-1.043,0.467-1.043,1.043C13.475,11.271,13.941,11.737,14.518,11.737z M14.518,10.348c0.191,0,0.348,0.155,0.348,0.348c0,0.191-0.156,0.348-0.348,0.348c-0.193,0-0.348-0.156-0.348-0.348C14.17,10.503,14.324,10.348,14.518,10.348z M14.518,15.212c0.574,0,1.041-0.467,1.041-1.043c0-0.575-0.467-1.042-1.041-1.042c-0.576,0-1.043,0.467-1.043,1.042C13.475,14.745,13.941,15.212,14.518,15.212z M14.518,13.822c0.191,0,0.348,0.155,0.348,0.347c0,0.192-0.156,0.348-0.348,0.348c-0.193,0-0.348-0.155-0.348-0.348C14.17,13.978,14.324,13.822,14.518,13.822z M10,15.212c0.575,0,1.042-0.467,1.042-1.043c0-0.575-0.467-1.042-1.042-1.042c-0.576,0-1.042,0.467-1.042,1.042C8.958,14.745,9.425,15.212,10,15.212z M10,13.822c0.192,0,0.348,0.155,0.348,0.347c0,0.192-0.156,0.348-0.348,0.348s-0.348-0.155-0.348-0.348C9.653,13.978,9.809,13.822,10,13.822z M5.484,15.212c0.576,0,1.042-0.467,1.042-1.043c0-0.575-0.467-1.042-1.042-1.042s-1.042,0.467-1.042,1.042C4.441,14.745,4.908,15.212,5.484,15.212z M5.484,13.822c0.192,0,0.347,0.155,0.347,0.347c0,0.192-0.155,0.348-0.347,0.348s-0.348-0.155-0.348-0.348C5.136,13.978,5.292,13.822,5.484,13.822z M10,11.737c0.575,0,1.042-0.467,1.042-1.042c0-0.576-0.467-1.043-1.042-1.043c-0.576,0-1.042,0.467-1.042,1.043C8.958,11.271,9.425,11.737,10,11.737z M10,10.348c0.192,0,0.348,0.155,0.348,0.348c0,0.191-0.156,0.348-0.348,0.348s-0.348-0.156-0.348-0.348C9.653,10.503,9.809,10.348,10,10.348z"></path>
						</svg>
            Events
          </button>
          <button
            class="nav-link text-start"
            id="v-pills-misc-hours-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-misc-hours"
            type="button"
            role="tab"
            aria-controls="v-pills-misc-hours"
            aria-selected="false"
          >
            <svg width="18" height="18" class="mb-1" fill="currentColor" viewBox="2 0 20 20">
              <path
                d="M15.396,2.292H4.604c-0.212,0-0.385,0.174-0.385,0.386v14.646c0,0.212,0.173,0.385,0.385,0.385h10.792c0.211,0,0.385-0.173,0.385-0.385V2.677C15.781,2.465,15.607,2.292,15.396,2.292 M15.01,16.938H4.99v-2.698h1.609c0.156,0.449,0.586,0.771,1.089,0.771c0.638,0,1.156-0.519,1.156-1.156s-0.519-1.156-1.156-1.156c-0.503,0-0.933,0.321-1.089,0.771H4.99v-3.083h1.609c0.156,0.449,0.586,0.771,1.089,0.771c0.638,0,1.156-0.518,1.156-1.156c0-0.638-0.519-1.156-1.156-1.156c-0.503,0-0.933,0.322-1.089,0.771H4.99V6.531h1.609C6.755,6.98,7.185,7.302,7.688,7.302c0.638,0,1.156-0.519,1.156-1.156c0-0.638-0.519-1.156-1.156-1.156c-0.503,0-0.933,0.322-1.089,0.771H4.99V3.062h10.02V16.938z M7.302,13.854c0-0.212,0.173-0.386,0.385-0.386s0.385,0.174,0.385,0.386s-0.173,0.385-0.385,0.385S7.302,14.066,7.302,13.854 M7.302,10c0-0.212,0.173-0.385,0.385-0.385S8.073,9.788,8.073,10s-0.173,0.385-0.385,0.385S7.302,10.212,7.302,10 M7.302,6.146c0-0.212,0.173-0.386,0.385-0.386s0.385,0.174,0.385,0.386S7.899,6.531,7.688,6.531S7.302,6.358,7.302,6.146"
              ></path>
            </svg>
            Individual Tasks
          </button>
          <button
            class="nav-link text-start"
            id="v-pills-qr-codes-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-qr-codes"
            type="button"
            role="tab"
            aria-controls="v-pills-qr-codes"
            aria-selected="false"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path
                d="M1.5 1a.5.5 0 0 0-.5.5v3a.5.5 0 0 1-1 0v-3A1.5 1.5 0 0 1 1.5 0h3a.5.5 0 0 1 0 1h-3zM11 .5a.5.5 0 0 1 .5-.5h3A1.5 1.5 0 0 1 16 1.5v3a.5.5 0 0 1-1 0v-3a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 1-.5-.5zM.5 11a.5.5 0 0 1 .5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 1 0 1h-3A1.5 1.5 0 0 1 0 14.5v-3a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v3a1.5 1.5 0 0 1-1.5 1.5h-3a.5.5 0 0 1 0-1h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 1 .5-.5zM3 4.5a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-7zm3 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7z"
              />
            </svg>
            QR Codes
          </button>
          <button
            class="nav-link text-start"
            id="v-pills-settings-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-settings"
            type="button"
            role="tab"
            aria-controls="v-pills-settings"
            aria-selected="false"
            @click="setSettingsFields"
          >
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
							<path d="M17.498,11.697c-0.453-0.453-0.704-1.055-0.704-1.697c0-0.642,0.251-1.244,0.704-1.697c0.069-0.071,0.15-0.141,0.257-0.22c0.127-0.097,0.181-0.262,0.137-0.417c-0.164-0.558-0.388-1.093-0.662-1.597c-0.075-0.141-0.231-0.22-0.391-0.199c-0.13,0.02-0.238,0.027-0.336,0.027c-1.325,0-2.401-1.076-2.401-2.4c0-0.099,0.008-0.207,0.027-0.336c0.021-0.158-0.059-0.316-0.199-0.391c-0.503-0.274-1.039-0.498-1.597-0.662c-0.154-0.044-0.32,0.01-0.416,0.137c-0.079,0.106-0.148,0.188-0.22,0.257C11.244,2.956,10.643,3.207,10,3.207c-0.642,0-1.244-0.25-1.697-0.704c-0.071-0.069-0.141-0.15-0.22-0.257C7.987,2.119,7.821,2.065,7.667,2.109C7.109,2.275,6.571,2.497,6.07,2.771C5.929,2.846,5.85,3.004,5.871,3.162c0.02,0.129,0.027,0.237,0.027,0.336c0,1.325-1.076,2.4-2.401,2.4c-0.098,0-0.206-0.007-0.335-0.027C3.001,5.851,2.845,5.929,2.77,6.07C2.496,6.572,2.274,7.109,2.108,7.667c-0.044,0.154,0.01,0.32,0.137,0.417c0.106,0.079,0.187,0.148,0.256,0.22c0.938,0.936,0.938,2.458,0,3.394c-0.069,0.072-0.15,0.141-0.256,0.221c-0.127,0.096-0.181,0.262-0.137,0.416c0.166,0.557,0.388,1.096,0.662,1.596c0.075,0.143,0.231,0.221,0.392,0.199c0.129-0.02,0.237-0.027,0.335-0.027c1.325,0,2.401,1.076,2.401,2.402c0,0.098-0.007,0.205-0.027,0.334C5.85,16.996,5.929,17.154,6.07,17.23c0.501,0.273,1.04,0.496,1.597,0.66c0.154,0.047,0.32-0.008,0.417-0.137c0.079-0.105,0.148-0.186,0.22-0.256c0.454-0.453,1.055-0.703,1.697-0.703c0.643,0,1.244,0.25,1.697,0.703c0.071,0.07,0.141,0.15,0.22,0.256c0.073,0.098,0.188,0.152,0.307,0.152c0.036,0,0.073-0.004,0.109-0.016c0.558-0.164,1.096-0.387,1.597-0.66c0.141-0.076,0.22-0.234,0.199-0.393c-0.02-0.129-0.027-0.236-0.027-0.334c0-1.326,1.076-2.402,2.401-2.402c0.098,0,0.206,0.008,0.336,0.027c0.159,0.021,0.315-0.057,0.391-0.199c0.274-0.5,0.496-1.039,0.662-1.596c0.044-0.154-0.01-0.32-0.137-0.416C17.648,11.838,17.567,11.77,17.498,11.697 M16.671,13.334c-0.059-0.002-0.114-0.002-0.168-0.002c-1.749,0-3.173,1.422-3.173,3.172c0,0.053,0.002,0.109,0.004,0.166c-0.312,0.158-0.64,0.295-0.976,0.406c-0.039-0.045-0.077-0.086-0.115-0.123c-0.601-0.6-1.396-0.93-2.243-0.93s-1.643,0.33-2.243,0.93c-0.039,0.037-0.077,0.078-0.116,0.123c-0.336-0.111-0.664-0.248-0.976-0.406c0.002-0.057,0.004-0.113,0.004-0.166c0-1.75-1.423-3.172-3.172-3.172c-0.054,0-0.11,0-0.168,0.002c-0.158-0.312-0.293-0.639-0.405-0.975c0.044-0.039,0.085-0.078,0.124-0.115c1.236-1.236,1.236-3.25,0-4.486C3.009,7.719,2.969,7.68,2.924,7.642c0.112-0.336,0.247-0.664,0.405-0.976C3.387,6.668,3.443,6.67,3.497,6.67c1.75,0,3.172-1.423,3.172-3.172c0-0.054-0.002-0.11-0.004-0.168c0.312-0.158,0.64-0.293,0.976-0.405C7.68,2.969,7.719,3.01,7.757,3.048c0.6,0.6,1.396,0.93,2.243,0.93s1.643-0.33,2.243-0.93c0.038-0.039,0.076-0.079,0.115-0.123c0.336,0.112,0.663,0.247,0.976,0.405c-0.002,0.058-0.004,0.114-0.004,0.168c0,1.749,1.424,3.172,3.173,3.172c0.054,0,0.109-0.002,0.168-0.004c0.158,0.312,0.293,0.64,0.405,0.976c-0.045,0.038-0.086,0.077-0.124,0.116c-0.6,0.6-0.93,1.396-0.93,2.242c0,0.847,0.33,1.645,0.93,2.244c0.038,0.037,0.079,0.076,0.124,0.115C16.964,12.695,16.829,13.021,16.671,13.334 M10,5.417c-2.528,0-4.584,2.056-4.584,4.583c0,2.529,2.056,4.584,4.584,4.584s4.584-2.055,4.584-4.584C14.584,7.472,12.528,5.417,10,5.417 M10,13.812c-2.102,0-3.812-1.709-3.812-3.812c0-2.102,1.71-3.812,3.812-3.812c2.102,0,3.812,1.71,3.812,3.812C13.812,12.104,12.102,13.812,10,13.812"></path>
						</svg>
            Settings
          </button>
          <button
            class="nav-link text-start"
            id="v-pills-links-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-links"
            type="button"
            role="tab"
            aria-controls="v-pills-links"
            aria-selected="false"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              fill="currentColor"
              class="mb-1"
              viewBox="0 0 16 16"
            >
              <path
                d="M13 2.5a1.5 1.5 0 0 1 3 0v11a1.5 1.5 0 0 1-3 0v-.214c-2.162-1.241-4.49-1.843-6.912-2.083l.405 2.712A1 1 0 0 1 5.51 15.1h-.548a1 1 0 0 1-.916-.599l-1.85-3.49a68.14 68.14 0 0 0-.202-.003A2.014 2.014 0 0 1 0 9V7a2.02 2.02 0 0 1 1.992-2.013 74.663 74.663 0 0 0 2.483-.075c3.043-.154 6.148-.849 8.525-2.199V2.5zm1 0v11a.5.5 0 0 0 1 0v-11a.5.5 0 0 0-1 0zm-1 1.35c-2.344 1.205-5.209 1.842-8 2.033v4.233c.18.01.359.022.537.036 2.568.189 5.093.744 7.463 1.993V3.85zm-9 6.215v-4.13a95.09 95.09 0 0 1-1.992.052A1.02 1.02 0 0 0 1 7v2c0 .55.448 1.002 1.006 1.009A60.49 60.49 0 0 1 4 10.065zm-.657.975 1.609 3.037.01.024h.548l-.002-.014-.443-2.966a68.019 68.019 0 0 0-1.722-.082z"
              />
            </svg>
            Advertising + Links
          </button>
        </div>
      </div>
      <div class="col-10 tab-content px-4" id="v-pills-tabContent">
        <div
          class="tab-pane fade show active"
          id="v-pills-members"
          role="tabpanel"
          aria-labelledby="v-pills-members-tab"
        >
          <MembersTab :clubs="clubs" :currentClub="currentClub" @success-members="success" />
        </div>
        <div
          class="tab-pane fade"
          id="v-pills-events"
          role="tabpanel"
          aria-labelledby="v-pills-events-tab"
        >
          <EventsTab :clubs="clubs" :currentClub="currentClub" :currentClubData="currentClubData"  @success-events="successEvents"/>
        </div>
        <div
          class="tab-pane fade px-5"
          id="v-pills-misc-hours"
          role="tabpanel"
          aria-labelledby="v-pills-misc-hours-tab"
        >
          <RecordsTab :clubs="clubs" :currentClub="currentClub" :currentClubData="currentClubData"  @success-records="success"/>
        </div>
        <div
          class="tab-pane fade px-5"
          id="v-pills-qr-codes"
          role="tabpanel"
          aria-labelledby="v-pills-qr-codes-tab"
        >
          <QRCodeTab :clubs="clubs" :currentClub="currentClub" />
        </div>
        <div
          class="tab-pane fade"
          id="v-pills-settings"
          role="tabpanel"
          aria-labelledby="v-pills-settings-tab"
        >
          <SettingsTab :currentClubData="currentClubData" ref="settingsTab" @success-officer="success"/>
        </div>
        <div
          class="tab-pane fade"
          id="v-pills-links"
          role="tabpanel"
          aria-labelledby="v-pills-links-tab"
        >
          <LinksTab />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { apiService } from "../common/api_service";
import { FilterMatchMode } from "primevue/api";
import Toast from "primevue/toast";
import ConfirmDialogue from "../components/ConfirmDialogue";
import MembersTab from "../components/MembersTab";
import SettingsTab from "../components/SettingsTab";
import QRCodeTab from "../components/QRCodeTab"
import EventsTab from "../components/EventsTab"
import RecordsTab from "../components/RecordsTab"
import LinksTab from "../components/LinksTab"

export default {
  name: "Dashboard",
  components: {
    Toast,
    ConfirmDialogue,
    MembersTab,
    SettingsTab,
    QRCodeTab,
    EventsTab,
    RecordsTab,
    LinksTab
  },
  props: {
    is_auth: {
        type: Boolean,
        default: false,
    },
  },
  data() {
    return {
      modal: null,
      clubs: [],
      currentClub: null,
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      loading: false,
    };
  },
  computed: {
    currentClubData: function () {
      if (this.clubs.length == 0) {
        return {
          name: "",
          id: "",
          officers: [],
        };
      } else {
        return this.clubs.find((obj) => {
          return obj.id === this.currentClub;
        });
      }
    },
  },
  methods: {
    successEvents(msg) {
      this.getClubsData(false, true);
      this.$toast.add({
        severity: "success",
        summary: "Success",
        detail: msg,
        life: 3000,
      });
    },
    success(msg) {
      this.getClubsData();
      this.$toast.add({
        severity: "success",
        summary: "Success",
        detail: msg,
        life: 3000,
      });
    },
    sortEvents() {
      let today = new Date();
      today.setMinutes(today.getMinutes()-10);
      let upcomingEvents = [];
      let pastEvents = [];
      for (var clubIndex in this.clubs) {
        upcomingEvents = [];
        pastEvents = [];
        for (var eventIndex in this.clubs[clubIndex].events) {
          if (
            new Date(this.clubs[clubIndex].events[eventIndex].startTime) >=
            today
          ) {
            upcomingEvents.push(this.clubs[clubIndex].events[eventIndex]);
          } else {
            pastEvents.push(this.clubs[clubIndex].events[eventIndex]);
          }
        }
        this.clubs[clubIndex].upcomingEvents = upcomingEvents;
        this.clubs[clubIndex].pastEvents = pastEvents;
      }
    },
    getClubsData(spinner = false, events = false) {
      if (spinner) this.loading = true;
      let endpoint = "/api/officerships/";
      apiService(endpoint).then((data) => {
        if (data.officerClubs.length > 0) {
          this.clubs = data.officerClubs;
          if(events){
            this.sortEvents();
          }
          if (this.currentClub == null) {
            this.currentClub = data.officerClubs[0].id;
          }
        } else {
          this.clubs = null;
        }
        this.loading = false;
      });
    },
    setSettingsFields() {
      this.$refs.settingsTab.setSettingsFields();
    }
  },
  created() {
    if(this.is_auth) this.getClubsData(true, true);
  }
};
</script>

<style scoped>
tr:hover .button {
  display: inline-block;
}
tr .button {
  display: none;
}
</style>
