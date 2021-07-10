<template>
  <div
    class="modal fade"
    id="deleteRecurringModal"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-sm modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete recurring event</h5>
        </div>
        <div class="modal-body">
          <div class="form-check">
            <input
              class="form-check-input"
              value="this"
              type="radio"
              name="deleteRecurringRadio"
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
              name="deleteRecurringRadio"
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
              name="deleteRecurringRadio"
              v-model="option"
              id="allEvents"
            />
            <label class="form-check-label" for="allEvents"> All events </label>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button type="button" class="btn btn-primary">OK</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DeleteRecurringModal",
  data() {
    return {
      option: "this",
    };
  },
};
</script>
