<template>
<div>
    <h4 class='mb-3'>Advertising + Links</h4>
    <div>
        <div v-for="link in filteredLinks" :key="link.id" class="card text-center">
            <div class="card-body">
                <h5 class="card-title">{{ link.name }}</h5>
                <a :href="link.url" target="_blank" class="btn btn-primary">Open</a>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { apiService } from "../common/api_service";

export default {
    name: "LinksTab",
    data(){
        return{
            links: []
        }
    },
    computed:{
        filteredLinks: function() {
            return this.links.filter((item) => {
                return item.category=="officers-only"
            });
        }
    },
    methods: {
        getLinks(){
            let endpoint = "/api/link/";
            apiService(endpoint).then((data) => {
                this.links = [];
                this.links.push(...data);
            });
        }
    },
    mounted(){
        this.getLinks();
    }
};
</script>

<style scoped>
.card{
    width: 31%;
    display: inline-block;
    margin: 1%;
}
</style>