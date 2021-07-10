<template>
<div class="container-fluid">
    <div class="row">
        <div class="d-none d-md-block col-2 ps-3 pt-4">
            <div style="position: sticky; top: 94px">
                <input
                    @keyup="getClubs(false)"
                    v-model="nameInput"
                    type="text"
                    class="form-control"
                    placeholder="Search"
                />
                <hr />
                <label class="form-label text-secondary">
                    Tags
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M17.35,2.219h-5.934c-0.115,0-0.225,0.045-0.307,0.128l-8.762,8.762c-0.171,0.168-0.171,0.443,0,0.611l5.933,5.934c0.167,0.171,0.443,0.169,0.612,0l8.762-8.763c0.083-0.083,0.128-0.192,0.128-0.307V2.651C17.781,2.414,17.587,2.219,17.35,2.219M16.916,8.405l-8.332,8.332l-5.321-5.321l8.333-8.332h5.32V8.405z M13.891,4.367c-0.957,0-1.729,0.772-1.729,1.729c0,0.957,0.771,1.729,1.729,1.729s1.729-0.772,1.729-1.729C15.619,5.14,14.848,4.367,13.891,4.367 M14.502,6.708c-0.326,0.326-0.896,0.326-1.223,0c-0.338-0.342-0.338-0.882,0-1.224c0.342-0.337,0.881-0.337,1.223,0C14.84,5.826,14.84,6.366,14.502,6.708"></path>
                    </svg>
                </label>
                <input
                    type="text"
                    class="form-control select-form"
                    :placeholder="placeholder"
                    @focus="focused"
                    v-model="taginput"
                />
                <div v-show="isFocused" class="list-group select-form" style="max-height: 200px; overflow:scroll">
                <button
                    type="button"
                    class="list-group-item list-group-item-action select-form"
                    v-for="tag in filteredtags"
                    :value="tag.id"
                    :key="tag.id"
                    @click="toggleTag(tag.id)"
                >
                    <input
                        class="form-check-input me-2 select-form"
                        type="checkbox"
                        :value="tag.id"
                        v-model="selectedTags"
                        disabled
                    />
                    {{ tag.name }}
                </button>
                </div>
                <hr />
                <label class="form-label text-secondary">
                    Umbrella
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="mb-1 bi bi-umbrella" viewBox="0 0 16 16">
                        <path d="M8 0a.5.5 0 0 1 .5.5v.514C12.625 1.238 16 4.22 16 8c0 0 0 .5-.5.5-.149 0-.352-.145-.352-.145l-.004-.004-.025-.023a3.484 3.484 0 0 0-.555-.394A3.166 3.166 0 0 0 13 7.5c-.638 0-1.178.213-1.564.434a3.484 3.484 0 0 0-.555.394l-.025.023-.003.003s-.204.146-.353.146-.352-.145-.352-.145l-.004-.004-.025-.023a3.484 3.484 0 0 0-.555-.394 3.3 3.3 0 0 0-1.064-.39V13.5H8h.5v.039l-.005.083a2.958 2.958 0 0 1-.298 1.102 2.257 2.257 0 0 1-.763.88C7.06 15.851 6.587 16 6 16s-1.061-.148-1.434-.396a2.255 2.255 0 0 1-.763-.88 2.958 2.958 0 0 1-.302-1.185v-.025l-.001-.009v-.003s0-.002.5-.002h-.5V13a.5.5 0 0 1 1 0v.506l.003.044a1.958 1.958 0 0 0 .195.726c.095.191.23.367.423.495.19.127.466.229.879.229s.689-.102.879-.229c.193-.128.328-.304.424-.495a1.958 1.958 0 0 0 .197-.77V7.544a3.3 3.3 0 0 0-1.064.39 3.482 3.482 0 0 0-.58.417l-.004.004S5.65 8.5 5.5 8.5c-.149 0-.352-.145-.352-.145l-.004-.004a3.482 3.482 0 0 0-.58-.417A3.166 3.166 0 0 0 3 7.5c-.638 0-1.177.213-1.564.434a3.482 3.482 0 0 0-.58.417l-.004.004S.65 8.5.5 8.5C0 8.5 0 8 0 8c0-3.78 3.375-6.762 7.5-6.986V.5A.5.5 0 0 1 8 0zM6.577 2.123c-2.833.5-4.99 2.458-5.474 4.854A4.124 4.124 0 0 1 3 6.5c.806 0 1.48.25 1.962.511a9.706 9.706 0 0 1 .344-2.358c.242-.868.64-1.765 1.271-2.53zm-.615 4.93A4.16 4.16 0 0 1 8 6.5a4.16 4.16 0 0 1 2.038.553 8.688 8.688 0 0 0-.307-2.13C9.434 3.858 8.898 2.83 8 2.117c-.898.712-1.434 1.74-1.731 2.804a8.687 8.687 0 0 0-.307 2.131zm3.46-4.93c.631.765 1.03 1.662 1.272 2.53.233.833.328 1.66.344 2.358A4.14 4.14 0 0 1 13 6.5c.77 0 1.42.23 1.897.477-.484-2.396-2.641-4.355-5.474-4.854z"/>
                    </svg>
                </label>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="ED4ALL"
                        id="ED4ALL"
                    />
                    <label class="form-check-label text-secondary" for="ED4ALL">
                        Education for All
                    </label>
                </div>
                <div class="form-check">
                <input
                    @change="getClubs"
                    v-model="umbrellas"
                    class="form-check-input"
                    type="checkbox"
                    value="SASCENTRIC"
                    id="SASCENTRIC"
                />
                <label class="form-check-label text-secondary" for="SASCENTRIC">
                    SAS-Centric
                </label>
                </div>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="PE"
                        id="PE"
                    />
                    <label class="form-check-label text-secondary" for="PE">
                        Poverty Eradication
                    </label>
                </div>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="H4DI"
                        id="H4DI"
                    />
                    <label class="form-check-label text-secondary" for="H4DI">
                        Help for the Disabled and Ill
                    </label>
                </div>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="GI"
                        id="GI"
                    />
                    <label class="form-check-label text-secondary" for="GI">
                        Global Issues
                    </label>
                </div>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="NSC"
                        id="NSC"
                    />
                    <label class="form-check-label text-secondary" for="NSC">
                        New Service Clubs
                    </label>
                </div>
                <div class="form-check">
                    <input
                        @change="getClubs"
                        v-model="umbrellas"
                        class="form-check-input"
                        type="checkbox"
                        value="SP"
                        id="SP"
                    />
                    <label class="form-check-label text-secondary" for="SP">
                        Service Projects
                    </label>
                </div>
            </div>
        </div>
        <div class="col-md-10 col-12 px-md-5 p-4">
            <div class="px-md-5 mx-lg-5">
                <h1 class="clubGridTitle">Browse Clubs</h1>
                <h5 class="clubGridTitle">Find your people!</h5>
                <span
                    v-for="tag in selectedTagData"
                    @click="toggleTag(tag.id)"
                    :key="tag.id"
                    class="badge bg-secondary mx-1"
                >{{ tag.name }} <span style="cursor: pointer">&#x2715;
                </span>
                </span>
                <div class="d-flex justify-content-center" v-if="loading">
                    <div
                        class="spinner-border mt-3"
                        style="width: 5rem; height: 5rem"
                        role="status"
                    >
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="mt-4" v-else>
                    <div v-if="clubs.length > 0">
                        <div
                            v-for="club in clubs"
                            v-bind:key="club.id"
                            class="clubCard card"
                            :style="{ backgroundColor: club.color_primary }"
                        >
                        <router-link
                            :to="{ name: 'ClubPage', params: { id: club.id } }"
                            class="club-link"
                            :style="{ color: club.color_secondary }"
                        >
                            <div class="card-body">
                                <img class="float-end me-1" :src="club.logo">
                                <h4 class="card-title">{{ club.name }}</h4>
                                <div class="mb-2">
                                    <span
                                        v-for="tag in club.tags"
                                        :key="tag.id"
                                        class="badge bg-secondary me-2"
                                    >
                                        {{ tag.name }}
                                    </span>
                                </div>
                                <p class="card-text">{{ club.mission }}</p>
                            </div>
                            <div class="card-footer">{{ club.umbrella }}</div>
                        </router-link>
                        </div>
                    </div>
                    <div class='text-dark mt-4' v-else>
                        <h3 class="py-3">Oops...</h3>
                        <h6>No clubs matched your search query.</h6>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import { apiService } from "../common/api_service";

export default {
    name: "Clubs",
    data() {
        return {
            clubs: [],
            nameInput: "",
            umbrellas: [],
            tags: [],
            selectedTags: [],
            isFocused: false,
            taginput: "",
            loading: false,
        };
    },
    methods: {
        focused() {
            this.isFocused = true;
        },
        getClubs(spinner = true) {
            if (spinner) this.loading = true;
            let endpoint = "/api/club/?search=";
            if (this.nameInput != null) {
                endpoint += this.nameInput;
            }
            if (this.umbrellas.length != 0) {
                endpoint += "&umbrella=" + this.umbrellas.join();
            }
            if (this.selectedTags.length != 0) {
                endpoint += "&tag=" + this.selectedTags.join();
            }
            apiService(endpoint).then((data) => {
                this.clubs = [];
                this.clubs.push(...data);
                this.loading = false;
            });
        },
        getTags() {
            let endpoint = "/api/tag/";
            apiService(endpoint).then((data) => {
                this.tags = [];
                this.tags.push(...data);
            });
        },
        onClickOutside(event) {
            if (!event.target.classList.contains("select-form")) {
                this.isFocused = false;
                this.taginput = "";
            }
        },
        toggleTag(tag_id) {
            if (this.selectedTags.indexOf(tag_id) > -1) {
                var index = this.selectedTags.indexOf(tag_id);
                this.selectedTags.splice(index, 1);
            } else {
                this.selectedTags.push(tag_id);
            }
            this.getClubs();
            this.isFocused = false;
        },
    },
    computed: {
        filteredtags: function () {
            if (this.taginput == "") {
                return this.tags;
            } else {
                return this.tags.filter((item) => {
                    return item.name
                            .toLowerCase()
                            .includes(this.taginput.toLowerCase().trim());
                });
            }
        },
        selectedTagData: function () {
            return this.tags.filter((item) => {
                return this.selectedTags.indexOf(item.id) > -1;
            });
        },
        placeholder: function () {
            if (this.selectedTags.length == 0) {
                return "Search for tags";
            } else {
                return this.selectedTags.length + " tag(s) selected";
            }
        },
    },
    watch: {
        selectedTags() {
            this.getClubs();
        },
    },
    mounted() {
        this.getClubs();
        this.getTags();
        document.addEventListener("click", this.onClickOutside);
    },
    beforeUnmount() {
        document.removeEventListener("click", this.onClickOutside);
    },
};
</script>
<style scoped>
.clubGridTitle {
    margin-left: 10px;
}

.clubCard {
    display: inline-block;
    margin: 4px 10px 10px;
    width: calc(50% - 20px);
    vertical-align: top;
}

.club-link {
    text-decoration: none;
}

.clubCard:hover {
    box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.466);
}

img{
    max-height:80px;
    max-width:110px;
    height:auto;
    width:auto;
}

.form-check-input, .form-check-label{
    cursor: pointer;
}

@media only screen and (max-width: 575px) {
    .clubCard {
        display: inline-block;
        margin: 4px 0px 10px;
        width: 100%;
        vertical-align: top;
    }
}
</style>
