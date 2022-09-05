<template>
  <div>
    <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
    <AddOfficerDialogue ref="addOfficerModal" />
    <table
      class="table"
      v-bind:class="{
        'table-hover': list.length != 0,
        'table-striped': list.length != 0,
      }"
    >
      <tbody v-if="list.length == 0">
        <tr>
          <td>No {{ name }} found.</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="item in list" :key="item.id">
          <td>
            <input
              class="form-check-input"
              :value="item.id"
              type="checkbox"
              v-model="selected"
              v-bind:id="item.id"
            />
            <label class="form-check-label ms-2" v-bind:for="item.id">
              {{ item.firstName + " " + item.lastName }}
            </label>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="gap-2 d-flex justify-content-end">
      <button class="btn btn-danger btn-sm" type="button" @click="remove" v-bind:disabled="selected.length == 0">
        Remove
      </button>
      <button class="btn btn-success btn-sm" type="button" @click="add">
        Add
      </button>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api_service";
import AddOfficerDialogue from "./AddOfficerDialogue";
import ConfirmDialogue from "../components/ConfirmDialogue";

export default {
  name: "Table",
  components: { AddOfficerDialogue, ConfirmDialogue },
  props: {
    list: {
      type: Array,
      default: function () {
        return [];
      },
    },
    name: {
      type: String,
      default: "",
    },
    club: {
      type: Object,
      default: function () {
        return {};
      },
    },
  },
  data() {
    return {
      selected: [],
    };
  },
  methods: {
    async add() {
      const response = await this.$refs.addOfficerModal.show(
        this.club.id,
        this.name
      );
      if(response) this.$emit("addOfficerSuccess");
    },
    async remove() {
      const confirm = await this.$refs.confirmDialogue.show({
        title: "Remove Officers",
        message:
          "Are you sure you want to remove the selected officers?",
        okButton: "Remove",
      });
      if (confirm) {
        let endpoint = "/api/club/" + this.club.id + "/remove-officer/";
        apiService(endpoint, "POST", this.selected).then(() => {
          this.$emit("removeOfficerSuccess");
          // console.log(this.selected);
          this.selected = [];
        });
      }
    },
  },
};
</script>
