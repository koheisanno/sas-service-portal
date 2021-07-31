<template>
<div>
    <div class="d-flex flex-row mb-3">
        <button type="button" class="btn btn-secondary me-2" @click="copyMembers" v-bind:disabled="selectedMembers.length == 0">
            <span>
                <svg v-if="copied" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="mb-1" viewBox="0 0 16 16">
                    <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
                </svg>
                <svg v-else
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    class="mb-1"
                    fill="currentColor"
                    viewBox="0 0 16 16"
                >
                    <path
                        d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"
                    />
                    <path
                        d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"
                    />
                </svg>
                Copy Selected Emails
            </span>
        </button>
    </div>
    <input ref="memberEmails" hidden />
    <div
        v-for="club in clubs"
        v-bind:key="club.id"
        :class="club.name"
        v-show="currentClub == club.id"
    >
        <DataTable
            :value="club.members"
            :rowHover="true"
            v-model:filters="filters"
            v-model:selection="selectedMembers"
            filterDisplay="menu"
            :globalFilterFields="['fullName']"
            responsiveLayout="scroll"
            :paginator="true"
            :rows="10"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
        >
            <template #header>
                <div class="d-flex align-items-center">
                    <h5 class="m-0">{{ club.name }} Members</h5>
                    <span class="ms-auto p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText
                            v-model="filters['global'].value"
                            placeholder="Search by name"
                        />
                    </span>
                </div>
            </template>
            <template #empty> No members found. </template>
            <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
            <Column field="fullName" header="Full Name" :sortable="true"></Column>
            <Column header="Status">
                <template #body="{ data }">
                    <span v-if="checkIfOfficer(club.officers, data.id)" :class="'badge bg-primary'">
                        Officer
                    </span>
                    <span v-else :class="'badge bg-secondary'"> Member </span>
                </template>
            </Column>
            <Column header="Hours">
                <template #body="{ data }">
                    <span v-if="club.name in data.hours">
                        {{ data.hours[club.name] }}
                    </span>
                    <span v-else>0</span>
                </template>
            </Column>
        </DataTable>
    </div>
</div>
</template>

<script>
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import { FilterMatchMode } from "primevue/api";

export default {
    name: "MembersTab",
    components: {
        DataTable,
        Column,
        InputText,
    },
    props: {
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
            selectedMembers: [],
            copied: false
        };
    },
    methods: {
        copyMembers() {
            var text = this.$refs.memberEmails;
            text.value = this.selectedMembers.map((a) => a.email);
            text.removeAttribute("hidden");
            text.select();
            document.execCommand("copy");
            text.setAttribute("hidden", "true");
            this.copied=true;
            setTimeout(() => { this.copied=false; }, 2000);
        },
        checkIfOfficer(officers, id){
            return officers.some(e => e.id === id);
        }
    },
    watch: {
        currentClub: function () {
            this.selectedMembers = []
        }
    },
};
</script>
