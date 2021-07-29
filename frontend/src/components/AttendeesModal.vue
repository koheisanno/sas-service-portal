<template>
<popup-modal ref="popup" medium>
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Attendees</h5>
        </div>
        <div class="modal-body">
            <table class="mt-1 table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Hours</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in event.records" :key="record.user.id">
                        <td class="align-middle">
                            <input
                                @click="toggleAttendance(record.user.id, $event)"
                                class="form-check-input"
                                type="checkbox"
                                :id="record.user.id"
                                :value="record.id"
                                :ref="record.user.id+'_check'"
                                checked
                            />
                            <label class="form-check-label ms-2" v-bind:for="record.user.id">
                                {{ record.user.firstName + " " + record.user.lastName }}
                            </label>
                            <p :ref="record.user.id+'_warning'" class='text-danger' hidden>Hours must be greater than 0.</p>
                        </td>
                        <td class="align-middle">
                            <div class="input-group" style="width: 140px">
                                <span class="input-group-text">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                                    </svg>
                                </span>
                                <input @change="updateRecord(record.user.id)" :ref="record.user.id+'_input'" type="text" :value="record.hours" class="form-control" placeholder="Hours">
                            </div>
                        </td>
                    </tr>
                    <tr v-for="member in filteredMembers" :key="member.id">
                        <td class="align-middle">
                            <input
                                @click="toggleAttendance(member.id, $event)"
                                class="form-check-input"
                                type="checkbox"
                                :id="member.id"
                                :ref="member.id+'_check'"
                            />
                            <label class="form-check-label ms-2" :for="member.id">
                                {{ member.firstName + " " + member.lastName }}
                            </label>
                            <p :ref="member.id+'_warning'" class='text-danger' hidden>Hours must be greater than 0.</p>
                        </td>
                        <td class="align-middle">
                            <div class="input-group" style="width: 140px">
                                <span class="input-group-text">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                                    </svg>
                                </span>
                                <input @change="updateRecord(member.id)" :ref="member.id+'_input'" type="text" value=0 class="form-control" placeholder="Hours" disabled>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="_cancel">Close</button>
        </div>
    </div>
</popup-modal>
</template>

<script>
import PopupModal from './PopupModal.vue'
import { apiService } from "../common/api_service";

export default {
    name: "AttendeesModal",
    components: { PopupModal },
    data(){
        return{
            club: { members: [], },
            event: { records: [], },

            // Private variables
            resolvePromise: undefined,
            rejectPromise: undefined,
        }
    },
    computed: {
        filteredMembers: function () {
            return this.club.members.filter((member) => {
                if(!this.event.records.some(el => el.user.id === member.id)){
                    return member;
                }
            });
        }
    },
    methods:{
        show(club, event) {
            this.club = club;
            this.event = event;

            this.$refs.popup.open();

            return new Promise((resolve, reject) => {
                this.resolvePromise = resolve
                this.rejectPromise = reject
            });
        },
        updateRecord(id){
            let endpoint = `/api/record/${this.$refs[id+"_check"].value}/`;
            if(this.$refs[id+"_input"].value>0){
                this.$refs[id+"_warning"].hidden = true;
                let body = {
                    "hours": this.$refs[id+"_input"].value
                }
                apiService(endpoint, "PATCH", body)
                    .then(()=>{
                        this.$emit("edited");
                    });
            }
            else{
                this.$refs[id+"_warning"].hidden = false;
            }
        },
        toggleAttendance(id, event){
            if(event.target.checked){
                let today = new Date()
                let endpoint = "/api/record/";
                let body = {
                    "club": this.club.id,
                    "userprofile": id,
                    "event": this.event.id,
                    "hours": this.event.hours,
                    "checkInDate": `${today.getFullYear()}-${today.getMonth()+1}-${today.getDay()}`
                }
                apiService(endpoint, "POST", body)
                    .then((data) =>{
                        this.$refs[id+"_check"].value=data.id;
                        this.$refs[id+"_input"].value=data.hours;
                        this.$refs[id+"_input"].disabled=false;
                        this.$emit("edited");
                    });
            }
            else{
                let endpoint = `/api/record/${this.$refs[id+"_check"].value}/`;
                apiService(endpoint, "DELETE")
                    .then(() =>{
                        this.$refs[id+"_input"].value=0;
                        this.$refs[id+"_input"].disabled=true;
                        this.$emit("edited");
                    });
            }
        },
        _cancel(){
            this.$refs.popup.close();
        }
    }
}
</script>