<template>
<div>
    <h4 class="mb-3">
        QR Codes
        <span ref="tooltipInfoQRCodes"
                data-bs-toggle="tooltip" data-bs-placement="bottom" title="Scan the 'check-in' QR Code within 20 minutes before or after the event to confirm attendance.">
            <svg xmlns="http://www.w3.org/2000/svg"
                width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
            </svg>
        </span>
    </h4>
    <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button
                class="nav-link active"
                id="check-in-tab"
                data-bs-toggle="tab"
                data-bs-target="#check-in"
                type="button"
                role="tab"
                aria-controls="check-in"
                aria-selected="true"
                @click="qrCodeOption = 'check-in'"
            >
                Check-in
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button
                class="nav-link"
                id="join-tab"
                data-bs-toggle="tab"
                data-bs-target="#join"
                type="button"
                role="tab"
                aria-controls="join"
                aria-selected="false"
                @click="qrCodeOption = 'join'"
            >
                Join
            </button>
        </li>
    </ul>
    <div class="tab-content">
        <div
            class="tab-pane fade show active border container d-flex justify-content-center py-4"
            id="check-in"
            role="tabpanel"
            aria-labelledby="check-in-tab"
        >
            <img
                v-for="club in clubs"
                v-bind:key="club.id"
                :class="'border border-3 border-primary img-fluid mx-auto'"
                :src="base_url + '/checkin?id=' + club.id"
                v-show="currentClub == club.id && qrCodeOption == 'check-in'"
            />
            <img
                v-for="club in clubs"
                v-bind:key="club.id"
                :class="'border border-3 border-primary img-fluid mx-auto'"
                :src="base_url + '/join?id=' + club.id"
                v-show="currentClub == club.id && qrCodeOption == 'join'"
            />
        </div>
    </div>
</div>
</template>

<script>
import { Tooltip } from "bootstrap";

export default {
    name: "QRCodeTab",
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
            qrCodeOption: "check-in",
            base_url: `https://chart.googleapis.com/chart?chs=547x547&cht=qr&chl=${window.location.protocol}//${window.location.hostname}`,
        };
    },
    methods: {
        setTooltips() {
            let options = {
                trigger: "hover",
            };
            for (var ref in this.$refs) {
                if (ref.indexOf("tooltip") > -1) {
                    return new Tooltip(this.$refs[ref], options);
                }
            }
        }
    },
    mounted(){
        this.setTooltips();
    }
};
</script>
