<template>
<div>
    <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
    <CreateRecordModal ref="createRecordModal"></CreateRecordModal>
    <EditRecordModal ref="editRecordModal"></EditRecordModal>
    <div class="d-flex flex-row mb-3">
        <button
            type="button"
            class="btn btn-success me-2"
            @click="createRecord"
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
            v-bind:disabled="selectedRecords.length == 0"
            @click="deleteRecords"
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
    <div class="d-flex align-items-center bg-white p-3 border-bottom">
        <h5 class="m-0">Individual Tasks
            <span ref="tooltipInfoRecords"
                    data-bs-toggle="tooltip" data-bs-placement="bottom" title="Use 'individual tasks' to give hours to specific members for individual tasks.">
                <svg xmlns="http://www.w3.org/2000/svg"
                    width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                </svg>
            </span>
        </h5>
        <span class="ms-auto p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
                v-model="filters['global'].value"
                placeholder="Search by name"
            />
        </span>
    </div>
    <div
        v-for="club in clubs"
        v-bind:key="club.id"
        :class="club.name"
        v-show="currentClub == club.id"
    >
        <DataTable
            :value="filteredRecords[club.id]"
            v-model:selection="selectedRecords"
            :rowHover="true"
            v-model:filters="filters"
            filterDisplay="menu"
            :globalFilterFields="['user']"
            responsiveLayout="scroll"
            :paginator="true"
            :rows="10"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
        >
            <template #empty> No individual tasks found. </template>
            <Column
                selectionMode="multiple"
                headerStyle="width: 3rem"
            ></Column>
            <Column field="user" header="Member" :sortable="true"> </Column>
            <Column
                field="name"
                header="Description"
                :sortable="true"
            ></Column>
            <Column field="checkInDate" header="Date" :sortable="true"></Column>
            <Column field="hours" header="Hours" :sortable="true"></Column>
            <Column
                headerStyle="width: 2.5rem; text-align: center"
                bodyStyle="text-align: center; overflow: visible"
            >
                <template #body="{ data }">
                    <button class="btn btn-light border px-3" @click="editRecord(data.id)">
                        Edit
                    </button>
                </template>
            </Column>
        </DataTable>
    </div>
</div>
</template>

<script>
import { apiService } from "../common/api_service";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import { FilterMatchMode } from "primevue/api";
import ConfirmDialogue from "../components/ConfirmDialogue";
import CreateRecordModal from "../components/CreateRecordModal";
import EditRecordModal from "../components/EditRecordModal";
import { Tooltip } from "bootstrap";

export default {
    name: "RecordsTab",
    components: {
        DataTable,
        Column,
        InputText,
        ConfirmDialogue,
        CreateRecordModal,
        EditRecordModal
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
    computed: {
        filteredRecords: function () {
            var filtered={}
            for(var i=0; i<this.clubs.length; i++){
                var list = this.clubs[i].records.filter((obj) => {
                    return obj.event === null;
                });
                filtered[this.clubs[i].id] = list;
            }
            return filtered;
        }
    },
    data() {
        return {
            filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            },
            selectedRecords: [],
        };
    },
    methods: {
        async deleteRecords() {
            const confirm = await this.$refs.confirmDialogue.show({
                title: "Delete",
                message:
                    "Are you sure you want to delete " +
                    this.selectedRecords.length +
                    " record(s)?",
                okButton: "Delete Forever",
            });

            if (confirm) {
                let endpoint = "/api/record/delete/";
                let ids = [];
                for (let m = 0; m < this.selectedRecords.length; m++) {
                    ids.push(this.selectedRecords[m].id);
                }
                apiService(endpoint, "POST", ids).then(() => {
                    this.selectedRecords = [];
                    this.$emit("success-records", "Record(s) deleted successfully.");
                });
            }
        },
        async createRecord() {
            const response = await this.$refs.createRecordModal.show(
                this.currentClubData
            );

            if (response) {
                this.$emit("success-records", "Record(s) created successfully.");
            }
        },
        async editRecord(id) {
            let recordToEdit = this.currentClubData.records.filter((obj) => {
                return obj.id === id;
            })[0];

            this.selectedRecords = [];

            const response = await this.$refs.editRecordModal.show(recordToEdit);

            if (response) {
                this.$emit("success-records", "Record(s) edited successfully.");
            }
        },
        setTooltips() {
            let options = {
                trigger: "hover",
            };
            for (var ref in this.$refs) {
                if (ref.indexOf("tooltip") > -1) {
                    return new Tooltip(this.$refs[ref], options);
                }
            }
        },
    },
    watch: {
        currentClub: function () {
            this.selectedRecords = [];
            this.filters['global'].value = ""
        }
    },
    mounted(){
        this.setTooltips();
    }
};
</script>
