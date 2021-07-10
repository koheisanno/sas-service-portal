<template>
<div>
    <RecurringDialogue ref="editConfirmDialogue"></RecurringDialogue>
    <PopupModal ref="popup" large>
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{event.name}}</h5>
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
                            <label class="col-form-label">Event Name</label>
                            <input type="text" class="form-control"  v-model.trim = "eventName">
                        </div>
                        <div class="col-md-5">
                            <label class="col-form-label">Date (<a class='label-link' @click="setTodayDate">Today?</a>)</label>
                            <input v-model='date' type="date" class="form-control">
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label class="col-form-label">Start Time (<a class='label-link' @click="setNowTime">Now?</a>)</label>
                            <input v-model="startTime" type="time" class="form-control" @change="resetHours">
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label">End Time</label>
                            <input v-model="endTime" type="time" class="form-control" @change="resetHours">
                        </div>
                        <div class="col-md-4">
                            <div class="mt-2 mb-1 form-check">
                                <input type="checkbox" class="form-check-input" id="overrideEditCheck" v-model="overrideHours" @change="resetHours">
                                <label class="form-check-label" for="overrideEditCheck">Override hours?</label>
                            </div>
                            <div>
                                <input type="number" class="form-control" v-model="hours" min="0" max="24" v-bind:disabled="!overrideHours">
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-7">
                            <label class="col-form-label">Location</label>
                            <input v-model="location" type="text" class="form-control">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="cancelForm">Cancel</button>
                <button type="button" class="btn btn-primary" @click="submitUpdateForm">
                    Edit
                </button>
            </div>
        </div>
    </PopupModal>
</div>
</template>

<script>
import { apiService } from "../common/api_service"
import RecurringDialogue from "../components/RecurringDialogue"
import PopupModal from './PopupModal.vue'

export default {
    name: "EditEventModal",
    components: {
        RecurringDialogue,
        PopupModal
    },
    data(){
        return{
            event: { name: "" },
            eventName: "",
            startTime:null,
            endTime:null,
            location: "",
            date: null,
            hours:null,
            overrideHours: false,
            errors: [],

            // Private variables
            resolvePromise: undefined,
            rejectPromise: undefined,
        }
    },
    methods:{
        show(event) {
            // Once we set our config, we tell the popup modal to open
            
            this.event = event;
            this.eventName = event.name;
            this.startTime = event.startTime.split(" ")[1];
            this.endTime = event.endTime.split(" ")[1];
            this.location = event.location;
            this.date = event.endTime.split(" ")[0];
            this.hours = event.hours;

            const today = new Date();
            let actualHours = Math.round((new Date(today.toDateString() + ' ' + this.endTime)-new Date(today.toDateString() + ' ' + this.startTime))/36000)/100;
            this.overrideHours = !(actualHours==this.event.hours)

            this.$refs.popup.open()

            return new Promise((resolve, reject) => {
                this.resolvePromise = resolve
                this.rejectPromise = reject
            })
        },
        cancelForm(){
            this.resolvePromise(false)
            this.$refs.popup.close()
        },
        validateForm(){
            this.errors=[]

            if(this.eventName=="" || this.startTime==null || this.endTime==null || this.location=="" || this.hours == null){
                this.errors.push('All fields required.');
            }

            if(this.hours<0){
                this.errors.push('Hours must be greater than 0.');
            }

            const today = new Date();
            if(new Date(today.toDateString() + ' ' + this.startTime)>new Date(today.toDateString() + ' ' + this.endTime)){
                this.errors.push('End time must be after start time.');
            }
        },
        async submitUpdateForm(){
            this.validateForm();

            if(this.errors.length==0){
                this.$refs.popup.close()
                if(this.event.series!=null){
                    const option = await this.$refs.editConfirmDialogue.show("Edit")
                    if(option=="allEvents"){
                        let endpoint=`/api/event/series/${this.event.id}/${this.event.series}/all/`;
                        let body = {
                                    "startTime": this.startTime,
                                    "endTime": this.endTime,
                                    "date": this.date,
                                    "name": this.eventName,
                                    "location": this.location,
                                    "hours": this.hours
                                }
                        await apiService(endpoint, "PUT", body)
                    }
                    else if(option=="thisAndFollowing"){
                        let endpoint=`/api/event/series/${this.event.id}/${this.event.series}/following/`;
                        let body = {
                                    "startTime": this.startTime,
                                    "endTime": this.endTime,
                                    "date": this.date,
                                    "name": this.eventName,
                                    "location": this.location,
                                    "hours": this.hours
                                }
                        await apiService(endpoint, "PUT", body)
                    }
                    else{
                        let endpoint=`/api/event/${this.event.id}/`;
                        let body = {
                                    "startTime": this.date + " " + this.startTime,
                                    "endTime": this.date + " " + this.endTime,
                                    "name": this.eventName,
                                    "location": this.location,
                                    "hours": this.hours
                                }

                        console.log(body)
                        await apiService(endpoint, "PUT", body)
                    }
                }
                else{
                    let endpoint=`/api/event/${this.event.id}/`;
                    let body = {
                                "startTime": this.date + " " + this.startTime,
                                "endTime": this.date + " " + this.endTime,
                                "name": this.eventName,
                                "location": this.location,
                                "hours": this.hours
                            }
                    await apiService(endpoint, "PUT", body)
                }
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
        },
        setNowTime(){
            let today = new Date();
            let hour = today.getHours();
            let minute = today.getMinutes();
            if(hour<10){
                hour = "0"+hour;
            }
            if(minute<10){
                minute = "0"+minute;
            }
            this.startTime = hour+":"+minute;
        },
        resetHours(){
            if(this.overrideHours==false){
                if(this.startTime!=null && this.endTime!=null){
                    const today = new Date();
                    this.hours = Math.round((new Date(today.toDateString() + ' ' + this.endTime)-new Date(today.toDateString() + ' ' + this.startTime))/36000)/100;
                }
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