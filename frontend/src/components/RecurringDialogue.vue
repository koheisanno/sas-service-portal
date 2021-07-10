<template>
  <popup-modal ref="popup" small>
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ title }} Recurring Event</h5>
      </div>
      <div class="modal-body">
        <div class="form-check">
          <input
            class="form-check-input"
            value="this"
            type="radio"
            name="editRecurringRadio"
            id="this"
            v-model="option"
            checked
          />
          <label class="form-check-label" for="this"> This event </label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            value="thisAndFollowing"
            type="radio"
            name="editRecurringRadio"
            v-model="option"
            id="thisAndFollowing"
          />
          <label class="form-check-label" for="thisAndFollowing">
            This and following events
          </label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            value="allEvents"
            type="radio"
            name="editRecurringRadio"
            v-model="option"
            id="allEvents"
          />
          <label class="form-check-label" for="allEvents"> All events </label>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="_cancel">
          Cancel
        </button>
        <button type="button" class="btn btn-primary" @click="_confirm">
          OK
        </button>
      </div>
    </div>
  </popup-modal>
</template>

<script>
import PopupModal from "./PopupModal.vue";

export default {
  name: "RecurringDialogue",

  components: { PopupModal },

  data: () => ({
    title: "",
    option: "this",
    // Private variables
    resolvePromise: undefined,
    rejectPromise: undefined,
  }),

  methods: {
    show(title) {
      this.title = title;
      // Once we set our config, we tell the popup modal to open
      this.$refs.popup.open();
      // Return promise so the caller can get results
      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve;
        this.rejectPromise = reject;
      });
    },

    _confirm() {
      this.$refs.popup.close();
      this.resolvePromise(this.option);
      this.option = "this";
    },

    _cancel() {
      this.$refs.popup.close();
      this.resolvePromise(false);
      this.option = "this";
    },
  },
};
</script>
