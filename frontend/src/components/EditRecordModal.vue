<template>
<popup-modal ref="popup" medium>
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Edit Task Details</h5>
      </div>
      <div class="modal-body">
        <p v-if="errors.length">
            <ul class='text-danger'>
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </p>
        <form>
            <div class="row mb-3">
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
        <button type="button" class="btn btn-secondary" @click="cancelForm">Close</button>
        <button type="button" class="btn btn-primary" @click="submitUpdateForm">
            Edit
        </button>
      </div>
    </div>
</popup-modal>
</template>


<script>
import { apiService } from "../common/api_service"
import PopupModal from './PopupModal.vue'

export default {
    name: "EditRecordModal",
    components: {
        PopupModal
    },
    props:{
        event:{
            type: Object,
            default: function () {
                return { name: "" }
            }
        },
    },
    data(){
        return{
            record: null,
            name:'',
            hours:0,
            date: null,

            errors: [],

            resolvePromise: undefined,
            rejectPromise: undefined,
        }
    },
    methods:{
        show(record) {
            this.$refs.popup.open();
            this.record = record;
            this.name = record.name;
            this.hours = record.hours;
            let dateStrings = record.checkInDate.split("/");
            this.date = dateStrings[2]+"-"+dateStrings[1]+"-"+dateStrings[0];

            return new Promise((resolve, reject) => {
                this.resolvePromise = resolve
                this.rejectPromise = reject
            })
        },
        cancelForm(){
            this.resolvePromise(false);
            this.$refs.popup.close();
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
        async submitUpdateForm(){
            this.validateForm();

            if(this.errors.length==0){
                this.$refs.popup.close()
                let endpoint=`/api/record/${this.record.id}/`;
                let body = {
                    "checkInDate": this.date,
                    "name": this.name,
                    "hours": this.hours
                }
                apiService(endpoint, "PATCH", body)
                    .then(data =>{
                        if(data!=false){
                            this.resolvePromise(true);
                        }
                        else{
                            this.resolvePromise(false);
                        }
                    });
                this.resolvePromise(true)
            }
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
        }
    }
}
</script>