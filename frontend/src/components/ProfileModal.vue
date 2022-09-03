<template>
<div class="modal fade" id="profileModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Profile Settings</h5>
      </div>
      <div class="modal-body">
        <p v-if="errors.length">
            <ul class='text-danger'>
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </p>
        <form>
          <div class="mb-3">
            <label class="col-form-label">First Name</label>
            <input type="text" class="form-control"  v-model.trim = "user.firstName" v-on:input="changeSaveState">
          </div>
          <div class="mb-3">
            <label class="col-form-label">Last Name:</label>
            <input type="text" class="form-control" v-model.trim = "user.lastName" v-on:input="changeSaveState">
          </div>
          <div class="mb-3">
            <label class="col-form-label">Class:</label>
            <select class="form-control" v-model = "user.classOf" v-on:change="changeSaveState">
                <option v-for="year in years" :key="year" :value="year">
                    {{ year }}
                </option>
            </select>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="getUser">Close</button>
        <button type="button" class="btn btn-primary" @click="updateUser">
            <span v-show="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{loadingButton}}
        </button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { apiService } from "../common/api_service"

export default {
    name: "ProfileModal",
    data(){
        return{
            user:{
                lastName: "",
                firstName: "",
                classOf: ""
            },
            errors: [],
            years:[],
            loadingButton: "Save",
            loading: false
        }
    },
    methods:{
        getUser(){
            let endpoint = "/api/user/";
            apiService(endpoint).then((data) => {
                console.log(data);
                this.user.lastName = data.lastName;
                this.user.firstName = data.firstName;
                this.user.classOf = data.classOf;
            });
        },
        setYears(){
            var date = new Date()
            var month = date.getMonth()
            var year = date.getFullYear();

            if(month>=7){
                for(var i=1; i<5; i++){
                    this.years.push(year+i);
                }
            }
            else{
                for(var n=0; n<4; n++){
                    this.years.push(year+n)
                }
            }
        },
        updateUser(){
            this.loading = true;
            this.errors=[]
            if(this.user.firstName==""){
                this.errors.push('First name required.')
            }
            if(this.user.lastName==""){
                this.errors.push('Last name required.')
            }
            if(!Number.isSafeInteger(this.user.classOf)){
                this.errors.push('Class year required.')
            }

            if(this.errors.length==0){
                let endpoint = "/api/user/";
                let body = {
                    "firstName": this.user.firstName,
                    "lastName": this.user.lastName,
                    "classOf": this.user.classOf
                    }
                apiService(endpoint, "PATCH", body)
                    .then(data =>{
                        if(data!=false){
                            this.loading = false;
                        }
                    });
            }
        },
        changeSaveState(){
            this.loadingButton = "Save";
        }
    },
    watch: {
        loading: function (newState) {
            if(newState == false){
                this.loadingButton = "Saved!"
            }
        }
    },
    mounted(){
        this.getUser();
        this.setYears();
    }
}

</script>

<style scoped>
    .navbar-brand{
    font-family: 'Pattaya', sans-serif;
    font-size: 20px;
    }
</style>