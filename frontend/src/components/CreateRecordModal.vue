<template>
<popup-modal ref="popup" medium>
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Hours</h5>
      </div>
      <div class="modal-body">
        <p v-if="errors.length">
            <ul class='text-danger'>
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </p>
        <form>
            <div class="row mb-3">
                <div class="col-md-7">
                    <label class="col-form-label">Member</label>
                    <select class="form-select" v-model="selectedMember">
                        <option v-for="member in club.members" :key="member.id" :value="member.id">{{ member.fullName }}</option>
                    </select>
                </div>
                <div class="col-md-5">
                    <label class="col-form-label">Date (<a class='label-link' @click="setTodayDate">Today?</a>)</label>
                    <input v-model='date' type="date" class="form-control">
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-7">
                    <label class="col-form-label">Description</label>
                    <input v-model="name" type="text" maxlength="50" class="form-control">
                </div>
                <div class="col-md-5">
                    <label class="col-form-label">Hours</label>
                    <input v-model="hours" type="number" min="0" max="24" class="form-control">
                </div>
            </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="resetForm">Cancel</button>
        <button type="button" class="btn btn-primary" @click="submitCreationForm">
            Submit
        </button>
      </div>
    </div>
</popup-modal>
</template>

<script>
import PopupModal from './PopupModal.vue'
import { apiService } from "../common/api_service"

export default {
    name: "CreateRecordModal",
    components: { PopupModal },
    data(){
        return{
            selectedMember: null,
            club:{
                name: '',
                members:[]
            },
            name:'',
            hours:0,
            date: null,
            errors: [],

            resolvePromise: undefined,
            rejectPromise: undefined,
        }
    },
    methods:{
        show(club) {
            // Once we set our config, we tell the popup modal to open
            this.club = club;
            this.selectedMember = club.members[0].id;
            this.$refs.popup.open();

            return new Promise((resolve, reject) => {
                this.resolvePromise = resolve
                this.rejectPromise = reject
            })
        },
        setTodayDate(){
            let today = new Date();
            let month = today.getMonth()+1;
            let day = today.getDate();
            if(month<10){
                month = "0"+month;
            }
            if(day<10){
                day = "0"+day;
            }
            this.date = today.getFullYear()+"-"+month+"-"+day;
        },
        resetForm(){
            this.$refs.popup.close();
            this.errors = [];
            this.date = null;
            this.hours = 0;
            this.selectedMember = {
                name: '',
                members:[]
            };
            this.name = '';
        },
        validateForm(){
            this.errors=[];

            if(this.date==null){
                this.errors.push('Date is required.');
            }

            if(this.hours==null){
                this.errors.push('Hours is required.');
            }

            if(this.name==''){
                this.errors.push('Description is required.');
            }

            if(this.hours<0){
                this.errors.push('Hours must be greater than 0.');
            }
        },
        async submitCreationForm(){
            this.validateForm();
            if(this.errors.length==0){
                this.$refs.popup.close()
                let endpoint = "/api/record/";
                let body = {
                    "club": this.club.id,
                    "userprofile": this.selectedMember,
                    "checkInDate": this.date,
                    "name": this.name,
                    "hours": this.hours
                }
                console.log(body)
                apiService(endpoint, "POST", body)
                    .then(data =>{
                        if(data!=false){
                            this.resolvePromise(true);
                        }
                        else{
                            this.resolvePromise(false);
                        }
                    });
                this.resetForm();
            }
        }
    }
}

</script>

<style scoped>
    .label-link{
        color: #1A73E8;
        cursor: pointer;
    }
    .customBtn{
        border-radius: 50%;
        height: 1.9em;
        width: 1.9em;
        border-color: #1A73E8;
        border: 2px solid;
    }
</style>