<template>
<div>
    <AttendeesModal @edited="this.$emit('success-events', 'Attendees edited successfully.');" ref="attendeesModal"></AttendeesModal>
    <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
    <CreateEventModal ref="createEventModal"></CreateEventModal>
    <EditEventModal ref="editEventModal"></EditEventModal>
    <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button
                class="nav-link active"
                id="upcoming-events-tab"
                data-bs-toggle="tab"
                data-bs-target="#upcoming-events"
                type="button"
                role="tab"
                aria-selected="true"
            >
                Upcoming Events
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button
                class="nav-link"
                id="past-events-tab"
                data-bs-toggle="tab"
                data-bs-target="#past-events"
                type="button"
                role="tab"
                aria-selected="false"
            >
                Past Events
            </button>
        </li>
    </ul>
    <div class="tab-content">
        <div
            class="tab-pane fade show active py-4 px-4"
            id="upcoming-events"
            role="tabpanel"
        >
            <div class="d-flex flex-row mb-3">
                <button
                    type="button"
                    class="btn btn-success me-2"
                    @click="createEvent"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="20"
                        viewBox="0 2 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    New
                </button>
                <button
                    type="button"
                    class="btn btn-danger"
                    v-bind:disabled="selectedUpcomingEvents.length == 0"
                    @click="deleteUpcomingEvents"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="20"
                        viewBox="0 2 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path
                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                        ></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                    Delete
                </button>
            </div>
            <div
                v-for="club in clubs"
                v-bind:key="club.id"
                :class="club.name"
                v-show="currentClub == club.id"
            >
                <DataTable
                    :value="club.upcomingEvents"
                    v-model:selection="selectedUpcomingEvents"
                    :rowHover="true"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :globalFilterFields="['name']"
                    responsiveLayout="scroll"
                    :paginator="true"
                    :rows="10"
                    currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
                >
                    <template #header>
                        <div class="d-flex align-items-center">
                            <h5 class="m-0">{{ club.name }} Events</h5>
                            <span class="ms-auto p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText
                                v-model="filters['global'].value"
                                placeholder="Search by name"
                            />
                            </span>
                        </div>
                    </template>
                    <template #empty> No events found. </template>
                    <Column
                        selectionMode="multiple"
                        headerStyle="width: 3rem"
                    ></Column>
                    <Column field="name" header="Name" :sortable="true">
                        <template #body="{ data }">
                            <span>{{ data.name }}</span>
                        </template>
                    </Column>
                    <Column
                        field="location"
                        header="Location"
                        :sortable="true"
                    ></Column>
                    <Column field="endTime" header="Date" :sortable="true">
                        <template #body="{ data }">
                            <span>{{ convertDate(data.endTime.split(" ")[0]) }}</span>
                        </template>
                    </Column>
                    <Column
                        field="startTime"
                        header="Start Time"
                        :sortable="true"
                    >
                        <template #body="{ data }">
                            <span>{{ data.startTime.split(" ")[1] }}</span>
                        </template>
                    </Column>
                    <Column
                        field="hours"
                        header="Hours"
                        :sortable="true"
                    ></Column>
                    <Column
                        headerStyle="width: 2.5rem; text-align: center"
                        bodyStyle="text-align: center; overflow: visible"
                    >
                        <template #body="{ data }">
                            <button class="btn btn-light border px-3" @click="editEvent(data.id)">
                                Edit
                            </button>
                        </template>
                    </Column>
                    <Column
                        headerStyle="width: 2.5rem; text-align: center"
                        bodyStyle="text-align: center; overflow: visible"
                    >
                        <template #body="{ data }">
                            <button class="btn btn-light border px-3" @click="editAttendees(data.id)">
                                Attendees
                            </button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
        <div
            class="tab-pane fade show py-4 px-4"
            id="past-events"
            role="tabpanel"
        >
            <div class="d-flex flex-row mb-3">
                <button
                    type="button"
                    class="btn btn-success me-2"
                    @click="createEvent"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="20"
                        viewBox="0 2 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    New
                </button>
                <button
                    type="button"
                    class="btn btn-danger"
                    v-bind:disabled="selectedPastEvents.length == 0"
                    @click="deletePastEvents"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="20"
                        viewBox="0 2 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path
                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                        ></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                    Delete
                </button>
            </div>
            <div
                v-for="club in clubs"
                v-bind:key="club.id"
                :class="club.name"
                v-show="currentClub == club.id"
            >
                <DataTable
                    :value="club.pastEvents"
                    v-model:selection="selectedPastEvents"
                    :rowHover="true"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :globalFilterFields="['name']"
                    responsiveLayout="scroll"
                    :paginator="true"
                    :rows="10"
                    currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
                >
                    <template #header>
                        <div class="d-flex align-items-center">
                            <h5 class="m-0">{{ club.name }} Events</h5>
                            <span class="ms-auto p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText
                                v-model="filters['global'].value"
                                placeholder="Search by name"
                            />
                            </span>
                        </div>
                    </template>
                    <template #empty> No events found. </template>
                    <Column
                        selectionMode="multiple"
                        headerStyle="width: 3rem"
                    ></Column>
                    <Column field="name" header="Name" :sortable="true">
                        <template #body="{ data }">
                            <span>{{ data.name }}</span>
                        </template>
                    </Column>
                    <Column
                        field="location"
                        header="Location"
                        :sortable="true"
                    ></Column>
                    <Column field="endTime" header="Date" :sortable="true">
                        <template #body="{ data }">
                            <span>{{ convertDate(data.endTime.split(" ")[0]) }}</span>
                        </template>
                    </Column>
                    <Column
                        field="startTime"
                        header="Start Time"
                        :sortable="true"
                    >
                        <template #body="{ data }">
                            <span>{{ data.startTime.split(" ")[1] }}</span>
                        </template>
                    </Column>
                    <Column
                        field="hours"
                        header="Hours"
                        :sortable="true"
                    ></Column>
                    <Column
                        headerStyle="width: 2.5rem; text-align: center"
                        bodyStyle="text-align: center; overflow: visible"
                    >
                        <template #body="{ data }">
                            <button class="btn btn-light border px-3" @click="editEvent(data.id)">
                                Edit
                            </button>
                        </template>
                    </Column>
                    <Column
                        headerStyle="width: 2.5rem; text-align: center"
                        bodyStyle="text-align: center; overflow: visible"
                    >
                        <template #body="{ data }">
                            <button class="btn btn-light border px-3" @click="editAttendees(data.id)">
                                Attendees
                            </button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import { FilterMatchMode } from "primevue/api";
import ConfirmDialogue from "../components/ConfirmDialogue";
import CreateEventModal from "../components/CreateEventModal";
import EditEventModal from "../components/EditEventModal";
import AttendeesModal from "../components/AttendeesModal"
import { apiService } from "../common/api_service";

export default {
    name: "EventsTab",
    components: {
        DataTable,
        Column,
        InputText,
        ConfirmDialogue,
        CreateEventModal,
        EditEventModal,
        AttendeesModal
    },
    props: {
        currentClubData: {
            type: Object,
            default: function () {
            return {};
            },
        },
        currentClub: {
            type: Number,
            default: null,
        },
        clubs: {
            type: Array,
            default: function () {
            return [];
            },
        },
    },
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      selectedUpcomingEvents: [],
      selectedPastEvents: []
    };
  },
  methods: {
    async deleteUpcomingEvents() {
        const confirm = await this.$refs.confirmDialogue.show({
            title: "Delete",
            message: `Are you sure you want to delete  ${this.selectedUpcomingEvents.length} event(s)? Hours associated with the event will be removed.`,
            okButton: "Delete Forever",
        });

        if (confirm) {
            let endpoint = "/api/event/delete/";
            let success = true;
            let ids = [];
            for (let m = 0; m < this.selectedUpcomingEvents.length; m++) {
                ids.push(this.selectedUpcomingEvents[m].id);
            }
            await apiService(endpoint, "POST", ids).then((data) => {
                if (data == false) {
                    success = false;
                }
            });
            this.selectedUpcomingEvents = [];
            if (success) {
                this.$emit("success-events", "Event(s) deleted successfully.");
            }
        }
    },
    async deletePastEvents() {
      const confirm = await this.$refs.confirmDialogue.show({
        title: "Delete",
        message: `Are you sure you want to delete  ${this.selectedPastEvents.length} event(s)? Hours associated with the event will be removed.`,
        okButton: "Delete Forever",
      });

      if (confirm) {
        let endpoint = "/api/event/delete/";
        let success = true;
        let ids = [];
        for (let m = 0; m < this.selectedPastEvents.length; m++) {
          ids.push(this.selectedPastEvents[m].id);
        }
        await apiService(endpoint, "POST", ids).then((data) => {
          if (data == false) {
            success = false;
          }
        });
        this.selectedPastEvents = [];
        if (success) {
            this.$emit("success-events", "Event(s) deleted successfully.");
        }
      }
    },
    async createEvent() {
        const response = await this.$refs.createEventModal.show(
            this.currentClubData
        );

        if (response) {
            this.$emit("success-events", "Event(s) created successfully.");
        }
    },
    async editEvent(id) {
        let eventToEdit = this.currentClubData.events.filter((obj) => {
            return obj.id === id;
        })[0];
        this.selectedEvents = [];

        const response = await this.$refs.editEventModal.show(eventToEdit);

        if (response) {
            this.$emit("success-events", "Event(s) edited successfully.");
        }
    },
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
    editAttendees(id){
        let eventToEdit = this.currentClubData.events.filter((obj) => {
            return obj.id === id;
        })[0];

        console.log(eventToEdit)

        this.$refs.attendeesModal.show(
            this.currentClubData, eventToEdit
        );
    },
  },
  watch: {
    currentClub: function () {
        this.selectedUpcomingEvents = [],
        this.selectedPastEvents = []
    }
  },
};
</script>
