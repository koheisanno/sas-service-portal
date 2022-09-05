<template>
  <popup-modal ref="popup" medium>
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add {{ type }}</h5>
      </div>
      <div class="modal-body">
        <input
          type="text"
          class="form-control select-form"
          v-model="userinput"
          :placeholder="placeholder"
          @focus="focused"
        />
        <div v-show="isFocused" id="usersList" class="list-group">
          <button
            type="button"
            class="select-form list-group-item list-group-item-action"
            v-for="item in filteredlist"
            :value="item.id"
            :key="item.id"
            @click="setSelected(item.id, item.firstName + ' ' + item.lastName)"
          >
            {{ item.firstName + " " + item.lastName }}
          </button>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="_cancel">
          Cancel
        </button>
        <button type="button" class="btn btn-primary" @click="_confirm">
          Add
        </button>
      </div>
    </div>
  </popup-modal>
</template>

<script>
import PopupModal from "./PopupModal.vue";
import { apiService } from "../common/api_service";

export default {
  name: "AddOfficerDialogue",

  components: { PopupModal },

  data: () => ({
    clubId: null,
    isFocused: false,
    list: [],
    userinput: "",
    selected: {
      name: "",
      id: null,
    },
    type: null,
    // Private variables
    resolvePromise: undefined,
    rejectPromise: undefined,
  }),

  computed: {
    filteredlist: function () {
      if (this.userinput == "") {
        return this.list;
      } else {
        return this.list.filter((item) => {
          return (item.firstName + " " + item.lastName)
            .toLowerCase()
            .includes(this.userinput.toLowerCase());
        });
      }
    },
    placeholder: function () {
      if (this.selected.id == null) {
        return "Search...";
      } else {
        return this.selected.name;
      }
    },
  },

  methods: {
    focused() {
      this.isFocused = true;
      this.userinput = "";
    },
    setSelected(id, name) {
      this.isFocused = false;
      this.selected.id = id;
      this.selected.name = name;
      this.userinput = name;
    },
    show(clubId, type) {
      document.addEventListener("click", this.onClickOutside);
      this.type = type;
      this.clubId = clubId;
      console.log(clubId);
      this.loadUsers();
      this.$refs.popup.open();
      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve;
        this.rejectPromise = reject;
      });
    },

    _confirm() {
      let endpoint = `/api/club/${this.clubId}/add-officer/`;
      apiService(endpoint, "POST", this.selected.id);

      this.$refs.popup.close();
      this.resolvePromise(true);
    },

    _cancel() {
      this.$refs.popup.close();
      this.resolvePromise(false);
      document.removeEventListener("click", this.onClickOutside);
    },

    loadUsers() {
      let endpoint = "/api/user-list/";
      apiService(endpoint).then((data) => {
        if (this.type == "officers") {
          this.list = data.filter((obj) => {
            return obj.status === "student";
          });
        } else if (this.type == "sponsors") {
          this.list = data.filter((obj) => {
            return obj.status === "faculty";
          });
        }
      });
    },
    onClickOutside(event) {
      if (!event.target.classList.contains("select-form")) {
        this.isFocused = false;
        if (this.selected.id == null) {
          this.userinput = "";
        } else {
          this.userinput = this.selected.name;
        }
      }
    },
  },
};
</script>

<style scoped>
.modal-body {
  max-height: 30vh;
  overflow-y: auto;
}
input {
  width: 460px;
}
#usersList {
  height: 200px;
  width: 460px;
  overflow-y: auto;
  z-index: 30;
  position: fixed;
}
</style>
