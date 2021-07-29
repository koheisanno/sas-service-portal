<template>
<popup-modal ref="popup" large>
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">New Event for {{club.name}}</h5>
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
                    <input v-model='date' type="date" class="form-control" @change="changeLockedDate">
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-4">
                    <label class="col-form-label">Start Time (<a class='label-link' @click="setNowTime();resetHours()">Now?</a>)</label>
                    <input v-model="startTime" type="time" class="form-control" @change="resetHours">
                </div>
                <div class="col-md-4">
                    <label class="col-form-label">End Time</label>
                    <input v-model="endTime" type="time" class="form-control" @change="resetHours">
                </div>
                <div class="col-md-4">
                    <div class="mt-2 mb-1 form-check" v-show="startTime!=null && endTime!=null">
                        <input type="checkbox" class="form-check-input" id="overrideCheck" v-model="overrideHours" @change="resetHours">
                        <label class="form-check-label" for="overrideCheck">Override hours?</label>
                    </div>
                    <div v-show="startTime!=null && endTime!=null">
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
            <div class="mb-2 form-check" v-show="date!=null">
                <input type="checkbox" class="form-check-input" id="recurringCheck" v-model="repeats">
                <label class="form-check-label" for="recurringCheck">Recurring?</label>
            </div>
            <div v-show="repeats" style="border-radius:10px;" class="border border-primary">
                <div class="row my-3" v-show="date!=null">
                    <div class="ms-3 col-md-6">
                        <select v-model='repeatOption' class="form-select">
                            <option selected>Daily</option>
                            <option>Weekly</option>
                            <option>Every Weekday</option>
                            <option>Custom</option>
                        </select>
                    </div>
                </div>
                <div class="row mb-3" v-show="repeatOption=='Custom' && date!=null">
                    <div class="ms-3 col-md-6">
                        <button type="button" class="customBtn me-1" @click="changeCustomDates('0')" v-bind:style="sunStyle">S</button>
                        <button type="button" class="customBtn mx-1" @click="changeCustomDates('1')" v-bind:style="monStyle">M</button>
                        <button type="button" class="customBtn mx-1" @click="changeCustomDates('2')" v-bind:style="tueStyle">T</button>
                        <button type="button" class="customBtn mx-1" @click="changeCustomDates('3')" v-bind:style="wedStyle">W</button>
                        <button type="button" class="customBtn mx-1" @click="changeCustomDates('4')" v-bind:style="thuStyle">T</button>
                        <button type="button" class="customBtn mx-1" @click="changeCustomDates('5')" v-bind:style="friStyle">F</button>
                        <button type="button" class="customBtn ms-1" @click="changeCustomDates('6')" v-bind:style="satStyle">S</button>
                    </div>
                </div>
                <div class="row mb-3" v-show="date!=null">
                    <div class="ms-3 col-md-4">
                        <label class="col-form-label">Until</label>
                        <input v-model='untilDate' type="date" class="form-control">
                    </div>
                </div>
            </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="resetForm">Cancel</button>
        <button type="button" class="btn btn-primary" @click="submitCreationForm">
            Create
        </button>
      </div>
    </div>
</popup-modal>
</template>

<script>
import PopupModal from './PopupModal.vue'
import { apiService } from "../common/api_service"
import { v4 as uuidv4 } from 'uuid';

export default {
    name: "CreateEventModal",
    components: { PopupModal },
    data(){
        return{
            club: { name: '' },
            eventName: "",
            startTime:null,
            endTime:null,
            location: "",
            repeats: false,
            repeatOption: "Daily",
            date: null,
            selectedStyle: {
                backgroundColor: "#1A73E8",
                color: "white"
            },
            unselectedStyle: {
                backgroundColor: "white",
                color: "#1A73E8"
            },
            customDates: [false,false,false,false,false,false,false],
            untilDate: null,
            errors: [],
            overrideHours: false,
            hours:null,

            // Private variables
            resolvePromise: undefined,
            rejectPromise: undefined,
        }
    },
    methods:{
        show(club) {
            this.club = club;
            // Once we set our config, we tell the popup modal to open
            this.$refs.popup.open();

            return new Promise((resolve, reject) => {
                this.resolvePromise = resolve
                this.rejectPromise = reject
            });
        },
        resetHours(){
            if(this.overrideHours==false){
                if(this.startTime!=null && this.endTime!=null){
                    const today = new Date();
                    this.hours = Math.round((new Date(today.toDateString() + ' ' + this.endTime)-new Date(today.toDateString() + ' ' + this.startTime))/36000)/100;
                }
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
            this.changeLockedDate();
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
        resetForm(){
            this.$refs.popup.close();
            this.customDates = [false,false,false,false,false,false,false];
            this.untilDate = null;
            this.errors = [];
            this.eventName = "";
            this.startTime = null;
            this.endTime = null;
            this.location = "";
            this.repeats = false;
            this.repeatOption = "Daily";
            this.date = null;
            this.overrideHours = false;
            this.hours = null;
        },
        validateForm(){
            this.errors=[];

            if(this.eventName=="" || this.startTime==null || this.endTime==null || this.location=="" || this.date==null || this.hours == null){
                this.errors.push('All fields required.');
            }

            if(this.hours<0){
                this.errors.push('Hours must be greater than 0.');
            }

            const today = new Date();
            if(new Date(today.toDateString() + ' ' + this.startTime)>new Date(today.toDateString() + ' ' + this.endTime)){
                this.errors.push('End time must be after start time.');
            }

            if(this.repeats==true && new Date(this.untilDate)<new Date(this.date)){
                this.errors.push('End date must be after start date.');
            }
        },
        async submitCreationForm(){
            this.validateForm();
            if(this.errors.length==0){
                this.$refs.popup.close()
                let endpoint = `/api/club/${this.club.id}/event/`;
                let data = {
                    "startTime": this.date + " " + this.startTime,
                    "endTime": this.date + " " + this.endTime,
                    "name": this.eventName,
                    "series": null,
                    "location": this.location,
                    "hours": this.hours
                }                  
                if(this.repeats){
                    let arrayData = []
                    let uuid = uuidv4();
                    data.series = uuid;

                    arrayData.push({ ...data });

                    let eventDate = new Date(this.date);
                    let endDate = new Date(this.untilDate);
                    if(this.repeatOption=="Daily"){
                        while(endDate > eventDate){
                            eventDate.setDate(eventDate.getDate() + 1);
                            data.startTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.startTime;
                            data.endTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.endTime;
                            arrayData.push({ ...data });
                        }
                    }
                    else if(this.repeatOption=="Weekly"){
                        let tempDate = new Date();
                        tempDate.setDate(endDate.getDate() - 7);
                        while(tempDate > eventDate){
                            eventDate.setDate(eventDate.getDate() + 7);
                            data.startTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.startTime;
                            data.endTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.endTime;
                            arrayData.push({ ...data });
                        }
                    }
                    else if(this.repeatOption=="Every Weekday"){
                        while(endDate > eventDate){
                            eventDate.setDate(eventDate.getDate() + 1);
                            if(eventDate.getDay()!=0 && eventDate.getDay()!=6){
                                data.startTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.startTime;
                                data.endTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.endTime;
                                arrayData.push({ ...data });
                            }
                        }
                    }
                    else if(this.repeatOption=="Custom"){
                        while(endDate > eventDate){
                            eventDate.setDate(eventDate.getDate() + 1);
                            if(this.customDates[eventDate.getDay()]){
                                data.startTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.startTime;
                                data.endTime = eventDate.getFullYear()+"-"+(eventDate.getMonth()+1)+"-"+eventDate.getDate() + " " + this.endTime;
                                arrayData.push({ ...data });
                            }
                        }
                    }

                    apiService(endpoint, "POST", arrayData)
                        .then(() =>{
                            this.resolvePromise(true);
                        });
                }
                else{
                    apiService(endpoint, "POST", data)
                        .then(() =>{
                            this.resolvePromise(true);
                        });
                }
                this.resetForm();
            }
        },
        changeCustomDates(dateNum){
            if(dateNum!=this.lockedDate){
                if(this.customDates[dateNum]){
                    this.customDates[dateNum] = false;
                }
                else{
                    this.customDates[dateNum] = true;
                }
            }
        },
        changeLockedDate(){
            this.customDates = [false,false,false,false,false,false,false];
            this.customDates[this.lockedDate] = true;
        }
    },
    computed: {
        lockedDate(){
            return new Date(this.date).getDay();
        },
        sunStyle() {
            if(this.customDates[0]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        monStyle() {
            if(this.customDates[1]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        tueStyle() {
            if(this.customDates[2]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        wedStyle() {
            if(this.customDates[3]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        thuStyle() {
            if(this.customDates[4]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        friStyle() {
            if(this.customDates[5]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
        satStyle() {
            if(this.customDates[6]){
                return this.selectedStyle;
            } else {
                return this.unselectedStyle;
            }
        },
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